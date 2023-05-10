# CO3069_Assignment


## Requirements
```
pip install -r requirements.txt
```

## Hashing static files
This program is used to generate hashes for all files in a directory to detect any changes made to them, thus detecting a deface attack where static files are changed.

### Usage
```
python defacecheck.py update
```
generates hashes and store them somewhere (based on the configured driver).

```
python defacecheck.py run
```
runs the program indefinitely, every once in a while recalculates the hashes and verifies with the previous hashes that nothing has been changed. If something has been added, removed or modified, an alert email is sent to the configured recipient and the program terminates, at which point it is up to the user to take actions (restoring their files to their backup states, updating the hashes, restarting the program,...).

## Direct response text comparison
HTTP response initially contains raw text that is rendered into actual UI by the browser. Prior to that, we have the raw response text that we can use to perform checks on, similar to the checksums above. If a text is similar enough to the known, trusted state of the website, an alert is not raised.

### Usage
```
python responsecheck.py update
```
get response and store them somewhere (based on the configured driver).

```
python responsecheck.py run
```
runs the program indefinitely, every once in a while requests the webpage and gets the raw text, then verifies with the previous response that nothing has been changed. If similarity is lower than the threshold, an alert email is sent to the configured recipient and the program terminates.

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
