from fabric.api import *
from fabric.contrib.console import confirm
import fabric 
from tigrisCONFIGforCB.py import *



def couch_check():
	# check if couchbase-serv available on server
	dpkgLog = run ('dpkg -l')
	if dpkgLog.find('couchbase-serv') != -1:
		print('CouchBase exist')
	else:
		print ('CouchBase not here and will be installed now. ')
	# Download Coachbase
		run (' wget http://packages.couchbase.com/releases/1.8.0/couchbase-server-community_x86_64_1.8.0.deb')
	# Install CoachBase	
		sudo ('dpkg -i couchbase-server-community_x86_64_1.8.0.deb')

def conf_check():
	# Check configuration file. If -name string not here,create it and add to config 

	# Stop service
	sudo ('service couchbase-server stop')
    
	# Get conf file from server #/opt/couchbase/bin/couchbase-server'
	fabric.operations.get('/opt/couchbase/bin/couchbase-server', './tmp/fromServ')

	frServ = open ('./tmp/fromServ','r+')
	toServ = open ('./tmp/toServ','r+')
	data = frServ.read()
	strings = data.splitlines()
	frServ.close()

	i = 0    
	l = len(strings)

	# Remove empty strings from the end of strins array
 	while strings[l-1-i].strip()=='':
		strings.pop(l-1-i)
		i=i+1

	# Write strings array elemets to output config file
	i = 0
 	while i<(len(strings)-1):
		strings[i] = strings[i]+'\n'
		toServ.writelines(strings[i])
		i = i+1
	
	# Check last string
 	if strings[i].count("-name ") == 0:
    	# Write last string to output config file. If last symbol not \, add it    
 		if strings[i][len(strings[i])-1] != '\\':
 			toServ.writelines(strings[i]+'\\'+'\n')       
	 	else:
			toServ.writelines(strings[i]+'\n')
    # Recive IP addres from server
		ipAddr = run('hostname -I')
    # Form and write name string
		toServ.writelines("    -name ns@"+ipAddr)
	else:
		toServ.writelines(strings[i])

	toServ.close()

# Send conf file to server

	fabric.operations.put('./tmp/toServ', '/opt/couchbase/bin/couchbase-server', use_sudo=True)


# Start DB service
	sudo ('chown couchbase:couchbase /opt/couchbase/bin/couchbase-server && chmod 755 /opt/couchbase/bin/couchbase-server ')   
	sudo ('service couchbase-server start')

def addToCluster():

	# Configure new node and add it to cluster. Rebalance cluster

	ipAddr = run('hostname -I')
	
	sudo('/opt/couchbase/bin/couchbase-cli rebalance -c '+CB_CONF['clusterIP']+':8091 -u qa-tigris -p qa-tigris --server-add='+ipAddr+' --server-add-username= qa-tigris --server-add-password =qa-tigris')

    
def newclusterInit():

	# Should Work once, only on master node
	#  Set username,password, ram allocation

	run('/opt/couchbase/bin/couchbase-cli cluster-init -c '+CB_CONF['clusterIP']+':8091 --cluster-init-username='+CB_CONF['uName']+' --cluster-init-password='+CB_CONF['pwd']+' --cluster-init-port=8091 --cluster-init-ramsize='+CB_CONF['ClusterInitRamsize'])

	# Set data path for node

	run('/opt/couchbase/bin/couchbase-cli node-init -c '+CB_CONF['clusterIP']+':8091 -u '+CB_CONF['uName']+' -p '+CB_CONF['pwd']+' --node-init-data-path='+CB_CONF['data-dir'])

	# Create bukets

	run('/opt/couchbase/bin/couchbase-cli bucket-create -c '+CB_CONF['clusterIP']+':8091 -u '+CB_CONF['uName']+' -p '+ CB_CONF['pwd']+' --bucket=profiles --bucket-type=membase --bucket-ramsize='+ CB_CONF['profilesQuota'])

	run('/opt/couchbase/bin/couchbase-cli bucket-create -c '+CB_CONF['clusterIP']+':8091 -u '+CB_CONF['uName']+' -p '+CB_CONF['pwd']+' --bucket=sessions --bucket-type=membase --bucket-ramsize='+CB_CONF['sessionsQuota'])

	run('/opt/couchbase/bin/couchbase-cli bucket-create -c '+CB_CONF['clusterIP']+':8091 -u '+CB_CONF['uName']+' -p '+CB_CONF['pwd']+' --bucket=sessionlist --bucket-type=membase --bucket-ramsize='+CB_CONF['sessionlistQuota'])

def install_s3cmd():
	run ('wget "http://downloads.sourceforge.net/project/s3tools/s3cmd/1.1.0-beta3/s3cmd-1.1.0-beta3.tar.gz?r=http%3A%2F%2Fsourceforge.net%2Fprojects%2Fs3tools%2F&ts=1339515276&use_mirror=freefr"') 
	run ('mv s3cmd-1.1.0-beta3.tar.gz* s3cmd-1.1.0-beta3.tar.gz') 
	run ('tar -xvf s3cmd-1.1.0-beta3.tar.gz')
	sudo ('cd s3cmd-1.1.0-beta3/ && python setup.py install ')
	fabric.operations.put('/script_Git/.s3cfg', '/home/ubuntu')
	#run ('s3cmd --configure ')

