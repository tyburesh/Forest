"""
Copyright (c) 2017 Eric Shook. All rights reserved.
Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.
@author: eshook (Eric Shook, eshook@gmail.edu)
@contributors: <Contribute and add your name here!>
"""

from .Primitive import *
from ..bobs.Bobs import *

import math
import numpy as np

# FIXME: Instead of making a class for each Primitive type
#        we can make a pop2data wrapper as part of __init__ parameter
#        that way you can create RasterAdd like this:
#        RasterAdd = Primitive(name="RasterAdd",pop2data = np.add)
#        If you have a function that accepts/outputs bobs then you could have
#        BobOutput = Primitive(name="SomePrim",pop2 = function)

class RasterAdd(Primitive):
    def __call__(self):
        # This decorator will wrap the pop2data function around data2
        @pop2data
        def data2(l,r):
            return np.add(l,r)

RasterAdd = RasterAdd()

# Need a wrapper function around object methods unfortunately...
class RasterSub(Primitive):
    def __call__(self):
        # This decorator will wrap the pop2data function around data2
        @pop2data
        def data2(l,r):
            return np.subtract(l,r)

RasterSub = RasterSub()

# Need a wrapper function around object methods unfortunately...
class RasterMul(Primitive):
    def __call__(self):
        # This decorator will wrap the pop2data function around data2
        @pop2data
        def data2(l,r):
            return np.multiply(l,r)

RasterMul = RasterMul()

# Need a wrapper function around object methods unfortunately...
class RasterDiv(Primitive):
    def __call__(self):
        # This decorator will wrap the pop2data function around data2 
        @pop2data
        def data2(l,r):
            return np.divide(l,r)

RasterDiv = RasterDiv()

# Need a wrapper function around object methods unfortunately...
class RasterMin(Primitive):
    def __call__(self):
        # This decorator will wrap the pop2data function around data2 
        @pop2data
        def data2(l,r):
            return np.minimum(l,r)

RasterMin = RasterMin()

# Need a wrapper function around object methods unfortunately...
class RasterMax(Primitive):
    def __call__(self):
        # This decorator will wrap the pop2data function around data2 
        @pop2data
        def data2(l,r):
            return np.maximum(l,r)

RasterMax = RasterMax()

# This lambda function is an unamed function that wraps up an object method.
# This is the only way to make the __add/sub/mul__ overrides work unfortunately.
Raster.__add__ = lambda l,r: RasterAdd.wrap(l,r) 
Raster.__sub__ = lambda l,r: RasterSub.wrap(l,r) 
Raster.__mul__ = lambda l,r: RasterMul.wrap(l,r) 
Raster.__truediv__ = lambda l,r: RasterDiv.wrap(l,r) 

def LocalSum(l,r):
    return RasterAdd.wrap(l,r)
def LocalMinimum(l,r):
    return RasterMin.wrap(l,r)
def LocalMaximum(l,r):
    return RasterMax.wrap(l,r)




## Brown Marmorated Stink Bug Related Raster Primitives


# initialize_grid(MATRIX_SIZE) 
class Initialize_grid(Primitive):
    def __call__(self):
         if not self.size:
             self.size = 4 # By default you get a grid of 4x4

         grid = Raster(h=self.size,w=self.size,nrows=self.size,ncols=self.size)

         # Set seed
         middle_cell = int(self.size/2)
         grid.data[middle_cell][middle_cell] = 1

         #return grid 
         Config.engine.stack.push(grid)

    # Save the size of the grid parameter
    def size(self,size):
         self.size = size
         return self # Must still return self so there is something to call

initialize_grid = Initialize_grid()

# empty_grid() 
class Empty_grid(Primitive):
    def __call__(self):
         if not self.size:
             self.size = 4 # By default you get a grid of 4x4

         grid = Raster(h=self.size,w=self.size,nrows=self.size,ncols=self.size)

         #return grid 
         Config.engine.stack.push(grid)

    # Save the size of the grid parameter
    def size(self,size):
         self.size = size
         return self # Must still return self so there is something to call

empty_grid = Empty_grid()

# initialize_kernel() 
class Initialize_kernel(Primitive):
    def __call__(self):
         if not self.kernel:
             self.kernel = "" # By default you get an empty string 

         # Run kernel stuff
         #kernel = kernel_code.format(MATRIX_SIZE, P_LOCAL, MATRIX_SIZE, P_NON_LOCAL)			# format kernel code w/ constants
	 #mod = SourceModule(kernel)	

         return None 

    # Save the kernel string 
    def kernel(self,kernel):
         self.kernel = kernel 
         return self # Must still return self so there is something to call

