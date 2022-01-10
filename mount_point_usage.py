from runcommand import runcommand
from runcommand import output_command

nfsserver="10.53.187.250"
usage_threshold=50
##Get a list of the namespaces. 
get_namespaces_command="kubectl get ns --no-headers -o jsonpath='{.items[*].metadata.name}'"
list_of_namespaces = output_command(get_namespaces_command)
##debug##print(type(list_of_namespaces))
##debug##print(list_of_namespaces)

##For all the namespaces
for current_namespace in list_of_namespaces:
  ##Get a list of pods per namespace
  print("Now checking NAMESPACE:",current_namespace)
  get_po_per_namespace_command="kubectl -n %s  get po -o jsonpath='{.items[*].metadata.name}'"%current_namespace
  list_of_pods_per_namespace = output_command(get_po_per_namespace_command,"True")
  ##debug##print(type(list_of_pods_per_namespace))
  ##debug##print(list_of_pods_per_namespace)
  get_pvc_per_namespace_command="kubectl -n %s  get pvc -o jsonpath='{.items[*].metadata.name}'"%current_namespace
  list_of_pvcs_per_namespace = output_command(get_pvc_per_namespace_command,"True")
  ##If the namespace has at least one pod and there is at least one pvc at the namespace
  ##debug##print(current_namespace,list_of_pods_per_namespace,list_of_pvcs_per_namespace)
  if (len(list_of_pods_per_namespace) > 0 and len(list_of_pods_per_namespace[0]) >0 and len(list_of_pvcs_per_namespace) >0 and len(list_of_pvcs_per_namespace[0]) >0) :
   ##For every pod inside the namespace get the nfs mounts
   for pod in list_of_pods_per_namespace:
     print ("Now checking POD:",pod)
     list_mounts_command = "kubectl -n %s exec -it %s -- mount 2>/dev/null|grep %s"%(current_namespace, pod, nfsserver)
     mounts_per_pod = output_command(list_mounts_command,"False","False")
     substring = "var/lib/kubelet/pods"
     ##debug##print(mounts_per_pod) 
     if (len(mounts_per_pod) > 0 and len(mounts_per_pod[0]) > 0):
       if not substring in mounts_per_pod[2] :
          df_command = 'kubectl -n {0} exec -it {1} -- df -hP {2}'.format(current_namespace,pod,mounts_per_pod[2])
          df_usage= output_command(df_command)
          if int(df_usage[-2].replace("%", "")) >= usage_threshold:
            print("----------------------------------------------------------------------------------------------------------------------------------------")
            print("PROBLEM!!You need to check usage for mount point ", df_usage[-1],"Usage is ", df_usage[-2],"The pod is ",pod," and the namespace is ",current_namespace)
            print("----------------------------------------------------------------------------------------------------------------------------------------")
