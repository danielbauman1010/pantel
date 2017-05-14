import os
import subprocess
print "Welcome to PANTEL - a Python based virtual assistant"
if not os.path.isdir('data'):
	os.mkdir('data')
if not os.path.isdir('data/libraries'):
	os.mkdir('data/libraries')
def save(filename, data):
	fw = open('data/{}.data'.format(filename),'w')
	for l in data:
		fw.write('{}: {}\n'.format(l,data[l]))
	fw.close()
def load(filename):
	if os.path.isfile('data/{}.data'.format(filename)):
		fr = open('data/{}.data'.format(filename),'r')
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
def configure():
	if 'name' in database['user_preferences']:
		print 'Welcome back, {}'.format(database['user_preferences']['name'])
	else:
		name = raw_input('How should I call you?\t')
		print 'OK, welcome {}'.format(name)
		database['user_preferences']['name'] = name
		save('user_preferences',database['user_preferences'])

database = {}
database['user_preferences'] = load('user_preferences')
database['commands'] = load('commands')
configure()
interface = ['add','delete','create','show','quit','exit', 'remove','what\'s', 'execute', 'run', 'read', 'save']

def runcmd(cmd):
	return subprocess.check_output(cmd)

def pretty_print(d):
	for i in d:
		print '{}: {}'.format(i, d[i])

arguments = {}

def process_custom_command(command):
	commands = []
	for cmd in database['commands'][command].split(';'):
		scmd = cmd.split(' ')
		if cmd not in database['commands']:
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
		if ' '.join(command) in database['commands']:
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
					database['commands'][newCommand] = ';'.join(commandsList)
				elif command[1] == 'to':
					if len(command)<4:
						print 'save what to where?'
					else:
						if command[2] == 'database':
							database[' '.join(command[3:])] = {}
						elif ' '.join(' '.join(command).split(':')[0].split(' ')[2:]) in database:
							database[' '.join(' '.join(command).split(':')[0].split(' ')[2:])][' '.join(command).split(':')[1].split('=')[0]] = ' '.join(command).split(':')[1].split('=')[1]
		elif command[0] == 'show' or command[0] == 'what\'s' or command[0] == 'read':
			if len(command)<2:
				print 'show what?'
			else:
				if command[1] == 'database':
					pretty_print(database)
				elif ' '.join(command[1:]) in database:
					pretty_print(database[' '.join(command[1:])])
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
					database['commands'].pop(' '.join(command[2:]))
				else:
					print '{} does not exist in my database.'.format(command[1])
		elif command[0] == 'run' or command[0] == 'execute':
			if len(command)<2:
				print runcmd(raw_input('Execute what?\t').split(' '))
			else:
				print runcmd(command[1:])
		else:
			print 'unforseen-failure.'
			run = 0

run = 1
while run:
	command = raw_input('>>>').split(' ')
	arguments = {}
	if (len(command)==0) or (not (command[0] in interface) and not (' '.join(command) in database['commands'])):
		print '{} is an invalid command.'.format(' '.join(command))
		print 'A command must start with: '
		print interface
		print database['commands']
	elif command[0] == 'quit' or command[0] == 'exit':
		for f in database:
			save(f, database[f])
		run = 0
	else:
		for word in command:
			if word[0] == '$':
				arguments[word] = raw_input('{}='.format(word))
			elif word[0] == '{' and word[len(word)-1] == '}':
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
