def counter_d(count_out, clk, ena, rst, updown ,step ,MIN_COUNT = 0,MAX_COUNT ):
    
    
    #limit = Signal(intbv()[(MAX_COUNT):MIN_COUNT])
    limit = int()
    
    if updown == 1:
        limit = MAX_COUNT
    else:
        limit = MIN_COUNT
        
    direction = Signal(bool())
    #updown_1 = updown_d(limit, direction, updown, MIN_COUNT, MAX_COUNT)
    cnt = Signal(intbv(0)[int((len(count_out))):])
    
    @always(clk.posedge)
    def counter_logic():
        
        if rst == 1:
            cnt.next = 0
        elif ena == 1:
            if updown == 1:
                if cnt == limit - 1:
#                    print "resetting",cnt,limit
                    cnt.next = 0
                else:
#                    print "going to add",cnt,step,limit
                    cnt.next = cnt + step
            else:
                if cnt == limit + 1:
                    cnt.next = MAX_COUNT
                else:
                    cnt.next = cnt - step
        count_out.next = cnt   
    return counter_logic