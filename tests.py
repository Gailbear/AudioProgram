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


m2o0 = cwd + '/TestFiles/music2_original.wav'
m2o1 = cwd + '/TestFiles/music2_original_0.wav'
m2o2 = cwd + '/TestFiles/music2_original_1.wav'

m2e0 = cwd + '/TestFiles/music2_encrypted.wav'
m2e1 = cwd + '/TestFiles/music2_encrypted_0.wav'
m2e2 = cwd + '/TestFiles/music2_encrypted_1.wav'


m3o0 = cwd + '/TestFiles/music3_original.wav'
m3o1 = cwd + '/TestFiles/music3_original_0.wav'
m3o2 = cwd + '/TestFiles/music3_original_1.wav'

m3e0 = cwd + '/TestFiles/music3_encrypted.wav'
m3e1 = cwd + '/TestFiles/music3_encrypted_0.wav'
m3e2 = cwd + '/TestFiles/music3_encrypted_1.wav'


m4o0 = cwd + '/TestFiles/music4_original.wav'
m4o1 = cwd + '/TestFiles/music4_original_0.wav'
m4o2 = cwd + '/TestFiles/music4_original_1.wav'

m4e0 = cwd + '/TestFiles/music4_encrypted.wav'
m4e1 = cwd + '/TestFiles/music4_encrypted_0.wav'
m4e2 = cwd + '/TestFiles/music4_encrypted_1.wav'

dir1 = cwd + '/TestFiles/'


limit = 10

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
    if "NO MATCH" in output:
        return NO_MATCH
    elif "MATCH" in output:
        return MATCH
    else:
        return NO_MATCH

def ResultDir(d1,d2):
    cmd [prog,"-d",d1,"-d",d2]
    c = Command(cmd)
    output = c.run(limit)
    if "NO MATCH" in output:
        return NO_MATCH
    elif "MATCH" in output:
        return MATCH
    else:
        return NO_MATCH


