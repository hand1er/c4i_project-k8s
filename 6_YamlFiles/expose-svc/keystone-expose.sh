#!/bin/bash


kubectl expose deployment keystone-app --type=LoadBalancer --name=keystone-external --external-ip="172.21.2.123" --port=5000 --target-port=5000

