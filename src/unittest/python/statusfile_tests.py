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
        self.statusfile = StatusFile("/tmp/statusfile.status")
        self.patcher = patch('statusfile_writer.statusfile.open',
                             mock_open(),
                             create=True)
        self.mock_open_ = self.patcher.start()

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
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()