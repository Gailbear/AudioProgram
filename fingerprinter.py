import numpy
import operator
import scipy.io.wavfile
import sys
import wave

class FingerPrinter(object):
    fpdb = {}

    def max_idx(self, values):
        return max(enumerate(values), key=operator.itemgetter(1))[0]

    def get_database(self):
        return self.fpdb

    def add_fingerprint(self, fname):
        print "Fingerprinting %s" % fname

        self.fpdb[fname] = {}

        f = wave.open(fname)
        nsamp = f.getnframes()
        width = f.getsampwidth()
        rate, data = scipy.io.wavfile.read(fname)
        print "Rate: %d" % rate
        print "Width: %d" % width
        print "Samples: %d" % nsamp
        print "Data: %s" % data[0:20]

        # We only want to read 32 samples per second
        skip = rate / 32
        print "Skip = %d" % skip

        # Parse through the samples
        for idx in xrange(0, nsamp, skip):
            chunk = data[idx:idx+skip]
            size = len(chunk)
            result = [abs(x) for x in numpy.fft.fft(chunk)][0:size/2]
            maxidx = self.max_idx(result)
            freq = maxidx * rate / size
            print "Maximum intensity frequency: %f" % freq
            self.fpdb[fname][idx] = freq
