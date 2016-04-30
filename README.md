# PyTimer
A simple timed callback function for python

# Use:

 ```
  from PyTimer import Timer

  def callback(a, b, **kwargs):
     print a, b
 
  Timer(2, callback, "Hello", "World")
 ```

# Requirements
 ```
   gevent
   python 2.7
 ```
