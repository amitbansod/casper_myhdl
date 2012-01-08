from myhdl import *
import math
import numpy as np
import signed_multiplier
import mux_2_1
#import concat_signed
import signed_adder_subtractor
import complex_multiplier
import Delay
#import ROM
import slice
import slice_m
import bit_reverse
import counter_d
import array
DATA_WIDTH = 18

def twiddle_0(a_re,a_im,bw_re,bw_im,sync_out,clk,sync,a,b,Coeffs,FFTSize,FFTStage):
    
	""" Twiddle block for FFT Stage  = 0
	Twiddle Coeffs = 0
	"""
	#slice(dout, clk, slice_mode,SLICE_WIDTH, din)
    slice_a_re = slice.slice(dout = a_re, clk = clk, slice_mode = 0,SLICE_WIDTH = DATA_WIDTH,din = a)
    slice_a_im = slice.slice(dout = a_im, clk =clk,slice_mode = 1,SLICE_WIDTH = DATA_WIDTH, din = a)
    
    slice_b_re = slice.slice(dout = bw_re, clk = clk, slice_mode = 0, SLICE_WIDTH = DATA_WIDTH, din = b)
    slice_b_im = slice.slice(dout = bw_im, clk = clk, slice_mode = 1, SLICE_WIDTH = DATA_WIDTH, din = b)
    
    @always(clk.posedge)
    def twiddle_0_logic():
        
        sync_out.next = sync

    return slice_a_re,slice_a_im,slice_b_re,slice_b_im,twiddle_0_logic

def twiddle_1(a_re,a_im,bw_re,bw_im,sync_out,clk,sync,a,b,Coeffs,FFTSize,FFTStage):
    
	""" Twiddle Block for FFT Stage = 1
	"""
    a_re1 = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH-1 ))))
    a_im1 = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH-1 ))))
    
    b_re1 = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH-1 ))))
    b_im1 = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH-1 ))))
    b_re11 = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH-1 ))))
    b_im11 = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH-1 ))))
    bb_im11 = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH-1 ))))
	
    sync_cnt = Signal(bool())
    sel = Signal(bool())
	
    count_out = Signal(intbv()[16:])
	
    slice_a_re = slice.slice(dout = a_re1, clk = clk, slice_mode = 0, SLICE_WIDTH = DATA_WIDTH, din = a)
    delay0 = Delay.Delay(dout = a_re, din = a_re1, Delay = 6, clk = clk )
    slice_a_im = slice.slice(dout = a_im1, clk = clk, slice_mode = 1,SLICE_WIDTH = DATA_WIDTH, din = a)
    delay1 = Delay.Delay(dout = a_im, din = a_im1, Delay = 6, clk = clk)
    
    slice_b_re = slice.slice(dout = b_re1, clk = clk, slice_mode = 0, SLICE_WIDH = DATA_WIDTH, din = b)
    delay2 = Delay.Delay(dout = b_re11, din = b_re1, Delay = 2, clk = clk )
    slice_b_im = slice.slice(dout = b_im1, clk = clk, slice_mode = 1, SLICE_MODE = DATA_WIDTH, din = b)
    delay7 = Delay.Delay(dout = b_im11, din = b_im1, Delay = 2, clk = clk )
    
    delay5 = Delay.Delay(dout = sync_cnt, din = sync, Delay = 2, clk = clk )
    counter = counter_d.counter_d(count_out, clk, 1, sync_cnt, 1,1,0,(2**FFTStage - 1))
	#slice_m(dout, clk, slice_mode,offset,SLICE_WIDTH, din)
    slice_cnt = slice_m.slice_m(dout = sel, clk = clk, slice_mode = 2, offset =1,SLICE_WIDTH = 0, din = count_out)
    
    delay6 = Delay.Delay(dout = sync_out, din = sync_cnt, Delay = 4, clk = clk )
	
    @always(clk.posedge)
    def twiddle1_logic():

        bb_im11.next = -1*b_im11
    
    mux0 = mux_2_1(bw_re,clk,sel,b_re11,b_im11)
    mux1 = mux_2_1(bw_im,clk,sel,b_im11,bb_im11) # add output from the negate block
    
    
    return twiddle1_logic,slice_a_re,slice_a_im,slice_b_re,slice_b_im,counter,mux0,mux1,slice_cnt,delay0,delay1,delay2,delay6
    
