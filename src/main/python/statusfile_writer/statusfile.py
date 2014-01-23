#!/usr/bin/env python
'''
Created on 16.01.2014

@author: mhoyer
'''

#!/usr/bin/env python
import argparse
import json
import logging
import os
import sys
import time


class StatusFile:
    
    STATUSFILE_DIRECTORY_SYSCONFIG = "/etc/sysconfig/statusfile-writer"
    KEY_STATUSFILE_PATH = 'STATUSFILE_PATH'

    def __init__(self, status_file):
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        self.logger = logging.getLogger("Statusfile-Writer")
        statusfile_dir = self._read_statusfile_directory_from_sysconfig()
        self.status_file = statusfile_dir + status_file
        
    def _create_statusfile_path(self, directory, filename):
        path = "" if not directory else directory
        path = path + os.sep if path and not path.endswith(os.sep) else path
        path = filename if filename.startswith(os.sep) else path + filename
        return path

    def _parse_line_from_status_file(self, line):
        statusfile_directory = ''
        if line and not line.startswith('#'):
            key, value = line.split('=')
            if key.strip() == self.KEY_STATUSFILE_PATH:
                statusfile_directory = value.strip()
        return statusfile_directory

    def _read_statusfile_directory_from_sysconfig(self):
        statusfile_directory = ''
        try:
            with open(self.STATUSFILE_DIRECTORY_SYSCONFIG, 'r') as f:
                for line in f.readlines():
                    statusfile_directory = self._parse_line_from_status_file(line)
        except (IOError, ValueError):
            pass

        return statusfile_directory

    def _generate_status_json(self, status_code, message, timestamp):
        status_dict = {'status': status_code, 'message': message, 'timestamp': timestamp}
        return json.dumps(status_dict, indent=2)

    def _write_to_status_file(self, json):
        try:
            with open(self.status_file, 'w') as fp:
                fp.write(json)
        except Exception as e:
            self.logger.error("Could not write status file: " + str(e))
            sys.exit(2)

    def write(self, status_code, message):
        if self._status_code_is_valid(status_code):
            status_json = self._generate_status_json(status_code, message, time.time())
            self._write_to_status_file(status_json)
        else:
            self.logger.error("Invalid status_code, use 0,1,2,3 as defined in icinga/nagios plugin api!")
            sys.exit(1)

    def _status_code_is_valid(self, status_code):
        if status_code in [0,1,2,3]:
            return True
        else:
            return False

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('statusfile', help="Path to write the status file to", type=str)
    parser.add_argument('statuscode', help="Nagios/Icinga plugin exit code", type=int)
    parser.add_argument('message', help="Message", type=str)
    return parser.parse_args()


def main():
    args = parse_arguments()
    # executed by shell
    statusfile = StatusFile(args.statusfile)
    statusfile.write(args.statuscode, args.message)


if __name__ == '__main__':
    main()
