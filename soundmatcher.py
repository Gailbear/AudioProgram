import logging
import numpy
import sys

# Don't judge me, it's just a prototype.

class SoundMatcher(object):
    def grabframes(self, w):
        chunksize = w.getnframes()
        frames = w.readframes(chunksize)
        chunk = numpy.fromstring(frames, dtype='uint8')
        return chunk, len(chunk)

    def match(self, file1, file2):
        f1len = file1.getnframes()
        f2len = file2.getnframes()

        sample_width = file1.getsampwidth()

        if sample_width != file2.getsampwidth():
            logging.error("ERROR: Input files must have same sample width (%d != %d)", sample_width, file2.getsampwidth())
            sys.exit(-1)

        # file1 is longer
        if f1len > f2len:
            longer = file1
            longer_len = f1len
            shorter = file2
            shorter_len = f2len

        # file2 is longer, or they're equal
        else:
            longer = file2
            longer_len = f2len
            shorter = file1
            shorter_len = f1len

        # Grab the frames of the shorter file
        chunk, chunksize = self.grabframes(shorter)
        haystack, haystacksize = self.grabframes(longer)

        lowest_dist = 500

        iters = ((haystacksize - chunksize) / sample_width) + 1

        # Iterate through each possible offset of the smaller in the larger file
        for offset in xrange(iters):

            index = offset * sample_width

            # Grab the frames from the larger file (at the specified offset)
            subsec = haystack[index:chunksize+index]

            # Do some maths
            dist = numpy.linalg.norm(subsec - chunk)

            logging.debug("dist for index %d = %d", index, dist)

            # Score this iteration
            if dist < lowest_dist:
                lowest_dist = dist

        return (lowest_dist < 500)
