from myhdl import *
import numpy as np
DATA_WIDTH = 18


def arith_shift(dout,clk,din,shift_num,direction):
    """
    arithmatic shift block
    """
    if direction == 0: # left shift
        @always(clk,din,shift_num)
        def shift_logic():
            dout.next = din<<shift_num
    else: #right shift
        @always(clk,din,shift_num)
        def shift_logic():
            dout.next = din>>shift_num
    return shift_logic