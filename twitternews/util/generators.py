from lprint import lprint, lprintln
from stopwatch import Stopwatch

def keep_progress(generator):
    totalTime = Stopwatch()
    stopwatch = Stopwatch()
    count = 0
    for item in generator:
        count += 1
        yield item
        if stopwatch.seconds() >= 1:
            lprint("Processed %d items (%d/s) (%s)" % (count, count/totalTime.seconds(), totalTime))
            stopwatch.start()
    lprintln("Done processing %d items (%s)" % (count, totalTime))
