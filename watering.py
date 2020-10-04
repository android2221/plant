import os
from helpers import *

load_dotenv()

develop_mode = os.getenv("DEVELOP_MODE", True)
water_switch_ip = os.getenv("WATER_SWITCH_IP")
watering_frequency = os.getenv("WATERING_FREQUENCY")
watering_duration = os.getenv("WATERING_DURATION")


if not develop_mode:
    water_switch = get_wemo_switch(water_switch_ip)

should_water = should_water(watering_frequency)
print("Should water??")
print(should_water)
