import sys
import paramiko
import time
key = paramiko.RSAKey.from_private_key_file(sys.argv[1]) #'/Users/amaldb/Downloads/amal-test.pem'
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=sys.argv[2], username="ec2-user", pkey=key) #13.126.163.195
with open('pem.txt','r') as pem:
    sshpem = pem.read()
print(sshpem)
cmd = ['sudo adduser ','sudo su - ','mkdir .ssh','chmod 700 .ssh','touch .ssh/authorized_keys','chmod 600 .ssh/authorized_keys','cat >> .ssh/authorized_keys',sshpem]
cmd[0]+=sys.argv[3]
cmd[1]+=sys.argv[3]
channel = client.invoke_shell()

# clear welcome message and send newline
time.sleep(1) 
channel.recv(9999)
channel.send("\n")
time.sleep(1)

for command in cmd:
    channel.send(command + "\n")
    while not channel.recv_ready(): #Wait for the server to read and respond
        time.sleep(0.1)
    time.sleep(0.1) #wait enough for writing to (hopefully) be finished
    output = channel.recv(9999) #read in
    print(output.decode('utf-8'))
    time.sleep(0.1)
channel.close()
print("Added keys")

# close the client connection once the job is done

client.close()

#except Exception, e:
    #print(e)