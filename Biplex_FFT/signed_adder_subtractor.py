from myhdl import *
import math
import Delay
import numpy as np
DATA_WIDTH = 18

def signed_adder_subtractor(resultreg,add_sub,a,b):
    """ Signed Adder and Subtractor
    a, b : inputs
    add_sub: adder = 1 , subtractor = 0
    result : output,
	Full precision or convert options
    """

    @always(a,b,add_sub)
    def add_sub_logic():
        if add_sub == 1:

            resultreg.next = a + b 
        else:

            resultreg.next = a - b

    return add_sub_logic

def adder_subtractor_reg(result,clk,add_sub,a,b):
    N = len(result)
    resultreg = Signal(intbv(0, min=-2*(2**(len(a) - 1)), max=2*(2**(len(b)-1 ))))
    sign_addsub_1 = signed_adder_subtractor(resultreg,add_sub,a,b)
    @always(clk.posedge)
    def reg_2():    
        result.next = resultreg[N:].signed()
    return sign_addsub_1, reg_2
	
"""VHDL Generator"""
# toVHDL(adder_subtractor_reg,result,clk,add_sub,a,b)