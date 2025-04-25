#!/usr/bin/env python3
import unittest
import sys
import os

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the test modules
from tests.test_element_properties_dock import TestElementPropertiesDock

def run_tests():
    """Run all tests in the test suite."""
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add the test classes
    test_suite.addTest(unittest.makeSuite(TestElementPropertiesDock))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Return 0 if all tests passed, 1 if any failed
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests()) 