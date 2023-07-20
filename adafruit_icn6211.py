# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2023 Timon Skerutsch for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_icn6211`
================================================================================

CircuitPython / Python driver for ICN6211 DSI to TTL RGB Display


* Author(s): Timon Skerutsch

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s).
  Use unordered list & hyperlink rST inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies
  based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports
from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice

from adafruit_register.i2c_struct import ROUnaryStruct, UnaryStruct
from adafruit_register.i2c_bits import ROBits, RWBits
from adafruit_register.i2c_bit import ROBit, RWBit

try:
    import typing  # pylint: disable=unused-import
    from busio import I2C
except ImportError:
    pass

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ICN6211.git"


_REG_VENDOR_ID = const(0x00)
_REG_DEVICE_ID_H = const(0x01)
_REG_DEVICE_ID_L = const(0x02)
_REG_VERSION_ID = const(0x03)

_REG_OUT_SEL_CONFIG = const(0x08) #Called "FIRMWARE_VERSION" register in datasheet but register documentation suggests that is a typo
_REG_CONFIG_FINISH = const(0x09)
_REG_SYS_CTRL_0 = const(0x10)
_REG_SYS_CTRL_1 = const(0x11)

_REG_HACTIVE_L = const(0x20)
_REG_VACTIVE_L = const(0x21)
_REG_VACTIVE_HACTIVE_H = const(0x22)
_REG_HFP_L = const(0x23)
_REG_HSW_L = const(0x24)
_REG_HBP_L = const(0x25)
_REG_HFP_HSW_HBP_H = const(0x26)
_REG_VFP = const(0x27)
_REG_VSW = const(0x28)
_REG_VBP = const(0x29)

_REG_BIST_POL = const(0x2a)
_REG_BIST_FRAME_TIME_L = const(0x31)
_REG_BIST_FRAME_TIME_H = const(0x32)
_REG_FIFO_MAX_ADDR = const(0x33)
_REG_SYNC_EVENT_DLY = const(0x34)
_REG_HSW_MIN = const(0x35)
_REG_HFP_MIN = const(0x36)

_REG_PLL_CTRL_1 = const(0x51)
_REG_PLL_CTRL_6 = const(0x56)
_REG_PLL_DIV_0 = const(0x63)
_REG_PLL_DIV_1 = const(0x64)
_REG_PLL_DIV_2 = const(0x65)
_REG_PLL_FRAC_0 = const(0x66)
_REG_PLL_FRAC_1 = const(0x67)
_REG_PLL_FRAC_2 = const(0x68)
_REG_PLL_INT_0 = const(0x69)
_REG_PLL_INT_1 = const(0x6a)
_REG_PLL_REF_DIV = const(0x6b)
_REG_MIPI_CFG_PW = const(0x7a)
_REG_GPIO_0_SEL = const(0x7b)
_REG_GPIO_1_SEL = const(0x7c)
_REG_IRQ_SEL = const(0x7d)
_REG_MIPI_ERR_VECTOR_L = const(0x80)
_REG_MIPI_ERR_VECTOR_H = const(0x81)
_REG_MIPI_MAX_SIZE_L = const(0x84)
_REG_MIPI_MAX_SIZE_H = const(0x85)
_REG_DSI_CTRL = const(0x86)
_REG_MIPI_PN_SWAP = const(0x87)
_REG_MIPI_T_TERM_EN = const(0x90)
_REG_MIPI_T_HS_SETTLE = const(0x91)
_REG_MIPI_T_TA_SURE_PRE = const(0x92)
_REG_MIPI_T_LPX_SET = const(0x94)
_REG_MIPI_T_CLK_MISS = const(0x95)
_REG_MIPI_INIT_TIME_L = const(0x96)
_REG_MIPI_INIT_TIME_H = const(0x97)
_REG_MIPI_T_CLK_TERM_EN = const(0x99)
_REG_MIPI_T_CLK_SETTLE = const(0x9a)
_REG_MIPI_PD_CK_LANE = const(0xb5)



class BIST_MODE:
    DISABLE = 0x00
    MONO = 0x01
    MONO_W_COLOR_BORDER = 0x02
    CHESSBOARD = 0x03
    COLORBAR = 0x04
    COLOR_SWITCH = 0x05

class OUT_RGB_SWAP:
    RGB = 0x00
    RBG = 0x01
    GRB = 0x02
    GBR = 0x03
    BRG = 0x04
    BGR = 0x05

class OUT_BIT_SWAP:
    MODE_666_5_0_to_5_0 = 0x00
    MODE_666_5_0_to_0_5 = 0x01
    MODE_666_7_2_to_5_0 = 0x02
    MODE_666_7_2_to_0_5 = 0x03
    MODE_888_7_0_to_7_0 = 0x04
    MODE_888_7_0_to_0_7 = 0x05

class ICN6211:

    def __init__(self, i2c_bus: I2C, addr: int = 0x2C) -> None:
        self.i2c_device = I2CDevice(i2c_bus, addr)
        self.i2c_addr = addr

    vendor_id = ROUnaryStruct(_REG_VENDOR_ID, ">B")
    device_id = ROUnaryStruct(_REG_DEVICE_ID_H, ">H")
    version_id = ROUnaryStruct(_REG_VERSION_ID, ">B")

    reset = RWBit(_REG_CONFIG_FINISH, 0)
    config_finish = RWBit(_REG_CONFIG_FINISH, 4)

    frc_en = RWBit(_REG_SYS_CTRL_0, 7)
    out_bit_swap = RWBits(3, _REG_SYS_CTRL_0, 4)
    out_rgb_swap = RWBits(3, _REG_SYS_CTRL_0, 0)



    def soft_reset(self):
        self.reset = 1

    def save_config(self):
        self.config_finish = 1