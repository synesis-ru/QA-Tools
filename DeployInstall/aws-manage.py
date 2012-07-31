import boto
from boto import ec2
from boto import *
from boto.ec2.blockdevicemapping import BlockDeviceMapping, BlockDeviceType
from boto.exception import EC2ResponseError
from boto.regioninfo import RegionInfo
from boto.ec2.elb import HealthCheck

from fabric import api as fapi
from fabric.contrib import files as cfapi

# Zabbix_api is not module and should be installed manualy
from zabbix_api import ZabbixAPI

import time
import tigrisCONFIG
from tigrisCONFIG import *

#
# HELPER FUNCTIONS
#
def getRegion(reg_name):
	return ec2.get_region(region_name=AWS_CONFIG['AWS_REGION'],
	 	aws_access_key_id=AWS_CONFIG['AWS_KEY'], 
		aws_secret_access_key=AWS_CONFIG['AWS_SECRET'])

def waitTillRunning(instance):
	while True:
		status = instance.update()
		if 'running' == status:
			return
		else:
			print status
			time.sleep(10)

# 
# communicates to Route53 in order to update stuff
#
def addUpdateDNS(domain, host, ip):
	dns = boto.connect_route53(AWS_CONFIG['AWS_KEY'], AWS_CONFIG['AWS_SECRET'])
	if not dns:
		print "Failed to connect to Route53"
		return False
	
	zone = dns.get_hosted_zone_by_name(domain)
	if not zone: 
		print "Domain %s is not known to Route53 service" % domain
		return False
	
	records = dns.get_all_rrsets(zone['GetHostedZoneResponse']['HostedZone']['Id'].replace('/hostedzone/',''))
	
	# now check if we already have this host in the DNS
	# route53 cannot 'update', we need make delete / create
	# route53 also returns everything with dot at the end, which we generally don't
	hostname = '%s.%s.' % (host,domain)
	hostRecords = filter(lambda h : h.name == hostname, records)
	if len(hostRecords) > 1:
		print "Received multiple records for host %s, check DNS in web console" % hostname
		return False
	elif len(hostRecords) == 1:
		# double'check that we're not deleting something not of DNS 'A' type
		if hostRecords[0].type != 'A':
			print "Host %s has record of type %s, aborting" % (hostname, hostRecords[0].type)
			return False
		records.add_change('DELETE', hostRecords[0].name, 'A').resource_records = hostRecords[0].resource_records
	
	# normally add 'A' record
	records.add_change('CREATE', hostname, 'A').resource_records = [ip]
	records.commit()
	
	return True

# 
# that assumes the instance is not created
# 
def prepareInstance(ec2con, config):
	# prepare block devices
	bdm = BlockDeviceMapping()
	bdm['/dev/sda1'] = BlockDeviceType(config['size']) # 8GB for Linux default, 30 Gb for windows
		
	# run instance
	reservation = ec2con.run_instances(
		image_id=config['ami-id'], 
		min_count=1, max_count=1, 
		key_name=config['key-name'], 
		user_data=AWS_CONFIG['DeployRegName'], 
		addressing_type=None, 
		instance_type=config['instance-type'], 
		placement=None, 
		kernel_id=None, ramdisk_id=None, 
		monitoring_enabled=True, 
		subnet_id=config['subnet-id'], 
		block_device_map=bdm, 
		disable_api_termination=True, 
		instance_initiated_shutdown_behavior=config['on-shutdown'], 
		private_ip_address=None, 
		client_token=None,
		security_group_ids=config['security-group-id'])

	print "Instance request submitted, %s" % reservation
	
	# allocate public IP address. instance must be running
	addr = ec2con.allocate_address(domain='vpc')
	instance = reservation.instances[0]
	waitTillRunning(instance)
	
	ec2con.associate_address(instance_id=instance.id, 
		allocation_id=addr.allocation_id, 
		network_interface_id=instance.networkInterfaceId)
	
	# assign friendly DNS name for external access
	# it will have internal IP embedded in it
	instance.update()
	hostName = '%s%s' % (config['dns-prefix'], instance.private_ip_address.replace('.','-'))
	instance.add_tag('Name', hostName)
	addUpdateDNS(config['dns-domain'], hostName, instance.publicIp)
	
	print "instance %s started, public DNS is %s " % (instance.id, '%s.%s'%(hostName, config['dns-domain']))
	
	return instance
	
