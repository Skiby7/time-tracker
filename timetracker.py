import time
import datetime
from sys import argv, exit
import sys
import os
import signal
import re
import enquiries
import pyfiglet
import readline
import atexit

class bcolors:
	MAGENTA = '\033[95m'
	BLUE = '\033[94m'
	CYAN = '\033[96m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BRIGHT_ORANGE = '\033[38:5:208:0m'
	DARK_ORANGE = '\033[38:5:166:0m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	ITALIC = '\033[3m'
	UNDERLINE = '\033[4m'
	CLEAR = '\033[2J\033[H'

path = os.path.dirname(os.path.realpath(__file__)) + "/Projects"
current_project = None
editing = False
quiet = False
if len(argv) > 1 and "-q" in argv:
	quiet = True
if len(argv) > 1 and ("-h" in argv or "--help" in argv):
	print(f"Use {bcolors.ITALIC}-q{bcolors.ENDC} option to disable the help message while the program is running")
	print(f"Use up/down keys to scroll through commands")
	help_msg = f""" {bcolors.CYAN}{bcolors.ITALIC}text{bcolors.ENDC} -> add annotation by simply writing the message and pressing enter
 {bcolors.CYAN}/todo{bcolors.ENDC} {bcolors.ITALIC}text{bcolors.ENDC} -> add todo
 {bcolors.CYAN}/done{bcolors.ENDC} -> mark todo as done
 {bcolors.CYAN}/dhist{bcolors.ENDC} -> print completed todos
 {bcolors.CYAN}/edit{bcolors.ENDC} -> edit todo
 {bcolors.CYAN}/chpro{bcolors.ENDC} -> change project
 {bcolors.CYAN}/delpro{bcolors.ENDC} -> delete project
 {bcolors.CYAN}/hist{bcolors.ENDC} -> print annotations
 {bcolors.CYAN}/exit{bcolors.ENDC}
	"""
	print(help_msg)
	exit(0)


def signal_handler(sig, frame):
	global editing
	if not editing:
		print('\n\nExiting...')
		if current_project is not None:
			current_project.close()
		exit(0)
   
def print_history():
	global current_project
	print()
	current_project.seek(0)
	for line in current_project.readlines():
		if 'TODO' not in line and 'DONE' not in line:
			print(line);
	input(bcolors.BOLD + 'Press enter to continue' + bcolors.ENDC)
	print(bcolors.CLEAR)

def print_done():
	global current_project
	print()
	current_project.seek(0)
	for line in current_project.readlines():
		if 'DONE' in line:
			print(line)
	input(bcolors.BOLD + 'Press enter to continue' + bcolors.ENDC)
	print(bcolors.CLEAR)
	
def print_todo():
	global current_project
	print(bcolors.MAGENTA)
	print(pyfiglet.figlet_format("TimeTrack") + bcolors.ENDC)
	help_msg = f""" {bcolors.CYAN}{bcolors.ITALIC}text{bcolors.ENDC} -> add annotation by simply writing the message and pressing enter
 {bcolors.CYAN}/todo{bcolors.ENDC} {bcolors.ITALIC}text{bcolors.ENDC} -> add todo
 {bcolors.CYAN}/done{bcolors.ENDC} -> mark todo as done
 {bcolors.CYAN}/dhist{bcolors.ENDC} -> print completed todos
 {bcolors.CYAN}/edit{bcolors.ENDC} -> edit todo
 {bcolors.CYAN}/chpro{bcolors.ENDC} -> change project
 {bcolors.CYAN}/delpro{bcolors.ENDC} -> delete project
 {bcolors.CYAN}/hist{bcolors.ENDC} -> print annotations
 {bcolors.CYAN}/exit{bcolors.ENDC}
	"""
	if not quiet:
		print(help_msg)
	current_project.seek(0)
	for line in current_project.readlines():
		if 'TODO'  in line:
			print(line);

def open_project(name):
	f = open(name, "a+")
	return f

def list_projects():
	return os.listdir(path)



def add_line(project, line):
	if "/todo" in line and line.strip() != "/todo":
		line = re.sub('/todo', '', line)
		line = "[ "+ bcolors.GREEN + "TODO" + bcolors.ENDC + " ] " + line + "\n"
		project.write(line)

	elif line != "":
		line = "[ "+ bcolors.YELLOW + datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + bcolors.ENDC + " ] " + line + "\n"
		project.write(line)

def rm_todo():
	global current_project, editing, path
	pj_name = current_project.name
	editing = True
	current_project.seek(0)
	lines = current_project.readlines()
	todos = []
	for line in lines:
		if "TODO" in line:
			todos.append(line)
	todos.append("Cancel")
	if len(todos) == 1:
		print(bcolors.GREEN + "Nothing to do! Take a nap!" + bcolors.ENDC)
		input("Press enter to continue")
		return
	choice = enquiries.choose('Select todo:', todos)
	if choice == "Cancel":
		editing = False
		return
	for line in lines:
		if line == choice:
			lines.remove(line)
			line = re.sub("\[[^\]]+?\]", '', line)
			lines.append('[ ' + bcolors.CYAN + 'DONE' + bcolors.ENDC + ' ]' + line)
	current_project.close()
	current_project = open(path + "/" + pj_name, "w")
	for line in lines:
		current_project.write(line)
	current_project.close()
	current_project = open_project(pj_name)
	editing = False

def edit_todo():
	global current_project, editing, path
	pj_name = current_project.name
	editing = True
	current_project.seek(0)
	lines = current_project.readlines()
	todos = []
	for line in lines:
		if "TODO" in line:
			todos.append(line)
	todos.append("Cancel")
	if len(todos) == 1:
		print(bcolors.GREEN + "Nothing to do! Take a nap!" + bcolors.ENDC)
		input("Press enter to continue")
		return
	choice = enquiries.choose('Select todo:', todos)
	if choice == "Cancel":
		editing = False
		return
	for line in lines:
		if line == choice:
			print(f"{line}\n{bcolors.GREEN}Edit todo ->{bcolors.ENDC}", end=" ")
			edited = input()
			lines[lines.index(line)] = "[ "+ bcolors.GREEN + "TODO" + bcolors.ENDC + " ] " + edited + "\n"
	current_project.close()
	current_project = open(path + "/" + pj_name, "w")
	for line in lines:
		current_project.write(line)
	current_project.close()
	current_project = open_project(pj_name)
	editing = False

def del_project():
	global current_project
	lines = list_projects()
	prjs = []
	for line in lines:
		prjs.append(line)
	prjs.append("Cancel")
	choice = enquiries.choose('Select project to delete:', prjs)
	if choice == "Cancel":
		choose_project()
		return
	else:
		print(f"{bcolors.RED}ARE YOU SURE TO DELETE {choice}? [y/n]{bcolors.ENDC}", end=" ")
		confirm = input()
		if confirm == "y":
			current_project.close()
			os.remove(path + "/" + choice)
			print(f"{bcolors.GREEN}Project deleted!{bcolors.ENDC}")

		else:
			print(f"{bcolors.YELLOW}Project not deleted!{bcolors.ENDC}")
	choose_project()

def choose_project():
	global current_project
	lines = list_projects()
	prjs = []
	for line in lines:
		prjs.append(line)
	prjs.append("Create new project")
	prjs.append("Exit")
	choice = enquiries.choose('Select project:', prjs)
	if choice == "Exit":
		exit(0)
	elif choice == "Create new project":
		choice = input(bcolors.GREEN + "Project name: " + bcolors.ENDC)
	current_project = open_project(choice)

def main():
	global current_project, window
	cmd_file = os.path.join(os.path.expanduser("~"), ".tracktime_cmd")
	with open(cmd_file, "w") as f:
		cmd = f"""/exit
/hist 
/delpro 
/chpro 
/edit 
/dhist 
/done 
/todo 
"""
		f.write(cmd)
	readline.read_history_file(cmd_file)
	signal.signal(signal.SIGINT, signal_handler)
	print(bcolors.CLEAR)
	try:
		os.chdir(path=path)
	except FileNotFoundError:
		os.mkdir(path=path)
	print(bcolors.MAGENTA + "Welcome to ")
	print(pyfiglet.figlet_format("TimeTrack") + bcolors.ENDC)
	projects = list_projects()
	if not projects:
		new_project = input(bcolors.RED + "No projects available, insert new one: " + bcolors.ENDC)
		current_project = open_project(new_project)
	else:
		choose_project()
	print(bcolors.CLEAR, end="")
	while True:
		print_todo()
		input_ = input(bcolors.CYAN + current_project.name + "> " + bcolors.ENDC)
		print(bcolors.CLEAR, end='')
		if input_ == "/exit":
			current_project.close()
			break
		if input_ == "/chpro":
			current_project.close()
			choose_project()
			continue
		if input_ == "/delpro":
			current_project.close()
			del_project()
			continue
		if input_ == "/done":
			rm_todo()
			continue
		if input_ == "/edit":
			edit_todo()
			continue
		if input_ == "/dhist":
			print_done()
			continue
		if input_ == "/hist":
			print_history()
			continue
		add_line(current_project, input_)
		

if __name__ == "__main__":
	main()
	
