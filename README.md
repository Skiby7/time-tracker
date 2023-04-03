# Usage

Install the requirements by running: 
```bash
pip install -r requirements.txt
```
Then run the script:
```bash
python3 timetracker.py
```
The script will automatically create the `Projects` folder where the to-do lists will be saved.
The available commands are:

* `/chpro`: change the current project or create a new one
* `/todo` + *what to do*: insert a new task 
* `/done`: flag a task as completed
* `/dhist`: show the completed tasks history
* `/exit`

It is also possible to insert some text and then press enter to insert a new note/commit message to keep track of the work done. To print the notes history enter `/hist`. 