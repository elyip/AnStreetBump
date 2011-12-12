#######################################################################
##  gengcell.py
##
## Copyright 2011 Elizabeth Yip
##
## This file is part of AnStreetBump.
##
## AnStreetBump is free software: you can redistribute it and/or modify
## it under the terms of the Lesser GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## AnStreetBump is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## Lesser GNU General Public License for more details.
##
## You should have received a copy of the Lesser GNU General Public License
## long with AnStreetBump.  If not, see <http://www.gnu.org/licenses/>.
##
#######################################################################
from numpy import zeros, ceil, floor, average, argsort 
import math
from util import sortshrink

class gcell:
    """
    self.llc is the 'lower level corner of the cell'
    self.csize is the size.  These are vectors. 
    lind is the index of the cell in the array LEVELC[level][ ... ]
    """

    def __init__(self, level, parent, llc, csize, lind):
        self.level    = level
        self.parent   = parent
        self.llc      = llc
        self.csize    = csize
        self.lind     = lind
        self.adj      = []
        self.points   = []
        self.children = []

def FindCenter(A,points):
    """
    Find the center of A[j,:], where j is in points, a subset of 
    {0,1,..., A.shape[0]-1].
    """
    DA     = zeros( (len(points),A.shape[1] ) )
    center = zeros( (A.shape[1] ) )
    for i in range( len(points) ):
        DA[i,:]=A[points[i],:]
    for i in range(A.shape[1]):
        center[i] = average(DA[:,i])
    return center       
        
class cluster:
    """
    The cluster is defined by the array self.cells for level at self.level.
    """
    def __init__(self,level,cells,A,LevelC):
        self.level  = level
        self.cells  = cells
        self.points = []
        for i in range(len(cells)):
            P = LevelC[level][cells[i]]
            self.points = self.points + P.points
        self.center = FindCenter(A,self.points)        
        
    def UpdateCluster(self,level,cells,A,LevelC):
        self.cells = self.cells + cells
        for i in range(len(cells)):
            P = LevelC[level][cells[i]]
            self.points = self.points + P.points
        self.center = FindCenter(A,self.points)        
            
            
def FindClusters(A,maxlevel,LevelC):
    """
    The first cluster consists of the most populated cell and its neigbors.
    To find the next cluster, look at the cells that has not been picked ... .    
    """
    lp = zeros( (len(LevelC[maxlevel])) ,int)    
    for i in range(len(LevelC[maxlevel])):
        lp[i]= len( LevelC[maxlevel][i].points )
    slp = argsort(lp)
    cls = []
    while sum(lp) > 0 :
        cells = []
        idd = slp[len(slp) - 1]
        P=LevelC[maxlevel][idd]
        for i in P.adj:
            if lp[i] > 0 :
                cells.append(i)
                lp[i] = 0
        cls.append(cluster(maxlevel,cells,A,LevelC)) 
        slp = argsort(lp)               
    return cls
          
def BinaryNdim(ndim):
    """
    returns the vertices of a unit cube of dimension ndim with
    the lower left corner at the origin.
    """
    t = zeros( (2**ndim, ndim) )
    B = 2**ndim
    for i in range(B):
         s = str(bin(B+i))
         ls = len(s)-1
         for j in range(ndim):
            t[i,j]=s[ls - j]
    return t
            
def binaryeval(iv):
    " evaluate a binary number where the digits are stored in iv "
    ind = 0
    for i in range(iv.shape[0]):
        ind = ind + iv[i]*2**i
    return int(ind)    
                
