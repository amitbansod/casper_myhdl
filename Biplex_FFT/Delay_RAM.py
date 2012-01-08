def Delay_lat(dout,latency,clk,din): 
	""" Delay Block using RAM
	din - data to be delayed
	latency - delay value
	dout - output
	"""
    count_delay = Signal(intbv(0,min=0, max = latency+1))

    mem  =  [Signal(intbv(min = -2*2**(len(din)-1),max = 2*2**(len(din)-1)))  for  i  in  range(latency)]
       

    @always(clk.posedge)
    def dlogic():
        if count_delay < latency-1:
            mem[count_delay].next = din
            count_delay.next = count_delay + 1
        else:
            dout.next = mem[0]
            count_delay.next = 0
    
    return dlogic
   
def RAM(dout,  din,  addr,  we,  clk,  depth):
    """    Ram  model  """
    mem  =  [Signal(intbv(0)[len(din):])  for  i  in  range(depth)]
    
    @always(clk.posedge)
    def  dram():
        if  we==1:
            mem[addr].next  =  din
        else:

            dout.next  =  mem[addr]

    return  dram