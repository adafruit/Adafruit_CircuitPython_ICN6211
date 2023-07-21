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
    vactive_l = UnaryStruct(_REG_VACTIVE_L, ">B")
    hactive_l = UnaryStruct(_REG_HACTIVE_L, ">B")
    vactive_hactive_h = UnaryStruct(_REG_VACTIVE_HACTIVE_H, ">B")

    hfp_l = UnaryStruct(_REG_HFP_L, ">B")
    hsw_l = UnaryStruct(_REG_HSW_L, ">B")
    hbp_l = UnaryStruct(_REG_HBP_L, ">B")
    hfp_h = RWBits(2, _REG_HFP_HSW_HBP_H, 4)
    hsw_h = RWBits(2, _REG_HFP_HSW_HBP_H, 2)
    hbp_h = RWBits(2, _REG_HFP_HSW_HBP_H, 0)

    vfp = UnaryStruct(_REG_VFP, ">B")
    vsw = UnaryStruct(_REG_VSW, ">B")
    vbp = UnaryStruct(_REG_VBP, ">B")

    bist_mode = RWBits(4, _REG_BIST_POL, 4)
    bist_gen = RWBit(_REG_BIST_POL, 3)
    hs_pol = RWBit(_REG_BIST_POL, 2)
    vs_pol = RWBit(_REG_BIST_POL, 1)
    de_pol = RWBit(_REG_BIST_POL, 0)

    pll_cali_en = RWBit(_REG_PLL_CTRL_1, 7)
    pll_cali_req = RWBit(_REG_PLL_CTRL_1, 6)
    pll_vco_isel = RWBits(6, _REG_PLL_CTRL_1, 0)
    pll_lpf_c = RWBits(3, _REG_PLL_CTRL_6, 5)
    pll_lpf_r = RWBits(3, _REG_PLL_CTRL_6, 2)
    pll_refsel = RWBits(2, _REG_PLL_CTRL_6, 0)

    pll_div_0 = UnaryStruct(_REG_PLL_DIV_0, ">B")
    pll_div_1 = UnaryStruct(_REG_PLL_DIV_1, ">B")
    pll_div_2 = UnaryStruct(_REG_PLL_DIV_2, ">B")

    pll_frac_0 = UnaryStruct(_REG_PLL_FRAC_0, ">B")
    pll_frac_1 = UnaryStruct(_REG_PLL_FRAC_1, ">B")
    pll_frac_2 = UnaryStruct(_REG_PLL_FRAC_2, ">B")

    pll_int_0 = UnaryStruct(_REG_PLL_INT_0, ">B")
    pll_int_1 = RWBits(2, _REG_PLL_INT_1, 0)

    ssc_enable = RWBit(_REG_PLL_INT_1, 3)
    det_lock_sel = RWBit(_REG_PLL_INT_1, 2)

    pll_divide_ratio = RWBits(2, _REG_PLL_REF_DIV, 5)
    pll_ref_clk_divide_ratio = RWBits(5, _REG_PLL_REF_DIV, 0)

    mipi_cfg_pw = UnaryStruct(_REG_MIPI_CFG_PW, ">B")
    gpio_0_sel = UnaryStruct(_REG_GPIO_0_SEL, ">B")
    gpio_1_sel = UnaryStruct(_REG_GPIO_1_SEL, ">B")
    irq_sel = UnaryStruct(_REG_IRQ_SEL, ">B")

    sot_err = RWBit(_REG_MIPI_ERR_VECTOR_L, 0)
    sot_sync_err = RWBit(_REG_MIPI_ERR_VECTOR_L, 1)
    eot_sync_err = RWBit(_REG_MIPI_ERR_VECTOR_L, 2)
    emec_err = RWBit(_REG_MIPI_ERR_VECTOR_L, 3)
    lpt_sync_err = RWBit(_REG_MIPI_ERR_VECTOR_L, 4)
    peripheral_err = RWBit(_REG_MIPI_ERR_VECTOR_L, 5)
    false_ctrl_err = RWBit(_REG_MIPI_ERR_VECTOR_L, 6)
    contention_err = RWBit(_REG_MIPI_ERR_VECTOR_L, 7)
    ecc_single_err = RWBit(_REG_MIPI_ERR_VECTOR_H, 0)
    ecc_multi_err = RWBit(_REG_MIPI_ERR_VECTOR_H, 1)
    crc_err = RWBit(_REG_MIPI_ERR_VECTOR_H, 2)
    ddtnr_err = RWBit(_REG_MIPI_ERR_VECTOR_H, 3)
    dsi_vc_err = RWBit(_REG_MIPI_ERR_VECTOR_H, 4)
    tran_len_err = RWBit(_REG_MIPI_ERR_VECTOR_H, 5)
    #reserved_err = RWBit(_REG_MIPI_ERR_VECTOR_H, 6)
    prot_vio_err = RWBit(_REG_MIPI_ERR_VECTOR_H, 7)

    mipi_max_size = UnaryStruct(_REG_MIPI_MAX_SIZE_L, ">H")

    mipi_line_div_en = RWBit(_REG_DSI_CTRL, 7)
    mipi_bit_swap = RWBit(_REG_DSI_CTRL, 6)
    mipi_crc_en = RWBit(_REG_DSI_CTRL, 5)
    mipi_8B9B_en = RWBit(_REG_DSI_CTRL, 4) #not used by IC according to datasheet
    mipi_video_mode = RWBits(2, _REG_DSI_CTRL, 2) #not used by IC according to datasheet
    mipi_lane_num = RWBits(2, _REG_DSI_CTRL, 0)

    auto_lx_en = RWBit(_REG_MIPI_PN_SWAP, 5)
    mipi_clk_pn_swap = RWBit(_REG_MIPI_PN_SWAP, 4)
    mipi_data_pn_swap = RWBits(4, _REG_MIPI_PN_SWAP, 0)

    mipi_t_term_en = UnaryStruct(_REG_MIPI_T_TERM_EN, ">B")
    mipi_t_hs_settle = UnaryStruct(_REG_MIPI_T_HS_SETTLE, ">B")

    mipi_t_ta_sure_pre = RWBits(5, _REG_MIPI_T_TA_SURE_PRE, 0)
    mipi_t_lpx_set = UnaryStruct(_REG_MIPI_T_LPX_SET, ">B")
    mipi_t_clk_miss = UnaryStruct(_REG_MIPI_T_CLK_MISS, ">B")

    mipi_init_time_l = UnaryStruct(_REG_MIPI_INIT_TIME_L, ">B")
    mipi_init_time_h = RWBits(4, _REG_MIPI_INIT_TIME_H, 0)

    mipi_t_clk_term_en = UnaryStruct(_REG_MIPI_T_CLK_TERM_EN, ">B")
    mipi_t_clk_settle = UnaryStruct(_REG_MIPI_T_CLK_SETTLE, ">B")

    pd_ck_term_force = RWBit(_REG_MIPI_PD_CK_LANE, 7)
    pd_ck_term_value = RWBit(_REG_MIPI_PD_CK_LANE, 6)
    pd_ck_hsrx_force = RWBit(_REG_MIPI_PD_CK_LANE, 5)
    pd_ck_hsrx_value = RWBit(_REG_MIPI_PD_CK_LANE, 4)
    pd_ck_lprx = RWBit(_REG_MIPI_PD_CK_LANE, 3)
    pd_lpcd_force = RWBit(_REG_MIPI_PD_CK_LANE, 2)


    

    def soft_reset(self):
        self.reset = 1

    def save_config(self):
        self.config_finish = 1

    def set_resolution(self, width, height):
        self.hactive_l = width & 0xFF
        self.vactive_l = height & 0xFF
        self.vactive_hactive_h = (width >> 8) | ((height >> 8) << 4)

    def set_horizontal_front_porch(self, value):
        self.hfp_l = value & 0xFF
        self.hfp_h = (value >> 8) << 4

    def set_horizontal_sync_width(self, value):
        self.hsw_l = value & 0xFF
        self.hsw_h = (value >> 8) << 2

    def set_horizontal_back_porch(self, value):
        self.hbp_l = value & 0xFF
        self.hbp_h = (value >> 8) << 0

    def set_vertical_front_porch(self, value):
        self.vfp = value

    def set_vertical_sync_width(self, value):
        self.vsw = value

    def set_vertical_back_porch(self, value):
        self.vbp = value
        
    def set_test_mode(self, mode: BIST_MODE):
        self.bist_mode = mode

    

