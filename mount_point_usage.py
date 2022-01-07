import subprocess
import sys
##Get a list of the namespaces. 
##subprocess.check_output is returing bytes , so we conver bytes to string with decode and string to list with split
list_of_namespaces = subprocess.check_output("kubectl get ns --no-headers -o jsonpath='{.items[*].metadata.name}'",shell=True).decode(sys.stdout.encoding).split(" ")
#print(type(list_of_namespaces))
#print(list_of_namespaces)
##Get a list of pods per namespace
##Use the same convertion like namespaces to convert from bytes to a list
for current_namespace in list_of_namespaces:
 ##print(current_namespace)
 list_of_pods_per_namespace = subprocess.check_output("kubectl -n %s  get po -o jsonpath='{.items[*].metadata.name}'" % current_namespace,shell=True).decode(sys.stdout.encoding).split(" ")
 print(type(list_of_pods_per_namespace))
 print(list_of_pods_per_namespace)
