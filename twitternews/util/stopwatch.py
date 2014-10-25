from time import time


class Stopwatch:
    def __init__(self):
        """
        Creates and starts a new stopwatch
        """
        self.start()

    def start(self):
        """
        starts the stopwatch
        """
        self.startTime = time()

    def seconds(self):
        """
        :return:the time passed in seconds since start was called
        :rtype:int
        """
        return int(time() - self.startTime)

    def __str__(self):
        """
        :return:the string representation of the time of this stopwatch
        :rtype:str
        """
        seconds = self.seconds()
        minutes = seconds / 60
        hours = minutes / 60
        output = ""
        if hours >= 1:
            output += str(hours) + " hour"
            if hours > 1: output += "s"
        if minutes % 60 >= 1:
            if hours >= 1: output += " "
            output += str(minutes % 60) + " minute"
            if minutes % 60 > 1: output += "s"
        if seconds % 60 >= 1:
            if minutes >= 1: output += " "
            output += str(seconds % 60) + " second"
            if seconds % 60 > 1: output += "s"

        return output