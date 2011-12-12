#######################################################################
##  readsb.py
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
import csv
def getfname():
    """
    Read input file track_input.csv.
    If this file only has one data line,  the line is automatically read.
    If there are more data lines, the user is asked to choose.
    """
    infile=open("track_input.csv","rb")
    pref=csv.reader(infile)
    header = pref.next()
    filepref=list(pref)
    DataSet=[]
    ha=[]
    hd=[]
    ep=[]
    p1=[]
    for i in range(len(filepref)):
        DataSet.append(str(filepref[i][1])+".csv")
        ha.append(float(filepref[i][2]))
        hd.append(float(filepref[i][3]))
        ep.append(float(filepref[i][4]))        
        p1.append(float(filepref[i][5]))
    if len(DataSet) == 1:
        iwhich = 0
    else :         
        for i in range(len(DataSet)):
            print i, DataSet[i],ha[i],hd[i],p1[i] 
        iwhich = -1
        while iwhich < 0 or iwhich >len(DataSet) :           
            which=raw_input("Enter which dataset: ")
            iwhich = int(which)
    fname=DataSet[iwhich]
    return fname,iwhich,ha[iwhich],hd[iwhich],ep[iwhich],p1[iwhich]
    

class track_data:
    """
    Data from the StreetBump program.
    """
    def __init__(self,filename):
        infile = open(filename, "rU")
        stbumps = csv.reader(infile)
        self.Time=[]
        self.Longitude=[]
        self.Latitude=[]
        self.AccelX=[]
        self.AccelY=[]
        self.AccelZ=[]
        self.OrientX=[]
        self.OrientY=[]
        self.OrientZ=[]
        self.MagneticX=[]
        self.MagneticY=[]
        self.MagneticZ=[]
        self.Bearing=[]
        self.Speed=[]
        self.gpsAccuracy=[]
        self.Entropy=[] 
          
        header = stbumps.next()
        self.header = header
        Datalist=list(stbumps)
        infile.close()
        for i in range(len(Datalist)):
        
           if len(Datalist[i]) > 0 :
   
                self.Time.append(int(Datalist[i][0]))
                self.Longitude.append(float(Datalist[i][1]))
                self.Latitude.append(float(Datalist[i][2]))
                self.AccelX.append(float(Datalist[i][3]))
                self.AccelY.append(float(Datalist[i][4]))
                self.AccelZ.append(float(Datalist[i][5]))
                self.OrientX.append(float(Datalist[i][6]))
                self.OrientY.append(float(Datalist[i][7]))
                self.OrientZ.append(float(Datalist[i][8]))
                self.MagneticX.append(float(Datalist[i][9]))
                self.MagneticY.append(float(Datalist[i][10]))
                self.MagneticZ.append(float(Datalist[i][11]))
                self.Bearing.append(float(Datalist[i][12]))
                self.Speed.append(float(Datalist[i][13]))
                self.gpsAccuracy.append(float(Datalist[i][14]))
                self.Entropy.append(float(Datalist[i][15])) 

                   
def chksame(T,i,j):
    """
    Check to see if records i and j are the same.    
    """
    same =  T.Time[i]       == T.Time[j]  and \
            T.Longitude[i]  == T.Longitude[j]  and \
            T.Latitude[i]   == T.Latitude[j]  and \
            T.AccelX[i]     == T.AccelX[j]  and \
            T.AccelY[i]     == T.AccelY[j]  and \
            T.AccelZ[i]     == T.AccelZ[j]  and \
            T.OrientX[i]    == T.OrientX[j]  and \
            T.OrientY[i]    == T.OrientY[j]  and \
            T.OrientZ[i]    == T.OrientZ[j]  and \
            T.MagneticX[i]  == T.MagneticX[j]  and \
            T.MagneticY[i]  == T.MagneticY[j]  and \
            T.MagneticZ[i]  == T.MagneticZ[j]  and \
            T.Bearing[i]    == T.Bearing[j]  and \
            T.Speed[i]      == T.Speed[j]  and \
            T.gpsAccuracy[i]== T.gpsAccuracy[j]  and \
            T.Entropy[i]    == T.Entropy[j]  
    return same
    
def chksort(t):
    """
    Check if t is sorted.
    """
    nosort = True
    for i in range(len(t)):
        nosort = nosort and t[i] == i
    return nosort 
       
def sorttrack(T):
    """
    Sort with T.Time the track_data T.
    If T is already sorted, the returned value good is set to True, otherwise
    it is set to False.
    """
    from numpy import argsort
    time_sort=argsort(T.Time)
    i0 = time_sort[0]
    time_steps = []
    time_steps.append(0)
    for i in range(1,len(T.Time)):
        i1 = time_sort[i]
        if T.Time[i0] < T.Time[i1] :
            i0 = i1
            time_steps.append(i)
        else :
            same=chksame(T,i0,i1)
            if same == False :
                print 'More than one data set for same time stamp', i0,i1
                
    j0=time_sort[time_steps[0]]
    sumtimedel = 0
    maxtimedel = 0
    mintimedel = 900000
    n5000      = 0           
    for i in range(1,len(time_steps)):
        j1 = time_sort[time_steps[i]]
        timedel = T.Time[j1]-T.Time[j0]
        maxtimedel=max(timedel,maxtimedel)
        mintimedel=min(timedel,mintimedel)
        sumtimedel=sumtimedel+timedel
        if timedel > 5000 :
             n5000 = n5000 + 1
        j0=j1
        
    avgtimedel =  sumtimedel/(len(time_steps)-2) 
    print 'Maximum time step : ',maxtimedel
    print 'Minimum time step : ',mintimedel
    print 'Average time step : ',avgtimedel
    print 'No. of time step > 5000 :', n5000
    
    good = chksort(time_sort) and len(time_steps)==len(T.Time)                      
    
    return time_sort,time_steps, good

    
def rewritecsv_time(fname, T, time_sort, time_steps):
    """
    Rewrite the track_data T according to the output from sorttrack.
    """
    outfile = open(fname,"wb")
    rstbump = csv.writer(outfile)
    rstbump.writerow(T.header)
    for i in range(len(time_steps)):
        j = time_sort[time_steps[i]]
        row = ('%i'%T.Time[j],'%8.8f'%T.Longitude[j],'%8.8f'%T.Latitude[j],T.AccelX[j],T.AccelY[j],T.AccelZ[j],\
               T.OrientX[j],T.OrientY[j],T.OrientZ[j],T.MagneticX[j],T.MagneticY[j],T.MagneticZ[j],\
               T.Bearing[j],T.Speed[j],T.gpsAccuracy[j],T.Entropy[j])
        rstbump.writerow(row)
    outfile.close() 
          
def readTraining(fname):
    """
    Read the pot hole data set (not called by AnStreetBump).
    """
    infile = open(fname,"rb")
    TrData = csv.reader(infile)
    header = TrData.next()
    Trlist = list(TrData)
    setstart = zeros( (5), int)
    holes = zeros( (len(Trlist), 2) )
    iset = 0
    setstart[iset]=0
    for i in range(len(Trlist)):
        set = int(Trlist[i][0]) - 1
        if set > iset :
            iset = iset + 1
            setstart[iset]=int(Trlist[i][2])-1
        holes[i,0]=float(Trlist[i][3])
        holes[i,1]=float(Trlist[i][4])
    setstart[iset+1]=len(Trlist)    
    return setstart, holes   
