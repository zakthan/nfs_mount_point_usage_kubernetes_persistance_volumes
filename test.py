import subprocess
##subprocess.check_output('k exec -it bb -- mount|grep aaa')
aaa= subprocess.check_output(["kubectl", "get", "po"])
print(aaa)
subprocess.check_call(['ls'], stdout = DEVNULL, stderr = STDOUT)
