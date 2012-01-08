from myhdl import *
import numpy as np
DATA_WIDTH = 18

def slice_mod(dout, clk, slice_mode,offset,SLICE_WIDTH, din):
    """
    slice block
    slice_mode = 0 => range = lower bit + width
    slice mode = 1 => range = upper bit + width
    slice mode = 2 => boolian output
    dout => sliced data
    """
    
    if slice_mode ==0:
        @always(clk, din)
        def slice_logic():
            dout.next = din[SLICE_WIDTH//2:].signed()
    elif slice_mode == 1:
        @always(clk, din)
        def slice_logic():
            dout.next = din[SLICE_WIDTH:SLICE_WIDTH//2].signed()
    else:
        @always(clk, din)
        def slice_logic():
            dout.next = bool(din[(SLICE_WIDTH - offset - 1)])
    return slice_logic