#Author: Thanassis Zakopoulos
#Usage: This script calculates the NFS mounts of the nodes of a k8s cluster and alerts if disk or inode usage is above a given threshold
#!/bin/bash


#The IP of the NFS Server
NFS_SERVER="1.2.3.4"

#The threshold 
USAGE_THRESHOLD=60

#Get all the nodes of the k8s cluster
NODES=$(kubectl get nodes --no-headers|awk '{print $1}')

#For every node of the cluster find the NFS mount points
for NODE in  $NODES
do 
  MOUNTS=$(ssh $NODE "mount|grep $NFS_SERVER" |awk '{print $1" " $3}')
  MOUNT_POINTS=$(echo $MOUNTS|awk '{print $2}')
  for MOUNT_POINT in $MOUNT_POINTS
  do 
    DF_MOUNTPOINT=$(ssh $NODE "df -hP $MOUNT_POINT|grep -v Filesystem")
    INODES_MOUNTPOINT=$(ssh $NODE "df -ihP $MOUNT_POINT|grep -v Filesystem")
    USAGE=$(echo $DF_MOUNTPOINT|awk '{print $5}'|tr "%" " ")
    INODES_USAGE=$(echo $INODES_MOUNTPOINT|awk '{print $5}'|tr "%" " ")
    NFS_EXPORT=$(echo $DF_MOUNTPOINT|awk '{print $1}')
    NFS_EXPORT_INODES=$(echo $INODES_MOUNTPOINT|awk '{print $1}')
    if (( $USAGE > $USAGE_THRESHOLD ))
    then
	echo DISK USAGE  : Check $NODE for NFS export $NFS_EXPORT disk usage  $USAGE%  that is bigger than $USAGE_THRESHOLD%
    fi
    if (( $INODES_USAGE > $USAGE_THRESHOLD ))
    then
	echo INODES USAGE: Check $NODE for NFS export $NFS_EXPORT_INODES inodes usage $INODES_USAGE% that is bigger than $USAGE_THRESHOLD%
    fi
  done

done
