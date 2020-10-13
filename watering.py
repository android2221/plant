import os
from helpers import *

load_dotenv()

develop_mode = os.getenv("DEVELOP_MODE", True)
water_switch_ip = os.getenv("WATER_SWITCH_IP")
watering_frequency = os.getenv("WATERING_FREQUENCY")
watering_duration = os.getenv("WATERING_DURATION")
spreadsheet_name = os.getenv("GOOGLE_SPREADSHEET_NAME")

should_water = should_water(watering_frequency, spreadsheet_name)

if should_water:
    perform_watering(int(watering_duration), water_switch_ip, develop_mode)
    log_watering(spreadsheet_name, watering_duration)
    print("Watering complete!")
else:
    log_next_water(spreadsheet_name, watering_frequency)
