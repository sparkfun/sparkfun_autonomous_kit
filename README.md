<img alt="sphero rvr" src="https://cdn.sparkfun.com/assets/parts/1/3/8/0/5/15303-SparkFun_Advanced_Autonomous_Kit_for_Sphero_RVR-12.jpg"  align="right" width=320> 

# SparkFun Autonomous Kit Code
Python example code for the hardware included in the SparkFun Autonomous Kits. This repository is included in the home directory of the pre-configured image. This is primarily for users looking to build their own images and to make updating files simple for users.

## Clone Folder
To clone the folder use the following command:

`git clone https://github.com/sparkfun/sparkfun_autonomous_kit`

(*\*If you are following the [hookup guide](https://learn.sparkfun.com/tutorials/getting-started-with-the-autonomous-kit-for-the-sphero-rvr), it would be best to clone the repository into the `home` directory as that is how it is used in the [hookup guide](https://learn.sparkfun.com/tutorials/getting-started-with-the-autonomous-kit-for-the-sphero-rvr).*)

## Moving Firmware to Web Interface Folder
The  `piservohat_web_interface_firmware.py` file should be moved to the `RPi_Cam_Web_Interface folder`.

First, change directories into the `sparkfun_autonomous_kit` folder from the download location:

`cd sparkfun_autonomous_kit`

Then move the `piservohat_web_interface_firmware.py` into the the `RPi_Cam_Web_Interface folder`.

`mv piservohat_web_interface_firmware.py ~\RPi_Cam_Web_Interface folder`


## Pulling Repository (for Changes/Updates)
Use the pull command to download any updates or changes from the repository:

`git pull https://github.com/sparkfun/sparkfun_autonomous_kit`