def getConnection():
	r = ec2.get_region(region_name=AWS_CONFIG['AWS_REGION'], 
		aws_access_key_id=AWS_CONFIG['AWS_KEY'], 
		aws_secret_access_key=AWS_CONFIG['AWS_SECRET'])
	
	print "Connecting to region %s" % r
	conn = ec2.connection.EC2Connection(region=r, 
		aws_access_key_id=AWS_CONFIG['AWS_KEY'], 
		aws_secret_access_key=AWS_CONFIG['AWS_SECRET'])
	
	return conn

def waitForVolume(vol):
	while vol.update() != 'available':
		time.sleep(5)

def waitForVolumeToAttach(vol):
	while True:
		vol.update()
		st = vol.attachment_state()
		if st == 'attached':
			return
		else:
			print 'Volume %s is in %s state, waiting..' % (vol.id, st)
			time.sleep(5)

def getInstanceById(conn, instance_id):
	return conn.get_all_instances(instance_ids=instance_id)[0].instances[0]

def createAttachVolumes(instance, nVolumes, size):
	devNames = []
	for i in range(1, nVolumes+1):
		vol = instance.connection.create_volume(size, instance.placement)
		waitForVolume(vol)
		name = '/dev/sdh%d'%i
		devNames.append(name)
		try:
			instance.connection.attach_volume(instance_id=instance.id, volume_id=vol.id, device=name)
			waitForVolumeToAttach(vol)
			print "Volume %s (%dG) attached" % (name, size)
		except EC2ResponseError as e:
			print e
			vol.delete()

	return devNames

def createRAID(devices):	
	if cfapi.exists('/dev/md0'):
		print "/dev/md0 already exists on %s, nothing to do"
		return True
	
        # install mdadm

	fapi.run('wget http://archive.ubuntu.com/ubuntu/pool/main/m/mdadm/mdadm_2.6.7.1-1ubuntu15_amd64.deb')
	fapi.sudo('dpkg -i mdadm_2.6.7.1-1ubuntu15_amd64.deb')

	# initialize RAID
	fapi.sudo('mdadm --create --verbose --force --level=10 --raid-devices=%d /dev/md0 %s' % (len(devices), ' '.join(devices)))
	if cfapi.exists('/proc/mdstat'):
		fapi.run('cat /proc/mdstat')
	else:
		print "Apparently something is wrong, no /proc/mdstat"
		return False
	
	# now make filesystem on top
	fapi.sudo('mkfs.ext4 /dev/md0')
	
	# and make config file, otherwise the system won't boot
	fapi.sudo("echo \"DEVICE partitions\" > /etc/mdadm/mdadm.conf")
	fapi.sudo("mdadm --detail --scan --verbose | awk '/ARRAY/ {print}' >> /etc/mdadm/mdadm.conf")
	
	# mountpoint
	if not cfapi.exists('/raid'):
		fapi.sudo("mkdir /raid")
	cfapi.append("/etc/fstab", "/dev/md0      /raid     ext4    defaults    1 2", use_sudo=True)
	
	fapi.sudo("mount /raid")
	return '/raid'

#--------------------------------------------------------#
###      Zabbix auto_ops
#--------------------------------------------------------#
def addHostZabbix(hostname, ipAddr, type):
	
	
	# login to zabbix server
	zapi = ZabbixAPI(server=ZAB_CONF['server'], path="", log_level=6)
	zapi.login(ZAB_CONF['username'], ZAB_CONF['password'])
	# Select win or linux group
	
	if type == 'win-server':
		group_id = ZAB_CONF['win_group_id']
		template_id = ZAB_CONF['win_template_id'] 
	elif type == 'cb-server':
		group_id = ZAB_CONF['lin_group_id']
		template_id = ZAB_CONF['lin_template_id'] 	
		 	
	# Form string for Json request
	string = {'host':hostname,'ip':ipAddr,'dns':'','port':'10050','useip':1}
	string["groups"] = {'groupid': group_id}
	string ["templates"] = {'templateid': template_id}
	# Create host "string"
	createdhost=zapi.host.create(string)
	

def delHostZabbix(ip):

	# login to zabbix server
	zapi = ZabbixAPI(server=ZAB_CONF['server'], path="", log_level=6)
	zapi.login(ZAB_CONF['username'], ZAB_CONF['password'])
	
	hostids=zapi.host.get({"output":"extend", 'filter':{'ip':ip}})
	if len(hostids) == 1:
		return hostids[0]['hostid']
	else:
		print bold +"\nNothing founded. Please make sure you specified a correct IP \n"+reset
	result=zapi.host.delete({"hostid":hostids})
