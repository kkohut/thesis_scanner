"""
this script is a unittest script to the "timer.py" script 
by Daniel Rindin
"""
import os, sys, inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from thesis_scanner.timer import TimerError
from thesis_scanner.timer import Timer
import unittest, time

t = Timer()

class TestTimerMethods(unittest.TestCase):

    def test_running(self):
        if t.running():
            t.stop()
        t.start()
        self.assertTrue(t.running())
        t.stop()

    def test_not_running(self):
        if t.running():
            t.stop()
        t.start()
        t.stop()
        self.assertFalse(t.running())

    def test_start_exception(self):
        if t.running():
            t.stop()
        isOk = False
        t.start()
        try:
            t.start()
        except TimerError:
            isOk = True

        self.assertTrue(isOk)
        t.stop()

    def test_start(self):
        if t.running():
            t.stop()
        t.start()
        self.assertTrue(t.running())
        t.stop()

    def test_stop_exception(self):
        if t.running():
            t.stop()
        isOk = False
        t.start()
        t.stop()
        try:
            t.stop()
        except TimerError:
            isOk = True

        self.assertTrue(isOk)

    def test_stop(self):
        if t.running():
            t.stop()
        t.start()
        t.stop()
        self.assertFalse(t.running())
    
    def test_elapsed_time(self):
        if t.running():
            t.stop()
        t.start()
        time.sleep(1)
        #print(t.elapsed_time())
        elapsedTime = int(t.elapsed_time())
        #print(elapsedTime)
        self.assertEqual(elapsedTime,1)
        t.stop()
    
    def test_restart(self):
        if t.running():
            t.stop()
        isOk = False
        t.start()
        time.sleep(3)
        t.restart()
        if t.elapsed_time() < 3:
            isOk = True
        
        self.assertTrue(isOk)
        t.stop()

if __name__ == '__main__':
    unittest.main()