def twiddlea(a_re,a_im,bw_re,bw_im,sync_out,clk,sync,a,b,Coeffs,FFTSize,FFTStage):

    a_c = Signal(intbv(0, min=0, max=2**(2*DATA_WIDTH)))
    a_re1 = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH-1 ))))
    a_im1 = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH-1 ))))
	
    delay_a = Delay.Delay(dout = a_c, din = a, Delay = 6, clk = clk)
    slice_a_re = slice.slice(dout = a_re, clk = clk, slice_mode = 0, SLICE_WIDTH = DATA_WIDTH, din = a_c)
    slice_a_im = slice.slice(dout = a_im, clk = clk, slice_mode = 1, SLICE_WIDTH = DATA_WIDTH, din = a_c)
    
    b_c = Signal(intbv(0, min=0, max=2**(2*DATA_WIDTH)))
    b_re1 = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH -1))))
    b_im1 = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH -1 ))))
	
    delay_b = Delay.Delay(dout = b_c, din = b, Delay = 2, clk = clk)
    slice_b_re = slice.slice(dout = b_re1, clk = clk, slice_mode = 0, SLICE_WIDTH = DATA_WIDTH, din = b)
    slice_b_im = slice.slice(dout = b_im1, clk = clk, slice_mode = 1, SLICE_WIDTH = DATA_WIDTH, din = b)
    
    delay_sync = Delay.Delay(dout = sync_out, din = sync, Delay = 6, clk = clk)
    
    br_indices = bit_reverse(Coeffs,clk)
    ComplexCoeffs = np.exp(-2*np.pi*1j*np.array(br_indices)/2**FFTSize)
    
   
    w = Signal(intbv(0, min=0, max=2**(2*DATA_WIDTH)))
    w_re = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH -1))))
    w_im = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH -1))))
	
	#coeff_gen(sync, w,clk,CONTENT,FFTSize,FFTStage)
    coeff_gen_1 = coeff_gen.coeff_gen(syncIn = sync, Out = w, clkIn = clk, CONTENT = ComplexCoeffs, FFTSize = FFTSize, FFTStage = FFTStage)
    slice_coeff_gen_1 = slice.slice(dout = w_re, clk = clk, slice_mode = 0, SLICE_WIDTH = DATA_WIDTH, din = w)
    slice_coeff_gen_2 = slice.slice(dout = w_im, clk = clk, slice_mode  = 1, SLICE_WIDTH = DATA_WIDTH, din = w)
    
    bw_re1 = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH -1))))
    bw_im1 = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH -1))))
    mult_0 = signed_multiplier.complex_multiplier_IO_reg(bw_re,bw_im,clk,ena = 1,b_re1,b_im1,w_re,w_im,DATA_WIDTH)
    

    return delay_a, slice_a_re, slice_a_im, delay_b, slice_b_re, slice_b_im, delay_sync,  slice_coeff_gen_1, slice_coeff_gen_2, mult_0, coeff_gen_1,

#def testBench(width):
#    
#    a  = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=2**(DATA_WIDTH - 1)))
#    b  = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=2**(DATA_WIDTH - 1)))
#    a_re,a_im,bw_re,bw_im  = [Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=2**(DATA_WIDTH - 1)))for i in range(4)]  
#    sync_out = Signal(bool())   
#    CONTENT = range(32)
#
#    sync = Signal(bool(0))
#
#    clk= Signal(intbv(0))
#    
#    dut = twiddlea(a_re,a_im,bw_re,bw_im,sync_out,clk,sync,a,b,CONTENT,5,3)
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
#            a.next = intbv(0)
#            b.next = intbv(1)
#           # CONTENT = range(i)
#            #yield clk.posedge
#            yield delay(6*21)
##            print "%s a = %s, b = %s a_re = %s,a_im = %s,  bw_re = %s,bw_im = %s,  sync_out = %s content = %s clk = %s" % (now(), a, b, a_re,a_im,bw_re,bw_im,sync_out, CONTENT,clk)
##            print " %s" % (bw_re)
#        raise StopSimulation
#    return dut, stimulus, clkgen
#
#sim = Simulation(testBench(width=5))
#sim.run()

##a  = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=2**(DATA_WIDTH - 1)))
##b  = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=2**(DATA_WIDTH - 1)))
##a_re,a_im,bw_re,bw_im  = [Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=2**(DATA_WIDTH - 1)))for i in range(4)]  
##sync_out = Signal(bool())   
##CONTENT = (65536,
## 60547,
## 46341,
## 25080,
## 0,
## -25080,
## -46341,
## -60547,
## -65536,
## -60547,
## -46341,
## -25080,
## 0,
## 25080,
## 46341,
## 60547)
##
##sync = Signal(bool(0))
##
##clk= Signal(bool(0))
###CONTENT = (0, 0, 1, 0)
#"""toVHDL(twiddlea,a_re,a_im,bw_re,bw_im,sync_out,clk,sync,a,b,CONTENT)"""
##SLICE_WIDTH = Signal(intbv(0)[8:])
##dout = Signal(intbv(0, min=-2**(18 - 1), max=2**(18 - 1)))
##din = Signal(intbv(0, min=-2**(2*18 - 1), max=2**(2*18 - 1)))
##slice_mode = Signal(intbv(0)[2:])
#
##toVHDL(coeff_gen, sync, w,clk, updown)
