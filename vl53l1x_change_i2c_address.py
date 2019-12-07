#-----------------------------------------------------------------------
# VL53L1X - I2C Address Change (Adv. Autonomous Kit)
#-----------------------------------------------------------------------
#
# Ported by  SparkFun Electronics, October 2019
# Author: Wes Furuya
# SparkFun Electronics
# 
# License: This code is public domain but you buy me a beer if you use
# this and we meet someday (Beerware license).
#
# Compatibility: https://www.sparkfun.com/products/14667
# 
# Do you like this library? Help support SparkFun. Buy a board!
# For more information on Pi Servo Hat, check out the product page
# linked above.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http:www.gnu.org/licenses/>.
#
#=======================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#=======================================================================

import os, sys, time
import qwiic


print("Running VL53L1X I2C Address Change")

# Print out from i2cdetect
print("Running: i2cdetect -y 1")
os.system('i2cdetect -y 1')

# Scans I2C addresses
avail_addresses = qwiic.scan()

# Removes I2C addresses of Pi Servo pHat
try:
	avail_addresses.remove(0x40)
	avail_addresses.remove(0x70)
except ValueError:
	print("Addresses for Pi Servo pHat (0x40 and 0x70) not in scanned addresses.")

print("Possible VL53L1X addresses: ")
print("Hex: ", [hex(x) for x in avail_addresses])
print("Dec: ", [int(x) for x in avail_addresses])

while True:
	device_address = input("Select the address of the device to be changed (dec): ")

	try:
		device_address = int(device_address)
	except ValueError:
		print("Invalid input. Input needs to be an integer.")
	
	if device_address not in avail_addresses:
		print("Invalid selection. Select an available address from the list: ", avail_addresses)
	else:
		print("Initializing Device")
		ToF = qwiic.QwiicVL53L1X(device_address)

		try:
			ToF.SensorInit()
		except Exception as e:
			if e == OSError or e == IOError:
				print("Issue connecting to device.")
				print(e)
			else:
				print(e)
		else:
			break

while True:
	print("Reserved Addresses: [0x10, 0x29, 0x40, 0x70]")
	new_address = input("Select a new address for the device (dec): ")

	try:
		new_address = int(new_address)
	except ValueError:
		print("Invalid input. Input needs to be an integer.")
	
	if new_address == 0x40 or new_address == 0x70:
		print("Unavailable address. Addresses is reserved for the Pi Servo pHat are 0x40 and 0x70.")
	elif new_address == 0x10:
		print("Unavailable address. Addresses is reserved for the Titan GPS is 0x10.")
	elif new_address == device_address:
		print("Not a ner address. Device already has that I2C address: ", device_address)
	elif new_address > 119 or new_address < 8:
		print("Invalid input. Input is outside the range of valid I2C addresses (8 to 119).")
	else:
		if new_address == 0x29:
			print("Addresses is reserved for the VL53L1X ToF Distance Sensor (default) is 0x29.")

			keep = input("Proceed? (y or n)")

			if keep == "y" or keep == "Y":
				print("I2C Address Change")

				try:
					ToF.SetI2CAddress(new_address)
				except Exception as e:
					if e == OSError or e == IOError:
						print("Issue connecting to device.")
						print(e)
					else:
						print(e)
				else:
					print("Address change to new address (", hex(new_address), ") is complete.")
					break
		else:
			try:
				ToF.SetI2CAddress(new_address)
			except Exception as e:
				if e == OSError or e == IOError:
					print("Issue connecting to device.")
					print(e)
				else:
					print(e)
			else:
				print("Address change to new address (", hex(new_address), ") is complete.")
				break
			

# Print out from i2cdetect
print("Running: i2cdetect -y 1")
os.system('i2cdetect -y 1')

test = input("Want to test device? (y or n)")

if test == "y" or test == "Y":
	while True:
		try:
			ToF.StartRanging()						 # Write configuration bytes to initiate measurement
			time.sleep(.005)
			distance = ToF.GetDistance()	 # Get the result of the measurement from the sensor
			time.sleep(.005)
			ToF.StopRanging()

			distanceInches = distance / 25.4
			distanceFeet = distanceInches / 12.0

			print("Distance(mm): %s Distance(ft): %s" % (distance, distanceFeet))

		except Exception as e:
			print(e)
else:
	sys.exit()