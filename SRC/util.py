#######################################################################
##  util.py
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
from numpy import argsort
def sortshrink(T):
    """
    Sort and remove duplicate data.    
    """
    t_sort=argsort(T)
    i0 = t_sort[0]
    ST = []
    for i in range(1,len(T)):
        i1 = t_sort[i]
        if T[i0] < T[i1] :
            ST.append(T[i0])        
            i0 = i1

    ST.append(T[i0])
    return ST      

def OneSecLater(m,dtimek):
    """
    Find the smallest j such that \sum_{k=0}^{k=j} dtime[k] > 1 second.
    """
    d = 0
    j = 0
    while d < 1.0  :
       d += dtimek[m+j]
       j += 1
    return j - 1   
