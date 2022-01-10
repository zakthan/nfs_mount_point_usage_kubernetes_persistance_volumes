from runcommand import runcommand

nfsserver="10.53.187.250"
usage_threshold=50
##Get a list of the namespaces. 
get_namespaces_command="kubectl get ns --no-headers -o jsonpath='{.items[*].metadata.name}'"
code, stdout, err = runcommand(get_namespaces_command)
if code!=0:
  print("-----------------------------------------------------------------")
  print(f"For the command: {get_namespaces_command} \nThe error is : {err}")
  print("-----------------------------------------------------------------")
  exit()
##Convert str output to list
list_of_namespaces = stdout.split(" ")
##debug##print(type(list_of_namespaces))
##debug##print(list_of_namespaces)

##For all the namespaces
for current_namespace in list_of_namespaces:
  ##Get a list of pods per namespace
  ##Use the same convertion like namespaces to convert from str to a list
  ##debug##print(current_namespace)
  get_po_per_namespace_command="kubectl -n %s  get po -o jsonpath='{.items[*].metadata.name}'"%current_namespace
  ##debug##print(get_po_per_namespace_command)
  code2, stdout2, err2 = runcommand(get_po_per_namespace_command)
  if code2!=0:
    print("-----------------------------------------------------------------")
    print(f"For the command: {get_po_per_namespace_command} \nThe error is : {err2}")
    print("-----------------------------------------------------------------")
    exit()
  list_of_pods_per_namespace = stdout2.split(" ")
  ##debug##print(type(list_of_pods_per_namespace))
  ##debug##print(list_of_pods_per_namespace)
  get_pvc_per_namespace_command="kubectl -n %s  get pvc -o jsonpath='{.items[*].metadata.name}'"%current_namespace
  ##debug##print(get_pvc_per_namespace_command)
  code4, stdout4, err4 = runcommand(get_pvc_per_namespace_command)
  if code2!=0:
    print("-----------------------------------------------------------------")
    print(f"For the command: {get_po_per_namespace_command} \nThe error is : {err4}")
    print("-----------------------------------------------------------------")
    exit()
  list_of_pvcs_per_namespace = stdout4.split(" ")
  ##If the namespace has at least one pod and there is at least one pvc at the namespace
  ##debug##print(current_namespace,list_of_pods_per_namespace,list_of_pvcs_per_namespace)
  if len(list_of_pods_per_namespace) > 0 and len(list_of_pods_per_namespace[0]) >0 and len(list_of_pvcs_per_namespace) >0 and len(list_of_pods_per_namespace[0]) >0 :
   ##For every pod inside the namespace get the nfs mounts
   for pod in list_of_pods_per_namespace:
     list_mounts_command = "kubectl -n %s exec -it %s -- mount 2>/dev/null|grep %s"%(current_namespace, pod, nfsserver)
     code3, stdout3, err3 = runcommand(list_mounts_command)
     if code3 == 0:
       mounts_per_pod = stdout3.split(" ")
       substring = "var/lib/kubelet/pods"
       if not substring in mounts_per_pod[2]:
         df_command = 'kubectl -n {0} exec -it {1} -- df -hP {2}'.format(current_namespace,pod,mounts_per_pod[2])
         code5, stdout5, err5 = runcommand(df_command)
         if code5!=0:
           print("-----------------------------------------------------------------")
           print(f"For the command: {get_po_per_namespace_command} \nThe error is : {err5}")
           print("-----------------------------------------------------------------")
           exit()
         df_usage= stdout5.split(" ")
         if int(df_usage[-2].replace("%", "")) >= usage_threshold:
           print("You need to check usage for mount point ", df_usage[-1],"Usage is ", df_usage[-2],"The pod is ",pod," and the namespace is ",current_namespace)