initialize_kernel = Initialize_kernel()


# local_diffusion() 
class Local_diffusion(Primitive):
    def __call__(self):

        # This decorator will wrap the pop2data function around diff
        # It will pop off 2 bobs and pass in only the data (GPU'ified arrays)
        # It will push 2 bobs back on as GPU'ified arrays 
        @pop2data2
        def diff(gpu_grid_a,gpu_grid_b):
            # f1 = mod.get_function("local_diffuse")	
            # f1(gpu_grid_a, gpu_grid_b, randoms)	# call kernel function
            gpu_grid_a, gpu_grid_b = gpu_grid_b, gpu_grid_a

            return gpu_grid_a,gpu_grid_b 

local_diffusion = Local_diffusion()

# distance_diffusion() 
class Non_local_diffusion(Primitive):
    def __call__(self):

        # This decorator will wrap the pop2data function around diff
        # It will pop off 2 bobs and pass in only the data (GPU'ified arrays)
        # It will push 2 bobs back on as GPU'ified arrays 
        @pop2data2
        def diff(gpu_grid_a,gpu_grid_b):
            #f2 = mod.get_function("non_local_diffuse")		# non local diffusion function
	    #randoms = random_floats()				# random value between [0,1)
	    #x_coords, y_coords = random_coords()			# random grid coordinates
	    #f2(gpu_grid_a, gpu_grid_b, randoms, x_coords, y_coords)	# call kernel function
            gpu_grid_a, gpu_grid_b = gpu_grid_b, gpu_grid_a         # f1 = mod.get_function("local_diffuse")	

            return gpu_grid_a,gpu_grid_b 

non_local_diffusion = Non_local_diffusion()

# write_grid("output.tif")
# This already exists so it was modified




