create_format_file = '''
VGM Tag Edit

Title:\x20
TitleJAP:\x20
Game:\x20
GameJAP:\x20
System:\x20
SystemJAP:\x20
Author:\x20
AuthorJAP:\x20
Release: YYYY-MM-DD or YYYY-MM or YYYY
Vgmby:\x20
Notes: This one is multiline! :D
Also, from here, use tabs (\\t)
Example:\tA-E-S-T-H-E-T-I-C
Keys of 5 or less characters: two tabs
Keys of 6 or more characters: one tab
'''

import re

filename = input('VGM File: ')
try:
    with open(filename) as test: pass
except FileNotFoundError:
    with open(filename + '.vgm') as test: filename += '.vgm'

txt = input('Txt File: ')
FromFile = False
meta = {
    'EOF': 4, # End Of File
    'Offset': 20,
    'Length': 0,
    'Title':     '',
    'TitleJAP':  '',
    'Game':      '',
    'GameJAP':   '',
    'System':    '',
    'SystemJAP': '',
    'Author':    '',
    'AuthorJAP': '',
    'Release':   '',
    'Vgmby':     '',
    'Notes':     ''}
Num = ('','Title','Game','System','Author','Release','Vgmby','Notes','Close')

################################################################################

try:
    with open(txt) as test: FromFile = True
except FileNotFoundError:
    try:
        with open(txt + '.txt') as test:
            FromFile = True
            txt += '.txt'
    except FileNotFoundError: print('File not found... ok! You can edit it here.\n')

with open(filename,'rb') as vgm:
    vgm.seek(meta['Offset'])
    meta['Offset'] = int.from_bytes(vgm.read(4),'little') + 32

    vgm.seek(meta['Offset'] - 4)
    meta['Length'] = int.from_bytes(vgm.read(4),'little')

    vgm.seek(meta['EOF'])
    meta['EOF'] = int.from_bytes(vgm.read(4),'little') - meta['Length']

################################################################################

if FromFile:
    with open(txt,'r',-1,'utf-16le') as text:
        gd3 = text.read()

    n = gd3.upper().find('TITLE: ')
    if n != 1:
        temp = gd3[n:]
        meta['Title'] = temp[7:temp.find('\n')]
    else: meta['Title'] = ''

    n = gd3.upper().find('TITLEJAP: ')
    if n != 1:
        temp = gd3[n:]
        meta['TitleJAP'] = temp[10:temp.find('\n')]
    else: meta['TitleJAP'] = ''

    n = gd3.upper().find('GAME: ')
    if n != 1:
        temp = gd3[n:]
        meta['Game'] = temp[6:temp.find('\n')]
    else: meta['Game'] = ''

    n = gd3.upper().find('GAMEJAP: ')
    if n != 1:
        temp = gd3[n:]
        meta['GameJAP'] = temp[9:temp.find('\n')]
    else: meta['GameJAP'] = ''

    n = gd3.upper().find('SYSTEM: ')
    if n != 1:
        temp = gd3[n:]
        meta['System'] = temp[8:temp.find('\n')]
    else: meta['System'] = ''

    n = gd3.upper().find('SYSTEMJAP: ')
    if n != 1:
        temp = gd3[n:]
        meta['SystemJAP'] = temp[11:temp.find('\n')]
    else: meta['SystemJAP'] = ''

    n = gd3.upper().find('AUTHOR: ')
    if n != 1:
        temp = gd3[n:]
        meta['Author'] = temp[8:temp.find('\n')]
    else: meta['Author'] = ''

    n = gd3.upper().find('AUTHORJAP: ')
    if n != 1:
        temp = gd3[n:]
        meta['AuthorJAP'] = temp[11:temp.find('\n')]
    else: meta['AuthorJAP'] = ''

    n = gd3.upper().find('RELEASE: ')
    if n != 1:
        temp = gd3[n:]
        meta['Release'] = temp[9:temp.find('\n')]
    else: meta['Release'] = ''

    n = gd3.upper().find('VGMBY: ')
    if n != 1:
        temp = gd3[n:]
        meta['Vgmby'] = temp[7:temp.find('\n')]
    else: meta['Vgmby'] = ''

    n = gd3.upper().find('NOTES: ')
    if n != 1:
        temp = gd3[n:]
        meta['Notes'] = temp[7:]
    else: meta['Notes'] = ''

    print('')
    for key,val in meta.items(): print('{0}: {1}'.format(key,val))

