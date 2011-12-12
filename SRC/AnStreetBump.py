#######################################################################
##  AnStreetBump.py
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
from readsb import * 
from devices import * 
from gengcell import * 
from holes import * 
if __name__ =="__main__" :

    """
    This program analyze the StreetBump output on Boston streets.
    Around Boston, magnetic N is 15 degrees, 0.26178 radians west of true N.
    One degree Longitude is 69 miles or 111044.74 meters.
    """ 
    

    
    fname,iwhich,hole_accuracy_in_meters,\
    hole_threshold,epsilon,one_phone = getfname()
    T=track_data(fname)
    time_sort,time_steps,good= sorttrack(T)
    if good == False :
        newfile='sorted_'+fname
        rewritecsv_time(newfile, T, time_sort, time_steps)
        print "The data is sorted."
        print "A new file based on the sorted data has been created:", newfile
        T=track_data(newfile)
    print "The input file is ", newfile    
    AA,EE,BB,OO,LaLo = GetVectors(T)
    
    AllO = GetPhoneAngles(OO,BB)
    if one_phone == 1.0:
        Osize = 3 * math.pi
    else :    
        Osize = math.pi/2.
    oeps  = 1.e-4
    
    Dmaxlevel,DLevelC = BinTree(AllO,Osize,oeps,bincut=False)
    Phones = FindClusters(AllO,Dmaxlevel,DLevelC)
    
    Ssize = hole_accuracy_in_meters/111044.74
    seps = 1.e-8
    Smaxlevel,SLevelC = BinTree(LaLo,Ssize,seps,bincut=False)

    holesId=[]
    for i in range( len(Phones) ):
        print "Phone ", i
        C = Phones[i]
        A,E,B, Time,ph2o=GetPhoneVectors(T,C.points)
        sholesId =  StatisticsHoles(A,E,B,Time,ph2o,hole_threshold,epsilon)
        holesId = holesId + sholesId
    print "Total number of pot holes :", len(holesId)     
    pt2c = points2cell(SLevelC,Smaxlevel,LaLo.shape[0])        
    HolesinCells(holesId,pt2c,len(SLevelC[Smaxlevel]),LaLo,fname)
    print "The output file is ",'Solution_'+fname         
