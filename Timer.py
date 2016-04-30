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
import time
import threading

# Import Global
# Import local
from Resource import Resource

# Global variables
EventsList = Resource({})

# Setting up the events loop
TimedLooper = None

# Used to keep track of event Ids
EventsIdCache = 0

class Timer:

    def __init__(self, delay, callback, *args, **kwargs):
        """ Create an event timer, adding it to the EventsList """
        global EventsList, EventsIdCache, TimedLooper

        # Saving internal variables
        self.args = args
        self.kwargs = kwargs
        self.callback = callback

        # Set the timeout of our event
        self.delay   = delay
        self.timeout = time.time() + delay

        # Wait for the events list to become free
        with EventsList as eList:
            
            # Start the thread if it does not exist
            if not TimedLooper or not TimedLooper.is_alive():
                TimedLooper = threading.Thread(None, event_listener_loop)
                TimedLooper.start()

            # Save this event to the event list
            self.index_id = str(EventsIdCache)
            EventsIdCache += 1

            eList[self.index_id] = self

    def check(self):
        """ Check to see if the event timer has expired """
        # If the timeout of the event has passed
        nowTime = time.time()
        if nowTime >= self.timeout:

            # Call the internal function
            self.callback(*self.args, **self.kwargs)

            # Is the event repeating?
            if self.kwargs.get('repeat', False):
                return False

            # Event has been triggered
            return True

        # The event was not triggered
        return False

def event_listener_loop(*args, **kwargs):
    """ Listen for active events """
    global EventsList
    
    while True:
        # Reset the time to wait for the EventsList resource
        EventsList.sleepTime = 1
        
        # Checking all events until they are no longer pending
        with EventsList as eList:
            for index, event in eList.items():
                # If the event passed delete it
                if event.check():
                    del eList[event.index_id]

                # Set the time to wait to the granularity of the fastest event
                EventsList.sleepTime = min(EventsList.sleepTime, event.delay / 4.0)

            # Stop the thread when we have no more pending events
            if not len(eList):
                break

        # Wait until the next event is likely
        time.sleep(EventsList.sleepTime)

if __name__ == '__main__':

    startTime = time.time()
    def my_func(arg1, arg2):
        global startTime
    
        print 'Args recieved: "', arg1, arg2, '"'
        print 'Time since call:', time.time() - startTime, "\r\n"
        
    Timer(3, my_func, 'Hello', 'again!')
    Timer(1, my_func, 'Hello', 'world')
