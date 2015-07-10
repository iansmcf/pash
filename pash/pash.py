# -*- coding: utf-8 -*-
""" Python-bash (Pash)

This module contains a class which uses 'Popen' from the 'subprocess'
module in the standard Python library in order to easily carry out
interactions with the bourne-again shell.

While this module was written for and tested with Ubuntu 14.04, it
it may function in other environments thanks to the use of the Python
standard 'subprocess' module.

Example:
    >>> import pash
    >>> proc = pash.ShellProc()
    >>> proc.run("echo 'Yes!'")
    >>> print proc.get_val('stdout')
    Yes!
    <BLANKLINE>

"""

# Uses subprocess from the standard Python library to
# access a shell, implementation is tested with bash.
import subprocess


# Doctesting, only executes when module is run as a script
if __name__ == "__main__":
    import doctest
    doctest.testmod()


## Do not use with untrusted input!
# Creates a dict with stdout, stdin, and exit codes
class ShellProc(object):
    """ ShellProc class

    The default form of this object. Includes automatic error
    printing.

    Attributes are covered in the documentation for '__init__'.
    """
    # On starting, creates a small dict for results and
    # a variable for the command that was most recently run
    def __init__(self):
        """ Initialization

        Creates a dict with important values and a string
        containing the command that was most recently run.

        Attributes:
            dict: a dictionary containing stdout, stderr, and exit_code
            command: the most recently-run command
        """
        self.dict = {'stdout': None, 'stderr': None, 'exit_code': None}
        self.command = None

    # Runs the command given; this allows the same object
    # to be used for multiple commands, avoiding syntax bloat
    def run(self, command):
        """ Talking to the shell

        This runs a given command and stores the results (temporarily)
        as returned by the subprocess.

        Args:
            command (string): A command which is to be passed to
                the shell as though it had been typed into
                a terminal window

        Yields:
            Values for stdout, stderr, and the exit code of the
            shell are stored in 'self.dict' until some other
            value overwrites them
        """
        self.command = command
        proc = subprocess.Popen(command, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.dict['stdout'], self.dict['stderr'] = proc.communicate()
        self.dict['exit_code'] = proc.returncode
        self.exit_check()

    # Simple interface for accessing the dict, given a key
    def get_val(self, string='stdout'):
        """Getting a value from the dictionary

        Args:
            string (string): A string matching the value for the key
                which is believed to contain a value of interest to
                the caller

        Returns:
            self.dict[string] (object): A value mapped to 'string'
        """
        return self.dict[string]

    # Returns the last command run
    def get_comm(self):
        """Getting the last command run

        Returns:
            self.command (string): The last command that was
                passed to 'run'
        """
        return self.command

    # Checks the exit code from the shell; if 0,
    # prints a message. To suppress, use SilentShell.
    def exit_check(self):
        """Automatic exit code checking

        This function is automatically called by 'run',
        which allows the programmer to detect errors without
        the need for explicit error handling in program
        logic.

        To override the behavior of this function, use
        'SilentShell' in any place you would otherwise
        use 'ShellProc'.

        Yields:
            A printed error message about the command that was
            called and the exit code it returned on completion.
        """
        if self.dict['exit_code'] != 0:
            print (("(PDebug) The command...\n\t'%s'\n..."
                "exited with a non-zero exit status (%r).")
                % (self.command, self.dict['exit_code']))
            return False
        else:
            return True


# Simply overrides the exit check method to suppress print.
# Use for things which will have program-defined error
# handling, rather than the default.
class SilentShell(ShellProc):
    """ SilentShell

    A simple extension of 'ShellProc" which overrides the
    behavior of error messaging automatically in the 'run'
    function. Use this when you want to implement your own
    error handling, when the exit code of a command does not
    follow typical error code conventions, or when the
    command is expected to fail.

    An example of an expected failure is when using this module
    to wait for the presence of a directory by looping over a
    command that lists its contents until no error is detected.

    Example:
        >>> proc = pash.SilentShell()
    """

    def exit_check(self):
        """ Override for automatic exit checking

        De-fangs the default by removing functionality.
        """
        pass
