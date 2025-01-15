# Monkeys Data Calculation

## Getting started
Download [Python](https://www.python.org/downloads/). I'm using version 3.10, but any version of Python 3 should be fine. Make sure to select the "Add to PATH" option in the installer.

Open the `monkeys-data-calculations` folder in a command line. One way to do this is to open the folder in Windows explorer, then `SHIFT + RIGHT CLICK` on an empty space. Then click "Open PowerShell window here".

Run the following commands to set up the environment:
```bash
python -m venv venv
venv/Scripts/activate.bat
pip install -r requirements.txt
```

Now run the script with your folder path as an argument:
```bash
python calculate_times.py data_folder/*
```
