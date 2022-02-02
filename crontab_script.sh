##Athor: Athanasios Zakopoulos
## This scipt takes one argument. prod or uat

#!/bin/bash
SCRIPT_PATH=/root/scripts/scripts/k8sadmin/nfs_mount_point_usage/
PYTHON_FILE="mount_point_usage.py"
MAILLIST="k8sadmins.GRC01@ote.gr"

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
cat /dev/null > LOG

##run script, put output into a log file and send to recipients
##PATH and k8s context needs to be set because of crontab
echo AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
export PATH="/usr/local/bin:$PATH"
kubectl config --kubeconfig=/root/.kube/config use-context $KCTX
python3 $SCRIPT_PATH/$PYTHON_FILE > $LOG && mailx -s "k8s nfs usage $ENV" $MAILLIST < $LOG