def Branches(P,A,maxlevel,LevelC, asize = -1):
    """
    P is the parent node of the tree, 
    A is input data for the tree
    maxlevel is the 'leave' level of the tree
    LevelC is a list of cells at a certain level
    Default is to cut all sides by half.
    If asize is set, the side is only cut if it is larger than asize.
    """
    if P.level == maxlevel :
        return
        
    ndim  = A.shape[1]
    level = P.level + 1
    csize = zeros( (ndim) )
    if asize < 0 :
        csize = P.csize / 2.
    else :
        for i in range(ndim):
            if P.csize[i] > asize :
                csize[i] = P.csize[i] / 2
            else :
                csize[i] = P.csize[i]    
                    
    llc   = P.llc
    t     = zeros( (2**ndim),int)
    ic    = 0 
    for i in range(len(P.points)) :
        j = P.points[i]
        v = A[j,:] - llc
        iv = floor( v / csize)
        it = binaryeval(iv)
        if t[it] == 0 :
            rv =iv * csize + llc
            parent = P 
            iv = iv * (2**(maxlevel-level))
            lind = len(LevelC[level])
            C = gcell(level, parent, rv, csize, lind)
            LevelC[level].append(C)
            P.children.append(C)     
            ic = ic + 1
            t[it] = ic
        P.children[t[it]-1].points.append(j)

    """
    recursive 
    """         
    for i in range(len(P.children)):
        Branches(P.children[i],A,maxlevel,LevelC) 
        
def GenPjlist(L1,Pi,LevelC):
    """
    L1 is the parent level pf Pi.
    Pj_list is a list of cells at the same level as Pi.  
    Each of these cells either have the same parent as Pi or has parent
    adjacent to the parent of Pi
    """
    Pia = Pi.parent
    Pj_parent=[]
    Pj_parent.append(Pia.lind)
    for i in Pia.adj:
        Pj_parent.append(i)
    Pj_listT = []    
    for i in Pj_parent:
        Pja = LevelC[L1][i]
        for j in Pja.children:
            Pj_listT.append(j.lind)
    Pj_list = sortshrink(Pj_listT)          
    return Pj_list           
    
def Adj(Pi,Pj,TC):
    """
    Test whether Pi and Pj are adjacent
    """
    A = False
    if Pi.parent == Pj.parent :
        A = True
    else:
        Li = list(Pi.llc + TC*Pi.csize)
        Lj = list(Pj.llc + TC*Pj.csize)
        for i in range(len(Li)):
            for j in range(len(Lj)):
                if max(abs(Li[i]-Li[j])) < 1.e-6 :
                    A=True
                    return

            
    return A    
    
             
def Adjacency(LevelC,maxlevel,TC):
    """
    Generate the adjacency list for all the levels.
    When considering cell Pi, only look at Pj such that either Pi and Pj have
    the same parent, or their parents are adjacent.
    """

    P = LevelC[0][0]
    P.adj.append(0)
    for i in range(len(P.children)):
        Li = P.children[i].lind
        for j in range(i+1,len(P.children)): 
            Lj = P.children[j].lind
            P.children[i].adj.append(Lj)
            P.children[j].adj.append(Li)
           
    for L in range(2,maxlevel+1):
        L1 = L - 1
        for i in range(len(LevelC[L])):
            Pi = LevelC[L][i]
            Pj_list = GenPjlist(L1,Pi,LevelC)
            for j in Pj_list :
                Pj = LevelC[L][j]
                if Adj(Pi,Pj,TC) :
                    Pi.adj.append(j)
                    

def BinTree(A,asize,eps,bincut=True):
    """
    Generalized Binary Tree
    """
    ndim = A.shape[1]
    TC = BinaryNdim(ndim)
    csize = zeros( (ndim) )
    llc   = zeros( (ndim) )
    
    for i in range(ndim):
        llc[i] =  min(A[:,i]) - eps
        csize[i] = max(A[:,i]) + eps - llc[i]
        
    npart = max(max(csize)/asize,1) 
    maxlevel = int(ceil(math.log(npart,2))) 
    LevelC=[]
    for i in range(maxlevel+1):
        LevelC.append(i)
        LevelC[i] = []
        level = 0
        
    parent = None
    lind = 0
    P = gcell(level, parent, llc, csize, lind)
    for i in range(A.shape[0]):
        P.points.append(i)
            
    LevelC[0].append(P) 
       
    if bincut :
        Branches(P,A,maxlevel,LevelC)
    else :
        Branches(P,A,maxlevel,LevelC,asize)
        
    Adjacency(LevelC,maxlevel,TC)
    
    return maxlevel,LevelC
           
def points2cell(LevelC,level,N):
    """
    Return the bin number which the point reside
    """
    pt2c= zeros( (N), int)
    for i in range( len(LevelC[level]) ):
        P = LevelC[level][i]
        for j in range( len(P.points) ):
            k = P.points[j]
            pt2c[k] = i
    return pt2c                                   
