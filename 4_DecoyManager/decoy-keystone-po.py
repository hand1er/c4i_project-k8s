#!/usr/bin/python3.6

import re,sys,os

_YAML_PATH = '/root/middleware/4_DecoyManager'
_DECOY_COUNT = sys.argv[1]

po_template='\
apiVersion: apps/v1\n\
kind: Deployment\n\
metadata:\n\
 name: decoy-keystone-app\n\
spec:\n\
 replicas: decoy_count\n\
 selector:\n\
  matchLabels:\n\
   app: decoy-keystone\n\
 template:\n\
  metadata:\n\
   labels:\n\
    app: decoy-keystone\n\
  spec:\n\
   containers:\n\
   - name: decoy-keystone\n\
     image: obedmr/keystone\n\
     securityContext:\n\
       privileged: true\n\
     env:\n\
     - name: DATABASE_HOST\n\
       value: 10.105.16.120:3306\n\
     - name: KEYSTONE_DB_USER\n\
       value: keystone\n\
     - name: KEYSTONE_DB_PASSWORD\n\
       value: secret\n\
     - name: KEYSTONE_DB_NAME\n\
       value: keystone\n\
     resources:\n\
       requests:\n\
          cpu: "300m"\n\
       limits:\n\
          cpu: "300m"\n'


os.chdir(_YAML_PATH)
f = open('DecoyManagement.yaml', 'wt')
f.write(po_template.replace('decoy_count', _DECOY_COUNT))
f.close()

os.system('kubectl create -f DecoyManagement.yaml') 
