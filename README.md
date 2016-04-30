# PyTimer
A simple timed callout function for python

# Use:

  from PyTimer import Timer

  def callback(a, b, **kwargs):
     print a, b
 
  Timer(2, callback, "Hello", "World")
