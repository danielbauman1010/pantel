# The imports:

import os, subprocess, sys, platform


#=====================================================================================================


# Pre-defined-values: 



#		paths:

datadir = 'data'
personaldir = 'personal'
user_preferences_filename = 'user_preferences.settings'
custom_commands_filename = 'custom.commands'
librariesdir = 'libraries' 

allcommands = {}
database = {}


# Accessing filesystem helper-functions:

def save(filename, data):	#saves dict in file
	fw = open(filename,'w')
	for l in data:
		fw.write('{}: {}\n'.format(l,data[l]))
	fw.close()


def load(filename):	#reads dict from file
	if os.path.isfile(filename):
		fr = open(filename,'r')
		lines = fr.readlines()
		fr.close()
		data = {}
		for rawl in lines:
			rawl = ''.join(rawl.split('\n'))
			l = rawl.split(': ')
			if len(l)>1:
				data[l[0]] = ': '.join(l[1:])
		return data
	else:
		return {}


#check for startup/non-existing folders:

#check for data directory
if not os.path.isdir(datadir):
	os.mkdir(datadir)

#check for libraries directory:
if not os.path.isdir('{}/{}'.format(datadir,librariesdir)):
	os.mkdir('{}/{}'.format(datadir,librariesdir))

#check for personal directory:

if not os.path.isdir('{}/{}'.format(datadir,personaldir)):
	os.mkdir('{}/{}'.format(datadir,personaldir))


#check for user_preferences file
if not os.path.isfile('{}/{}/{}'.formayt(datadir,personaldir,user_preferences_filename)):
	osdata = {}
	osdata['os-type'] = platform.system()
	osdata['os-version'] = platform.release()
	save('{}/{}/{}'.format(datadir,personaldir,user_preferences_filename),osdata)

#check for custom_commands file
if not os.path.isfile('{}/{}/{}'.format(datadir,personaldir,custom_commands_filename)):
	custom_commands_data = {}
	save('{}/{}/{}'.format(datadir,personaldir,custom_commands_filename),custom_commands_data)

#data control:


#checks and returns:
def checkc

#adding categories
def addc(c):
	database[c] = {}
	cpath = '{}/{}'.format(datadir,c)
	if not os.path.isdir(cpath):
		os.mkdir(path)

#adding dictionaries (files)
def addd(c,d):
	database[c][d] = {}
	


def add_entry(c,d,k,e):	#c=category, d=dict, k=key, e=entry
	database[c][d][k]=e
	save('{}/{}/{}.data'.format(datadir,c,d),database[c][d])

def get_entry(c,d,k):
	if not c in database:
		return -2
	if not d in database[c]:
		return -1
	if not k in database[c][d]:
		return 0
	return database[d][k]


#configuration for new user:

def configure():
	if 'name' not in user_preferences:
		name = raw_input('How should I call you?\t')
		print 'OK, welcome {}'.format(name)
		add_data('personal','user_preferences.settings','name',name)


#command-line

def runcmd(cmd):
	return subprocess.check_output(cmd)

def runpython(scr):
	cmd = ['python']
	for part in scr.split(' '):
		cmd.append(part)
	return subprocess.check_output(cmd)

#loading database:

#load all files:

for dir in os.listdir(datadir):
	database[dir] = {}
	for filename in os.listdir(os.path.join(datadir,dir)):
		database[dir][filename] = load(os.path.join(datadir,dir,filename))
#load commands separately

for categoryname, category in database.iteritems():
	for listname, list in category.iteritems():
		if listname.endswith(".commands"):
			for command, translation in list.iteritems():
				allcommands[command] = translation


#interface definition:

interface = ['add','delete','create','show','quit','exit', 'remove','what\'s', 'execute', 'run', 'read', 'save']


#custom printing:

def list_print(d):
	for i in d:
		print '{}: {}'.format(i, d[i])

def category_print(c):
	print c
	for listname,list in database[c].iteritems():
		print '\t{}'.format(listname)

#set arguments and process custom commands:
	
