

def slice_m(dout, clk, slice_mode,offset,SLICE_WIDTH, din):
    """
    slice block
    slice_mode = 0 => range = lower bit + width
    slice mode = 1 => range = upper bit + width
    slice mode = 2 => boolian output
    dout => sliced data
    """
    N = len(din)
    if slice_mode == 0:
        @always_comb
        def slice_logic():
            dout.next = (din[N//2:].signed())
    elif slice_mode == 1:
        @always_comb
        def slice_logic():
            dout.next = (din[N:N//2].signed())
    else:
        @always_comb
        def slice_logic():
            dout.next = bool(din[(N - offset - 1)])
    return slice_logic