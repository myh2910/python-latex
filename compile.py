import os
from glob import glob
from colorama import Fore
from timeit import default_timer as timer

pacman = [
	{
		'name': 'array',
		'cmd': '\\begin{tabular}',
		'parent': None,
		'code': '\\usepackage{array}\n'
	},
	{
		'name': 'mhchem',
		'cmd': '\\ce{',
		'parent': None,
		'code': '\\usepackage{mhchem}\n'
	},
	{
		'name': 'multirow',
		'cmd': '\\multirow{',
		'parent': None,
		'code': '\\usepackage{multirow}\n'
	},
	{
		'name': 'xcolor',
		'cmd': '\\color{',
		'parent': None,
		'code': '\\usepackage{xcolor}\n'
	},
	{
		'name': 'tkz-euclide',
		'cmd': '\\tkz',
		'parent': None,
		'code': '\\usepackage{tkz-euclide}\n'
	},
	{
		'name': 'tikz',
		'cmd': '\\begin{tikzpicture}',
		'parent': None,
		'code': '\\usepackage{tikz}\n'
	},
	{
		'name': 'tikz.matrix',
		'cmd': '\\matrix',
		'parent': 'tikz',
		'code': '\\usetikzlibrary{matrix}\n'
	},
	{
		'name': 'mini',
		'cmd': '\\begin{mini}',
		'parent': None,
		'code': '\\newenvironment{mini}[1][.6]{\\begin{minipage}{#1\\linewidth}}{\\end{minipage}}\n'
	},
	{
		'name': 'tasks',
		'cmd': '\\begin{tasks}',
		'parent': None,
		'code': '\\usepackage{tasks}\n'
	},
	{
		'name': 'enum',
		'cmd': '\\begin{enum}',
		'parent': 'tasks',
		'code': '\\NewTasksEnvironment[label=\\Alph*)]{enum}[*]\n'
	},
	{
		'name': 'enum*',
		'cmd': '\\begin{enum*}',
		'parent': 'tasks',
		'code': '\\NewTasksEnvironment[label=\\Alph*)]{enum*}[*](4)\n'
	},
	{
		'name': 'task',
		'cmd': '\\begin{task}',
		'parent': 'enum*',
		'code': '\\newenvironment{task}{\\begin{minipage}{.6\\linewidth}\\begin{enum*}}{\\end{enum*}\\end{minipage}}\n'
	},
	{
		'name': 'dang',
		'cmd': '\\dang',
		'parent': None,
		'code': '\\newcommand{\\dang}{\\measuredangle}\n'
	},
	{
		'name': 'dg',
		'cmd': '\\dg',
		'parent': None,
		'code': '\\newcommand{\\dg}{^\\circ}\n'
	},
	{
		'name': 'ii',
		'cmd': '\\ii',
		'parent': None,
		'code': '\\newcommand{\\ii}{\\item}\n'
	},
	{
		'name': 'ol',
		'cmd': '\\ol',
		'parent': None,
		'code': '\\newcommand{\\ol}{\\overline}\n'
	},
	{
		'name': 'GA',
		'cmd': '\\GA',
		'parent': None,
		'code': '\\DeclareMathOperator{\\GA}{GA}\n'
	},
	{
		'name': 'GR',
		'cmd': '\\GR',
		'parent': None,
		'code': '\\DeclareMathOperator{\\GR}{GR}\n'
	}
]
for pkg in pacman:
	pkg['stat'] = False

def convert(level):
	pkgs = list(reversed(pacman))
	parents = []
	total = 0
	with open(level, 'r') as o:
		original = o.readlines()
		for i, line in enumerate(original):
			for pkg in pkgs:
				if pkg['name'] in parents or pkg['cmd'] in line:
					parent = pkg['parent']
					if parent:
						parents.append(parent)
					pkg['stat'] = True
			if '%%' in line and i > 0 or i > len(original) - 2:
				with open(tex_file, 'r+') as t:
					contents = t.readlines()
					if i > len(original) - 2:
						contents.append(line)
					if i > 0:
						contents.append('\\end{document}')
					for pkg in pkgs:
						if pkg['stat']:
							contents.insert(2, pkg['code'])
						pkg['stat'] = False
					t.seek(0)
					t.writelines(contents)
				print(f'{Fore.LIGHTMAGENTA_EX}Compiling file {Fore.LIGHTCYAN_EX}{tex_file}{Fore.LIGHTMAGENTA_EX}...{Fore.RESET}')
				os.system(f'latexmk -quiet -cd- -outdir={dirs[0]} {tex_file}')
				parents = []
				total += 1
			if '%%' in line:
				dirs = [f'{x}/{os.path.basename(level)[:-4]}/' for x in ['tex', 'png']]
				for d in dirs:
					if not os.path.exists(d):
						os.makedirs(d)
				types = line.strip().split('.')
				file_type = types[0][2:]
				tex_file = f'{dirs[0]}{file_type}.tex'
				with open(tex_file, 'w') as t:
					t.write(r'''\documentclass[margin=1pt,preview]{standalone}
\usepackage{amsmath,amssymb,cmbright}
''')
					if 'sp' in types:
						t.write('\\usepackage[spanish]{babel}\n')
					if file_type[0] == 'r':
						t.write(r'''\usepackage{xcolor}
\begin{document}
\color{red}
''')
					else:
						t.write('\\begin{document}\n')
			elif i < len(original) - 1:
				with open(tex_file, 'a') as t:
					t.write(line)
	return total

def compile(*levels):
	start = timer()
	if len(levels) == 0:
		levels = glob('levels/*.tex')
	else:
		levels = [f'levels/{x}.tex' for x in levels]
	total = 0
	for level in levels:
		if os.path.exists(level):
			print(f'{Fore.LIGHTGREEN_EX}File {Fore.LIGHTCYAN_EX}{level} {Fore.LIGHTGREEN_EX}found. Processing images...')
			total += convert(level)
		else:
			print(f'{Fore.LIGHTRED_EX}Error! The file {Fore.LIGHTYELLOW_EX}{level} {Fore.LIGHTRED_EX}does not exist.')
	end = timer()
	print(f'{Fore.LIGHTYELLOW_EX}Compiled files: {Fore.LIGHTCYAN_EX}{total} {Fore.LIGHTYELLOW_EX}documents.')
	print(f'Elapsed time: {Fore.LIGHTCYAN_EX}{end - start} {Fore.LIGHTYELLOW_EX}seconds.')

if __name__ == '__main__':
	compile()
