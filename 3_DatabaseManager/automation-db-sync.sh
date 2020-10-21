#!/bin/sh

echo "[*] ETCD Creating"
kubectl create -f database-sync-solution/1_etcd-create.yaml
sleep 10 
kubectl exec -it etcd0 -- etcdctl cluster-health

echo "[*] Persistent Volume and Persistent Volume Claim Creating"
kubectl create -f database-sync-solution/2_pv-create.yaml
kubectl create -f database-sync-solution/3_pvc-create.yaml
sleep 2

echo "[*] PV and PVC Bound Check"
kubectl get pv,pvc
sleep 2

echo "[*] Maria DB Creating"
kubectl create -f database-sync-solution/4_mariadb-create.yaml
sleep 3
