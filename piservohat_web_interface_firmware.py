#-----------------------------------------------------------------------
# Modified firmware for Pi Servo Hat web interface using Qwiic library
#-----------------------------------------------------------------------
#
# Written by SparkFun Electronics, November 2019
# Author: Mike Hord
# Modified by: Wes Furuya
#
# Compatibility:
#	* Original: https://www.sparkfun.com/products/14328
#	* v2: https://www.sparkfun.com/products/15316
# 
# Do you like this code? Help support SparkFun. Buy a board!
# For more information on Pi Servo Hat, check out the product page
# linked above.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http:www.gnu.org/licenses/>.
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


# Import Dependencies:
import pi_servo_hat
import time

# Function to rescale web interface controls
def scale(x, in_min, in_max, out_min, out_max):
	return (x - in_min)*(out_max - out_min)/(in_max - in_min) + out_min

########################################################################
# Main Function:
########################################################################

# Initialize Servo Hat
servohat = pi_servo_hat.PiServoHat()

# Restart Servo Hat
servohat.restart()

pan_seting_old = 0
tilt_seting_old = 0

while True:
	pipein = open("/var/www/html/FIFO_pipan", 'r')
	line = pipein.readline()
	line_array = line.split(' ')
	if line_array[0] == "servo":

		# Rescales Left/Right position values
		#	web controls:		Left = 250;	Right = 50
		#	library controls:	Left =  90;	Right =  0
		pan_setting = scale(int(line_array[1]), 50, 250, 0, 90)

		# Rescales Up/Down position values
		#	web controls:		Down = 220;	Up = 80
		#	library controls:	Down =  90;	Up =  0
		tilt_setting = scale(int(line_array[2]), 80, 220, 0, 90)

		if pan_setting != pan_setting_old:
			pan_setting_old = pan_setting
			servohat.move_servo_position(0, pan_setting, 90)
			time.sleep(.05)

		if tilt_setting != tilt_setting_old:
			tilt_setting_old = tilt_setting
			servohat.move_servo_position(1, tilt_setting, 90)
			time.sleep(.05)

pipein.close()
