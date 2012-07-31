#!/usr/bin/ksh
GRINDERPATH=/opt/grinder-3.8
GRINDERPROPERTIES=/home/sveta/Tigris/qa/server/grinder.properties
CLASSPATH=$GRINDERPATH/lib/grinder.jar:$CLASSPATH
JAVA_HOME=/usr/lib/jvm/java-6-openjdk
JYTHON_HOME=/home/sveta/jython2.5.2
PATH=$JYTHON_HOME:$JAVA_HOME/bin:$PATH
export CLASSPATH PATH GRINDERPROPERTIES