else:
    with open(filename,'r',-1,'utf-16le') as vgm:
        vgm.seek(meta['Offset'])
        gd3 = vgm.read()

        meta['Title'] = gd3[:gd3.find('\0')]
        gd3 = gd3[gd3.find('\0')+1:]
        gd3 = gd3[gd3.find('\0')+1:] # Skip Japanese title
        meta['Game'] = gd3[:gd3.find('\0')]
        gd3 = gd3[gd3.find('\0')+1:]
        gd3 = gd3[gd3.find('\0')+1:] # Skip Japanese game
        meta['System'] = gd3[:gd3.find('\0')]
        gd3 = gd3[gd3.find('\0')+1:]
        gd3 = gd3[gd3.find('\0')+1:] # Skip Japanese system
        meta['Author'] = gd3[:gd3.find('\0')]
        gd3 = gd3[gd3.find('\0')+1:]
        gd3 = gd3[gd3.find('\0')+1:] # Skip Japanese author
        meta['Release'] = gd3[:gd3.find('\0')]
        gd3 = gd3[gd3.find('\0')+1:]
        meta['Vgmby'] = gd3[:gd3.find('\0')]
        gd3 = gd3[gd3.find('\0')+1:]
        meta['Notes'] = gd3[:gd3.find('\0')]

    n = -2
    for key,val in meta.items():
        if not 'JAP' in key:
            if n > 0: print('{2} {0}: {1}'.format(key,val,n))
            n = n + 1

    print('8 or 9 Close')
    print('\nJapanese only supported from txt file!!')
    print('Syntax: Key = Value\n')
    print('Example: tItLe = A Creative Name')
    print('Or using numbers as keys: 4 = Cyorter')
    print('Note: Key is case insensitive.')
    print('Type 0 to Close + create a template txt file.\n')

    while True:
        edit = input('>> ')
        if edit[0] == '0':
            with open('VGM Tag Edit.txt','a',-1,'utf-16le') as newfile:
                newfile.write(create_format_file)

        if edit[0:5].title() == 'Close' or \
            edit[0:4].title() == 'Quit' or \
            edit[0:4].title() == 'Exit' or \
            edit[0] == '8' or edit[0] == '9' or edit[0] == '0': break

        if not '=' in edit: continue

        key = edit.split('=',1)[0]
        key = re.sub('\s','',key).title()
        val = edit.split('=',1)[1]
        if val[0] == ' ': val = val[1:]

        try:
            key = Num[int(key)]
        except ValueError: pass

        if key == 'Name' or key == 'Track': key = 'Title'
        if key == 'Artist' or key == 'Composer': key = 'Author'
        if key == 'Console': key = 'System'
        if key == 'Date' or key == 'Year': key = 'Release'
        if key == 'Note': key = 'Notes'

        if key == 'Notes':
            val = val.replace('\\n','\n').replace(': ',':\t')
            temp = ''
            for n in val.split('\n'):
                if n.find(':\t') <= 6: n = n.replace('\t','\t\t')
                temp += n + '\n'
            val = temp

        valid = False
        for test in Num:
            if key == test: valid = True

        if not valid: continue

        meta[key] = val
        print('{0}: {1}\n'.format(key,val))

################################################################################

with open(filename,'rb') as file:
    vgm = file.read(meta['Offset'])

if FromFile:
    n = -2
    metadata = ''
    for k,v in meta.items():
        if n > 0: metadata += meta[k] + '\0'
        n += 1

else:
    meta['Title']   += '\0\0'
    meta['Game']    += '\0\0'
    meta['System']  += '\0\0'
    meta['Author']  += '\0\0'
    meta['Release'] += '\0'
    meta['Vgmby']   += '\0'
    meta['Notes']   += '\0'

    metadata = ''
    for m in Num:
        try: metadata += meta[m]
        except KeyError: pass

meta['Length'] = len(metadata + '\0\0') * 2
meta['EOF'] += meta['Length']

vgm = vgm[0: 4] + meta['EOF'   ].to_bytes(4,'little') + \
      vgm[8:-4] + meta['Length'].to_bytes(4,'little')

with open(filename[:-4] + ' NEWMETA.vgm','wb') as file:
    file.write(vgm)
with open(filename[:-4] + ' NEWMETA.vgm','a',-1,'utf-16le') as file:
    file.write(metadata)
