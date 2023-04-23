import glob
import os
import hashlib
import json
import time
import argparse
from datetime import datetime

from modules.io_driver import *
from modules.mailer import *
import config

BASE_PATH = config.dir_path
DIR_BLACKLIST = config.blacklist


def get_all_files_from_dir(dirpath, blacklisted_dirs):
    blacklisted_dirs = [os.path.join(dirpath, blacklisted)
                        for blacklisted in blacklisted_dirs]
    walker = os.walk(dirpath)
    res = []
    for root, dir_names, file_names in walker:
        if any([blacklisted_dir in root for blacklisted_dir in blacklisted_dirs]):
            continue
        res.extend([os.path.join(root, file_name) for file_name in file_names])
    return res


def get_sha256_sum(file_name):
    with open(file_name, "rb") as f:
        data = f.read()
        digest = hashlib.sha256(data).hexdigest()
        f.close()
    return digest


def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o: (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
    same = set(o for o in shared_keys if d1[o] == d2[o])
    return added, removed, modified, same


def has_changed(added, removed, modified):
    return added or removed or modified


def main():
    global BASE_PATH

    parser = argparse.ArgumentParser(
        description="Periodically calculates the checksums of content in a specified directory and alerts through email if there are changes")
    parser.add_argument(
        "command", help="The operation to carry out, update updates the current hashes, run performs periodic checks", choices=['update', 'run'], type=str)
    # parser.add_argument(
    # "path", help="The absolute path to the folder to scan", type=str)
    args = parser.parse_args()

    # BASE_PATH = args.path

    try:
        if args.command == 'run':
            run()
        elif args.command == 'update':
            update()
    except KeyboardInterrupt:
        pass


def run():
    print("Program is now scanning, press Ctrl+C to stop")
    while True:
        check()
        time.sleep(config.scan_interval * 60)


def check():
    global BASE_PATH, DIR_BLACKLIST

    file_names = get_all_files_from_dir(BASE_PATH, DIR_BLACKLIST)
    sha256_sums = {}
    for file_name in file_names:
        sha256_sums[file_name] = get_sha256_sum(file_name)
    json_dict = json.dumps(sha256_sums, indent='  ')
    f_io = FileDriver('output.json')

    json_dict = f_io.read_from()
    old_sha256s = json.loads(json_dict)

    added, removed, modified, same = dict_compare(sha256_sums, old_sha256s)
    v_has_changed = has_changed(added, removed, modified)
    if v_has_changed:
        print(f"[{datetime.now()}] Scan finished, changes detected")
        print("Added", added)
        print("Removed", removed)
        print("Modified", modified)
        # send_alert_email()
        exit()
    else:
        print(f"[{datetime.now()}] Scan finished, no changes found")


def update():
    global BASE_PATH, DIR_BLACKLIST

    file_names = get_all_files_from_dir(BASE_PATH, DIR_BLACKLIST)
    sha256_sums = {}
    for file_name in file_names:
        sha256_sums[file_name] = get_sha256_sum(file_name)
    json_dict = json.dumps(sha256_sums, indent='  ')
    f_io = FileDriver('output.json')
    f_io.write_to(json_dict)


if __name__ == '__main__':
    main()
