statusfile-writer
=================

Simple python sniplet writing a status file parseable by check_remote_json and compatible with nagios/icinga plugin api

## Installation:

This is a bybuilder project. You will need to install pybuilder by:
pip install pybuilder

### verify project (unittests and coverage)
```bash
pyb verify
```

### install project dependencies
```bash
pyb install_dependencies
```

### build project
```bash
pyb publish
```

## Usage:

### Help
```bash
python statusfile_tests.py --help
```

###  write status file
```bash
python statusfile_tests.py /var/www/status/mycronjob-status.json 0 "Successfully resized 1000 files"
```

### Status Codes

0 - OK
1 - Warning
2 - Critical
3 - Unknown

(see: http://www.nagios-plugins.org/doc/guidelines.html)