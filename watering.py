import os
import pywemo
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

develop_mode = os.getenv("DEVELOP_MODE", True)
water_switch_ip = os.getenv("WATER_SWITCH_IP")

## Determine if we should water
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret_plant_watering.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Plant Watering").sheet1

# Extract and print all of the values
records = sheet.get_all_records()
print(records)


if not develop_mode:
    water_switch = get_wemo_switch(water_switch_ip)

## Get instance of wemo switch to control
def get_wemo_switch(ip_address):
    address = ip_address
    port = pywemo.ouimeaux_device.probe_wemo(address)
    url = 'http://%s:%i/setup.xml' % (address, port)
    plant_switch = pywemo.discovery.device_from_description(url, None)
    return plant_switch
