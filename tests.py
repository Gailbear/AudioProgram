import subprocess
import unittest
import threading
import os
from nose.tools import *

cwd = os.getcwd()
prog = cwd + "/p4500"
me0 = cwd + '/TestFiles/music1_encrypted.wav'
me1 = cwd + '/TestFiles/music1_encrypted_0.wav'
me2 = cwd + '/TestFiles/music1_encrypted_1.wav'
me3 = cwd + '/TestFiles/music1_encrypted_2.wav'

mo0 = cwd + '/TestFiles/music1_original.wav'
mo1 = cwd + '/TestFiles/music1_original_0.wav'
mo2 = cwd + '/TestFiles/music1_original_1.wav'
mo3 = cwd + '/TestFiles/music1_original_2.wav'

limit = 2.5

MATCH = "MATCH\n"
NO_MATCH = "NO MATCH\n"

class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
        self.stdout = open("/tmp/p4500out","w")

    def run(self, timeout):
        def target():
            self.process = subprocess.Popen(self.cmd, stdout=self.stdout)
            self.process.communicate()

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            self.process.terminate()
            thread.join()
            self.stdout.close()
            return "TERMINATED\n"
        self.stdout.close()
        self.stdout = open("/tmp/p4500out", "r")
        string = self.stdout.readline()
        self.stdout.close()
        return string



def Result(f1,f2):
    cmd = [prog,"-f",f1,"-f",f2]
    c = Command(cmd)
    output = c.run(limit)
    return output

# Here's our "unit tests".
class ResultTests(unittest.TestCase):
    # Original vs Encrypted 
    def test1(self):
        self.assertEqual(MATCH,Result(mo0,me0))
    def test2(self):
        self.assertEqual(MATCH,Result(mo0,mo0))
    def test3(self):
        self.assertEqual(MATCH,Result(me0,me0))

    def test4(self):
        self.assertEqual(MATCH,Result(mo0,mo1))
    def test5(self):
        self.assertEqual(MATCH,Result(mo0,mo2))
    def test6(self):
        self.assertEqual(MATCH,Result(mo0,mo3))

    # Original vs Extracts
    def test7(self):
        self.assertEqual(MATCH,Result(mo0,me1))
    def test8(self):
        self.assertEqual(MATCH,Result(mo0,me2))
    def test9(self):
        self.assertEqual(MATCH,Result(mo0,me3))

    # Original_0 vs Original Extracts
    def test10(self):
        self.assertEqual(MATCH,Result(mo1,mo1))
    def test11(self):
        self.assertEqual(NO_MATCH,Result(mo1,mo2))
    def test12(self):
        self.assertEqual(NO_MATCH,Result(mo1,mo3))


    # Original vs Encrypted Extracts
    def test13(self):
        self.assertEqual(MATCH,Result(mo0,me1))
    def test14(self):
        self.assertEqual(MATCH,Result(mo0,me2))
    def test15(self):
        self.assertEqual(MATCH,Result(mo0,me3))

    # Original Extracts vs Encrypted Extracts
    def test16(self):
        self.assertEqual(MATCH,Result(mo0,me1))
    def test17(self):
        self.assertEqual(NO_MATCH,Result(mo0,me2))
    def test18(self):
        self.assertEqual(NO_MATCH,Result(mo0,me3))
    def test19(self):
        self.assertEqual(MATCH,Result(mo2,me2))
    def test20(self):
        self.assertEqual(MATCH,Result(mo3,me3))
    def test21(self):
        self.assertEqual(NO_MATCH,Result(mo3,me2))


    # Encrypted vs Original Extracts
    def test22(self):
        self.assertEqual(MATCH,Result(me0,mo1))
    def test23(self):
        self.assertEqual(MATCH,Result(me0,mo2))
    def test24(self):
        self.assertEqual(MATCH,Result(me0,mo3))


def main():
    unittest.main()

if __name__ == '__main__':
    main()
