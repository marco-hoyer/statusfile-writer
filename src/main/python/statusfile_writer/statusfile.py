#!/usr/bin/env python
'''
Created on 16.01.2014

@author: mhoyer
'''

#!/usr/bin/env python
import argparse
import json
import logging
import sys

class StatusFile:
    
    def __init__(self, status_file):
        self.logger = logging.getLogger(__name__)
        self.status_file = status_file

    def _generate_status_json(self, status_code, message):
        status_dict = {}
        status_dict['status'] = status_code
        status_dict['message'] = message
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
            status_json = self._generate_status_json(status_code, message)
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
    parser.add_argument('statuscode', help="Path to write the status file to", type=int)
    parser.add_argument('message', help="Message", type=str)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    # executed by shell
    statusfile = StatusFile(args.statusfile)
    statusfile.write(args.statuscode, args.message)