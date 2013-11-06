import numpy

class SoundMatcher(object):
    fpdb = None

    def __init__(self, fpdb):
        self.fpdb = fpdb

    def grabframes(self, w):
        chunksize = w.getnframes()
        frames = w.readframes(chunksize)
        return frames, len(frames)

    def match(self, file1, file2):
        db1 = numpy.array(self.fpdb[file1.name])
        db1len = len(db1)
        db2 = numpy.array(self.fpdb[file2.name])
        db2len = len(db2)

        # db1 is longer
        if db1len > db2len:
            longer = db1
            longer_len = db1len
            shorter = db2
            shorter_len = db2len

        # file2 is longer, or they're equal
        else:
            longer = db2
            longer_len = db2len
            shorter = db1
            shorter_len = db1len

        threshold = 300000

        iters = longer_len - shorter_len + 1

        # Iterate through each possible offset of the smaller in the larger
        for index in xrange(iters):

            # Grab the freqs from the larger file (at the specified offset)
            subsec = longer[index:shorter_len+index]

            # Do some maths
            dist = numpy.linalg.norm(subsec - shorter)

            # Score this iteration
            if dist < threshold:
                # Just return immediately
                return True

        return False
