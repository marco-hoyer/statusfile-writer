statusfile-writer
=================

Simple python sniplet writing a status file parseable by check_remote_json and compatible with nagios/icinga plugin api

## Installation:

This is a bybuilder project. You will need to install pybuilder by:
pip install pybuilder

### Verify project (unittests and coverage)
```bash
pyb verify
```

### Install project dependencies
```bash
pyb install_dependencies
```

### Build project
```bash
pyb publish
```

## Usage:

### Shell

#### Help
```bash
python statusfile_tests.py --help
```

####  Write status file
```bash
python statusfile_tests.py /var/www/status/mycronjob-status.json 0 "Successfully resized 1000 files"
```

### As python module
```python
from statusfile_writer.statusfile import StatusFile

statusfile = StatusFile("/var/www/status/myapp-status.json")
statusfile.write(2,"Fatal error occured")
```

## Example output:
```json
{
  "status": 0,
  "timestamp": 1390501647
  "message": "Successfully resized 1000 files"
}
```

## Status Codes:

0 - OK<br>
1 - Warning<br>
2 - Critical<br>
3 - Unknown<br>

(see: http://www.nagios-plugins.org/doc/guidelines.html)
