from myhdl import *
import math
import Delay
import numpy as np
DATA_WIDTH = 18

def complex_multiplier(datareg_real, datareg_img, clk, ena, dataa_real, dataa_img, datab_real, datab_img):
    """complex multiplier
    dataa, datab : complex inputs
    dataout: complex outputs
    """
    @always(clk.posedge)
    def comp_mult_logic():
        if ena == 1:
            datareg_real.next = dataa_real * datab_real - dataa_img * datab_img
            datareg_img.next = dataa_real * datab_img + datab_real * dataa_img
    return comp_mult_logic

def complex_multiplier_reg(dataout_real, dataout_img, clk, ena, dataa_real, dataa_img, datab_real, datab_img,DATA_WIDTH):
    
    datareg_real = Signal(intbv(0, min=-2**(2*DATA_WIDTH - 1), max=2**(2*DATA_WIDTH - 1)))
    datareg_img = Signal(intbv(0, min=-2**(2*DATA_WIDTH - 1), max=2**(2*DATA_WIDTH - 1)))

    complex_mult_1 = complex_multiplier(datareg_real, datareg_img, clk, ena, dataa_real, dataa_img, datab_real, datab_img)
    
    @always(clk.posedge)
    def reg_1():
        dataout_real.next = datareg_real
        dataout_img.next = datareg_img
    return complex_mult_1, reg_1
	
"""VHDL Generator"""
#toVHDL(complex_multiplier_reg,dataout_real, dataout_img, clk, ena, dataa_real, dataa_img, datab_real, datab_img,DATA_WIDTH)