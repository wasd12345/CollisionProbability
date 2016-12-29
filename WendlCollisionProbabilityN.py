# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 15:03:57 2016

@author: gk
"""



import numpy as np
from sympy.functions.combinatorial.numbers import stirling
from sympy.functions.combinatorial.factorials import FallingFactorial


def WendlCollisionProbabilityN(cardinalities,T):
    """
    Following article: 
    "Collision Probability Between Sets of Random Variables" by Michael Wendl
    from Statistics & Probability Letters 64(3):249-254 · September 2003
    https://www.researchgate.net/publication/23634894_Collision_Probability_Between_Sets_of_Random_Variables
    
    For a given cardinalities vector, 
    you can calculate the exact collision probability P
    
    
    This function is for the general case of N multisets.
    The function:
    WendlCollisionProbability2
    is specifically for the case of N=2.
    
    """

    
    #The number of multisets
    #N = 2 for this specialized case
    #N = Cardinalities.size
    
    #Cardinalities must be positive integers:
    if ((cardinalities.dtype != int) or (cardinalities.min() < 1)):
        raise Exception('The multiset cardinalities, m and n, must bot be positive integers')

        
    def outerN(*Vs):
        return np.multiply.reduce(np.ix_(*Vs))
    
    def RightProduct(cardinalities,T):
        Z = np.meshgrid(*[np.arange(1,cc+1) for cc in cardinalities],indexing='ij')
        print Z[0].shape
#        s = T - (np.array(Z).sum(axis=0) - 1)
#        print s.shape
        print Z
        print s
        
        #!!!!!!!!!!!!! need to make this sympy fLINGFACTORIAL INTO A UFUNC SO CAN do on multidimensional arrays...
        #http://stackoverflow.com/questions/41112052/python-numpy-product-of-integers-over-some-range
        right = np.array([[FallingFactorial(T,i+j) for j in xrange(1,n+1)] for i in xrange(1,m+1)])
        
        
        
#        print s
#        print s.shape
#        print right
#        print right.shape
        return right


    def LeftProduct(cardinalities):
        Vstirlings = []
        for cc in cardinalities:
            Vstirlings += [np.array([stirling(cc,kk,d=None,kind=2,signed=False) for kk in range(1,cc+1)])]
#        print Vstirlings
        
        left = outerN(*Vstirlings)
        print left.shape
        return left

    #Make meshgrid of for all (i,j) space, used in both LeftProduct and RightProduct
    #x,y = np.meshgrid(np.arange(1,m+1),np.arange(1,n+1))
    #Make meshgrid of repeats of m,n: used for LeftProduct
    #mx,ny = np.meshgrid(np.repeat(m,m),np.repeat(n,n))

    left = LeftProduct(cardinalities)
#    print left
    right = RightProduct(cardinalities,T)
#    print right
    
    #left*right is a 2D array
    num = np.sum(left*right)
    
    #Denominator is just total number of possible graphs
    denom = T**(cardinalities.sum())
    
    #Collision Probability [probability YES there is a collision]:
    #1 - (# of good graphs)/(# of total possible graphs)
    P = 1. - np.float(num)/np.float(denom)
    
    print 'Numerator:'
    print num
    print '\n'
    print 'Denominator:'
    print denom
    print '\n'
    print 'Collision Probability:'
    print P
    
    return P
    
    
    
    
    
    
if __name__ == '__main__':

    cardinalities = np.array([2,3,4,5])
    T=10
    
    WendlCollisionProbabilityN(cardinalities,T)