from myhdl import *
import math
def bit_reverse(list,clk):
    """
    reverses the order of bits in the list
    credit
    """
    N = len(list)
    list = list[:]
    br_indices = range(len(list))

    for i in downrange(len(list)):
        k =0
        b = N>>1
        a = 1
        while b >= a: 
            if b & i: k = k | a 
            if a & i: k = k | b 
            b = b>>1
            a = a<<1
        if i < k: # important not to swap back 
            temp = list[i]
            list[i] = list[k]  
            list[k] = temp
                

    for m in downrange(N):

        br_indices[m] = list[m]
#        print bin(m),bin(br_indices[m])
            
    #br_indices[N-1] = 0
    
    return br_indices
