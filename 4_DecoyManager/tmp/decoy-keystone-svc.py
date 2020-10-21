#!/usr/bin/python3.6
import sys,random, subprocess, os, time
from multiprocessing import Pool, Process

_PROCESS = 10
_IP_COUNT = int(sys.argv[1])
_PORT_COUNT = int(sys.argv[2])
_YAML_PATH = '/tmp/decoy/yaml/'

service_template='\
apiVersion: v1\n\
kind: Service\n\
metadata:\n\
 name: decoy-1\n\
 labels:\n\
  app: decoy-keystone\n\
spec:\n\
 type: ClusterIP\n\
 selector:\n\
  app: decoy-keystone\n\
 ports:\n'

def create_service(name):
	cmd='kubectl create -f '+str(name)+'.yaml'
	try:
 		subprocess.check_output(cmd.split(' '),timeout=5)
	except subprocess.CalledProcessError as e:
		print("error:",e.output)

def delete_service(name):
	cmd='kubectl delete svc '+name
	try:
		subprocess.check_output(cmd.split(' '),timeout=5)
	except subprocess.CalledProcessError as e:
		print("error:",e.output)

def create_service_file(cnt):
        fout = open(str(cnt)+'.yaml','wt')
        fout.write(service_template.replace('decoy-1','decoy-'+str(cnt+1)))
        random_port_list = random.sample(range(1,65535),_PORT_COUNT)
        port_string="  - name: portname\n    port: number\n    targetPort: 5000\n    protocol: TCP\n"
        for i in range(len(random_port_list)):
                fout.write(port_string.replace('portname','decoy'+str(random_port_list[i])).replace('number',str(random_port_list[i])))
        fout.close()

if __name__ == '__main__':
    if not(os.path.isdir(_YAML_PATH)):
        os.makedirs(os.path.join(_YAML_PATH))

    os.chdir(_YAML_PATH)

    pool = Pool(_PROCESS)

    start=time.time()
    cmd = "kubectl get svc|grep 'decoy'|awk '{print $1}'"
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0].decode('utf-8').split('\n')[:-1]
    if len(output) > 0:
        pool.map(delete_service, output)
    pool.map(create_service_file, range(_IP_COUNT))
    pool.map(create_service, range(_IP_COUNT))

    time = "%.3fs finished" %(time.time()-start)

    fout = open('/tmp/decoy/decoy.log','a')
    fout.write(time)
    fout.write('\n')
    fout.close()
