"""
this script is a unittest script to the "timer.py" script 
by Daniel Rindin
"""

from timer import TimerError, Timer
import unittest, time

t = Timer()

class TestTimerMethods(unittest.TestCase):

    def test_running(self):
        t.start()
        self.assertTrue(t.running())
        t.stop()

    def test_not_running(self):
        t.start()
        t.stop()
        self.assertFalse(t.running())

    def test_start_exception(self):
        isOk = False
        t.start()
        try:
            t.start()
        except TimerError:
            isOk = True

        self.assertTrue(isOk)
        t.stop()

    def test_start(self):
        t.start()
        self.assertTrue(t.running())
        t.stop()

    def test_stop_exception(self):
        isOk = False
        t.start()
        t.stop()
        try:
            t.stop()
        except TimerError:
            isOk = True

        self.assertTrue(isOk)

    def test_stop(self):
        t.start()
        t.stop()
        self.assertFalse(t.running())
    
    def test_elapsed_time(self):
        t.start()
        time.sleep(1)
        elapsedTime = int(t.elapsed_time())
        self.assertEqual(elapsedTime,1)
        t.stop()
    
    def test_restart(self):
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