arguments = {}

def process_custom_command(command):
	commands = []
	for cmd in allcommands[command].split(';'):
		scmd = cmd.split(' ')
		scommand = ' '.join(scmd).split(' %')
		if len(scommand) > 1:
			scmd = scommand[0].split(' ')
			args = ' %'.join(scommand[1:]).split(' $')
			for arg in args:
				if arg is not '':
					sarg = arg.split(' = ')
					arguments['${}'.format(sarg[0])] = ' = '.join(sarg[1:])
		if ' '.join(scmd) not in allcommands:
			for arg in scmd:
				if arg[0] == '$' or (arg[0] == '{' and arg[len(arg)-1] == '}'):
					if arg in arguments:
						scmd[scmd.index(arg)] = arguments[arg]
					else:
						scmd[scmd.index(arg)] = raw_input('{}='.format(arg))
		commands.append(scmd)
	return commands

def execute(commands):
	for command in commands:
		scommand = ' '.join(command).split(' %')
		if len(scommand) > 1:
			command = scommand[0].split(' ')
			args = ' %'.join(scommand[1:]).split(' $')
			for arg in args:
				if arg is not '':
					sarg = arg.split(' = ')
					arguments['${}'.format(sarg[0])] = ' = '.join(sarg[1:])
		if ' '.join(command) in allcommands:
			execute(process_custom_command(' '.join(command)))
		elif command[0] == 'add' or command[0] == 'create' or command[0] == 'save':
			if len(command)<2:
				print 'add what?'
			else:
				if command[1] == 'command':
					newCommand = raw_input('New command:\t')
					tryrun = 1
					print 'Conversion to old commands:'
					commandsList = []
					while tryrun:
						anotherCommand = raw_input('')
						if len(anotherCommand) == 0:
							tryrun = 0
						else:
							commandsList.append(anotherCommand)
					add_data(personaldir,custom_commands_filename,newCommand, ';'.join(commandsList))
					allcommands[newCommand] = ';'.join(commandsList)
				elif command[1] == 'to':
					if len(command)<4:
						print 'save what to where?'
					else:
						if command[2] == 'personal':
							database['personal'][' '.join(command[3:])] = {}
							save('{}/{}/{}'.format(datadir,personaldir,' '.join(command[3:])), {})
						elif ' '.join(' '.join(command).split(':')[0].split(' ')[2:]) in database['personal']:
							add_data('personal',' '.join(' '.join(command).split(':')[0].split(' ')[2:]), ':'.join(' '.join(command).split(':')[1:]).split('=')[0], '='.join(':'.join(' '.join(command).split(':')[1:]).split('=')[1:])) 
		elif command[0] == 'show' or command[0] == 'what\'s' or command[0] == 'read':
			if len(command)<2:
				print 'show what?'
			else:
				if command[1] == 'database':
					for category in database:
						category_print(category)
				elif ' '.join(command[1:]) in database:
					category_print(' '.join(command[1:]))
				else:
					splitedcmd = ' '.join(command[1:]).split(':')
					if splitedcmd[0] in database and splitedcmd[1] in database[splitedcmd[0]]:
						list_print(database[splitedcmd[0]][splitedcmd[1]])
					else:
						print '{} does not exist in my database.'.format(command[1:])
		elif command[0] == 'delete':
			if len(command)<2:
				print 'delete what?'
			else:
				if ' '.join(command[1:]) in database:
					database[' '.join(command[1:])] = {}
					runcmd(['rm','-rf','{}/{}'.format(datadir,' '.join(command[1:]))])
					if ' '.join(command[1:]) == personaldir:
						runcmd(['mkdir','{}/{}'.format(datadir,personaldir)])						
						configure()
					elif ' '.join(command[1]) == librariesdir:
						runcmd(['mkdir','{}/{}'.format(datadir,librariesdir)])
				elif command[1] == 'from':
					if len(command)<3:
						print 'delete what to where?'
					else:
						if ' '.join(command[2:]).split(':')[0] in database and ' '.join(command[2:]).split(':')[1] in database[' '.join(command[2:]).split(':')[0]]:
							database[' '.join(command[2:]).split(':')[0]].pop(' '.join(command[2:]).split(':')[1])
							deleting_command = ['rm','-rf','{}/{}/{}'.format(datadir,' '.join(command[2:]).split(':')[0],' '.join(command[2:]).split(':')[1])]
							runcmd(deleting_command)
				else:
					if command[1] == 'entry':
						parts = ' '.join(command[2:]).split(':')
						c = parts[0]
						d = parts[1]
						k = parts[2]
						database[c][d].pop(k)
						save('{}/{}/{}'.format(datadir,c,d))
					else:					
						print '{} does not exist in my database.'.format(' '.join(command[1:]))
		elif command[0] == 'run' or command[0] == 'execute':
			if len(command)<2:
				print runcmd(raw_input('Execute what?\t').split(' '))
			else:
				print runcmd(command[1:])
		else:
			print 'unforseen-failure.'
			run = 0
