import os
import sys
import subprocess
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

def runcmd(cmd,loc):
	return subprocess.check_output(cmd,cwd=loc)

repositories = load('data/gitLib.data')

if len(sys.argv)<2:
    print 'Do what?'
else:
	if sys.argv[1] == 'add':
		if len(sys.argv)<5:
			print 'Add what?'
		else:
			if sys.argv[2] == 'rep':
				repositories['{}'.format(sys.argv[3])] = '{}'.format(sys.argv[4])
			elif sys.argv[2] == 'file':
				runcmd(['git','add','{}'.format(sys.argv[4])],repositories[sys.argv[3]])
	elif sys.argv[1] == 'init':
		if len(sys.argv)<4:
			print 'Where is the repository?'
		else:
			repositories['{}'.format(sys.argv[2])] = '{}'.format(sys.argv[3])
			runcmd(['git','init'],sys.argv[3])
	elif sys.argv[1] == 'status':
		print runcmd(['git','status'],repositories[sys.argv[2]])
	elif sys.argv[1] == 'delete':
		if len(sys.argv)<4:
			print 'Delete what?'
		else:
			if sys.argv[2] == 'rep':
				repositories.pop(sys.argv[3])
			elif sys.argv[2] == 'file':
				runcmd(['git','rm','-rf','{}'.format(sys.argv[4])],repositories[sys.argv[3]])
	elif sys.argv[1] == 'show':
		if sys.argv[2] == 'repositories':
			for r in repositories:
				print '{}: {}'.format(r,repositories[r])
		elif sys.argv[2] in repositories:
			print repositories[sys.argv[2]]
	elif sys.argv[1] == 'commit':
		if len(sys.argv)<4:
			print 'A message is required when commiting.'
		else:
			runcmd(['git','commit','-m','\"{}\"'.format(' '.join(sys.argv[3:]))],repositories[sys.argv[2]])
	elif sys.argv[1] == 'origin':
		runcmd(['git','remote','add','origin',sys.argv[3]],repositories[sys.argv[2]])
	elif sys.argv[1] == 'checkout':
		runcmd(['git','checkout',sys.argv[3]],repositories[sys.argv[2]])
	elif sys.argv[1] == 'new':
		runcmd(['git','checkout','-b',sys.argv[3]],repositories[sys.argv[2]])
	elif sys.argv[1] == 'pull':
		runcmd(['git','pull','origin',sys.argv[3]],repositories[sys.argv[2]])
	elif sys.argv[1] == 'push':
		runcmd(['git','push','origin',sys.argv[3]],repositories[sys.argv[2]])
	elif sys.argv[1] == 'branches':
		runcmd(['git','branch'],repositories[sys.argv[2]])
	elif sys.argv[1] == 'install':
		currcommands = load('../commands.data')
		currcommands['git init $rep $location'] = 'run python data/libraries/gitLib.py init $rep $location'
		currcommands['git add $rep $location'] = 'run python data/libraries/gitLib.py add rep $rep $location'
		currcommands['git $rep add $file'] = 'run python data/libraries/gitLib.py add file $rep $file'
		currcommands['git delete $rep'] = 'run python data/libraries/gitLib.py delete rep $rep'
		currcommands['git $rep delete $file'] = 'run python data/libraries/gitLib.py delete file $rep $file'
		currcommands['git $rep status'] = 'run python data/libraries/gitLib.py status $rep'
		currcommands['git $rep commit $message'] = 'run python data/libraries/gitLib.py commit $rep $message'
		currcommands['git show'] = 'run python data/libraries/gitLib.py show repositories'
		currcommands['git show $rep'] = 'run python data/libraries/gitLib.py show $rep'
		currcommands['git $rep add $origin'] = 'run python data/libraries/gitLib.py origin $rep $origin'
		currcommands['git $rep checkout $branch'] = 'run python data/libraries/gitLib.py checkout $rep $branch'
		currcommands['git $rep new $branch'] = 'run python data/libraries/gitLib.py new $rep $branch'
		currcommands['git $rep pull $branch'] = 'run python data/libraries/gitLib.py pull $rep $branch'
		currcommands['git $rep push $branch'] = 'run python data/libraries/gitLib.py push $rep $branch'
		currcommands['git $rep branch'] = 'run python data/libraries/gitLib.py branches $rep'
		save('../commands.data',currcommands)
save('data/gitLib.data',repositories)
