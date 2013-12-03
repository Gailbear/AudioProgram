import numpy
import os

THRESH = 1

class SoundMatcher(object):
    fpdb = None

    def __init__(self, fpdb):
        self.fpdb = fpdb

    def match(self, filename1, filename2):
        db1 = numpy.array(self.fpdb[filename1])
        db1len = len(db1)
        db2 = numpy.array(self.fpdb[filename2])
        db2len = len(db2)

        # db1 is longer
        if db1len > db2len:
            longer = db1
            longer_len = db1len
            longer_name = filename1
            shorter = db2
            shorter_len = db2len
            shorter_name = filename2

        # file2 is longer, or they're equal
        else:
            longer = db2
            longer_len = db2len
            longer_name = filename2
            shorter = db1
            shorter_len = db1len
            shorter_name = filename1

        threshold = shorter_len * THRESH

        iters = longer_len - shorter_len + 1
        mindist = 9999999999999999999999999999999

        # Iterate through each possible offset of the smaller in the larger
        for index in xrange(iters):

            # Grab the freqs from the larger file (at the specified offset)
            subsec = longer[index:shorter_len+index]

            # Calculate Euclidean distance
            dist = numpy.linalg.norm(subsec - shorter)

            #print "Dist @ index %d: %d" % (index, dist)

            # Score this iteration
            name1 = os.path.basename(shorter_name)
            name2 = os.path.basename(longer_name)
            if dist < threshold:
                print "MATCH %s %s" % (name1, name2)
                return
            if dist < mindist:
                mindist = dist

        print "NO MATCH %s %s %d" % (name1, name2, mindist)
        return

