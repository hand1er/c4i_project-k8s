#!/usr/bin/python3.6
import hashlib, re, sys, os, random, time, datetime

_YAML_PATH = '/root/middleware/5_NetworkHoppingManager/yaml-file/'
HASH_NUM = 5
password = sys.argv[1]
NETWORK_CLASS = int(sys.argv[2])
interval = int(sys.argv[3])

service_template='\
apiVersion: v1\n\
kind: Service\n\
metadata:\n\
 name: keystone-service-n\n\
 labels:\n\
  app: keystone\n\
spec:\n\
 type: LoadBalancer\n\
 clusterIP: ip_addr\n\
 selector:\n\
  app: keystone\n\
 ports:\n'

# hash 리스트 생성
hash_data = list()
encoded_password = password.encode()
hexdigest = hashlib.sha256(encoded_password).hexdigest()
for i in range(HASH_NUM):
    hash_data.append(hexdigest)
    encoded_hexdigest = hexdigest.encode()
    hexdigest = hashlib.sha256(encoded_hexdigest).hexdigest()
hash_data.reverse()

# ip address 리스트 생성
addr_data = list()
f = open('/root/middleware/5_NetworkHoppingManager/ip_addr.txt','w')

#if NETWORK_CLASS == 0:
#for i in range(HASH_NUM):
#    parse  = re.sub('[0]', '', hash_data[i])
#    number_extraction = re.findall("\d", parse)
#    addr_data.append("10." + number_extraction[1] + number_extraction[2] + "." + number_extraction[3] + number_extraction[4] + "." + number_extraction[5] + number_extraction[6])
#    f.write(addr_data[i] + "\n")
#f.close()

#if NETWORK_CLASS == 1:
#  for i in range(HASH_NUM):
#    parse  = re.sub('[0]', '', hash_data[i])
#    number_extraction = re.findall("\d", parse)
#    addr_data.append("10.96." + number_extraction[1] + number_extraction[2]  + "." + number_extraction[3] + number_extraction[4])
#    f.write(addr_data[i] + "\n")
#  f.close()

if NETWORK_CLASS == 2:
  for i in range(HASH_NUM):
    parse  = re.sub('[0]', '', hash_data[i])
    number_extraction = re.findall("\d", parse)
    addr_data.append("10.105.197." + number_extraction[1] + number_extraction[2])
    f.write(addr_data[i] + "\n")
  f.close()


# .yaml 파일 생성
os.chdir(_YAML_PATH)
for i in range(HASH_NUM):
    f = open(str(i) + "_" + addr_data[i] + '.yaml', 'wt')
    f.write(service_template.replace('keystone-service-n', 'keystone-service-' + str(i+1)).replace('ip_addr', addr_data[i]))
    random_port = random.sample(range(1,65535), 1)
    port_string = "  - name: default\n    port: number\n    targetPort: 5000\n    protocol: TCP\n"
    f.write(port_string.replace('number', str(random_port[0])))
#    f.write(port_string.replace('number', '5000'))
    selector = " selector:\n  app: keystone\n"
    f.write(selector)
f.close()

# hopping
os.system('kubectl delete svc keystone-service')
os.system('kubectl create -f 0_' + addr_data[0] + '.yaml')
time.sleep(interval)
ff = open("/var/log/service-change.log","w")
ff.write("------------------------------------------\n")
ff.close()
for i in range(HASH_NUM):
    if(i%12==11):
        os.system('echo hi')
        time.sleep(2)
    ff = open("/var/log/service-change.log","a")
    if(i==HASH_NUM-1):
        ff.write(str(datetime.datetime.now())+" "+ addr_data[i] + " => FINISHED\n")
    else:
        ff.write(str(datetime.datetime.now())+" "+ addr_data[i] + " => " + addr_data[i+1] +"\n")
    time.sleep(interval)
    if(i<HASH_NUM-1):
        os.system('kubectl create -f ' + str(i+1) + "_" + addr_data[i+1] + '.yaml')
        time.sleep(5)
        os.system('kubectl delete -f ' + str(i+0) + "_" + addr_data[i] + '.yaml')
    ff.close()

