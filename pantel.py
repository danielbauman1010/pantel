# Imports:

import os, subprocess, sys, platform


#=====================================================================================================


# Pre-defined-values: 

#	paths and dirs:

keypaths = {}
keydirs = {}

keydirs['datadir'] = 'data'
keydirs['personaldir'] = os.path.join(datadir,'personal')
keydirs['librariesdir'] = os.path.join(datadir,'libraries')
keypaths['user_preferences_path'] = os.path.join(personaldir,'user_preferences.settings')
keypaths['custom_commands_path'] = os.path.join(personaldir,'custom.commands')
 

#-----------------------------------------------------------------------------------------------------

#	dictionaries:

allcommands = {}
database = {}


#=====================================================================================================


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


#=====================================================================================================


# Check for missing environment

def check_config():
	for path in keypaths:
		if not os.path.exists(keypaths[path]):
			save(keypaths[path],{})
	for dir in keydirs:
		if not os.path.exists(keydirs[dir]):
			os.mkdir(keydirs[dir])
	for c in database:
		if c not in os.listdir(datadir):
			os.mkdir(c)
		for f in database[c]: 
			fpath = os.path.join(datadir,c,f)
			if not f in os.listdir(fpath):
				save(fpath,database[c][f])


#=====================================================================================================


# Data control:

#c=category, d=dict, k=key, e=entry

#	categories:

def addc(c):
	database[c] = {}
	cpath = os.path.join(datadir,c)
	if not os.path.isdir(cpath):
		os.mkdir(path)
	return 1

def getc(c):
	if not c in database:
		return -2
	return database[c]

def delc(c):
	database.pop(c)
	os.rmdir(os.path.join(datadir,c))

#-----------------------------------------------------------------------------------------------------

#	dictionaries (files):

def addd(c,d):
	if not c in database:
		return -2
	database[c][d] = {}
	fpath = os.path.join(datadir,c,d)	
	if not os.path.exists(fpath):
		save(fpath, database[c][d])
	return 1

def getd(c,d):
	if not c in database:
		return -2
	if not d in database[c]:
		return -1
	return database[c][d]

def deld(c,d):
	if not c in database:
		return -2
	database[c].pop(d)
	os.remove(os.path.join(datadir,c,d))
	return 1	

#-----------------------------------------------------------------------------------------------------

#	entries:

def adde(c,d,k,e):
	if not c in database:
		return -2
	if not d in database[c]:
		return -1
	database[c][d][k]=e
	save(os.path.join(datadir,c,d),database[c][d])
	return 1

def gete(c,d,k):
	if not c in database:
		return -2
	if not d in database[c]:
		return -1
	if not k in database[c][d]:
		return 0
	return database[c][d][k]

def dele(c,d,k):
	if not c in database:
		return -2
	if not d in database[c]:
		return -1
	if not k in database[c][d]:
		return 0
	database[c][d].pop(k)
	return 1

#=====================================================================================================


# Configuration for new user:


def configure():
	if 'name' not in database['personal']['user_preferences.settings']:
		name = raw_input('How should I call you?\t')
		print 'OK, welcome {}'.format(name)
		adde('personal','user_preferences.settings','name',name)


#=====================================================================================================


# Command-line:

def runcmd(cmd):
	return subprocess.check_output(cmd)

def runpython(scr):
	cmd = ['python']
	for part in scr.split(' '):
		cmd.append(part)
	return subprocess.check_output(cmd)


#=====================================================================================================


# Loading database:


#	load all files:

for dir in os.listdir(datadir):
	database[dir] = {}
	for filename in os.listdir(os.path.join(datadir,dir)):
		database[dir][filename] = load(os.path.join(datadir,dir,filename))

#-----------------------------------------------------------------------------------------------------

#	load commands separately

for categoryname, category in database.iteritems():
	for listname, list in category.iteritems():
		if listname.endswith(".commands"):
			for command, translation in list.iteritems():
				allcommands[command] = translation


#=====================================================================================================


# Interface definition:

interface = ['add','delete','create','show','quit','exit', 'remove','what\'s', 'execute', 'run', 'read', 'save']


#=====================================================================================================


# Custom printing:

def list_print(d):
	for i in d:
		print '{}: {}'.format(i, d[i])

def category_print(c):
	print c
	for listname,list in database[c].iteritems():
		print '\t{}'.format(listname)


#=====================================================================================================


# Handle commands: (main)


# 	set arguments and process custom commands:
	
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

#-----------------------------------------------------------------------------------------------------

#	execute commands:

def execute(commands):
	for command in commands:
		#check for pre-defined commands
		scommand = ' '.join(command).split(' %')
		if len(scommand) > 1:
			command = scommand[0].split(' ')
			args = ' %'.join(scommand[1:]).split(' $')
			for arg in args:
				if arg is not '':
					sarg = arg.split(' = ')
					arguments['${}'.format(sarg[0])] = ' = '.join(sarg[1:])
		#check if in commands:
		if ' '.join(command) in allcommands:
			execute(process_custom_command(' '.join(command)))
		#otherwise - check if database related:
		#adding:
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
					commandstr = ';'.join(commandsList)
					adde(personaldir,'custom.commands',newCommand, commandstr)
					allcommands[newCommand] = commandstr
				elif command[1] == 'to':
					if len(command)<4:
						print 'save what to where?'
					else:
						potdict = ' '.join(command[3:]) #potentially dict
						potargsparts = ' '.join(command[2:]).split(':')
						potdname = potargsparts[0]
						potdparts = ':'.join(potargsparts[1:]).split('=')
						potdkey = potdparts[0]
						potde = '='.join(potdparts[1:])
						if command[2] == 'personal':
							if addd('personal',potdict) is not 1:
								print 'category error -  personal doesn\'t exist!'
						elif potdname in database['personal']:
							r = adde('personal',potdname, potdkey,potde)
							if r == -2:
								print 'personal doesn\'t exist!'
							if r == -1:
								print '{} doesn\'t exist!'.format(potdname)
								  
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
				potc = ' '.join(command[1:]) 
				if potc in database:
					delc(potc)
					if potc == 'personal':
						os.mkdir(personaldir)
						configure()
					elif potc == 'libraries':
						os.mkdir(librariesdir)
				else:
					if len(command)<2:
						print 'delete what to where?'
					else:
						potargs = ' '.join(command[1:]).split(':')
						potc = potargs[0]
						potd = potargs[1]
						poteparts = potparts[1].split('=')
						potdname = poteparts[0]
						potk = poteparts[1]
						if potc in database and potd in database[potc]:
							deld(potc,potd)
				
						if potc in database and potdname in database[pote]:
							dele(potc,potdname,potk)
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
