import pywemo
from dotenv import load_dotenv
import gspread
from datetime import date, datetime, timedelta
import time
from oauth2client.service_account import ServiceAccountCredentials

def log_watering(spreadsheet_name, watering_duration):
    print("Logging watering...")
    sheet = get_google_sheet(spreadsheet_name)
    log_line = [str(datetime.now()), watering_duration]
    sheet.append_row(log_line)
    print("done!")

def log_next_water(spreadsheet_name, watering_frequency):
    print("Logging next watering...")
    sheet = get_google_sheet(spreadsheet_name, "Next Watering")
    last_water_date = get_last_water_date(spreadsheet_name)
    next_water = get_next_water_date(last_water_date, watering_frequency)
    line = str(next_water)
    records = sheet.get_all_records()
    if not any(line in r['Next Watering'] for r in records):
        sheet.append_row([line])
    print("done!")

def perform_watering(watering_duration, water_switch_ip, develop_mode=True):
    if develop_mode == 'False':
        water_switch = get_wemo_switch(water_switch_ip)
        water_switch.toggle()
    print(f"Watering for {watering_duration} seconds...")
    time.sleep(watering_duration)
    if develop_mode == 'False':
        water_switch.toggle()
    print('done!')
    return True

def should_water(watering_frequency, spreadsheet_name):
    todays_date = datetime.now() 
    try:
        last_water_date = get_last_water_date(spreadsheet_name)              
        return is_next_water_time(last_water_date, watering_frequency)
    except:
        print("Could not get the last water date, something is wrong!")
        return False
    else:
        print("This is a new watering!")
        return True

def get_last_water_date(spreadsheet_name):
    records = get_sheet_records(spreadsheet_name)
    if len(records) > 0:
        last_record = records[-1]
        last_water_date_string = last_record["Datestamp"]
        last_water_date = datetime.strptime(last_water_date_string, '%Y-%m-%d %H:%M:%S.%f')
        return last_water_date

def get_next_water_date(last_water_date, watering_frequency):
    next_water_date = last_water_date + timedelta(days=int(watering_frequency))
    return next_water_date

def is_next_water_time(last_water_date, watering_frequency):
    next_water_date = get_next_water_date(last_water_date, watering_frequency)
    if datetime.now() >= next_water_date:
        return True
    else:
        print(f"Next water time is {str(next_water_date)}")
        return False

def get_google_sheet(sheet_name, ws_name=False):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret_plant_watering.json', scope)
    client = gspread.authorize(creds)
    if not ws_name:
        sheet = client.open(sheet_name).sheet1
    else:
        sheet = client.open(sheet_name).worksheet(ws_name)
    return sheet

def get_sheet_records(sheet_name):
    sheet = get_google_sheet(sheet_name)
    records = sheet.get_all_records()
    return records

def get_wemo_switch(ip_address):
    address = ip_address
    port = pywemo.ouimeaux_device.probe_wemo(address)
    url = 'http://%s:%i/setup.xml' % (address, port)
    plant_switch = pywemo.discovery.device_from_description(url, None)
    return plant_switch

