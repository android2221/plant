
import pywemo
from dotenv import load_dotenv
import gspread
from datetime import date, datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials

def should_water(watering_frequency):
    todays_date = datetime.now()
    records = get_sheet_records("Plant Watering")
    if len(records) > 0:
        last_record = records[-1]
        last_water_date_string = last_record["Datestamp"]
        try:
            last_water_date = datetime.strptime(last_water_date_string, '%Y-%m-%d %H:%M:%S.%f')
            return is_next_water_time(last_water_date, watering_frequency)
        except:
            print("Could not get the last water date, something is wrong!")
            return False
    else:
        print("This is a new watering!")
        return True

def is_next_water_time(last_water_date, watering_frequency):
    next_water_date = last_water_date + timedelta(days=3)
    if datetime.now() >= next_water_date:
        return True
    else:
        return False


def get_sheet_records(sheet_name):
    ## Determine if we should water
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret_plant_watering.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open(sheet_name).sheet1

    # Extract and print all of the values
    records = sheet.get_all_records()
    return records

## Get instance of wemo switch to control
def get_wemo_switch(ip_address):
    address = ip_address
    port = pywemo.ouimeaux_device.probe_wemo(address)
    url = 'http://%s:%i/setup.xml' % (address, port)
    plant_switch = pywemo.discovery.device_from_description(url, None)
    return plant_switch

