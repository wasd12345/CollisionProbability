# -*- coding: utf-8 -*-
"""
Created on Fri Dec 02 11:00:32 2016

@author: gk
"""



#COLLISION PROBABILITY SIMULATION


import numpy as np
import matplotlib.pyplot as plt

from WendlCollisionProbability2 import WendlCollisionProbability2
from WendlCollisionProbabilityN import WendlCollisionProbabilityN


class SingleSimulation():

    
    def __init__(self,N,M,K,J,T,Cmax,Cardinalities=None):

        #Attributes used to generate the multisets
        self.N = N
        self.M = M
        self.K = K #Must be 2 or greater or else would always have collision since a multiset would collide with itself
        self.T = T
        self.J = J
        self.Cmax = Cmax
        
        #Attributes that are generated during simulation
        self.Cardinalities = Cardinalities #If this is not None, then this vector will override the self.Cmax value and be used for creating the mutlisets.
        self.Multisets = []
        self.MultiplicityMatrix = np.zeros((self.N,self.T)).astype(np.int)
        
        #Attributes that are calculated after simulation
        self.CollidingElements = None
        self.nCollidingElements = None
        self.Collision = None
        #self.ElementSharingMatrix = np.zeros((self.N,self.N))
        
        print 'N={}'.format(self.N)
        print 'M={}'.format(self.M)
        print 'K={}'.format(self.K)
        print 'J={}'.format(self.J)
        print 'T={}'.format(self.T)
        print 'Cmax={}'.format(self.Cmax)
        
        
            
    def GenerateMultisets(self):
        """
        Randomly create the multisets based on given parameters.
        """

        #If user supplied Cardinalities vector, then use it, otherwise randomly draw:
        if self.Cardinalities != None:
            if self.Cardinalities.size != self.N:
                Exception('Cardinalities vector must be same length as number of multisets')
            self.Cmax = None
        elif self.Cardinalities == None:
            #Generate a vector of multiset cardinalities. Element i of this vector is the cardinality of multiset i.
            self.Cardinalities = np.random.randint(1,self.Cmax,size=self.N)
        
        #For each of the N multisets, generate the elements:
        for i in xrange(self.N):
            #Randomly generate integers on [1,2,...,T]
            multiset = np.sort(np.random.randint(1,T+1,size=self.Cardinalities[i]))#May as well sort to make ordering more obvious and easier to see
            self.Multisets += [multiset] 
            #Update the matrix continaing the multiplicities for each element.
            g = np.bincount(multiset)[1:] #[1:] since 1st element is always number of 0's, which we don't care about since lowest value of t is 1.
            Nels = g.size            
            g = np.pad(g,(0,T-Nels),mode='constant') #Also, unless a given multiset has the max possible value of T as an element(s), then bincount won't count high enough, so pad with zeros
            self.MultiplicityMatrix[i,:] = g
        print 'Multisets:\n', self.Multisets
        print 'Cardinalities:\n', self.Cardinalities
        print 'MultiplicityMatrix:\n', self.MultiplicityMatrix
            
    
    
    def ViewMultisets(self):
        """
        Visualize the multisets.
        Will only look good when the values of N and T are not too large.
        """
        #Grid image for multisets ...
        #Easiest view is just heatmap of the multiplicities of each element
        plt.figure()
        plt.title('Multiplicities',fontsize=30)
        plt.imshow(self.MultiplicityMatrix,interpolation='None',vmin=0)
        plt.xlabel('Element Value',fontsize=20)
        plt.ylabel('Multiset',fontsize=20)
        plt.xticks(np.arange(self.T),np.arange(self.T)+1,fontsize=20)
        plt.yticks(np.arange(self.N),np.arange(self.N)+1,fontsize=20)
        plt.colorbar()#Should only have int scale
        #Overlay multplicity values on grid
        x,y = np.meshgrid(np.arange(T),np.arange(N))
        x = x.flatten()
        y = y.flatten()
        mm = self.MultiplicityMatrix.flatten().astype(np.str)
        for ss in xrange(x.size):
            plt.text(x[ss],y[ss],mm[ss])
            
        #if want discrete colorbar:
        #http://stackoverflow.com/questions/14777066/matplotlib-discrete-colorbar
    
    
    
    def CheckCollision(self):
        """
        For a set of N multisets, check how many collisions there are.
        
        M - int: Element collision criterion number
        
        K - int: Multiset collision criterion number
        
        Multisets - list of length N: list of arrays. Each array is one of the N multisets
        """
        
        #Collision is defined as: There is collision on this set of multisets if:
        #K or more multisets satisfy the "element sharing condition", where 
        #"element sharing condition" is defined as: for at least J of the 
        #possible element values [1,...,T], all of the K multisets have at least 
        #multiplicity M.
        #For example, with the following set of 3 multisets:
        #[1,1,2,2,4,5], [1,1,2,2,5,6], [1,1,5,4,8], [2,5,5,9]
        #with K=3, M=2, J=1:
        #There is a collision on the element 1 since K=3 or greater multisets 
        #(the 1st, 2nd, and 3rd) all have multicplicity M=2 or greater for the
        #value 1. However, there is NOT a collision on the element 2 since only 
        #2 of the multisets (the 1st and 2nd) have multiplicity M=2 or greater 
        #for this value (and since the 4th multiset doesn't have multiplicity 
        #M=2 or greater). The setup as a whole (the set of multisets) is considered 
        #to be in collision since the number of colliding elements is >=J=1. If
        #J had been 2, then the setup would not have been considered to be in 
        #collision since only a single element [1] is in collision.

        valid = self.MultiplicityMatrix>=self.M
        CollisionVector = valid.sum(axis=0)
        #print valid
        #print CollisionVector      
                
        #The actual elements that are in collision
        self.CollidingElements = np.arange(1,T+1)[CollisionVector>=self.K]
        #The number of colliding elements in this set of multisets        
        self.nCollidingElements = self.CollidingElements.size
        
        #True/False: Whether or not this setup is considered to be a collision
        self.Collision = True if self.nCollidingElements>=self.J else False
        
        print 'Colliding Elements:\n', self.CollidingElements
        print '# of Colliding Elements:\n', self.nCollidingElements
        print 'Collision on this setup (T/F):\n', self.Collision
        

        #Binary NxN matrix of whether or not pairs of multisets are considered 
        #to share elements (1 or more). E.g. the (i,j) entry is 0 if multiset i
        #and multiset j do not satisfy the element sharing condition, i.e. they 
        #do not each have multiplicity >=M for some common element (an element
        #in the set intersection).
        #self.ElementSharingMatrix = ...



        
        
        
    def RunSimulation(self):
        self.GenerateMultisets()
        self.ViewMultisets()
        self.CheckCollision()
        
        
    
        
        
        
        
        
        
        
        

        
        
        

        
        
        
        
        
        
        
        
        
if __name__ == '__main__':


    m=142
    n=122
    T=10
    WendlCollisionProbability2(m,n,T)
    
    
#    WendlCollisionProbabilityN
    
    
    
    seed=None
    np.random.seed(seed)

    #Run ensemble of simulations
    Ntrials = 3
    N = 5 #Number of multisets
    M = 2 #Number of elements that must be shared to be counted as a collision
    K = 3 #Number of multisets that must have M
    J = 1 #Number of distinct elements that must satisfy the M,K conditions in order for this setup to be in collision
    T = 10 #number of discrete values the multisets can have
    Cmax = 22 #Max cardinality of the multisets, i.e. each multiset has cardinality anywhere from [1,2,...Cmax]
    Cardinalities=None#np.array([5,5,7,9,8])
    for trial in xrange(Ntrials):
        SS = SingleSimulation(N,M,K,J,T,Cmax,Cardinalities)
        SS.RunSimulation()
        print
        
        
    #Compare to analytical formula from Wendl:
    #This is the special case where:
#    K = 2
#    M = 1
#    WendlCollisionProbability(**)
    K=2
    M=1
