from helpers import *
import time

develop_mode=False

if not develop_mode:
    water_switch = get_wemo_switch("192.168.86.31")

input('Press enter to start watering')

if not develop_mode:
    water_switch.on()

start = time.time()

input('Press enter to stop watering')

if not develop_mode:
    water_switch.off()

end = time.time()

print('Total watering time:')
print(end - start)