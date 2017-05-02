import os
import subprocess
print "Welcome to PANTEL - a Python based virtual assistant"
def save(filename, data):
	fw = open(filename,'w')
	for l in data:
		fw.write('{}: {}\n'.format(l,data[l]))
	fw.close()
def load(filename):
	if os.path.isfile(filename):
		fr = open(filename,'r')
		lines = fr.readlines()
		fr.close()
		data = {}
		for rawl in lines:
			rawl = ''.join(rawl.split('\n'))
			l = rawl.split(': ')
			if len(l)>1:
				data[l[0]] = l[1]
		return data
	else:
		return {}
def configure():
	if 'name' in database['.user_preferences']:
		print 'Welcome back, {}'.format(database['.user_preferences']['name'])
	else:
		name = raw_input('How should I call you?\t')
		print 'OK, welcome {}'.format(name)
		database['.user_preferences']['name'] = name
		save('.user_preferences',database['.user_preferences'])

database = {}
database['.user_preferences'] = load('.user_preferences')
database['.commands'] = load('.commands')
configure()
interface = ['add','delete','create','show','quit','exit', 'remove','what\'s', 'execute', 'run']

def runcmd(cmd):
	return subprocess.check_output(cmd)

def execute(commands):
	for command in commands:
		if command[0] == 'add' or command[0] == 'create':
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
					database['.commands'][newCommand] = ';'.join(commandsList)
		elif command[0] == 'show' or command[0] == 'what\'s':
			if len(command)<2:
				print 'show what?'
			else:
				if command[1] == 'database':
					print database
				elif command[1] in database:
					print database[command[1]]
				else:
					print '{} does not exist in my database.'.format(command[1])
		elif command[0] == 'delete':
			if len(command)<2:
				print 'delete what?'
			else:
				if command[1] in database:
					database[command[1]] = {}
					configure()
				elif command[1] == 'command':
					database['.commands'].pop(' '.join(command[2:]))
				else:
					print '{} does not exist in my database.'.format(command[1])
		elif command[0] == 'run' or command[0] == 'execute':
			if len(command)<2:
				print runcmd(raw_input('Execute what?\t').split(' '))
			else:
				print runcmd(command[1:])
run = 1
while run:
	command = raw_input('>>>').split(' ')
	if (len(command)==0) or (not (command[0] in interface) and not (' '.join(command) in database['.commands'])):
		print '{} is an invalid command.'.format(' '.join(command))
		print 'A command must start with: '
		print interface
		print database['.commands']
	elif command[0] == 'quit' or command[0] == 'exit':
		for f in database:
			save(f, database[f])
		run = 0
	elif ' '.join(command) in database['.commands']:
			commands = []
			arguments = {}
			for arg in command:
				if arg[0] == '$':
					arguments[arg] = raw_input('{}='.format(arg))
				elif arg[0:2] == '\\$':
					command[command.index(arg)] = '${}'.format(arg[1:])
			for cmd in database['.commands'][' '.join(command)].split(';'):
				scmd = cmd.split(' ')
				for argument in arguments:
					if argument in scmd:
						scmd[scmd.index(argument)] = arguments[argument]
				commands.append(' '.join(scmd).split(' '))
			execute(commands)
	elif command[0] in interface:
		execute([command])
	else:
		print 'unforseen-failure.'
		run = 0
