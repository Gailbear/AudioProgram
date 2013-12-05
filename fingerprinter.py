import math
import numpy
import operator
import scipy.io.wavfile
import wave

class FingerPrinter(object):
    fpdb = {}

    def max_idx(self, values):
        return max(enumerate(values), key=operator.itemgetter(1))[0]

    def get_database(self):
        return self.fpdb

    def in_database(self, filename):
        return filename in self.fpdb

    def add_fingerprint(self, filename, wavefile):
        self.fpdb[filename] = []

        wf = wave.open(wavefile)
        nsamp = wf.getnframes()
        width = wf.getsampwidth()
        rate, data = scipy.io.wavfile.read(wavefile.name)

        # We only want to read 32 samples per second
        skip = rate / 32

        # Parse through the samples
        for idx in xrange(0, nsamp, skip):
            chunk = data[idx:idx+skip]
            size = len(chunk)
            end = int(math.ceil(size/2.0))
            result = [abs(x) for x in numpy.fft.rfft(chunk)][0:end]
            maxidx = self.max_idx(result)
            freq = maxidx * rate / size

            self.fpdb[filename].append(freq)
