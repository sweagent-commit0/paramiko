"""
Attempt to generalize the "feeder" part of a `.Channel`: an object which can be
read from and closed, but is reading from a buffer fed by another thread.  The
read operations are blocking and can have a timeout set.
"""
import array
import threading
import time
from paramiko.util import b

class PipeTimeout(IOError):
    """
    Indicates that a timeout was reached on a read from a `.BufferedPipe`.
    """
    pass

class BufferedPipe:
    """
    A buffer that obeys normal read (with timeout) & close semantics for a
    file or socket, but is fed data from another thread.  This is used by
    `.Channel`.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._cv = threading.Condition(self._lock)
        self._event = None
        self._buffer = array.array('B')
        self._closed = False

    def set_event(self, event):
        """
        Set an event on this buffer.  When data is ready to be read (or the
        buffer has been closed), the event will be set.  When no data is
        ready, the event will be cleared.

        :param threading.Event event: the event to set/clear
        """
        pass

    def feed(self, data):
        """
        Feed new data into this pipe.  This method is assumed to be called
        from a separate thread, so synchronization is done.

        :param data: the data to add, as a ``str`` or ``bytes``
        """
        pass

    def read_ready(self):
        """
        Returns true if data is buffered and ready to be read from this
        feeder.  A ``False`` result does not mean that the feeder has closed;
        it means you may need to wait before more data arrives.

        :return:
            ``True`` if a `read` call would immediately return at least one
            byte; ``False`` otherwise.
        """
        pass

    def read(self, nbytes, timeout=None):
        """
        Read data from the pipe.  The return value is a string representing
        the data received.  The maximum amount of data to be received at once
        is specified by ``nbytes``.  If a string of length zero is returned,
        the pipe has been closed.

        The optional ``timeout`` argument can be a nonnegative float expressing
        seconds, or ``None`` for no timeout.  If a float is given, a
        `.PipeTimeout` will be raised if the timeout period value has elapsed
        before any data arrives.

        :param int nbytes: maximum number of bytes to read
        :param float timeout:
            maximum seconds to wait (or ``None``, the default, to wait forever)
        :return: the read data, as a ``str`` or ``bytes``

        :raises:
            `.PipeTimeout` -- if a timeout was specified and no data was ready
            before that timeout
        """
        pass

    def empty(self):
        """
        Clear out the buffer and return all data that was in it.

        :return:
            any data that was in the buffer prior to clearing it out, as a
            `str`
        """
        pass

    def close(self):
        """
        Close this pipe object.  Future calls to `read` after the buffer
        has been emptied will return immediately with an empty string.
        """
        pass

    def __len__(self):
        """
        Return the number of bytes buffered.

        :return: number (`int`) of bytes buffered
        """
        self._lock.acquire()
        try:
            return len(self._buffer)
        finally:
            self._lock.release()