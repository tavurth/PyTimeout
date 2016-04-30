################################################################################################
#
#    The MIT License (MIT)
#    
#    Copyright (c) 2016 Will Whitty > Tavurth@gmail.com > github.com/tavurth
#    
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#    
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.
#    
################################################################################################

# Import Std
import gevent
from gevent import lock

# Import Global
# Import Local

class Resource:

    def __init__(self, resource, **kwargs):
        """ Save a Resource, and add an associated Semaphore """
        self.resource  = resource
        self.semaphore = gevent.lock.Semaphore()

        # Allow the caller to change the sleeping time for wait handler
        self.sleepTime = kwargs.get('sleep', 1)

    def unlock(self):
        """ Unlock a shared resource """
        self.semaphore.release()

    def lock(self, **kwargs):
        """ Lock the selected resource, and return it """
        while True:

            # Try to acquire the semaphore, else continue
            if not self.semaphore.acquire(timeout = kwargs.get('timeout', 1)):
                # Sleep to save CPU
                gevent.sleep(self.sleepTime)

                # Continue to wait for the locking mechanism
                continue

            # Found and locked resource
            return self.resource

    def locked(self):
        """ Boolean, is this semaphore locked? """
        return self.semaphore.locked()

    def __enter__(self):
        """ Use this object in a 'with' statement """

        # First lock the internal Semaphore
        self.lock()

        # Then return the resource
        return self.resource

    def __exit__(self, type, value, traceback):
        """ Exit a 'with' statement """
        self.unlock()

    def __del__(self):
        """ Remove a Global Resource """
        del(self.resource)
        del(self.semaphore)
