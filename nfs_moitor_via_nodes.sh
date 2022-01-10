#Author: Thanassis Zakopoulos
#Usage: This script calculates the NFS mounts of the nodes of a k8s cluster and alerts if disk or inode usage is above a given threshold
#!/bin/bash
NFS_SERVER="10.53.187.250"
USAGE_THRESHOLD=60
NODES=$(kubectl get nodes --no-headers|awk '{print $1}')
for NODE in  $NODES
do 
  MOUNTS=$(ssh $NODE "mount|grep $NFS_SERVER" |awk '{print $1" " $3}')
  MOUNT_POINTS=$(echo $MOUNTS|awk '{print $2}')
  for MOUNT_POINT in $MOUNT_POINTS
  do 
    ##echo $NODE
    DF_MOUNTPOINT=$(ssh $NODE "df -hP $MOUNT_POINT|grep -v Filesystem")
    ##echo DF_MOUNTPOINT is $DF_MOUNTPOINT
    INODES_MOUNTPOINT=$(ssh $NODE "df -ihP $MOUNT_POINT|grep -v Filesystem")
    ##echo INODES_MOUNTPOINT is $INODES_MOUNTPOINT
    USAGE=$(echo $DF_MOUNTPOINT|awk '{print $5}'|tr "%" " ")
    INODES_USAGE=$(echo $INODES_MOUNTPOINT|awk '{print $5}'|tr "%" " ")
    NFS_EXPORT=$(echo $DF_MOUNTPOINT|awk '{print $1}')
    NFS_EXPORT_INODES=$(echo $INODES_MOUNTPOINT|awk '{print $1}')
    if (( $USAGE > $USAGE_THRESHOLD ))
    then
	echo DISK USAGE  : Check $NODE for NFS export $NFS_EXPORT disk usage that is bigger than $USAGE_THRESHOLD%
    fi
    if (( $INODES_USAGE > $USAGE_THRESHOLD ))
    then
	echo INODES USAGE: Check $NODE for NFS export $NFS_EXPORT_INODES inodes usage that is bigger than $USAGE_THRESHOLD%
    fi
  done

done
