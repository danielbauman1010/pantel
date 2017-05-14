import os
import sys

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

def read(filename):
	if os.path.isfile(filename):
		fr = open(filename,'r')
		lines = fr.readlines()
		fr.close()
		data = []
		for l in lines:
			l = ''.join(l.split('\n'))
			data.append(l)
		return data
	else:
		return []
def write(filename,data):
	fw = open(filename,'w')
	for l in data:
		fw.write('{}\n'.format(l))
	fw.close()

if len(sys.argv) < 2:
    print 'Arguments needed to run.'
elif sys.argv[1] == 'read':
    if len(sys.argv)<3:
        print 'read what?'
    else:
        lines = read(' '.join(sys.argv[2:]))
        for l in lines:
            print l
elif sys.argv[1] == 'write':
    if len(sys.argv)<4:
        print 'Write what and to where?'
    else:
        splitedargs = ' '.join(sys.argv[2:]).split(' : ')
        if len(splitedargs) < 2:
            print 'Write to where?'
        else:
            filename = splitedargs[0]
            text = ' : '.join(splitedargs[1:]).split(';')
            write(filename,text)
elif sys.argv[1] == 'install':
	currcommands = load('../commands.data')
	currcommands['read $file'] = 'run python data/libraries/fileLib.py read $file'
	currcommands['write $text to $file'] = 'run python data/libraries/fileLib.py write $file : $text'
	currcommands['write {text} to $file'] = 'run python data/libraries/fileLib.py write $file : {text}'
	currcommands['show files'] = 'run ls'
	currcommands['show files in $dir'] = 'run ls $dir'
	save('../commands.data',currcommands)
