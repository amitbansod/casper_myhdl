from myhdl import *
import fft_stage


def biplex_fft(dataOut_0, dataOut_1, syncOut, of_Out, dataIn_0, dataIn_1, of_In, syncIn, shiftIn, clkIn):
    
    FFTSize = int(4)
    internal_data_signals_0 = [Signal(intbv( 0,min=0, max=2 ** (2 * DATA_WIDTH))) for i in range(FFTSize)]
    
    internal_data_signals_1 =[Signal(intbv( 0,min=0, max=2 ** (2 * DATA_WIDTH))) for i in range(FFTSize)]
    
    internal_sync_signals = [Signal(bool(0)) for i in range(FFTSize)]
    
    internal_of_signals = [Signal(bool(0)) for i in range(FFTSize)]
    
  
    stage_syncIn = []
    stage_of_In = []
    stage_dataIn_0 = []
    stage_dataIn_1 = []

                
    nstage = [None for i in range(FFTSize)]
    for i in range(FFTSize):
        if i == 0:

            nstage[i] = fft_stage.fft_stage(internal_data_signals_0[i], internal_data_signals_1[i], 
                                  internal_sync_signals[i], internal_of_signals[i] , 
                                  dataIn_0, dataIn_1, of_In, syncIn, shiftIn, clkIn, 
                                  FFTSize=FFTSize, FFTStage=(i+1))

            
        elif i == (FFTSize - 1): #last stage

            nstage[i] = fft_stage.fft_stage(dataOut_0, dataOut_1,syncOut, of_Out, 
                                  internal_data_signals_0[i-1], internal_data_signals_1[i-1], 
                                  internal_sync_signals[i-1], internal_of_signals[i-1], shiftIn, 
                                  clkIn, FFTSize=FFTSize, FFTStage=(i+1))

        else:

            nstage[i] = fft_stage.fft_stage(internal_data_signals_0[i], internal_data_signals_1[i], 
                                  internal_sync_signals[i], internal_of_signals[i] , 
                                  internal_data_signals_0[i-1], internal_data_signals_1[i-1], 
                                  internal_sync_signals[i-1], internal_of_signals[i-1], shiftIn, 
                                  clkIn, FFTSize=FFTSize, FFTStage=(i+1))

        
    return  nstage
  
                
    
#dataOut_0, dataOut_1, dataIn_0, dataIn_1 = [Signal(intbv(0, min=0, max=2 ** (2 * DATA_WIDTH))) for i in range(4)]
#syncOut = Signal(bool())
#of_Out = Signal(bool())    
#of_In = Signal(bool(0)) 
#
##FFTSize = Signal(intbv(5))
##FFTSize = Signal(intbv(5)[4:0])
##FFTStage = Signal(intbv(4)) 
#syncIn = Signal(bool(0))
#shiftIn = Signal(intbv(0)[7:0])
#clkIn = Signal(bool())
#
#toVHDL(biplex_fft, dataOut_0, dataOut_1, syncOut, of_Out, dataIn_0, dataIn_1, of_In, syncIn, shiftIn, clkIn)

#def testBench(width):
#    
#    dataOut_0, dataOut_1, dataIn_0, dataIn_1 = [Signal(intbv(0, min=0, max=2 **(2*DATA_WIDTH))) for i in range(4)]
#    syncOut = Signal(bool())
#    of_Out = Signal(bool())    
#    of_In = Signal(bool(0)) 
#    
#    #FFTSize = Signal(intbv(5))
#    #FFTSize = Signal(intbv(5)[4:0])
#    #FFTStage = Signal(intbv(4)) 
#    syncIn = Signal(bool(0))
#    shiftIn = Signal(intbv(0)[4:0])
#    clk = Signal(bool(0)) 
#    
#    of = Signal(bool())
#    sync = Signal(bool(0))
#    shift = Signal(bool(0))
#    clk= Signal(intbv(0))
#    
#    dut = biplex_fft(dataOut_0, dataOut_1, syncOut, of_Out, dataIn_0, dataIn_1, of_In, syncIn, shiftIn, clk)
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
#            
#            if i==0:
#                syncIn.next = 1
#                yield delay(21)
#            syncIn.next = 0
#            dataIn_0.next = i
#            #print"%s datainbiplex=%s %s"%(now(),dataIn_0,i)
#            dataIn_1.next = 0
#            of_In.next = 0
#            shiftIn.next = 0
#        
#            yield delay((10+2**width)*21*2)
#            #syncIn.next = 0
#            #yield delay(21*49)
#            print "%s dataOut_0_Re = %s, dataOut_0_im = %s,dataOut_1_re = %s, dataOut_1_im = %s syncOut = %s,of_Out = %s,  syncIn = %s,  clkIn = %s dataIn_0=%s " % (now(), dataOut_0[DATA_WIDTH:], dataOut_0[2*DATA_WIDTH:DATA_WIDTH+1],dataOut_1[DATA_WIDTH:], dataOut_1[2*DATA_WIDTH:DATA_WIDTH+1], syncOut, of_Out, syncIn, clk,dataIn_0)
#        raise StopSimulation
#    return dut, stimulus, clkgen
#
#sim = Simulation(testBench(width=4))
#sim.run()