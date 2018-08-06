from flask import Flask

import os
import glob
import time
import re

# For LCD display.
import Adafruit_CharLCD as LCD

# Raspberry Pi pin configuration:
lcd_rs        = 25  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 21
lcd_d7        = 22
# lcd_backlight = 4  # Not used for my LCD.

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows)

# initialize modprobe stuff
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# path of the all the temp sensors
base_dir = '/sys/bus/w1/devices/'

# file location in each sensor
file_location = '/w1_slave'

# full list of all the temp sensors unique ID
temp_sensors = ['28-00000729be6e', '28-000007291af0', '28-000007296c0d', '28-0000072a26c3', '28-0000072a2e50']

# Loops through each sensor and prepends and appends the dir and file location to each.
temp_sensor_paths = []
for sensor in temp_sensors:
	temp_sensor_paths.append(base_dir + sensor + file_location)
	
print(temp_sensor_paths)	

# make regex to find 'YES'
yesRegex = re.compile(r'''(
	(YES)
)''', re.VERBOSE)

# make regex to find temp reading
tempRegex = re.compile(r'''(
	(t=\d+)
)''', re.VERBOSE)

# read temp from sensor file
def read_temp_raw():
	f = open(temp_sensor_paths[0], 'r')
	lines = str(f.readlines())
	f.close()
	return lines

# make raw data pretty
def read_temp():
	lines = read_temp_raw()
	for groups in yesRegex.findall(lines):
		if groups[0] != 'YES':
			time.sleep(0.5)
			lines = read_temp_raw()
		for groups in tempRegex.findall(lines):
			temp = groups[0]
			temp_number = temp[2:]
			if temp_number != -1:
				return temp_number
			else:
				return 'Temp error: value = -1'

# calculate to celcius and farenheit
def calc_temps():
	temp = read_temp()
	temp_c = float(temp) / 1000.0
	temp_f = temp_c * 9.0 / 5.0 + 32.0
	return temp_c, temp_f

def save_to_file():
	get_temps = calc_temps()
	temp_c = str(get_temps[0])
	temp_f = str(get_temps[1])
	data_file = open('temp_data.txt', 'a')
	data_file.write('Celcius: ' + temp_c + ' Fahrenheit: ' + temp_f)
	data_file.close()

while True:
  #	save_to_file()
	get_temps = calc_temps()
	temp_c = str(round(get_temps[0], 1))
	temp_f = str(round(get_temps[1], 1))

	# Set LCD cursor to home position.
	lcd.set_cursor(0, 0)
	# Print to LCD.
	lcd.message('Temp:')

	# Set LCD cursor to next line.
	lcd.set_cursor(0, 1)
	# Print actual temperature.
	lcd.message('{}'.format(temp_f))

	# Special ASCII char. Degree symbol.
	lcd.write8(223, True)
	# Print F for fahrenheit.
	lcd.message('F')

	# Print a two line message
	# lcd.message('Temp:\n{}F'.format(temp_f))
	# print('Celcius: ' + temp_c + '\nFahrenheit: ' + temp_f)
	time.sleep(1)

app = Flask(__name__)

@app.route('/')
def index():
    get_temps = calc_temps()
    temp_fx = str(round(get_temps[1], 1))
    return 'Temp F: {}'.format(temp_fx)