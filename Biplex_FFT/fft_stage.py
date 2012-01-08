from myhdl import *
import butterfly
import sync_delay
import Delay
import slice_m
import slice_mod
import counter_d
import mux_2_1
import math
import numpy as np
DATA_WIDTH = 18

def fft_stage(dataOut_0, dataOut_1, syncOut, of_Out, dataIn_1, dataIn_2, of_In, syncIn, shiftIn, clkIn, FFTSize, FFTStage):
    
    
  
    mux_count = Signal(intbv(0, min=0, max=2**(FFTSize - FFTStage + 2)))
    #StepPeriod = Signal(intbv(0, min=0, max=int((FFTSize - FFTStage + 1))))
    dIn1_m, dIn1_b, dIn2_m, dataIn_2_m = [Signal(intbv(0, min=0, max=2 ** (2 * DATA_WIDTH))) for i in range(4)]
    mux_sel, sync_1,sync_2 = [Signal(bool(0)) for i in range(3)]
    shift, shift_b, ofOut, ofOut_d = [Signal(bool()) for i in range(4)]
    updown = Signal(bool(1))

    
    Coeffs = range(2 ** (FFTStage - 1))
    
#    if FFTStage < 10:
    delay_f = Delay.Delay(dataIn_2_m,dataIn_2,2**(FFTSize - FFTStage),clkIn)
#    else:
#        delay_f = twiddle.Delay_lat(dataIn_2_m, 2**(FFTSize - FFTStage), clkIn, dataIn_2)
    
    
    count_mux = counter_d.counter_d(mux_count, clkIn, 1, syncIn, updown,1, 0, 2**(FFTSize - FFTStage + 2)) #(Nbits=FFTSize-FFTStage+2)
    counter_slice = slice_m.slice_m(mux_sel, clkIn, 2, 0, len(mux_count), mux_count)
    
    mux_1 = mux_2_1.mux_2_1(dIn1_m, clkIn, mux_sel, dataIn_1, dataIn_2_m)
    
##    if FFTStage < 10:
    delay_b = Delay.Delay(dIn1_b,dIn1_m,2**(FFTSize - FFTStage),clkIn)
##    else:
#    delay_b = twiddle.Delay_lat(dIn1_b, 2**(FFTSize - FFTStage), clkIn, dIn1_m)
    
    mux_2 = mux_2_1.mux_2_1(dIn2_m, clkIn, mux_sel, dataIn_2_m, dataIn_1)

    syncdelay2 = sync_delay.sync_delay(sync_2,syncIn,clkIn,DELAY=2**(FFTSize-FFTStage)+1)
    
    shift_slice = slice_mod.slice_mod(shift, clkIn, 2, 2, len(shiftIn), shiftIn)
    
    
    ofOut_delay = Delay.Delay(of_Out, ofOut_d, clk = clkIn,Delay = 1 ) 
    #butterfly_fft(a_plus_bw,a_minus_bw,of_c,sync_out, clk,a,b,sync,shift,FFTSize,StepPeriod,Coeffs, Biplex)
    butterfly_direct = butterfly.butterfly_fft(a_plus_bw=dataOut_0, a_minus_bw=dataOut_1, 
                                               of_c=ofOut, sync_out=syncOut, clk=clkIn, 
                                               a=dIn1_b, b=dIn2_m, sync=sync_2, shift=shift, 
                                               FFTSize=FFTSize, FFTStage=FFTStage,  Coeffs=Coeffs, 
                                               Biplex=True)
    
        
    @always(sync_2,mux_count,mux_sel,dIn1_m, dIn1_b)
    def fftstage_logic():

        ofOut_d.next = of_In or ofOut
    return   shift_slice,  butterfly_direct,fftstage_logic,ofOut_delay,syncdelay2,counter_slice, count_mux ,mux_1, mux_2, delay_f, delay_b