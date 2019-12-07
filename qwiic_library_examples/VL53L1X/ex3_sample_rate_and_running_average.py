#-----------------------------------------------------------------------
# VL53L1X - Example 3
#-----------------------------------------------------------------------
#
# Ported by  SparkFun Electronics, October 2019
# Author: Nathan Seidle
# Ported: Wes Furuya
# SparkFun Electronics
# 
# License: This code is public domain but you buy me a beer if you use
# this and we meet someday (Beerware license).
#
# Compatibility: https://www.sparkfun.com/products/14722
# 
# Do you like this library? Help support SparkFun. Buy a board!
# For more information on VL53L1x (ToF), check out the product page
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
	Reading distance from the laser based VL53L1X

	This example configures the sensor to short distance mode and then
	prints the distance to an object. The output also includes a
	running average of the last 10 readings along with some statistics,
	like signal rate and frequency (of the measurements).
	
	If you are getting weird readings, be sure the vacuum tape has been
	removed from the sensor.
"""

import qwiic
import time statistics

print("VL53L1X Qwiic Test\n")
ToF = qwiic.QwiicVL53L1X()

if (ToF.SensorInit() == None):					 # Begin returns 0 on a good init
	print("Sensor online!\n")

ToF.SetDistanceMode(1)	# Sets Distance Mode Short (Long- Change value to 2)

distance = [] # Initialize list

while True:
	start = time.time()

	try:
		ToF.StartRanging()									# Write configuration bytes to initiate measurement
		time.sleep(.005)
		distance.append(ToF.GetDistance())	# Get the result of the measurement from the sensor
		time.sleep(.005)
		ToF.StopRanging()

	except Exception as e:
		print(e)

	end = time.time()

	distanceInches = distance[len(distance)-1] / 25.4
	distanceFeet = distanceInches / 12.0
	
	if len(distance) < 10:
		avgdistance = statistics.mean(distance)
	else:
		distance.remove(distance[0])
		avgdistance = statistics.mean(distance[len(distance)-10:len(distance)+1]) # Running average of last 10 measurements
	
	signalrate = ToF.GetSignalRate()
	rangestatus = ToF.GetRangeStatus()
	
	#print("Distance(mm): %s avgDistance(mm): %s Distance(ft): %.3f Signal Rate: %s Range Status: %s Hz: %.5f" % (distance[len(distance)-1], avgdistance, distanceFeet, signalrate, rangestatus,(end-start)))
	print("Distance(mm): %s avgDistance(mm): %.2f Signal Rate: %s Range Status: %s Hz: %.5f" % (distance[len(distance)-1], avgdistance, signalrate, rangestatus,(end-start)))


	#if rangestatus == 0:
		#print("Good ")
	#elif rangestatus == 1:
		#print("Signal Fail ")
	#elif rangestatus == 2:
		#print("Sigma Fail ")
	#elif rangestatus == 7:
		#print("Wrapped Target Fail ")
	#else:
		#print("Unknown (code: %s) ", rangestatus)
