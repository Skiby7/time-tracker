import time
import datetime
from sys import argv, exit
import os
import signal
import re
import enquiries

path = os.path.dirname(os.path.realpath(__file__)) + "/Projects"
current_project = None
removing = False
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
	UNDERLINE = '\033[4m'
	CLEAR = '\033[2J\033[H'


def signal_handler(sig, frame):
	global removing
	if not removing:
		print('\n\nExiting...')
		if current_project is not None:
			current_project.close()
		exit(0)
   
def print_history():
	global current_project
	print()
	current_project.seek(0)
	for line in current_project.readlines():
		if 'TODO' not in line:
			print(line);
	input(bcolors.BOLD + 'Press enter to continue' + bcolors.ENDC)
	print(bcolors.CLEAR)
	
def print_todo():
	global current_project
	print()
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
	if "/todo" in line:
		line = re.sub('/todo', '', line)
		line = "[ "+ bcolors.GREEN + "TODO" + bcolors.ENDC + " ] " + line + "\n"
		project.write(line)

	else:
		line = "[ "+ bcolors.YELLOW + datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + bcolors.ENDC + " ] " + line + "\n"
		project.write(line)

def rm_todo():
	global current_project, removing, path
	pj_name = current_project.name
	removing = True
	current_project.seek(0)
	lines = current_project.readlines()
	todos = []
	for line in lines:
		if "TODO" in line:
			todos.append(line)
	if not todos:
		print(bcolors.GREEN + "Nothing to do! Take a nap!" + bcolors.ENDC)
		return
	choice = enquiries.choose('Select todo:', todos)
	for line in lines:
		if line == choice:
			lines.remove(line)
	current_project.close()
	current_project = open(path + "/" + pj_name, "w")
	for line in lines:
		current_project.write(line)
	current_project.close
	current_project = open_project(pj_name)
	removing = False
		


def main():
	global current_project, window
	
	signal.signal(signal.SIGINT, signal_handler)
	print(bcolors.CLEAR)
	try:
		os.chdir(path=path)
	except FileNotFoundError:
		os.mkdir(path=path)

	print(bcolors.MAGENTA + "Welcome to TimeTrack!" + bcolors.ENDC)
	projects = list_projects()
	if not projects:
		new_project = input(bcolors.RED + "No projects available, insert new one: " + bcolors.ENDC)
		current_project = open_project(new_project)
	else:
		str_ = " "
		to_open = input(bcolors.GREEN + "Choose project to open or create a new one -> [" + str_.join([str(elem) for elem in list_projects()]) + "]: " + bcolors.ENDC)
		current_project = open_project(to_open)
	while True:
		print_todo()
		input_ = input(bcolors.CYAN + current_project.name + "> " + bcolors.ENDC)
		print(bcolors.CLEAR, end='')
		if input_ == "/exit":
			current_project.close()
			break
		if input_ == "/chpro":
			current_project.close()
			str_ = " "
			to_open = input(bcolors.GREEN + "Choose project to open or create a new one -> [" + str_.join([str(elem) for elem in list_projects()]) + "]: " + bcolors.ENDC)
			current_project = open_project(to_open)
			continue
		if input_ == "/done":
			rm_todo()
			continue
		if input_ == "/hist":
			print_history()
			continue
		add_line(current_project, input_)
		

if __name__ == "__main__":
    main()
	