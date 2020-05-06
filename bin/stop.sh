#!/bin/bash
pids=`ps -ef | grep gunicorn | grep -v grep | awk '{print $2}'`
for id in ${pids}
do	
	 echo "$id"
	 kill -9 $id
done
