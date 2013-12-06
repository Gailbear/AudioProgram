from __future__ import division
import numpy
import os
import wave
from collections import Counter

THRESH = 5

class SoundMatcher(object):
    fpdb = None

    def __init__(self, fpdb):
        self.fpdb = fpdb

    def rabin_karp(self, shorter, longer, shorter_len, iters):
        threshold = THRESH * shorter_len

        # Attempt at rabin karp
        ssub = sum(shorter)
        ss = sum(longer[0:shorter_len])

        for index in xrange(iters):
            dist = abs(ss-ssub)
            if dist < threshold:
                return True
            ss = ss - longer[index] + longer[shorter_len + index -1]
        return False


    def match(self, file1, file2):
        filename1 = file1[0]
        filename2 = file2[0]
        db1 = numpy.array(self.fpdb[filename1])
        db1len = len(db1)
        db2 = numpy.array(self.fpdb[filename2])
        db2len = len(db2)

        # db1 is longer
        if db1len > db2len:
            longer_file = file1[1]
            longer = db1
            longer_len = db1len
            longer_name = filename1
            shorter_file = file2[1]
            shorter = db2
            shorter_len = db2len
            shorter_name = filename2

        # file2 is longer, or they're equal
        else:
            longer_file = file2[1]
            longer = db2
            longer_len = db2len
            longer_name = filename2
            shorter_file = file1[1]
            shorter = db1
            shorter_len = db1len
            shorter_name = filename1


        name1 = os.path.basename(shorter_name)
        name2 = os.path.basename(longer_name)


        if not self.rabin_karp(shorter, longer, shorter_len, iters):
          print "NO MATCH"
          return
        

        print "MATCH %s %s" % (name1, name2)
        return
