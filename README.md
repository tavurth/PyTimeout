# PyTimeout
A simple timed callback function for python

# Use

 ```
  from PyTimeout import Timeout

  def callback(a, b, **kwargs):
     print a, b
 
  Timeout(2, callback, "Hello", "World")
 ```

# Requirements
 ```
   gevent
   python 2.7
 ```
