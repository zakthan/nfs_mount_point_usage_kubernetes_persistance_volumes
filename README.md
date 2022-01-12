# Nfs mount point usage of Persistance volumes for kubernetes clusters.
---

This repository contains a python and a bash script.

Both scripts need a bastion host to run that has ssh connectivity using ssh keys to the nodes of the cluster

Run "python3 mount_point_usage.py" for python script

Run "./nfs_moitor_via_nodes.sh" for shell script"

## Python Script

- Usage: python3 mount_point_usage.py --threshold <INT> --nfsserver <STR> (if no argument is given default value is threshold=90 and nfsserver=10.53.187.250

- This script id doing the following:
  1. Checks for bounded PVs 

## To do:

- For Python script to work we need namespaces to have at least one running pod
- What happens if pod has 2 mounts
