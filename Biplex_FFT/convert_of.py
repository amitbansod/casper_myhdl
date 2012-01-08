from myhdl import *
import math
import slice_mod
import numpy as np


def convert_of(dout,of,clk,din,mode):
    
    """ convert_of block
    din - input
    dout - convert_output
    of - overflow check
    """
    dout_0,dout_1,dout_2,dout_3 = [Signal(bool()) for i in range(4)]
    dout_00,dout_11,dout_22,dout_33 = [Signal(bool()) for i in range(4)]
    nand_0, nand_1, of_0 = [Signal(bool()) for i in range(3)]
	
    stage_of_0 = slice_mod(dout_0, clk, slice_mode = 2,offset = 0, SLICE_WIDTH = len(din), din)
    
    
    stage_of_1 = slice_mod(dout_1, clk, slice_mode = 2, offset = 1,SLICE_WIDTH = len(din), din)
    
    
    stage_of_2 = slice_mod(dout_2, clk, slice_mode = 2, offset = 2,SLICE_WIDTH = len(din), din)
    
    
    stage_of_3 = slice_mod(dout_3, clk, slice_mode = 2,offset = 3,SLICE_WIDTH = len(din), din)
    """@always(din)
    def quantization_logic():
       should be added for fixed point arithmetic"""
       
    @always(din,mode)
    def oveflow_logic():
        
        if mode == 0: #wrap mode
             dout.next = din

        else: #saturate
             dout.next = (2**len(dout) - 1)
        
             
    @always(din,dout_0,dout_1,dout_2,dout_3,dout_00,dout_11,dout_22,dout_33,nand_0,nand_1)
    def convert_of_logic():

        dout_00.next = not dout_0
        dout_11.next = not dout_1
        dout_22.next = not dout_2
        dout_33.next = not dout_3
        nand_0.next = not (dout_0 & dout_1 & dout_2 & dout_3)
        
    @always(dout_00 , dout_11 , dout_22 , dout_33)
    def nand_logic():
        nand_1.next = not (dout_00 & dout_11 & dout_22 & dout_33)
        
    @always(nand_0,nand_1)
    def or_logic():
        of.next = nand_0 & nand_1 

    return stage_of_0, stage_of_1, stage_of_2, stage_of_3, convert_of_logic,nand_logic,or_logic,oveflow_logic 