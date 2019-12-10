#-----------------------------------------------------------------------
# Autonoumous Kit - Test ToF (Single)
#-----------------------------------------------------------------------
#
# Written by  SparkFun Electronics, October 2019
# Author: Wes Furuya
# SparkFun Electronics
# 
# License: This code is public domain but you buy me a beer if you use
# this and we meet someday (Beerware license).
#
# Compatibility: https://www.sparkfun.com/products/14667
# 
# Do you like this library? Help support SparkFun. Buy a board!
# For more information on VL53L1x ToF, check out the product page
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

"""
	Reading distance from two VL53L1X sensors.
"""

import os, sys, time
import qwiic

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

print("Available device addresses: ")
print("Hex: ", [hex(x) for x in avail_addresses])
print("Dec: ", [int(x) for x in avail_addresses])

# Does a channel on the Mux need to be enabled?
ch = input("Does a channel on the Qwiic Mux need to be enabled? (y or n)")

while ch == "y" or ch == "Y":
	mux = qwiic.QwiicTCA9548A()

	# Display Mux Configuration
	print("Mux Configuration:")
	print("-------------------")
	mux.list_channels()

	# Which channel on the Mux needs to be enabled?
	en_ch = input("Which channel(s) on the Qwiic Mux needs to be enabled? (0-7)")

	# Check Entry
	while type(en_ch) != int and type(en_ch) != list:
		print("Invalid input. Input needs to be an integer or list.")
		en_ch = input("Which channel(s) on the Qwiic Mux needs to be enabled? (0-7)")

	while True:
		for x in en_ch:
			if en_ch < 0 or 7 < en_ch:
				print("Input outside range of available channels on Qwiic mux (0-7).")
				en_ch = input("Which channel(s) on the Qwiic Mux needs to be enabled? (0-7)")
	
	# Enable Channel
	try:
		mux.enable_channels(en_ch)
	except Exception as e:
		print(e)

	# Scans I2C addresses
	avail_addresses = qwiic.scan()

	print("Available device addresses: ")
	print("Hex: ", [hex(x) for x in avail_addresses])
	print("Dec: ", [int(x) for x in avail_addresses])
	
	# Does a channel on the Mux need to be enabled?
	ch = input("Does another channel on the Qwiic Mux still need to be enabled? (y or n)")

print("Available device addresses: ")
print("Hex: ", [hex(x) for x in avail_addresses])
print("Dec: ", [int(x) for x in avail_addresses])

while True:
	device_address = input("Select the address of the sensor (dec): ")

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
			print("Forward sensor initialized.")
			break

		except Exception as e:
			if e == OSError or e == IOError:
				print("Issue connecting to device.")
				print(e)
			else:
				print(e)

while True:
	try:
		# Start Measurements
		ToF.StartRanging()
		time.sleep(.005)

		# Take Measurements
		distance = ToF.GetDistance()
		time.sleep(.005)

		# Stop Measurements
		ToF.StopRanging()
 
		print("Distance(mm): %s" % distance)

	except Exception as e:
		print(e)
