import time
import datetime
from sys import argv, exit
import os
import signal
import re
path = os.path.dirname(os.path.realpath(__file__)) + "/Projects"
current_project = None

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


def signal_handler(sig, frame):
	print('\n\nExiting...')
	if current_project is not None:
		current_project.close()
	exit(0)
   
def print_history():
	global current_project
	current_project.seek(0)
	i = 0
	for line in reversed(current_project.readlines()):
		print_timestamp()
		print(re.sub('\[[^\]\[]+?\]', '', str(line)))
		i += 1
		if i > 10:
			break

def open_project(name):
	f = open(name, "a+")
	return f

def list_projects():
	return os.listdir(path)

def print_timestamp():
	print("[ "+ bcolors.BRIGHT_ORANGE + datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + bcolors.ENDC + " ]", end=" ")

def main():
	global current_project
	signal.signal(signal.SIGINT, signal_handler)
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
		input_ = input(bcolors.CYAN + current_project.name + "> " + bcolors.ENDC)
		if input_ == "/exit":
			current_project.close()
			break
		if input_ == "/chpro":
			current_project.close()
			str_ = " "
			to_open = input(bcolors.GREEN + "Choose project to open or create a new one -> [" + str_.join([str(elem) for elem in list_projects()]) + "]: " + bcolors.ENDC)
			current_project = open_project(to_open)
			continue
		current_project.write("[ "+ datetime.datetime.now().strftime("%d-%m-%Y %H:%M") + " ] " + input_ + "\n")
		print_history()

if __name__ == "__main__":
    main()
	