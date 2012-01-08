from myhdl import *
import math
import numpy as np
import counter_d
DATA_WIDTH = 18



def RAM(dout,  din,  addr,  we,  clk,  depth):
    """    Ram  model  """
    mem  =  [Signal(intbv(0,min=-2*2**len(dout),max=2*2**len(dout)))  for  i  in  range(depth)]
    #print "%s   %s   " % (addr,din)
    @always(clk.posedge)
    def  bram():
        if  we==1:
            mem[addr].next  =  din

        dout.next  =  mem[addr]
#    print "%s   %s   " % (addr,dout)
    return  bram

def Delay(dout,din,Delay,clk):
    
    """Delay block using
    Single Port RAM"""
    latency = 1
    num_bits = int(np.max((np.ceil(np.log2(Delay)),2)))
    count_to = Delay - latency - 1
    if count_to >= 1:
        count_out = Signal(intbv(0)[num_bits:])
        counter_1 = counter_d(count_out, clk, 1, 0, updown=1,step=1,MIN_COUNT=0,MAX_COUNT=count_to)
        RAM_1 = RAM(Out,data,count_out,1,clk,2**num_bits)
        return counter_1,RAM_1
    else:
        @always(clk.posedge)
        def reglogic():
            dout.next = din
        return reglogic