GMAIL_SENDER_EMAIL = "qwertydefacecheck@gmail.com"
"""The sender's email, use this as the default if you don't want to set up a new one"""
GMAIL_SENDER_PASSWORD = "hreglqhofoqvjvnx"
"""The password of said email, use this as the default if you don't want to set up a new one"""

RECIPIENT_EMAIL = !MISSING
"""The user email we want to send alerts to"""

SCAN_INTERVAL = 1
"""The program performs a check every now and then, this specifies the interval between scans in MINUTES"""

BLACKLIST = [r".git"]
"""Directories to ignore"""
DIR_PATH = r"path/to/server/directory"
"""Path to the server directory"""

IO_DRIVER = "file"
"""The IO driver to use to store hashes. Accepted values: 'file', 'adafruit'"""

"""Adafruit IO is free to use, consider creating your own account and use your own credentials"""
ADAFRUIT_IO_USERNAME = !MISSING
"""The Adafruit username to use in AdafruitIODriver"""
ADAFRUIT_IO_KEY = !MISSING
"""The Adafruit key to use in AdafruitIODriver"""

BROWSER = 'firefox'
"""The selenium driver to use in response checking. Accepted values: 'firefox', 'chrome', 'edge'. This also relies on the browsers installed on the system"""

DIFF_THRESHOLD = 0.9
"""The minimum threshold value for direct response comparison before it is considered to have been changed"""
RESPONSECHECK_URL = !MISSING
"""The website to check using response comparison"""