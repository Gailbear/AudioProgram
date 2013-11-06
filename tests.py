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


def IsValidSyntax(c):
    output = os.system(c) == 0
    return output

def Result(f1,f2):
    cmd = [prog,"-f",f1,"-f",f2]
    c = Command(cmd)
    output = c.run(limit)
    return output

# Here's our "unit tests".
class ResultTests(unittest.TestCase):

    # Command Syntax Tests    
    # All true
    def test00(self):
        self.assertTrue(IsValidSyntax(prog+" -f "+mo0+" -f "+me0))
    def test01(self):
        self.assertTrue(IsValidSyntax(prog+" -f "+mo1+" -f "+me1))
    def test02(self):
        self.assertTrue(IsValidSyntax(prog+" -f "+mo2+" -f "+me2))
    def test03(self):
        self.assertTrue(IsValidSyntax(prog+" -f "+mo3+" -f "+me3))

    # All false
    def test04(self):
        self.assertFalse(IsValidSyntax(prog+" -f "+mo0))
    def test05(self):
        self.assertFalse(IsValidSyntax(prog+" -f "))
    def test06(self):
        self.assertFalse(IsValidSyntax("-f "+mo0+" -f "+me0))
    def test08(self):
        self.assertFalse(IsValidSyntax("-f "+" -f "+me0))
    def test09(self):
        self.assertFalse(IsValidSyntax("-f "+me0))
    def test010(self):
        self.assertFalse(IsValidSyntax("-f "+mo0+" -f "))
    def test011(self):
        self.assertFalse(IsValidSyntax(prog+" -f "+mo0+" -f "))
    def test012(self):
        self.assertFalse(IsValidSyntax(prog+" -f "+mo0+" -f "))
    def test013(self):
        self.assertFalse(IsValidSyntax(prog+" -a "+mo3+" -a "+me3))
    def test014(self):
        self.assertFalse(IsValidSyntax(prog+"-filename "+mo3+"-filename "+me3))
    def test015(self):
        self.assertFalse(IsValidSyntax(prog+" "+mo3+" "+me3))
    def test016(self):
        self.assertFalse(IsValidSyntax(prog+"f"+mo3+" -g "+me3))
    def test017(self):
        self.assertFalse(IsValidSyntax(" -f "+" -f "+mo3+" -f "+me3))
    def test018(self):
        self.assertFalse(IsValidSyntax("/p4500"+" -f "+mo3+" -f "+me3))


    # Original vs Encrypted 
    def test1(self):
        self.assertEqual(MATCH,Result(mo0,me0))
    def test2(self):
        self.assertEqual(MATCH,Result(mo0,mo0))
    def test3(self):
        self.assertEqual(MATCH,Result(me0,me0))

    # Original vs Orignal Extracts
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

    # Original_0 Extract vs Original Extracts
    def test10(self):
        self.assertEqual(MATCH,Result(mo1,mo1))
    def test11(self):
        self.assertEqual(NO_MATCH,Result(mo1,mo2))
    def test12(self):
        self.assertEqual(NO_MATCH,Result(mo1,mo3))

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
