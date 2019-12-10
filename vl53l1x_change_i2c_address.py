#-----------------------------------------------------------------------
# VL53L1X - I2C Address Change (Adv. Autonomous Kit)
#-----------------------------------------------------------------------
#
# Written by  SparkFun Electronics, October 2019
# Author: Wes Furuya
# SparkFun Electronics
# 
# License: This code is public domain but you buy me a beer if you use
# this and we meet someday (Beerware license).
#
# Compatibility:
# 	VL53L1X: https://www.sparkfun.com/products/14667
#	Pi Servo pHat: https://www.sparkfun.com/products/15316
# 
# Do you like this library? Help support SparkFun. Buy a board!
# For more information on VL53L1x ToF or Pi Servo Hat, check out the
# product page linked above.
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

# Check I2C addresses for Pi Servo pHat
while 0x40 in avail_addresses:
	print("Pi Servo pHAT detected on I2C bus at default address (0x40 or 64).")

	# Is the Pi Servo pHat on the I2C bus?
	pi_hat = input("Is the Pi Servo pHat on the I2C bus? (y or n)")

	if pi_hat == "y" or pi_hat == "Y":
		if 0x70 in avail_addresses:
			print("General Call Address detected on I2C bus. Also, shared with Qwiic Mux.")

			# Does the General Call Address need to beed disabled?
			gc = input("Does the General Call Address need to beed disabled (required to use Qwiic Mux)? (y or n)")

			if gc == "y" or gc == "Y":
				# Disable the General Call Address if it is (shared with Mux)
				pca = qwiic.QwiicPCA9685()
				pca.set_addr_bit(0, 0)

				# Re-scans I2C addresses
				avail_addresses = qwiic.scan()

		# Remove Pi Servo pHat from avail_address list
		try:
			avail_addresses.remove(0x40)
		except ValueError:
			print("Addresses for Pi Servo pHat (0x40) not in scanned addresses.")

	else:
		break

# Connect to Mux
mux = qwiic.QwiicTCA9548A()
# Initially Disable All Channels
mux.disable_all()

# Check I2C addresses for VL53L1X
while 0x29 not in avail_addresses:
	print("VL53L1X ToF sensor not detected on I2C bus at default address (0x29 or 41).")

	# Is the VL53L1X attached to the Mux?
	vl = input("Is the VL53L1X ToF attached to a Qwiic Mux? (y or n)")

	if vl == "y" or vl == "Y":
		# Display Mux Configuration
		print("Mux Configuration:")
		print("-------------------")
		mux.list_channels()

		# Does a channel on the Mux need to be enabled?
		ch = input("Does a channel on the Qwiic Mux need to be enabled? (y or n)")
		
		while ch == "y" or ch == "Y":
			# Which channel on the Mux needs to be enabled?
			en_ch = input("Which channel on the Qwiic Mux needs to be enabled? (0-7)")

			# Check Entry
			try:
				en_ch = int(en_ch)
				while en_ch < 0 or 7 < en_ch:
					print("Input outside range of available channels on Qwiic mux (0-7).")
					en_ch = input("Which channel on the Qwiic Mux needs to be enabled? (0-7)")
					en_ch = int(en_ch)
			except ValueError:
				print("Invalid input. Input needs to be an integer.")
				en_ch = input("Which channel on the Qwiic Mux needs to be enabled? (0-7)")
			
			# Enable Channel
			try:
				mux.enable_channels(en_ch)
			except Exception as e:
				print(e)

			# Scans I2C addresses
			avail_addresses = qwiic.scan()

			while 0x29 not in avail_addresses:
				print("VL53L1X ToF sensor not detected on I2C bus at default address (0x29 or 41).")

			# Display Mux Configuration
			print("Mux Configuration:")
			print("-------------------")
			mux.list_channels()

			# Does a channel on the Mux need to be enabled?
			ch = input("Does another channel on the Qwiic Mux need to be enabled? (y or n)")

		if (vl == "n" or vl == "N") or (ch == "n" or ch == "N"):
			# Is the VL53L1X at another address?
			adr = input("Is the VL53L1X ToF at another address? (y or n)")

			if adr == "n" or adr =="N":
				print("Check connection. Device not found.")
				continue
			elif adr == "y" or adr =="Y":
				break

print("Possible VL53L1X addresses (Default = 0x29 or 41):")
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
	
	if new_address == 0x40:
		print("Unavailable address. Address (0x40) is reserved for the Pi Servo pHat.")
	elif new_address == 0x70 and (vl == "y" or vl == "Y"):
		print("Unavailable address. Address (0x70) is reserved for the Qwiic Mux.")
	elif new_address == 0x10:
		print("Unavailable address. Address (0x10) is reserved for the Titan GPS.")
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
				continue
			else:
				exit()

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