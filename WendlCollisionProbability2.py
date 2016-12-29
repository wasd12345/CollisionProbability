# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 13:24:57 2016

@author: gk
"""



import numpy as np
from sympy.functions.combinatorial.numbers import stirling
from sympy.functions.combinatorial.factorials import FallingFactorial


def WendlCollisionProbability2(m,n,T):
    """
    Following article: 
    "Collision Probability Between Sets of Random Variables" by Michael Wendl
    from Statistics & Probability Letters 64(3):249-254 · September 2003
    https://www.researchgate.net/publication/23634894_Collision_Probability_Between_Sets_of_Random_Variables
    
    For a given pair of cardinalities m and n, 
    you can calculate the exact collision probability P
    
    
    This function is for the specific case of 2 multisets.
    For the general case of N multisets, use:
    WendlCollisionProbabilityN
    """

    
    #The number of multisets
    #N = 2 for this specialized case
    #N = Cardinalities.size
    
    #m,n must both be positive integers:
    if ((type(m)!=int) or (type(n)!=int) or (m<1) or (n<1)):
        raise Exception('The multiset cardinalities, m and n, must bot be positive integers')

        
    
    
    def RightProduct(m,n,T):
        x,y = np.meshgrid(np.arange(1,n+1),np.arange(1,m+1))
        s = T - (x + y - 1)
        #right = np.array([[np.prod(np.arange(s[i,j],T+1).clip(1)) for j in xrange(n)] for i in xrange(m)])
#        right1 = np.array([[np.prod(np.arange(s[i,j],T+1)) for j in xrange(n)] for i in xrange(m)])
#        right2 = np.array([[np.prod(np.arange(s[i,j],T+1).astype(np.int64)) for j in xrange(n)] for i in xrange(m)])
        
        #using sympy
        #FallingFactorial(T,i+j) means T*(T-1)*(T-2)...*(T-i-j+1), i.e. the product of i+j terms
        right = np.array([[FallingFactorial(T,i+j) for j in xrange(1,n+1)] for i in xrange(1,m+1)])

        
#        print np.argmin(right1),right1[10] 
#        print np.argmin(right2),right2[10] 
#        print np.argmin(right),right[10] 

#        print right1 
#        print right
#        print s
#        print s.shape
#        print right.shape
        return right


    def LeftProduct(m,n):
        A = np.array([stirling(m,kk,d=None,kind=2,signed=False) for kk in range(1,m+1)])
        B = np.array([stirling(n,kk,d=None,kind=2,signed=False) for kk in range(1,n+1)])
#        print A
#        print B
        left = np.outer(A,B) #is m x n array
#        print left
        return left

    #Make meshgrid of for all (i,j) space, used in both LeftProduct and RightProduct
    #x,y = np.meshgrid(np.arange(1,m+1),np.arange(1,n+1))
    #Make meshgrid of repeats of m,n: used for LeftProduct
    #mx,ny = np.meshgrid(np.repeat(m,m),np.repeat(n,n))

    left = LeftProduct(m,n)
#    print left
    right = RightProduct(m,n,T)
#    print right
    
    #left*right is a 2D array
    num = np.sum(left*right)
    
    #Denominator is just total number of possible graphs
    denom = T**(m+n)#T**(Cardinalities.sum())
    
    print '#non-colliding:'
    print num
    print '\n'
    print '#total:'
    print denom
    print '\n'
    
    
    #Collision Probability [probability YES there is a collision]:
    #1 - (# of good graphs)/(# of total possible graphs)
    try:
        P = 1. - np.float(num)/np.float(denom)
        print 'Collision Probability:'
        print P
    except:
        P = 1. - ApproximateDivision(num,denom)
        print 'APPROXIMATE Collision Probability:'
        print P

    return P
    
    
  





def ApproximateDivision(num,denom):
    """
    When the numbers are large, the sympy integers have so many digits that 
    numpy cannot divide them to get a float.
    
    Instead, get the approximate ratio by:
    1) seeing how many digits each number is
    2) truncating both numbers after N digits and treating all remaining 
    digits as 0's
    3) dividing (truncated numerator) / (truncated denominator)
    4) finally multiplying by 10^D, where D = (# right digits cut off from 
    numerator  -  # right digits cut off from denominator)
    
    Result is a number that is approximately correct
    """
    
    pass


    
    
    
if __name__ == '__main__':

    m=61
    n=63
    T=150
    
    WendlCollisionProbability2(m,n,T)