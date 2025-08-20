# Build / Run (super simple)

This is a small fan project. You don’t need fancy tools.

## 1) Put files in one folder
Keep this layout:

AgeOfDuck/
├─ AgeofDuck.py
└─ tooltip.py
├─ civ_data.json
├─ units_db.json
├─ duck.png
├─ profile.png
├─ Units/ (images)
└─ CivIcons/ (images)
 requirements.txt


## 2) Install Python (once)
- Windows 10/11 64-bit: install **Python 3.11+** from https://www.python.org  
- During install, tick **“Add Python to PATH.”**

## 3) Quick start (from source)
Open **Command Prompt** in the project folder and run:

```bat
python -m pip install --upgrade pip
pip install -r requirements.txt
python src\AgeofDuck.py