#######################################################################
##  holes.py
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
from sigma import *
from util import OneSecLater
import csv
def ndsigmaz(dAp,Ap,nd,epsilon,dtimek,ph2o):
    """
    Return array of indices for entries where 
    AccelZ is greater than nd standard deviations and
    where pot holes are indicated.
    """
    signdz=[]
    mindk = 1.e14
    maxdk = 0.
    m = 0
    typ = [0,0]
    while m < Ap.shape[0] - 1:
        if  dAp[m,2] > nd   :
            t,s, ty =PotHole(Ap,dAp,dtimek,m,nd,epsilon )
            if t >= 0:
                j = OneSecLater(t,dtimek)  
                
                k=ph2o[t+j]    
                signdz.append( (k,s) )
                typ[ty] += 1
            mindk = min(mindk,dtimek[m])
            maxdk = max(mindk,dtimek[m])
                    
        m = m + 1     
    print "No. of pot holes:", len(signdz)        
    print "minimum and maximium time step of holes: ",mindk,maxdk
    print "Number of Type 0 pot holes:", typ[0]
    print "Number of Type 1 pot holes:", typ[1]         
    return signdz
    
    
def PotHole(Ap,dAp,dtimek,m,nd,epsilon ):
    """
    dAp[m] > nd.
    If the time steps surrrounding m are less than 1 second, try to
    determin whether it is a pot hole.  Type 0
    Otherwise, we don't have enough information to determin whether it is 
    a pot hole or speed bump.  We report it as a pot hole. Type 1
    
    Return t,s,ty.
    t = -1, not a pot hole
    s = severity
    ty = type of pot hole.    
    """
    if dtimek[m-1] > 1.0 or dtimek[m] > 1.0 or dtimek[m+1] >1.0 :
        t = m
        s = dAp[m,2]
        ty = 1
    else :
        t = -1
        s = 0.
        ty = 1    
        if Ap[m,2] > 0. :
           if Ap[m-2,2]  > -epsilon and Ap[m-1,2] < 0 and dAp[m+1,2] < nd :     
                t=m-1
                s=dAp[m-1,2]+dAp[m,2]
                ty = 1     
        else :           
           if  Ap[m+2,2]  < epsilon and Ap[m+1,2] > 0 and dAp[m-1,2] < nd :
                t = m
                s = dAp[m,2]+dAp[m+1,2] 
                if dAp[m+1,2] > nd:
                    m = m + 1
           ty = 0
                    
    return t,s, ty                

def StatisticsHoles(A,E,B,Time,ph2o,nstd,epsilon):
    """
    For each phone:
    Compute car coordinates relative to the phone coordinates.
    Use basic statistics to find the pot holes.
    """
    dtimek = (Time[1:] - Time[0:len(Time)-1])/1000.
    findholes = []
    Rput, gravity,O=getRput(A,E,B,dtimek)
    print "Gravity Vector :", gravity
    print "Rput Matrix:"
    print Rput
    print "Phone Orientation in car: ", O*180/math.pi
    Ap,sigma,dAp = getSigma(Rput,A,gravity)
    findholes = findholes + ndsigmaz(dAp,Ap,nstd,epsilon,dtimek,ph2o)
    return findholes
 
def HolesinCells(holesId,pt2c,N,LaLo,fname):
    """
    Check the bins where pot holes are reported.  Take the average for each bin.
    This means only one pot hole is reported per bin.
    """
    hl=[]    
    for i in range(N):
        hl.append(i)
        hl[i]=[]
    for i in range(len(holesId)):
        k = holesId[i][0]
        j = pt2c[k]
        hl[j].append(i)
        
    outfile = open('Solution_'+fname,'wb')
    wstbump = csv.writer(outfile)
    wstbump.writerow(('longitude', 'latitude', 'severity'))

    for i in range(N):
        h=[0,0]
        s=0
        if len(hl[i]) > 0:
            for j in range(len(hl[i])):
                k  = hl[i][j]
                m  = holesId[k][0]
                h += LaLo[m]
                s += holesId[k][1]
            h[0]  = h[0] / len(hl[i])
            h[1]  = h[1] / len(hl[i])
            s     =    s / len(hl[i])
            row = ('%8.6f'%h[1],'%8.6f'%h[0],"%i"%s)
            wstbump.writerow(row)
    outfile.close()     
    return                   
   
