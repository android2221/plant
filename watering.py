import pywemo

## Get instance of wemo switch to control
address = "192.168.86.31"
port = pywemo.ouimeaux_device.probe_wemo(address)
url = 'http://%s:%i/setup.xml' % (address, port)
plant_switch = pywemo.discovery.device_from_description(url, None)


## Determine if we should water

plant_switch.toggle()