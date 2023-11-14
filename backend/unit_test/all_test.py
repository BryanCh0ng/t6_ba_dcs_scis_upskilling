import unittest
from test_all_classes import *
from test_course import *

# Add tests from all test.py files here
test_suite = unittest.TestSuite()
test_suite.addTest(unittest.defaultTestLoader.discover(start_dir='', pattern='test_all_classes.py'))
test_suite.addTest(unittest.defaultTestLoader.discover(start_dir='', pattern='test_course.py'))

# Run the test suite
unittest.TextTestRunner().run(test_suite)
