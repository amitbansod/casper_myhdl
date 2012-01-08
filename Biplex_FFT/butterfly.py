from myhdl import *
import twiddle
import Delay
import math
import mux_2_1
import slice_mod
import arith_shift
import numpy as np
DATA_WIDTH = 18
 
 
  
def butterfly_fft(a_plus_bw,a_minus_bw,of_c,sync_out, clk,a,b,sync,shift,FFTSize,FFTStage,Coeffs, Biplex):
    
    re_1,im_1,re_2,im_2 = [Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH - 1)))) for i in range(4)]
    a_plus_bw1,a_minus_bw1  = [Signal(intbv(0, min=0, max=2**(2*DATA_WIDTH) )) for i in range(2)]
    a_re,a_im,bw_re,bw_im = [Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH-1)))) for i in range(4)]
    d_0,d_1,d_2,d_3 = [Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH-1)))) for i in range(4)]
    d_0s,d_1s,d_2s,d_3s = [Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH-1)))) for i in range(4)]
    din_0,din_1,din_2,din_3 = [Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH-1)))) for i in range(4)]
	
    shift_num = Signal(intbv(1)[np.ceil(np.log2(FFTSize)):])
	
    of1, sync_out1,sync_out11,of_1,of_2,of_3,of_4, sel = [Signal(bool()) for i in range(8)]
	
    add = Signal(bool(1))
    sub = Signal(bool(0))    
    mode = Signal(bool(0))
    
    if FFTStage == 1 :
        twiddle_1 = twiddle.twiddle_0(a_re,a_im,bw_re,bw_im,sync_out11,clk,sync,a,b,Coeffs,FFTSize,FFTStage)
    elif FFTStage == 2:
        twiddle_1 = twiddle.twiddle_1(a_re,a_im,bw_re,bw_im,sync_out11,clk,sync,a,b,Coeffs,FFTSize,FFTStage)
    else:
        twiddle_1 = twiddle.twiddlea(a_re,a_im,bw_re,bw_im,sync_out11,clk,sync,a,b,Coeffs,FFTSize,FFTStage)
    
    AddSub_0 =  twiddle.adder_subtractor_reg(d_0,clk,add,a_re,bw_re)
    AddSub_1 =  twiddle.adder_subtractor_reg(d_1,clk,add,a_im,bw_im)
    AddSub_2 =  twiddle.adder_subtractor_reg(d_2,clk,sub,a_re,bw_re)
    AddSub_3 =  twiddle.adder_subtractor_reg(d_3,clk,sub,a_im,bw_im)
    
    delay_shift = Delay.Delay(sel,shift,1,clk)
    
    arith_0 = arith_shift.arith_shift(d_0s,clk,d_0,shift_num,1)
    arith_1 = arith_shift.arith_shift(d_1s,clk,d_1,shift_num,1)
    arith_2 = arith_shift.arith_shift(d_2s,clk,d_2,shift_num,1)
    arith_3 = arith_shift.arith_shift(d_3s,clk,d_3,shift_num,1)
    
    mux_0 = mux_2_1.mux_2_1(din_0,clk,sel,d_0,d_0s)
    mux_1 = mux_2_1.mux_2_1(din_1,clk,sel,d_1,d_1s)
    mux_2 = mux_2_1.mux_2_1(din_2,clk,sel,d_2,d_2s)
    mux_3 = mux_2_1.mux_2_1(din_3,clk,sel,d_3,d_3s)
    
    convert_of_1 = convert_of.convert_of(re_1,of_1,clk,din_0,mode)
    convert_of_2 = convert_of.convert_of(im_1,of_2,clk,din_1,mode)
    convert_of_3 = convert_of.convert_of(re_2,of_3,clk,din_2,mode)
    convert_of_4 = convert_of.convert_of(im_2,of_4,clk,din_3,mode)
    
    
    concat_0 = twiddle.concat_signed(a_plus_bw1,re_1,im_1,clk)
    concat_1 = twiddle.concat_signed(a_minus_bw1,re_2,im_2,clk)
    
    delay_sync = Delay.Delay(sync_out1,sync_out11,3,clk)
    
    
    @always(clk.posedge)
    def butterfly_logic():
        
