statusfile-writer
=================

Simple python sniplet writing a status file parseable by check_remote_json and compatible with nagios/icinga plugin api

## Installation:

### verify project (unittests and coverage)
pyb verify

### install project dependencies
pyb install_dependencies

### build project
pyb publish

## Usage:

### Help
python statusfile_tests.py --help

###  write status file
python statusfile_tests.py /var/www/status/mycronjob-status.json 0 "Successfully resized 1000 files"

### Status Codes

0 - OK
1 - Warning
2 - Critical
3 - Unknown

(see: http://www.nagios-plugins.org/doc/guidelines.html)