if len(sys.argv)>1:
	command = sys.argv[1:]
	for i in command:
		if i[0] == '*':
			command[command.index(i)] = '${}'.format(i[1:])
	arguments = {}
	scommand = ' '.join(command).split(' %')
	if len(scommand) > 1:
		command = scommand[0].split(' ')
		args = ' %'.join(scommand[1:]).split(' $')
		for arg in args:
			if arg is not '':
				sarg = arg.split(' = ')
				arguments['${}'.format(sarg[0])] = ' = '.join(sarg[1:])
	if (len(command)==0) or (not (command[0] in interface) and not (' '.join(command) in allcommands)):
		print '{} is an invalid command.'.format(' '.join(command))
		print 'A command must start with: '
		print interface
		list_print(allcommands)
	else:
		for word in command:
			if word[0] == '$':
				if word not in arguments:
					arguments[word] = raw_input('{}='.format(word))
			elif word[0] == '{' and word[len(word)-1] == '}':
				if word not in arguments:
					print '{} :'.format(word)
					tryRun = True
					lines = []
					while tryRun:
						nextline = raw_input('')
						if nextline is '':
							tryRun = False
						else:
							lines.append(nextline)
						arguments[word] = '{}'.format(';'.join(lines))
		execute([command])
	for c in database:
		for d in database[c]:
			save('{}/{}/{}'.format(datadir,c,d),database[c][d])
else:
	run = 1
	print "Welcome to PANTEL - a Python based virtual assistant"
	print 'Welcome back, {}'.format(database[personaldir][user_preferences_filename]['name'])
	while run:
		command = raw_input('>>>').split(' ')
		arguments = {}
		scommand = ' '.join(command).split(' %')
		if len(scommand) > 1:
			command = scommand[0].split(' ')
			args = ' %'.join(scommand[1:]).split(' $')
			for arg in args:
				if arg is not '':
					sarg = arg.split(' = ')
					arguments['${}'.format(sarg[0])] = ' = '.join(sarg[1:])
		if (len(command)==0) or (not (command[0] in interface) and not (' '.join(command) in allcommands)):
			print '{} is an invalid command.'.format(' '.join(command))
			print 'A command must start with: '
			print interface
			list_print(allcommands)
		elif command[0] == 'quit' or command[0] == 'exit':			
			for c in database:
				for d in database[c]:
					save('{}/{}/{}'.format(datadir,c,d),database[c][d])
			run = 0
		else:
			for word in command:
				if len(word)>0:
					if word[0] == '$':
						if word not in arguments:
							arguments[word] = raw_input('{}='.format(word))
					elif word[0] == '{' and word[len(word)-1] == '}':
						if word not in arguments:
							print '{} :'.format(word)
							tryRun = True
							lines = []
							while tryRun:
								nextline = raw_input('')
								if nextline is '':
									tryRun = False
								else:
									lines.append(nextline)
								arguments[word] = '{}'.format(';'.join(lines))
			execute([command])