#--------------------------------------------------------#
###      ELB operations for win instances              ###
#--------------------------------------------------------#

def getELBConnection():
	r=RegionInfo(name='eu-west-1',endpoint='elasticloadbalancing.eu-west-1.amazonaws.com')
	
	print "Connect to region %s" %r
	conn = boto.connect_elb(aws_access_key_id=AWS_CONFIG['AWS_KEY'],aws_secret_access_key=AWS_CONFIG['AWS_SECRET'],region=r)

	return conn 

def addInstanceToELB(lb,inst):
	# Connect to ELB endpoint
	conn=getELBConnection()
	# Connect instance inst to loadbalancer LB
	lb.register_instances(inst)

def delInstanceFromELB(lb,inst):
	# Connect to ELB endpoint
	conn=getELBConnection()
	# Deregister instance inst from loadbalancer LB
	lb.degregister_instances(instance_ids)

def createLB(conn,name,regions, ports,config):
	lb = conn.create_load_balancer(name, regions, ports,subnets=config['subnet-id'], security_groups=config['security-group-id'])
	
	# Configure healthcheck
	hc = HealthCheck(interval=ELB_CONFIG['hc_interval'], 
			healthy_threshold=ELB_CONFIG['hc_healthy_threshold'],
			unhealthy_threshold=ELB_CONFIG['hc_unhealthy_threshold'], 
			target=ELB_CONFIG['hc_target']
			)

	lb.configure_health_check(hc)
	return lb

def checkLB(name,config):
	# Check if LB %name exist. If no, create it, and add CNAME DNS recort to ROUTE53
	print "balancername %s" %name
	conn = getELBConnection()
	balancers = conn.get_all_load_balancers()
	i=0
	while i<len(balancers):
		s = str(balancers[i])
		if s.find(name)>-1:
			# Balancer name already exist
			print "Balancer %s already exist" %name
			lb = balancers[i]
		else:
			print "Create balancer %s" %name
			lb = createLB(conn,name,ELB_CONFIG['regions'], ELB_CONFIG['ports'],config) 
		
			# Create CNAME DNS record for name ELB_CONFIG['balancerName'].tigris.peakgames.net
			conn = boto.route53.connection.Route53Connection(aws_access_key_id = AWS_CONFIG['AWS_KEY'], aws_secret_access_key=AWS_CONFIG['AWS_SECRET'], host='route53.amazonaws.com')
			ch = ResourceRecordSets(conn,ELB_CONFIG['hostedzoneID'])
			rec = ch.add_change("CREATE",'%s.tigris.peakgames.net' %ELB_CONFIG['balancerName'], "CNAME",60)
			rec.add_value(lb.dns_name)
			ch.commit()
		i=i+1
	return lb

#--------------------------------------------------------#
###         Create new instances                      ###
#--------------------------------------------------------#

def launchMore(type, count):
	ec2con = getConnection()
	
	if type not in INSTANCE_CONFIG:
		print "No configuration for instance type %s " % type
		return
	
	print 'Launching %s instances of type %s with configuration \n %s\n' % (count, type, INSTANCE_CONFIG[type])

	instList = []
	for i in range(0,int(count)):
		inst = prepareInstance(ec2con, INSTANCE_CONFIG[type])
		if not inst:
			print "Error creating instances, abort"
			return
		# Configure RAID for DB servers
		if 'RAID' in INSTANCE_CONFIG[type]:
			vols = createAttachVolumes(inst, INSTANCE_CONFIG[type]['RAID']['disks'], INSTANCE_CONFIG[type]['RAID']['size'])
			with (fapi.settings(host_string=inst.publicIp)):
				createRAID(vols)

		instList.append(inst.id)
		
	#For win instances add instance to ELB ELB_CONFIG['elb_name']
		if type == 'win-server':
			# check if application is runing 
			http_link = "http://"+str(inst.publicIp)+"/help"
			if urllib.urlopen(http_link):
				lb = checkLB(ELB_CONFIG['elb_name'],INSTANCE_CONFIG[type])
				print "Add Win instance to ELB %s" % ELB_CONFIG['elb_name']
				addInstanceToELB(lb,inst.id)
		# Register instance to zabbix
		name = type+'-'+inst.publicIp
		addHostZabbix(name,inst.publicIp,type)

	print "Launched instances IDs : %s " % instList
	
if __name__ == "__main__":
	prepareInstance(getConnection(), INSTANCE_CONFIG)
