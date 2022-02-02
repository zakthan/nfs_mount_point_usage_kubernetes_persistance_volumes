import argparse
from functions import runcommand
from functions import output_command
from functions import look_for_other_nfs_servers


# Create the parser
parser = argparse.ArgumentParser()

# Add an argument
parser.add_argument('--threshold', type=int, required=True)
parser.add_argument('--nfsserver', type=str, required=True)

# Parse the argument. If argument is empty or not good put default argument 
try:
  args = parser.parse_args()
  ##The usage threshold if none is given as an argument
  usage_threshold  = args.threshold
  ##The ip of the NFS server
  nfsserver  = args.nfsserver
except:
  ##The usage threshold if none is given as an argument
  usage_threshold  = 85
  ##The ip of the NFS server if none is given as an argument
  nfsserver="10.53.187.250"
  print('---------------------------------------------------------------------------------------------------------------------------------------')
  print(f"This script needs an int --threshold arg and a str --nfsserver arg.  Putting default value for threshold={usage_threshold} and nfsserver={nfsserver}")
  print('---------------------------------------------------------------------------------------------------------------------------------------')

#Print the value of the variable
print('-----------------------------------------------------------------------')
print('The value of the threshold for disk space and inodes is', str(usage_threshold) + "% of the usage")
print('The value of the NFS server is ', nfsserver)
print('-----------------------------------------------------------------------')

#Check for NFS servers other than the nfs server given
look_for_other_nfs_servers(nfsserver)

##Get a list of the namespaces. 
get_namespaces_command="kubectl get ns --no-headers -o jsonpath='{.items[*].metadata.name}'"
list_of_namespaces = output_command(get_namespaces_command)
##debug##print(type(list_of_namespaces))
##debug##print(list_of_namespaces)

##For all the namespaces
for current_namespace in list_of_namespaces:
  ##Get a list of pods per namespace
  ###debug##print("Now checking NAMESPACE:",current_namespace)
  get_po_per_namespace_command="kubectl -n %s  get po -o jsonpath='{.items[*].metadata.name}'"%current_namespace
  list_of_pods_per_namespace = output_command(get_po_per_namespace_command,"True")
  get_pvc_per_namespace_command="kubectl -n %s  get pvc -o jsonpath='{.items[*].metadata.name}'"%current_namespace
  list_of_pvcs_per_namespace = output_command(get_pvc_per_namespace_command,"True")
  ##If the namespace has at least one pod and there is at least one pvc at the namespace
  if (len(list_of_pods_per_namespace) > 0 and len(list_of_pods_per_namespace[0]) >0 and len(list_of_pvcs_per_namespace) >0 and len(list_of_pvcs_per_namespace[0]) >0) :
   ##For every pod inside the namespace get the nfs mounts
   for pod in list_of_pods_per_namespace:
     ##debug#print ("Now checking POD:",pod)
     list_mounts_command = "kubectl -n %s exec -it %s -- mount 2>/dev/null|grep %s"%(current_namespace, pod, nfsserver)
     mounts_per_pod = output_command(list_mounts_command,"False","False")
     substring = "var/lib/kubelet/pods"
     
     #If there are mounts get the df for these mounts
     if (len(mounts_per_pod) > 0 and len(mounts_per_pod[0]) > 0):
       if not substring in mounts_per_pod[2] :
          ###debug## print("NFS export for the pod is:",mounts_per_pod[0],mounts_per_pod[2])
          df_command = 'kubectl -n {0} exec -it {1} -- df -hP {2}'.format(current_namespace,pod,mounts_per_pod[2])
          df_command_inodes = 'kubectl -n {0} exec -it {1} -- df -hPi {2}'.format(current_namespace,pod,mounts_per_pod[2])
          df_usage= output_command(df_command)
          df_usage_inodes= output_command(df_command_inodes)
          
          #Compare size with threshold value
          if int(df_usage[-2].replace("%", "")) >= usage_threshold:
            print("----------------------------------------------------------------------------------------------------------------------------------------")
            print("PROBLEM!!You need to check usage for mount point ", df_usage[-1],"Usage is ", df_usage[-2],"The pod is ",pod," and the namespace is ",current_namespace)
            print("----------------------------------------------------------------------------------------------------------------------------------------")

          if int(df_usage_inodes[-2].replace("%", "")) >= usage_threshold:
            print("----------------------------------------------------------------------------------------------------------------------------------------")
            print("PROBLEM!!You need to check inodes usage for mount point ", df_usage_inodes[-1],"Usage is ", df_usage_inodes[-2],"The pod is ",pod," and the namespace is ",current_namespace)
            print("----------------------------------------------------------------------------------------------------------------------------------------")
