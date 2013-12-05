from __future__ import division
import numpy
import os
import wave
from collections import Counter

THRESH = 100
diff_thresh = .5

class SoundMatcher(object):
    fpdb = None

    def __init__(self, fpdb):
        self.fpdb = fpdb

    def confirm_match(self, shorter, longer, index):
        # Grab the frames of the shorter file
        chunksize = shorter.getnframes()
        frames = shorter.readframes(chunksize)
        chunk = numpy.fromiter((ord(c) for c in frames), int, count=len(frames))

        # Grab the frames from the larger file (at the specified offset)
        longer.setpos(index)
        frames = longer.readframes(chunksize)
        subsec = numpy.fromiter((ord(c) for c in frames), int, count=len(frames))

        # Calculate Euclidean distance
        dist = numpy.linalg.norm(subsec - chunk)
        
        threshold = chunksize * diff_thresh

        #print "dist %f; threshold %d" % (dist, threshold)
        return dist < threshold


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


        longer_wave = None
        shorter_wave = None

        threshold = THRESH * shorter_len

        iters = longer_len - shorter_len + 1
        mindist = 9999999999999999999999999999999
        maxpctmatch = 0

        name1 = os.path.basename(shorter_name)
        name2 = os.path.basename(longer_name)
        
        # Attempt at rabin karp
        ssub = sum(shorter)
        ss = sum(longer[0:shorter_len])

        for index in xrange(iters):
            dist = abs(ss-ssub)
            if dist < threshold:
                longer_wave = wave.open(longer_file.name, "r")
                shorter_wave = wave.open(shorter_file.name, "r")
                confirm = self.confirm_match(shorter_wave, longer_wave, index)
                if confirm:
                    print "MATCH %s %s (index %d)" % (name1, name2, index)
                    return
            if dist < mindist:
              mindist = dist
            ss = ss - longer[index] + longer[shorter_len + index -1]
        print "NO MATCH %s %s (%d)" % (name1, name2, mindist)
        return