'''

# RFunct is an extended primitive where you can apply a function
# to the left and right raster layers or just a single raster layer.
class RFunct(Primitive):
    def __init__(self, name, function, buffersize = None):
        # Call Primitive.__init__ as the super class
        super(RFunct,self).__init__(name)
        
        # Reset the name
        self.name = "RFunct "+name
    
        # Set the function to be applied to left and right raster layers
        self.function = function

    # Define the __call__ function which will be called for all RFunct methods.
    def __call__(self, left = None, right = None):

        # Duplicate our left raster for the output # FIXME: Is this right?
        out = Raster(left.y,left.x,left.h,left.w,nrows=left.nrows,ncols=left.ncols)

        # If left and right are set, apply function to left and right
        if left != None and right != None:
            out.data = self.function(left.data,right.data)
        # If only left is set, then apply function to only left 
        elif left != None and right == None: 
            out.data = self.function(left.data)
        else: # This is a problem
            raise
        
        return out


# RMap is an extended primitive where you can apply a function
# to each element of the raster cell
# FIXME: This may need to additional work to make it truly generic
class RMap(Primitive):
    def __init__(self, name, function, buffersize = 0, pass_cellsize = False):
        # Call Primitive.__init__ as the super class
        super(RMap,self).__init__(name)
        
        # Reset the name
        self.name = "RMap "+name
    
        # Set the function to be applied to left and right raster layers
        self.function = function

        # Set the buffersize
        self.buffersize = buffersize
        
        # Determine if cellsize should be passed to the function
        self.pass_cellsize = pass_cellsize
        
    # Define the __call__ function which will be called for all RMap methods.
    # FIXME: I don't think that there is a need for a 'right' here.
    def __call__(self, left = None):

        buffersize = self.buffersize # Local variable for readability
        
        # Duplicate our left raster for the output # FIXME: Is this right?
        out = Raster(left.y,left.x,left.h,left.w,nrows = left.nrows, ncols = left.ncols, cellsize = left.cellsize)

        print("left = ",left)
        print("buffersize = ",buffersize)
        print("function = ",self.function)
        
        if self.pass_cellsize == True:
            for r in range(buffersize,len(out.data)-buffersize):
                for c in range(buffersize,len(out.data[0])-buffersize):
                    # Apply the function to the data in that cell
                    out.data[r][c]=self.function(
                                    left.data[r-buffersize:r + buffersize + 1, 
                                              c-buffersize:c + buffersize + 1], cellsize = left.cellsize)
        else: # Do not pass in cellsize
            # Loop over all the cells in the Raster Bob
            # Make sure to skip the buffered areas
            # Instead of a nested for loop, could we generate the pair of r,c
            # or use itertools.map or something to loop over the data efficiently.
            # nditer multi-indexing is promising: https://docs.scipy.org/doc/numpy-1.13.0/reference/arrays.nditer.html
            for r in range(buffersize,len(out.data)-buffersize):
                for c in range(buffersize,len(out.data[0])-buffersize):
                    # Apply the function to the data in that cell
                    out.data[r][c]=self.function(
                                    left.data[r-buffersize:r + buffersize + 1, 
                                              c-buffersize:c + buffersize + 1])
            
        return out


# Create a number of local primitives for raster data using Raster Function
# using numpy libraries
        
LocalSum =       RFunct("LocalSum",np.add)
LocalSub =       RFunct("LocalSubtract",np.subtract)
LocalMultiply =  RFunct("LocalMultiply",np.multiply)
LocalDivide =    RFunct("LocalDivide",np.divide)
LocalPower =     RFunct("LocalPower",np.power)
LocalMod =       RFunct("LocalModulus",np.mod)
LocalRemainder = RFunct("LocalRemainder",np.remainder)
LocalFloorDivide = RFunct("LocalFloorDivide",np.floor_divide)
LocalMaximum =   RFunct("LocalMaximum",np.maximum)
LocalMinimum =   RFunct("LocalMinimum",np.minimum)



# Create a number of focal operations for raster data using Raster Map
FocalMean =    RMap("FocalMean",np.mean,buffersize=1)
FocalMaximum = RMap("FocalMaximum",np.amax,buffersize=1)
FocalMinimum = RMap("FocalMinimum",np.amin,buffersize=1)



def _Raster_add(self,right):
    return LocalSum(self,right)

def _Raster_sub(self,right):
    return LocalSub(self,right)

def _Raster_div(self,right):
    return LocalDivide(self,right)

def _Raster_mul(self,right):
    return LocalMultiply(self,right)
    
# Overload Raster with new operators
Raster.__add__ = _Raster_add
Raster.__sub__ = _Raster_sub
Raster.__mul__ = _Raster_mul
Raster.__truediv__ = _Raster_div
    


# Create a number of local and focal primitives


# Hillshade method
class HillShadePrim(Primitive):
    def __init__(self):
        # Call Primitive.__init__ as the super class
        super(HillShadePrim,self).__init__("HillShade")
        
    # Define the __call__ function which will be called for hillshade
    def __call__(self, elev = None, altitude=45.0, azimuth=315.0, nodata_value = -999):

        buffersize = 1
        
        # Duplicate our elevation raster for the output
        out = Raster(elev.y,elev.x,elev.h,elev.w,nrows = elev.nrows, ncols = elev.ncols, cellsize = elev.cellsize)

        # Precalculate a few commonly used values
        rtod=0.017453292519943295 # ( pi / 180.0 )
        zenith_rad=(90-altitude)*rtod
        azimuth_rad=(360.0-azimuth+90)*rtod

        cellsize = elev.cellsize
        eight_cellsize = 8*cellsize # Used in the calculations

        for r in range(buffersize,len(out.data)-buffersize):
            # FIXME: Remove, used for testing only
            if r%10 == 0:
                print("r = ",r,"/",len(out.data))
            if r>500:
                break
            for c in range(buffersize,len(out.data[0])-buffersize):
                # Apply the function to the data in that cell
                arr = elev.data[r-buffersize:r + buffersize + 1, 
                                c-buffersize:c + buffersize + 1]

                dzdx=((arr[2][2]+2*arr[1][2]+arr[0][2]) - (arr[2][0]+2*arr[1][0]+arr[0][0])) / (eight_cellsize) # Same as 8*cellsize
                dzdy=((arr[2][0]+2*arr[2][1]+arr[2][2]) - (arr[0][0]+2*arr[0][1]+arr[0][2])) / (eight_cellsize) # Same as 8*cellsize

                aspect=math.atan2(dzdy,-dzdx)
                slope=math.atan( 1 * math.sqrt(dzdx*dzdx + dzdy*dzdy) )

                out.data[r][c] = 255.0 * ( (math.cos(zenith_rad) * math.cos(slope) ) +
                                         (  math.sin(zenith_rad) * math.sin(slope) * math.cos(azimuth_rad-aspect) ) )
            
        return out

HillShade = HillShadePrim()
       
''' 
