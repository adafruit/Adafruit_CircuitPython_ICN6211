# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Timon Skerutsch for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import time
import sys
import os
import board
import busio
from adafruit_extended_bus import ExtendedI2C as I2C

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from adafruit_icn6211 import ICN6211, OUT_RGB_SWAP

print("hello blinka!")

i2c = I2C(0)

print("I2C devices found: ", [hex(i) for i in i2c.scan()])
icn = ICN6211(i2c)

icn.out_rgb_swap = OUT_RGB_SWAP.RGB
icn.save_config()
icn.soft_reset()
print(icn.device_id)