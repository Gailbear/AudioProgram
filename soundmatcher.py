import numpy
import sys

class SoundMatcher(object):
    @staticmethod
    def match(file1, file2):
        f1len = file1.getnframes()
        f2len = file2.getnframes()

        # file1 is longer
        if f1len > f2len:
            shorter = file1
            shorter_len = f1len
            longer = file2
            longer_len = f2len

        # file2 is longer, or they're equal
        else:
            shorter = file2
            shorter_len = f2len
            longer = file1
            longer_len = f1len

        # Grab the frames of the shorter file
        chunksize = shorter.getnframes()
        frames = shorter.readframes(chunksize)
        chunk = numpy.fromiter((ord(c) for c in frames), int, count=len(frames))

        best_index = 0
        lowest_dist = 10000000

        # Iterate through each possible offset of the smaller in the larger file
        for idx in xrange(longer_len - shorter_len + 1):

            # Grab the frames from the larger file (at the specified offset)
            longer.setpos(idx)
            frames = longer.readframes(chunksize)
            subsec = numpy.fromiter((ord(c) for c in frames), int, count=len(frames))

            # Do some maths
            dist = numpy.linalg.norm(subsec - chunk)

            print "dist for index %d = %d" % (idx, dist)

            # Score this iteration
            if dist < lowest_dist:
                best_index = idx
                lowest_dist = dist

        return (lowest_dist < 100)
