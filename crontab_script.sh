##Athor: Athanasios Zakopoulos
## This scipt takes 3 arguments. 
##First is prod or uat enviromet
##Second is the value of the threshhold (if empty python script has default)
##The third is the IP of the NFS server (if empty python script has default)


#!/bin/bash
PYTHON_FILE="mount_point_usage.py"
SCRIPT_PATH=$(echo $0|sed 's/\$PYTHON_FILE//g')
##MAILLIST="k8sadmins.GRC01@ote.gr"
MAILLIST="azakopoulos@ote.gr"
THRESHOLD="--threshold=$2"
NFS_SERVER="--nfsserver=$3"

   case $1 in
      uat) 
           ENV=UAT
           KCTX="ucp_tk8smaster01.cosmote.gr:6443_admin"
           LOG="$SCRIPT_PATH/mount_point_usage.$ENV.log";; 
      prod) 
           ENV=PROD
           KCTX="ucp_pk8smaster.cosmote.gr:6443_admin"
           LOG="$SCRIPT_PATH/mount_point_usage.$ENV.log" ;;
      *) 
         echo Wrong argument . Accepted values are prod or uat
         exit 1;;
   esac

##empty old log
cat /dev/null > $LOG

##run script, put output into a log file and send to recipients
##PATH and k8s context needs to be set because of crontab
export PATH="/usr/local/bin:$PATH"
kubectl config --kubeconfig=$HOME/.kube/config use-context $KCTX

##if threshold and nfs server are given run script with arguments. Otherwise run with default values
if [ -z "$2" ] || [ -z "$3" ]
then
      python3 $SCRIPT_PATH/$PYTHON_FILE  > $LOG 
else
      python3 $SCRIPT_PATH/$PYTHON_FILE $THRESHOLD $NFS_SERVER > $LOG 

fi

## If no usage is above threshold do not sent any email
COUNTER=$(cat counter.txt)
if [[ $COUNTER -gt 0 ]]
then
mailx -s "k8s nfs usage $ENV" $MAILLIST < $LOG
fi
