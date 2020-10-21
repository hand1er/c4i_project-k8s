#!/bin/sh

version=$1
check5000=``
if [ $# -eq 1 ];then
        sed -i 's/version/'"$version"'/' /root/middleware/2_VersionManager/Dockerfile
   echo “[*] Dockerfile is updated”
fi
docker build -t yayaja11/keystoneimage:$version /root/middleware/2_VersionManager 
sleep 1
sed -i 's/'"$version"'/version/' /root/middleware/2_VersionManager/Dockerfile

sleep 10
kubectl set image deployments/keystone-app keystone=yayaja11/keystoneimage:$version
sleep 10
kubectl rollout status deployment/keystone-app
sleep 15
echo "[*] keystone is upgraded to $version"
