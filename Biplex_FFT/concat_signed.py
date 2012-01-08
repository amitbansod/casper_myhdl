from myhdl import *
import math
import Delay
import numpy as np
DATA_WIDTH = 18

def concat_signed(dout,lsb,msb,clk):
    """
    concats two signed signals
	lsb,msb - inputs
    """
    #print "%s re = %s im = %s  w = %s %s" % (now(), lsb,msb,dout,clk)
    @always(lsb,msb,clk)
    def concat_logic():
        
        for i in range(DATA_WIDTH):
            
            dout.next[DATA_WIDTH+i] = msb[i]
            dout.next[i] = lsb[i]
    return concat_logic
	
""" VHDL Generator"""
#toVHDL(concat_signed,dout,lsb,msb,clk)