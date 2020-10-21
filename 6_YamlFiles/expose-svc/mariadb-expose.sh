#!/bin/bash

kubectl expose pod galera-ss-0 --type=LoadBalancer --name=mariadb-external --external-ip="172.21.2.123" --port=3306 --target-port=3306

