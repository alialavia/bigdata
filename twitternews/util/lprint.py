
from sys import stdout

def lprint(obj):
    """
    Overwrites the current line in output and prints given object to it

    :param obj: The object to print
    """
    stdout.write("\033[2K\r")
    stdout.write(obj)
    stdout.flush()

def lprintln(obj):
    """
    Overwrites the current line in output and prints given object to it, ending with a newline

    :param obj: The object to print
    """
    stdout.write("\033[2K\r")
    stdout.write(obj)
    stdout.write("\n")
    stdout.flush()
