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

if not os.path.isdir('.notes'):
    os.makedirs('.notes')
notes = load('.notes/notes.list')
if 'noteId' not in notes:
    notes['noteId'] = '0'

if len(sys.argv)<2:
    print 'Notes program takes arguments in the form of add/show/delete <note>.'
elif sys.argv[1] == 'add':
    if len(sys.argv)<3:
        print 'A note must be at least one word long.'
    else:
        notes[notes['noteId']] = ' '.join(sys.argv[2:])
        notes['noteId'] = '{}'.format(int(notes['noteId'])+1)
        save('.notes/notes.list', notes)
elif sys.argv[1] == 'show':
    if len(sys.argv)<3:
        print notes
    else:
        if sys.argv[2] in notes:
            print '\n'.join(notes[sys.argv[2]].split(';'))
elif sys.argv[1] == 'delete':
    if len(sys.argv)<3:
        notes = {}
    else:
        if sys.argv[2] in notes:
            notes.pop(sys.argv[2],0)
        else:
            print 'Note doesn\'t exist.'
    save('.notes/notes.list',notes)
elif sys.argv[1] == 'install':
	currcommands = load('../commands.data')
	currcommands['add note $text'] = 'run python data/libraries/notesLib.py add $text'
	currcommands['show notes'] = 'run python data/libraries/notesLib.py show'
	currcommands['delete notes'] = 'run python data/libraries/notesLib.py delete'
	currcommands['show note $id'] = 'run python data/libraries/notesLib.py show $id'
	currcommands['delete note $id'] = 'run python data/libraries/notesLib.py delete $id'
	currcommands['add note {text}'] = 'run python data/libraries/notesLib.py add {text}'
	save('../commands.data',currcommands)