# Here's our "unit tests".
class ResultTests(unittest.TestCase):

    # Command Syntax Tests    
    # All true
    def test000(self):
        self.assertTrue(IsValidSyntax(prog+" -f "+mo0+" -f "+me0))
    def test001(self):
        self.assertTrue(IsValidSyntax(prog+" -f "+mo1+" -f "+me1))
    def test002(self):
        self.assertTrue(IsValidSyntax(prog+" -f "+mo2+" -f "+me2))
    def test003(self):
        self.assertTrue(IsValidSyntax(prog+" -f "+mo3+" -f "+me3))
    def test0031(self):
        self.assertTrue(IsValidSyntax(prog+" -d "+dir1+" -d "+dir1))
    def test0032(self):
        self.assertTrue(IsValidSyntax(prog+" -f "+mo1+" -d "+dir1))
    def test0032(self):
        self.assertTrue(IsValidSyntax(prog+" -d "+dir1+" -f "+mo1))

    # All false
    def test004(self):
        self.assertFalse(IsValidSyntax(prog+" -f "+mo0))
    def test005(self):
        self.assertFalse(IsValidSyntax(prog+" -f "))
    def test006(self):
        self.assertFalse(IsValidSyntax("-f "+mo0+" -f "+me0))
    def test008(self):
        self.assertFalse(IsValidSyntax("-f "+" -f "+me0))
    def test009(self):
        self.assertFalse(IsValidSyntax("-f "+me0))
    def test0010(self):
        self.assertFalse(IsValidSyntax("-f "+mo0+" -f "))
    def test0011(self):
        self.assertFalse(IsValidSyntax(prog+" -f "+mo0+" -f "))
    def test0012(self):
        self.assertFalse(IsValidSyntax(prog+" -f "+mo0+" -f "))
    def test0013(self):
        self.assertFalse(IsValidSyntax(prog+" -a "+mo3+" -a "+me3))
    def test0014(self):
        self.assertFalse(IsValidSyntax(prog+"-filename "+mo3+"-filename "+me3))
    def test0015(self):
        self.assertFalse(IsValidSyntax(prog+" "+mo3+" "+me3))
    def test0016(self):
        self.assertFalse(IsValidSyntax(prog+"f"+mo3+" -g "+me3))
    def test0017(self):
        self.assertFalse(IsValidSyntax(" -f "+" -f "+mo3+" -f "+me3))
    def test0018(self):
        self.assertFalse(IsValidSyntax("/p4500"+" -f "+mo3+" -f "+me3))




    # Original vs Encrypted 
    def test01(self):
        self.assertEqual(MATCH,Result(mo0,me0))
    def test02(self):
        self.assertEqual(MATCH,Result(mo0,mo0))
    def test03(self):
        self.assertEqual(MATCH,Result(me0,me0))

    # Original vs Orignal Extracts
    def test04(self):
        self.assertEqual(MATCH,Result(mo0,mo1))
    def test05(self):
        self.assertEqual(MATCH,Result(mo0,mo2))
    def test06(self):
        self.assertEqual(MATCH,Result(mo0,mo3))

    # Original vs Extracts
    def test07(self):
        self.assertEqual(MATCH,Result(mo0,me1))
    def test08(self):
        self.assertEqual(MATCH,Result(mo0,me2))
    def test09(self):
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

    # test music2
    #files full vs encrypted full
    def test25(self):
        self.assertEqual(MATCH,Result(m2o0,m2e0))
		
    # test music2 original full vs original segments
    def test26(self):
        self.assertEqual(MATCH,Result(m2o0,m2o1))
    def test27(self):
        self.assertEqual(MATCH,Result(m2o0,m2o2))
		
    # test music2 encrypted full vs encrypted segments
    def test28(self):
        self.assertEqual(MATCH,Result(m2e0,m2e1))
    def test29(self):
        self.assertEqual(MATCH,Result(m2e0,m2e2))
		
    # test music2 original segments vs encrypted segments
    def test30(self):
        self.assertEqual(MATCH,Result(m2o1,m2e1))
    def test31(self):
        self.assertEqual(MATCH,Result(m2o2,m2e2))
    def test32(self):
        self.assertEqual(NO_MATCH,Result(m2o1,m2e2))
    def test33(self):
        self.assertEqual(NO_MATCH,Result(m2o2,m2e1))		
		
    # test music2 original full vs encrypted segments
    def test34(self):
        self.assertEqual(MATCH,Result(m2o0,m2e1))
    def test35(self):
        self.assertEqual(MATCH,Result(m2o0,m2e2))
		
    # test music2 encrypted full vs original segments
    def test36(self):
        self.assertEqual(MATCH,Result(m2e0,m2o1))
    def test37(self):
        self.assertEqual(MATCH,Result(m2e0,m2o2))
		
	
    # test music3
    #files full vs encrypted full
    def test38(self):
        self.assertEqual(MATCH,Result(m3o0,m3e0))
		
    # test music3 original full vs original segments
    def test39(self):
        self.assertEqual(MATCH,Result(m3o0,m3o1))
    def test40(self):
        self.assertEqual(MATCH,Result(m3o0,m3o2))
		
    # test music3 encrypted full vs encrypted segments
    def test41(self):
        self.assertEqual(MATCH,Result(m3e0,m3e1))
    def test42(self):
        self.assertEqual(MATCH,Result(m3e0,m3e2))
		
    # test music3 original segments vs encrypted segments
    def test43(self):
        self.assertEqual(MATCH,Result(m3o1,m3e1))
    def test44(self):
        self.assertEqual(MATCH,Result(m3o2,m3e2))
    def test45(self):
        self.assertEqual(NO_MATCH,Result(m3o1,m3e2))
    def test46(self):
        self.assertEqual(NO_MATCH,Result(m3o2,m3e1))		
		
    # test music3 original full vs encrypted segments
    def test47(self):
        self.assertEqual(MATCH,Result(m3o0,m3e1))
    def test48(self):
        self.assertEqual(MATCH,Result(m3o0,m3e2))
		
    # test music3 encrypted full vs original segments
    def test49(self):
        self.assertEqual(MATCH,Result(m3e0,m3o1))
    def test50(self):
        self.assertEqual(MATCH,Result(m3e0,m3o2))
		
		
	
    # test music4
    #files full vs encrypted full
    def test51(self):
        self.assertEqual(MATCH,Result(m4o0,m4e0))
		
    # test music4 original full vs original segments
    def test52(self):
        self.assertEqual(MATCH,Result(m4o0,m4o1))
    def test53(self):
        self.assertEqual(MATCH,Result(m4o0,m4o2))
		
    # test music4 encrypted full vs encrypted segments
    def test54(self):
        self.assertEqual(MATCH,Result(m4e0,m4e1))
    def test55(self):
        self.assertEqual(MATCH,Result(m4e0,m4e2))
		
    # test music4 original segments vs encrypted segments
    def test56(self):
        self.assertEqual(MATCH,Result(m4o1,m4e1))
    def test57(self):
        self.assertEqual(MATCH,Result(m4o2,m4e2))
    def test58(self):
        self.assertEqual(NO_MATCH,Result(m4o1,m4e2))
    def test59(self):
        self.assertEqual(NO_MATCH,Result(m4o2,m4e1))		
		
    # test music4 original full vs encrypted segments
    def test60(self):
        self.assertEqual(MATCH,Result(m4o0,m4e1))
    def test61(self):
        self.assertEqual(MATCH,Result(m4o0,m4e2))
		
    # test music4 encrypted full vs original segments
    def test62(self):
        self.assertEqual(MATCH,Result(m4e0,m4o1))
    def test63(self):
        self.assertEqual(MATCH,Result(m4e0,m4o2))

		

def main():
    unittest.main()

if __name__ == '__main__':
    main()
