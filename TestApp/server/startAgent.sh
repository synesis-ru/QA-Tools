#!/usr/bin/ksh
. /home/sveta/Tigris/qa/server/setGrinderEnv.sh
java -classpath $CLASSPATH net.grinder.Grinder $GRINDERPROPERTIES
