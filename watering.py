import os
from helpers import *

load_dotenv()

develop_mode = os.getenv("DEVELOP_MODE", True)
water_switch_ip = os.getenv("WATER_SWITCH_IP")


if not develop_mode:
    water_switch = get_wemo_switch(water_switch_ip)

should_water = should_water()
