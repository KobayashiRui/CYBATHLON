import RPi.GPIO as IO
import time

IO.setmode(IO.BOARD)
IO.setup(11,IO.OUT)
IO.output(11,True)
time.sleep(3)
IO.output(11,False)



