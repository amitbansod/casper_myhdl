from myhdl import *
import math
import Delay
import numpy as np
DATA_WIDTH = 18

def mux_2_1(dout,clk,sel,d0,d1):
    """
    Multiplexer 2:1
    d0, d1 - inputs
    sel - control input
    dout - output
    """
#    delay_mux = Delay_lat(dout, 2**(FFTSize-FFTStage+1),clk,dout1)
    @always(clk,sel,d0,d1)
    def mux_logic():
        if sel == 0:
            dout.next = d0
        else:
            dout.next = d1
    return mux_logic
	
""" VHDL Generator"""
#toVHDL(mux_2_1,dout,clk,sel,d0,d1)