# Nfs mount point usage of Persistance volumes for kubernetes clusters.
---

This repository contains a python and a bash script.

Both scripts need a bastion host to run that has ssh connectivity using ssh keys to the nodes of the cluster

Run "python3 mount_point_usage.py" for python script

Run "./nfs_moitor_via_nodes.sh" for shell script"

## Python Script

- Usage: python3 mount_point_usage.py --threshold <INT> --nfsserver <STR> (if no argument is given default value is threshold=90 and nfsserver=10.53.187.250

- This script is doing the following:
  1. Checks for bounded PVs with IP other than the given NFS server. If any found , for each different IP, it prints the IP and the bounded PVs of it.
  2. It parses all the namespaces of the k8s cluster.
  3. For each namespace it checks for running pods and PVCs.
  4. If it finds at least one pod and at least one PVC:
     - It check the mounts of each pod for the IP of the NFS server.
       - If NFS mount is found it checks for the disk free of the exported folder and compares this value with the given threshold.
       - If disk or inodes usage is more than the given threshold it prints info for this export and the pod.

## Bash Script

- Usage: ./nfs_moitor_via_nodes.sh

- If a pod uses NFS mounts , kubernetes is mounting the NFS export at the node running this pod.
  Therefore this script:
  1. Parses the kuberentes cluster for all it's nodes


## To do:

- For Python script to work we need namespaces to have at least one running pod
- What happens if pod has 2 or more NFS mounts
