#!/usr/bin/python3.6

import re,sys,os

_YAML_PATH = '/root/middleware/1_TrafficLoadManager'
_MIN_REPLICAS = sys.argv[1]
_MAX_REPLICAS = sys.argv[2]
_CPU_UTILIZATION = sys.argv[3]

template='\
apiVersion: autoscaling/v1\n\
kind: HorizontalPodAutoscaler\n\
metadata:\n\
  name: keystone-app-hpa\n\
  namespace: default\n\
spec:\n\
  minReplicas: min_count\n\
  maxReplicas: max_count\n\
  scaleTargetRef:\n\
    apiVersion: apps/v1\n\
    kind: Deployment\n\
    name: keystone-app\n\
  targetCPUUtilizationPercentage: cpu_utilization\n'

os.chdir(_YAML_PATH)
f = open('TrafficLoadManagement.yaml', 'wt')
f.write(template.replace('min_count', _MIN_REPLICAS).replace('max_count', _MAX_REPLICAS).replace('cpu_utilization', _CPU_UTILIZATION))
f.close()

os.system('kubectl create -f TrafficLoadManagement.yaml')
