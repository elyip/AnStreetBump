#######################################################################
##  sigma.py
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
from numpy import zeros
from rgeometry import *

def getGravity(A,dtime):
    """
    Obtain the gravity vector from the weighted acclerometer vectors. 
    """
    gravity = zeros( (A.shape[1]) )  
    for j in range(A.shape[1]) :
        for i in range(1,A.shape[0]):
              gravity[j]=gravity[j] + 0.5*(A[i-1,j]+A[i,j])*dtime[i-1]
    gravity = gravity/sum(dtime)          
    return gravity
    
def getRput(A,E,B,dtime):
    """
    Generate Rput matrix.
    Rput is the rotation matrix that translate phone coordinates to
    car coordinates.
    """

    O       = zeros( (3) )
    O0B     = zeros( (len(B) ) )
    xy      = zeros( (len(B),2 ) )

    
    gravity = getGravity(A,dtime)
    
    for i in range(len(B)):
        R = RotationMatrix(gravity,E[i,:])
        O0B[i] =  GetOrientation0(R) - B[i]*math.pi/180 
        xy[i,0]= math.cos(O0B[i])
        xy[i,1]= math.sin(O0B[i])
    ca = average(xy[:,0])
    sa = average(xy[:,1])
    oa = math.atan2(sa,ca)
    O[0] = 75*math.pi/180 + oa
    O[1],O[2] = PitchRoll(gravity)
    
    Rput = Orientation2RotationMatrix(O)
    return Rput,gravity,O
       
def getSigma(Rput,A,gravity):
    """
    Compute :
    Ap = Rput(A - gravity).
    sigma is the standard deviation of Ap.
    dAp[i,j] is the number of standard deviation at [i,j].
    """   
    Ap  = zeros( (A.shape) )
    dAp = zeros( (A.shape) )
    sigma = zeros( (3) )
    for i in range(A.shape[0]):
        Ap[i,:] = dot(Rput, A[i,:] - gravity)
        for j in range( 3 ):
            sigma[j] = sigma[j] + Ap[i,j]**2
    for j in range( 3 ):
        sigma[j] = math.sqrt(sigma[j]/A.shape[0])
    for i in range(A.shape[0]):
        for j in range (3) :
            dAp[i,j]= abs(Ap[i,j])/sigma[j]         
    return Ap,sigma,dAp

