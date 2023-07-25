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

i2c = I2C(0)

# todo: fix module import, hack for development
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from adafruit_icn6211 import *

# print("I2C devices found: ", [hex(i) for i in i2c.scan()])
icn = ICN6211(i2c)

# icn.out_rgb_swap = OUT_RGB_SWAP.RGB
# print(icn.device_id)
# icn.set_test_mode(BIST_MODE.DISABLE)

icn.de_pol = True
icn.set_resolution(800,480)
icn.set_horizontal_front_porch(40)
icn.set_horizontal_sync_width(40)
icn.set_horizontal_back_porch(40)
icn.set_vertical_front_porch(10)
icn.set_vertical_sync_width(10)
icn.set_vertical_back_porch(10)
icn.sync_event_delay = 128
icn.pd_ck_term_force = True
icn.pd_ck_hsrx_force = True
icn.out_rgb_swap = OUT_RGB_SWAP.RGB
icn.out_bit_swap = OUT_BIT_SWAP.MODE_888_7_0_to_7_0
icn.mipi_lane_num = MIPI_LANE_NUM.ONE_LANE
icn.pll_refsel = PLL_REF_SEL.MIPI_CLK
icn.pll_int_0 = 3 #PLL clock
icn.pll_out_divide_ratio = PLL_OUT_DIV_RATIO.DIV_2
icn.pll_ref_clk_divide_ratio = PLL_REF_CLK_DIV_RATIO.DIV_1
icn.pll_ref_clk_extra_divide = True
icn.mipi_force_0 = 0x20 #not documented, magic value from Linux driver
icn.pll_vco_isel = 0x20 #not documented, magic value from Linux driver
icn.clk_phase_sel = CLK_PHASE.PHASE_0
icn.pll_clkqen = True
icn.mipi_xor = True #not documented what it does, taken from config tool

icn.save_config()

# icn.soft_reset()
icn.dump_registers()
icn.print_errors()
icn.reset_errors()

