# CO3069_Assignment


## Requirements
```
pip install -r requirements.txt
```

## Hashing static files
This program is used to generate hashes for all files in a directory to detect any changes made to them, thus detecting a deface attack where static files are changed.

## Usage
```
python defacecheck.py update
```
generates hashes and store them somewhere (based on the configured driver).

```
python defacecheck.py run
```
runs the program indefinitely, every once in a while recalculates the hashes and verifies with the previous hashes that nothing has been changed. If something has been added, removed or modified, an alert email is sent to the configured recipient and the program terminates, at which point it is up to the user to take actions (restoring their files to their backup states, updating the hashes, restarting the program,...).

## Drivers
The hashes must be stored somewhere to be retrieved later. Currently there are 2 supported drivers, file and Adafruit IO.
- File:
Stores the hashes in a local text file. Simple but prone to modification by an attacker.
- Adafruit IO:
Stores the hashes in a feed using Adafruit IO service. Requires an Adafruit account (free to use).

## Configurations
All things that should be modified are defined in config.py. From the example_config.py template, make a copy named config.py and make changes to the values as you see fit.

## Notes
It is obvious that ```python defacecheck.py update``` must be executed before ```python defacecheck.py run``` based on commonsense or it will throw some errors that I can't be bothered to label.

Use python/python3 and pip/pip3 based on your OS.
