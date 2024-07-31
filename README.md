Using Python 3.9.6

# Test task for the python position: File System Analyzer
### Objective
Develop a command-line tool that analyzes and reports on the file system structure and usage on a Linux system.

### Create virtual environment for python3 and activate
sudo apt install python3-venv

python3 -m venv <env_name>

source <env_name>/bin/activate

### Install dependencies:
pip install -r requirements.txt

### To launch the tool use the command:
python3 file_analyzer.py [-h] [-r] [-th THRESHOLD] directory_path

positional arguments:
directory_path

options:
  -h, --help            show this help message and exit
  -r, --recursive       It makes the tool to analyze files in the directory recursevely
  -th THRESHOLD, --threshold THRESHOLD
                        It makes the tool to print the list of files in the directory that have the size above the theshold (in bytes)


### To launch tests:
python3 tests.py
