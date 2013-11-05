import subprocess
import unittest
import nose
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


def IsMatch(f1,f2):
    cmd = [prog,"-f",f1,"-f",f2]
    return subprocess.check_output(cmd) == "MATCH\n"

# Here's our "unit tests".
class IsMatchTests(unittest.TestCase):
    # Original vs Encrypted 
    def test1(self):
        self.assertTrue(IsMatch(mo0,me0))
    def test2(self):
        self.assertTrue(IsMatch(mo0,mo0))
    def test3(self):
        self.assertTrue(IsMatch(me0,me0))

    def test4(self):
        self.assertTrue(IsMatch(mo0,mo1))
    def test5(self):
        self.assertTrue(IsMatch(mo0,mo2))
    def test6(self):
        self.assertTrue(IsMatch(mo0,mo3))

    # Original vs Extracts
    def test7(self):
        self.assertTrue(IsMatch(mo0,me1))
    def test8(self):
        self.assertTrue(IsMatch(mo0,me2))
    def test9(self):
        self.assertTrue(IsMatch(mo0,me3))

    # Original_0 vs Original Extracts
    def test10(self):
        self.assertTrue(IsMatch(mo1,mo1))
    def test11(self):
        self.assertFalse(IsMatch(mo1,mo2))
    def test12(self):
        self.assertFalse(IsMatch(mo1,mo3))


    # Original vs Encrypted Extracts
    def test13(self):
        self.assertTrue(IsMatch(mo0,me1))
    def test14(self):
        self.assertTrue(IsMatch(mo0,me2))
    def test15(self):
        self.assertTrue(IsMatch(mo0,me3))

    # Original Extracts vs Encrypted Extracts
    def test16(self):
        self.assertTrue(IsMatch(mo0,me1))
    def test17(self):
        self.assertFalse(IsMatch(mo0,me2))
    def test18(self):
        self.assertFalse(IsMatch(mo0,me3))
    def test19(self):
        self.assertTrue(IsMatch(mo2,me2))
    def test20(self):
        self.assertTrue(IsMatch(mo3,me3))
    def test21(self):
        self.assertFalse(IsMatch(mo3,me2))


    # Encrypted vs Original Extracts
    def test22(self):
        self.assertTrue(IsMatch(me0,mo1))
    def test23(self):
        self.assertTrue(IsMatch(me0,mo2))
    def test24(self):
        self.assertTrue(IsMatch(me0,mo3))


def main():
    unittest.main()

if __name__ == '__main__':
    main()
