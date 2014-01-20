'''
Created on 17.01.2014

@author: mhoyer
'''
import unittest
from statusfile_writer.statusfile import StatusFile
from mock import patch, Mock, call, mock_open
import logging

class StatusFileTest(unittest.TestCase):

    MSG = 'msg'
    ERROR_CODE = 42
    

    def setUp(self):
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        self.patcher = patch('statusfile_writer.statusfile.open',
                             mock_open(read_data='STATUSFILE_PATH=/any'),
                             create=True)
        self.mock_open_ = self.patcher.start()
        self.statusfile = StatusFile("/tmp/statusfile.status")

    def tearDown(self):
        self.patcher.stop()

    def test_generate_status_json(self):
        expected = '{\n  "status": %s, \n  "message": "%s"\n}' % \
                (self.ERROR_CODE, self.MSG)
        received = self.statusfile._generate_status_json(self.ERROR_CODE, self.MSG)
        self.assertEqual(expected, received)
         
    def test__write_puts_json_to_file(self):
        with patch('statusfile_writer.statusfile.StatusFile._generate_status_json') as mock_generate_status_json:
            with patch('statusfile_writer.statusfile.StatusFile._write_to_status_file') as mock_write_json:
                mock_generate_status_json.return_value = 'json'
                self.statusfile.write(0, self.MSG)
                mock_write_json.assert_called_once_with('json')
  
    def test__write_json_to_file_opens_correct_file(self):
        with patch('statusfile_writer.statusfile.open', mock_open(), create=True) as mock_open_:
            self.statusfile._write_to_status_file('json')
            mock_open_.assert_called_once_with(self.statusfile.status_file, 'w')
 
    def test_json_will_be_written_to_file(self):
        with patch('statusfile_writer.statusfile.open', mock_open(), create=True) as mock_open_:
            self.statusfile._write_to_status_file('json')
            mock_open_.return_value.write.assert_called_once_with('json')
             
    def test_exit_code_on_invalid_status_code(self):
        self.assertRaises(SystemExit, lambda: self.statusfile.write(5, "Test"))
 
    def test_validate_status_code(self):
        self.assertFalse(self.statusfile._status_code_is_valid(-1))
        self.assertTrue(self.statusfile._status_code_is_valid(0))
        self.assertTrue(self.statusfile._status_code_is_valid(1))
        self.assertTrue(self.statusfile._status_code_is_valid(2))
        self.assertTrue(self.statusfile._status_code_is_valid(3))
        self.assertFalse(self.statusfile._status_code_is_valid(4))
         
    def test_create_statusfile_path(self):
        test_values = [
            ('','testfile.status','testfile.status'),
            (None,'testfile.status','testfile.status'),
            ('/var/www/status','testfile.status','/var/www/status/testfile.status'),
            ('/var/www/status/','testfile.status','/var/www/status/testfile.status'),
            ('/var/www/status/','/tmp/testfile.status','/tmp/testfile.status')
        ]
        for directory, filename, expected_path in test_values:
            path = self.statusfile._create_statusfile_path(directory, filename)
            self.assertEqual(path, expected_path, "%s, created from '%s' and '%s' is not equal to %s" % (path, directory, filename, expected_path))
        
    def test__read_statusfile_directory_from_sysconfig_opens_file(self):
        with patch('statusfile_writer.statusfile.open', mock_open(), create=True) as mock_open_:
            self.statusfile._read_statusfile_directory_from_sysconfig()
            mock_open_.assert_called_once_with(self.statusfile.STATUSFILE_DIRECTORY_SYSCONFIG, 'r')
            
    def test__read_statusfile_directory_from_sysconfig(self):
        self.mock_open_.return_value.readlines.return_value = ['STATUSFILE_PATH=/any',]
        actual_path = self.statusfile._read_statusfile_directory_from_sysconfig()
        self.assertEqual('/any',  actual_path)
        
    def test__read_statusfile_directory_should_return_empty_value_if_there_is_invalid_config(self):
        self.mock_open_.return_value.readlines.return_value = ['STATUSFILE_PATH',]
        actual_path = self.statusfile._read_statusfile_directory_from_sysconfig()
        self.assertEqual('',  actual_path)
        
    def test__read_statusfile_directory_should_return_empty_value_if_there_is_no_value(self):
        self.mock_open_.return_value.readlines.return_value = ['STATUSFILE_PATH=',]
        actual_path = self.statusfile._read_statusfile_directory_from_sysconfig()
        self.assertEqual('',  actual_path)

    def test__read_statusfile_directory_should_return_empty_value_if_there_is_no_key(self):
        self.mock_open_.return_value.readlines.return_value = ['KEY=VALUE',]
        actual_path = self.statusfile._read_statusfile_directory_from_sysconfig()
        self.assertEqual('',  actual_path)
        
    def test__read_statusfile_directory_should_return_empty_value_if_ioerror_occurs(self):
        self.mock_open_.side_effect = IOError("unittest exception")
        actual_path = self.statusfile._read_statusfile_directory_from_sysconfig()
        self.assertEqual('',  actual_path)
        
if __name__ == "__main__":
    unittest.main()