#        print"re_1=%s,im_1=%s,re_2=%s,im_2=%s re_1=%s,im_1=%s,re_2=%s,im_2=%s re_1=%s,im_1=%s,
#        re_2=%s,im_2=%s re_1=%s,im_1=%s,re_2=%s,im_2=%s"%(re_1,im_1,re_2,im_2,d_0,d_1,d_2,d_3,
#d_0s,d_1s,d_2s,d_3s,din_0,din_1,din_2,din_3)
        a_plus_bw.next = a_plus_bw1
        a_minus_bw.next = a_minus_bw1
        of_c.next = (of_1 or of_2 or of_3 or of_4)
        sync_out.next = sync_out1

 
#        print"%s a_plus_bw1=%s,a_minus_bw1=%s,bw_re=%s,bw_im=%s,sync_out11=%s"%(now(),a_plus_bw1,a_minus_bw1,bw_re,bw_im,sync_out11)
    return concat_0,concat_1,arith_0,arith_1,arith_2,arith_3,butterfly_logic, AddSub_0, AddSub_1, AddSub_2, AddSub_3, mux_0, mux_1, mux_2, mux_3, convert_of_1, convert_of_2, convert_of_3, convert_of_4, delay_shift,twiddle_1, delay_sync 


#a  = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=2**(DATA_WIDTH - 1)))
#b  = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=2**(DATA_WIDTH - 1)))
#a_plus_bw,a_minus_bw  = [Signal(intbv(0, min=0, max=2**(2*DATA_WIDTH)))for i in range(2)]  
#sync_out = Signal(bool())   
#
#of_c = Signal(bool())
#sync = Signal(bool(0))
#shift = Signal(bool(0))
#clk= Signal(bool())
#
#toVHDL(butterfly_fft, a_plus_bw,a_minus_bw,of_c,sync_out, clk,a,b,sync,shift)
#
#def testBench(width):
#    
#    Coeffs = range(16)
#    
#    a  = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=2**(DATA_WIDTH - 1)))
#    b  = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=2**(DATA_WIDTH - 1)))
#    a_plus_bw,a_minus_bw  = [Signal(intbv(0, min=0, max=2**(2*DATA_WIDTH) ))for i in range(2)]  
#    sync_out = Signal(bool())   
#    
#    of = Signal(bool())
#    sync = Signal(bool(0))
#    shift = Signal(bool(0))
#    clk= Signal(intbv(0))
#    
#    dut = butterfly_fft(a_plus_bw,a_minus_bw,of,sync_out, clk,a,b,sync,shift,4,3,Coeffs, True)
#    #clock generation
#    HALF_PERIOD = delay(10)
#    @always(HALF_PERIOD)
#    def clkgen():
#        clk.next = not clk
#        #print " %s clk = %s fhdsfj" % (now(),clk)
#    @instance
#    def stimulus():
#        print '***************Start TestBench********************'
#        #add_sub = Signal(False)
#        yield clk.posedge
#        for i in range(2**width):
#            a.next = intbv(3)
#            b.next = intbv(0)
#            #yield clk.posedge
#            yield delay(251)
#            print "%s a = %s, b = %s a_plus_bw = %s,a_minus_bw = %s,  of = %s,  sync_out = %s clk = %s" % (now(), a, b, a_plus_bw,a_minus_bw, of,sync_out, clk)
#            #print "%s  d1&d2 = %s d3&d4 = %s,clk = %s" % (now(), concat(im_1,re_1),concat(im_2,re_2), clk)
#        raise StopSimulation
#    return dut, stimulus, clkgen
#
#sim = Simulation(testBench(width=2))
#sim.run()