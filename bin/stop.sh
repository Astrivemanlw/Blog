#!/bin/bash
pids=`ps -ef | grep gunicorn | grep -v grep | awk '{print $2}'`
for id in ${pids}
do	
	 echo "process $id killed!"
	 kill -9 $id
done
