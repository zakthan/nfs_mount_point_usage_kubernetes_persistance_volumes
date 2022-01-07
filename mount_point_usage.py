import subprocess
import sys
##Get a list of the namespaces. 
##subprocess.check_output is returing bytes , so we conver bytes to string with decode and string to list with split
list_of_namespaces = subprocess.check_output("kubectl get ns --no-headers -o jsonpath='{.items[*].metadata.name}'",shell=True).decode(sys.stdout.encoding).split(" ")
#print(type(list_of_namespaces))
#print(list_of_namespaces)
