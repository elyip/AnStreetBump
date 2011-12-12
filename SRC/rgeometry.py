#######################################################################
##  rgeometry.py
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
from numpy import *
import math
   
def Rz(ra):
    """
    Rotation matrix around Z-axis.
    """
    R = zeros( (3,3) )
    R[0,0]= math.cos(ra)
    R[0,1]=-math.sin(ra)
    R[1,0]= math.sin(ra)
    R[1,1]= math.cos(ra)
    R[2,2]= 1.
    return R

def RzO(ra):
    """
    Inverse of Rz.
    """
    return Rz(-ra)
            
def Rx(ra): 
    """
    Rotation matrix around x axis.
    """    
    R = zeros( (3,3) )
    R[1,1] = math.cos(ra)
    R[1,2] =-math.sin(ra)
    R[2,1] = math.sin(ra)
    R[2,2] = math.cos(ra)
    R[0,0] = 1.
    return R

def RxO(ra):
    """
    Inverse of Rx.
    """
    return Rx(-ra)
            
def Ry(ra):
    """
    Rotation matrix around y axis.
    """    

    R = zeros( (3,3) )
    R[0,0]= math.cos(ra)
    R[0,2]= math.sin(ra)
    R[2,0]=-math.sin(ra)
    R[2,2]= math.cos(ra)
    R[1,1]= 1.
    return R
    
def RotationMatrix(A,E):
    """
    Ported from Android's SensorManager.java.
    Maps phone coordinates to magnatic coordinates:    
    A is gravity
    E is geomagetic field
    World coodirinates System:
    Y is magnetic north
    Z is perpendicular to the ground
    X = cross(Y,Z)
    """    
    R=zeros( (3,3) )
    H=cross(E,A)
    nA=linalg.norm(A)
    nH=linalg.norm(H)
    An=A/nA
    Hn=H/nH

    M=cross(An,Hn)
    R[0,:]=Hn
    R[1,:]=M
    R[2,:]=An
    return R
    
def GetOrientation(R):
    """
    Ported from Android's SensorManager.java
    Return rotations around Z,X,Y axes in the following cooordinate system:
    Y is the same as the magnetic coordinates system
    X is -X of the world coordinate system
    Z is -Z of the world coordinate system    
    R = RzO(O[0])*RxO(O[1])*Ry(O[2])        
    """
    O=zeros( (3) )
    O[0]=math.atan2( R[0,1],R[1,1])
    O[1]=math.asin (-R[2,1])
    O[2]=math.atan2(-R[2,0],R[2,2])
    return O    

def GetOrientation0(R):
    """
    Get O[0] of GetOrientation.
    """
    return math.atan2( R[0,1],R[1,1])

def PitchRoll(A):
    """
    Get O[1] and O[2] of GetOrientation.
    """

    nA = linalg.norm(A) 
    R = A/nA
    pitch = math.asin (-R[1])
    roll  = math.atan2(-R[0],R[2]) 
    return pitch,roll  
       
def Orientation2RotationMatrix(O):
    """
    Compute Rotation matrix from rotation angles.
    """
    return dot(  RzO(O[0]),  dot(RxO(O[1]) ,Ry(O[2])) )
