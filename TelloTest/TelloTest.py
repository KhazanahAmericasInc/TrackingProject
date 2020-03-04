from easytello import tello

import time

my_drone = tello.Tello()

print(my_drone.get_battery())

my_drone.streamon()

my_drone.takeoff()

my_drone.wait(1)

for i in range (0,3):
	my_drone.forward(100)
	my_drone.cw(120)

my_drone.wait(1)
my_drone.land()

my_drone.streamoff()
print(my_drone.get_battery())