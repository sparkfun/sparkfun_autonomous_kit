#-----------------------------------------------------------------------
# Autonoumous Kit - Test ToF (Dual Configuration)
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

print("Available device addresses: ")
print("Hex: ", [hex(x) for x in avail_addresses])
print("Dec: ", [int(x) for x in avail_addresses])

while True:
	device_address = input("Select the address of the front sensor (dec): ")

	try:
		device_address = int(device_address)
	except ValueError:
		print("Invalid input. Input needs to be an integer.")
	
	if device_address not in avail_addresses:
		print("Invalid selection. Select an available address from the list: ", avail_addresses)
	else:
		print("Initializing Device")
		ToF_front = qwiic.QwiicVL53L1X(device_address)

		try:
			ToF_front.SensorInit()
            Print("Forward sensor initialized.")
            break

		except Exception as e:
			if e == OSError or e == IOError:
				print("Issue connecting to device.")
				print(e)
			else:
				print(e)

while True:
	device_address = input("Select the address of the rear sensor (dec): ")

	try:
		device_address = int(device_address)
	except ValueError:
		print("Invalid input. Input needs to be an integer.")
	
	if device_address not in avail_addresses:
		print("Invalid selection. Select an available address from the list: ", avail_addresses)
	else:
		print("Initializing Device")
		ToF_rear = qwiic.QwiicVL53L1X(device_address)

		try:
			ToF_rear.SensorInit()
            Print("Rear sensor initialized.")
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
        ToF_front.StartRanging()
        time.sleep(.005)
		ToF_rear.StartRanging()
		time.sleep(.005)

        # Take Measurements
		fwd_distance = ToF_front.GetDistance()
        time.sleep(.005)
        rear_distance = ToF_rear.GetDistance()
        time.sleep(.005)

		# Stop Measurements
		ToF_front.StopRanging()
        time.sleep(.005)
        ToF_rear.StopRanging()

		print("Forward Distance(mm): %s    Rear Distance(mm): %s" % (fwd_distance, rear_distance))

	except Exception as e:
		print(e)
