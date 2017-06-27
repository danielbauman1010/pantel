import os
import sys
import socket
import random
import string
import subprocess

def save(filename, data):
	fw = open(filename,'w')
	for l in data:
		fw.write('{}: {}\n'.format(l,data[l]))
	fw.close()

def load(filename):
	data = {}
	if os.path.isfile(filename):
		fr = open(filename,'r')
		lines = fr.readlines()
		fr.close()
		for rawl in lines:
			rawl = ''.join(rawl.split('\n'))
			l = rawl.split(': ')
			if len(l)>1:
				data[l[0]] = l[1]
	return data

def runcmd(cmd):
	return subprocess.check_output(cmd)

def listen(ip,port):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((ip,port))
	s.listen(3000)
	return s

def connect(ip,port):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((ip,port))
	return s

def pantelcmd(command):
	runcmd(['cp','pantel.py','cpantel.py'])
	splitcmd = command.split(' ')
	cmd = ['python','cpantel.py']
	for arg in splitcmd:
		cmd.append(arg)
	result = '{}'.format(runcmd(cmd))
	runcmd(['rm','-rf','cpantel.py'])
	return result

if sys.argv[1] == "install":
	currcommands = load('../commands.data')
	currcommands['add connect $setup'] = 'run python data/libraries/connectLib.py add $setup'
	currcommands['show connect setups'] = 'run python data/libraries/connectLib.py show'
	currcommands['delete connect $setup'] = 'run python data/libraries/connectLib.py delete $setup'
	currcommands['connect listen active $setup'] = 'run python data/libraries/connectLib.py listen -a $setup'
	currcommands['connect listen passive $setup'] = 'run python data/libraries/connectLib.py listen -p $setup'
	currcommands['send $setup $key $command'] = 'run python data/libraries/connectLib.py send $setup $key $command'	
	currcommands['connect to $setup $key'] = 'run python data/libraries/connectLib.py connect $setup $key'
	save('../commands.data',currcommands)
else:
	ips = load('data/connectIPs.data')
	ports = load('data/connectPorts.data')
	if sys.argv[1] == "add":
		ips[sys.argv[2]] = sys.argv[3]
		ports[sys.argv[2]] = sys.argv[4]
	elif sys.argv[1] == "show":
		for name,ip in ips.iteritems():
			print '{}:'.format(name)
			print '\t{}'.format(ip)
			print '\t{}'.format(ports[name])
	elif sys.argv[1] == "delete":
		ips.pop(sys.argv[2])
		ports.pop(sys.argv[2])
	elif sys.argv[1] == "listen":
		if sys.argv[2] == '-a':
			ip = ips[sys.argv[3]]
			port = int(ports[sys.argv[3]])
			chars = string.ascii_letters + string.digits + '!@#$%^&*()'
			random.seed = (os.urandom(1024))
			key = ''.join(random.choice(chars) for i in range(10))
			print key
			fw = open('key.txt','w')
			fw.write(key)
			fw.close()
			server = listen(ip,port)
			while 1:
				client,addr = server.accept()
				passlisten = 1
				listen = 0
				passcounter = 0
				while passlisten:
					passtry = client.recv(1024)
					if len(passtry)>0:
						print passtry
					if passtry == key:
						passlisten = 0
						listen = 1
						client.send('connected.')
						print '{} connected'.format(addr)
					else:
						passcounter = passcounter + 1
						client.send('wrong password, try again.')
						if passcounter == 3:
							passlisten = 0
							client.send('login failed.')
							fw = open('intruder{}.txt'.format(addr),'w')
							fw.write('{}'.format(addr))
							fw.close()
				while listen:
					command = client.recv(1024)
					if len(command)>0:
						if command == 'quit':
							listen = 0
							client.send('quiting')
							client.close()
						else:
							reply = pantelcmd(command)
							if reply == '':
								reply = 'no reply.\n'
							client.send(reply)
		elif sys.argv[2] == '-p':
			ip = ips[sys.argv[3]]
			port = int(ports[sys.argv[3]])
			chars = string.ascii_letters + string.digits + '!@#$%^&*()'
			random.seed = (os.urandom(1024))
			key = ''.join(random.choice(chars) for i in range(10))
			print key
			fw = open('key.txt','w')
			fw.write(key)
			fw.close()
			server = listen(ip,port)
			while 1:
				client,addr = server.accept()
				passlisten = 1
				listen = 0
				passcounter = 0
				while passlisten:
					passtry = client.recv(1024)
					if len(passtry)>0:
						print passtry
						if passtry == key:
							passlisten = 0
							print 'they are equal'
							listen = 1
							client.send('connected.')
							print '{} connected'.format(addr)
						else:
							print 'they are not equal'
							passcounter = passcounter + 1
							client.send('wrong password, try again.')
							if passcounter == 3:
								passlisten = 0
								client.send('login failed.')
								fw = open('intruder{}.txt'.format(addr),'w')
								fw.write('{}'.format(addr))
								fw.close()
				while listen:
					command = client.recv(1024)
					if len(command)>0:
						reply = pantelcmd(command)
						if reply == '':
							reply = 'no reply.\n'
						client.send(reply)
						listen = 0
						client.close()
	elif sys.argv[1]=='connect':
		ip = ips[sys.argv[2]]
		port = int(ports[sys.argv[2]])
		key = sys.argv[3]
		server = connect(ip,port)
		server.send(key)
		passsuccess = 1
		listen = 0
		while passsuccess:
			reply = server.recv(1024)
			if len(reply)>0:
				print reply
				if reply == 'connected.':
					passsuccess = 0
					listen = 1
				elif reply == 'wrong password, try again.':
					key = raw_input('key:\t')
					server.send(key)
				elif reply == 'login failed.':
					passsuccess = 0
		while listen:
			command = raw_input('>>>')
			server.send(command)
			tryreply = 1
			while tryreply:
				reply = server.recv(1024)
				if len(reply)>0:
					print reply
				tryreply = 0
			if command == 'quit':
				server.close()
				listen = 0
	elif sys.argv[1] == 'send':
		ip = ips[sys.argv[2]]
		port = int(ports[sys.argv[2]])
		key = sys.argv[3]
		server = connect(ip,port)
		server.send(key)
		passsuccess = 1
		loggedIn = 0
		while passsuccess:
			reply = server.recv(1024)
			if len(reply)>0:
				print reply
				if reply == 'connected.':
					passsuccess = 0
					loggedIn = 1
				elif reply == 'wrong password, try again.':
					key = raw_input('key:\t')
					server.send(key)
				elif reply == 'login failed.':
					passsuccess = 0
		if loggedIn:
			command = sys.argv[4:]
			server.send(' '.join(command))
			tryreply = 1
			while tryreply:
				reply = server.recv(1024)
				if len(reply)>0:
					print reply
					tryreply = 0
			loggedIn = 0
			server.close()
	save('data/connectIPs.data',ips)
	save('data/connectPorts.data',ports)
