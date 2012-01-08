def slice(dout, clk, slice_mode,SLICE_WIDTH, din):
    """
    slice block
    slice_mode = 0 => range = lower bit + width
    slice mode = 1 => range = upper bit + width
    dout => sliced data
    """
    dtemp = Signal(intbv(0, min=0, max=2**(len(dout))))
    
    
    N = len(din)
    if slice_mode == 0 and N>2:
        @always_comb
        def slice_logic():
            
            dtemp.next = din[SLICE_WIDTH:]
            #print"Ns=%s SLICE_WIDTH=%s din=%s dout=%s"%(N,SLICE_WIDTH,din,dtemp)
    elif slice_mode == 1 and N>2:
        @always_comb
        def slice_logic():
            
            dtemp.next = din[N:N - SLICE_WIDTH]

#                print"Ns=%s SLICE_WIDTH=%s din=%s dout=%s"%(N,SLICE_WIDTH,bin(din),bin(dtemp))
    elif slice_mode == 0 and N<2:
        @always_comb
        def slice_logic():
            dtemp.next = din[SLICE_WIDTH-1]
    else:
        @always_comb
        def slice_logic():
            dtemp.next = din[SLICE_WIDTH]
            #print"Nss=%s SLICE_WIDTH=%s din=%s dout=%s"%(N,SLICE_WIDTH,din,dout)
            
    @always(dtemp)
    def su_logic():
        if int(dtemp) >= 2**(len(dout)-1)-1:
            if dout.min < 0:
                #print"dtemp=%s SLICE_WIDTH=%s len(dout)=%s din=%s dout=%s"%(dtemp,SLICE_WIDTH,len(dout),din,dtemp)
                dout.next = dtemp.signed()
            else:
                dout.next = 2**(len(dout)-1)-1

        else:
            
            dout.next = dtemp
        
    return slice_logic,su_logic
