#######################################################################
##  devices.py
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
from numpy import zeros,argsort
import math
def AdjustAngle(B):
    """
    Make sure angles in B are between -180 and 180.
    """
    for i in range(len(B)):
        if B[i] > 180 :
            B[i] = B[i] - 360.
        if B[i] < -180 :
            B[i] = B[i] + 360   
    return
def GetVectors(T):
    """
    Get vectors from track_data T.
    """
    A      = zeros( (len(T.AccelX), 3) )
    E      = zeros( (len(T.AccelX), 3) )
    O      = zeros( (len(T.AccelX), 3) )
    LaLo   = zeros( (len(T.AccelX), 2) )
    A[:,0] = T.AccelX
    A[:,1] = T.AccelY
    A[:,2] = T.AccelZ
    O[:,0] = T.OrientX
    O[:,1] = T.OrientY
    O[:,2] = T.OrientZ    
    E[:,0] = T.MagneticX 
    E[:,1] = T.MagneticY
    E[:,2] = T.MagneticZ
    B      = T.Bearing    
    LaLo[:,0] = T.Latitude
    LaLo[:,1] = T.Longitude
    AdjustAngle(B)
    AdjustAngle(O[:,0])
    AdjustAngle(O[:,1])
    AdjustAngle(O[:,2])
    return A,E,B,O,LaLo
            
def GetPhoneAngles(OO,B):
    """
    Store the triplets: (O[0] - Bearing, O[1], O[2])
    """
    AllO = zeros( (len(B),3) )
    for i in range(len(B)): 
        O = OO[i,:]*math.pi/180.
        AllO[i,0] = O[0] - B[i]*math.pi/180. 
        if AllO[i,0] > math.pi :
            AllO[i,0] = AllO[i,0] - 2.*math.pi
        if AllO[i,0] < - math.pi :
            AllO[i,0] = AllO[i,0] + 2.*math.pi
        AllO[i,1] = O[1]
        AllO[i,2] = O[2]
    return AllO    

                   
def GetPhoneVectors(T,points):
    """
    Get the time-sorted vectors for the phone
    """
    np   = len(points)
    A    = zeros( (np, 3) )
    E    = zeros( (np, 3) )
    B    = zeros( (np) )
    Time = zeros( (np) )
    ph2o = zeros( (np), int )

    for i in range(np):
        Time[i]=T.Time[points[i]]
        
    ts = argsort(Time)        
    for i in  range(np):
        j = points[ts[i]]
        A[i,0]  = T.AccelX[j]
        A[i,1]  = T.AccelY[j]
        A[i,2]  = T.AccelZ[j]
        E[i,0]  = T.MagneticX[j]
        E[i,1]  = T.MagneticY[j]
        E[i,2]  = T.MagneticZ[j]
        B[i]    = T.Bearing[j]
        Time[i] = T.Time[j]
        ph2o[i]   = j
    return A,E,B,Time,ph2o        

