import from myhdl *
import ROM
import concat_signed
import numpy as np
def coeff_gen(syncIn, Out,clkIn,CONTENT,FFTSize,FFTStage):
    

    w1 = Signal(intbv(0)[FFTStage:])
    re = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH-1 ))))
    im = Signal(intbv(0, min=-2**(DATA_WIDTH - 1), max=(2**(DATA_WIDTH-1 ))))
	
	count_out = Signal(intbv()[FFTSize:])
    updown2 = 1
    counter_1 = counter_d.counter_d(count_out, clkIn, 1, syncIn, updown2,1, 0, 2**FFTStage)
    slice_1 = slice.slice(dout = w1, clk = clkIn, slice_mode = 1, SLICE_WIDTH = FFTStage, din = count_out)
    
    real_coeffs = np.round(CONTENT.real*2**(DATA_WIDTH-2)).astype('int')
    imag_coeffs = np.round(CONTENT.imag*2**(DATA_WIDTH-2)).astype('int')

    realContent = tuple(real_coeffs)
    imagContent = tuple(imag_coeffs )

    ROM_1 = ROM.ROM(dout = re, addr = w1, CONTENT = realContent)
    ROM_2 = ROM.ROM(dout = im, addr = w1, CONTENT = imagContent)

    concat_2 = concat_signed.concat_signed(dout = Out, lsb= re, msb = im, clk = clkIn)

        
    return  ROM_1, ROM_2,concat_2 ,counter_1, slice_1 #, coeff