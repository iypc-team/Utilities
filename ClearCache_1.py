# created: 7/22/2022
# updated: 07/26/2022
from __future__ import absolute_import, unicode_literals
from BashColors import C

import gc, glob, json, pip, os, shutil, sys, tarfile
from os.path import *

contentPath=os.getcwd()

class ClearCache(object):
    ''' '''
    def __init__(self):
        print(f"{C.BIGreen}ClearCache{C.ColorOff}")
        self.cc = ClearCache
        self.__all__ = self.getMethodList()
        self.created = 'created: 7/22/2022'
        self.updated = 'updated: 07/26/2022'
        # print(f'{C.BIPurple}{self.updated}{C.ColorOff}')
        self.contentPath = os.getcwd()
        
        self.garbageCollectList = gc.get_objects() 
        # Returns a list of all objects tracked by the collector
        gc.enable() #Enable automatic garbage collection.
        # gc.disable() # Disable automatic garbage collection.
        print(f'gc.isenabled: {C.BIGreen}{gc.isenabled()}{C.ColorOff}')
        # True if automatic collection is enabled.
        gc.collect()
        # gc.collect(generation=2)
        # gc.collect(generation=1)
        # gc.collect(generation=0)
        
        super(object, self).__init__()
        
    def __iter__(self):
        return self
    # def __len__(self):
        # return len(self.name)
    def __str__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
    def __iter__(self):
        for key in self.some_sequence:
            yield (key, 'Value for {}'.format(key))
            
    def getMethodList(self, silent=True):
        '''List all methods in JsonNumpyUtils\n Print silent = True'''
        method_list=[]
        for attribute in dir(self):
            # Get the attribute value
            attribute_value = getattr(self, attribute)
            # Check that it is callable
            if callable(attribute_value):
                # Filter all dunder (__ prefix) methods
                if attribute.startswith('__') == False:
                    method_list.append(attribute)
        if not silent:
            print(f'{len(method_list)} callable methods in JsonNumpyUtils')
            for method in method_list:
                print(method)
        return method_list
    
    def clear_Cache(removeCache=False):
        '''default removeCache=False'''
        globList = glob.glob('**', recursive=True)
        for fil in globList:
            if  fil.endswith('__'):
                full_Path = abspath(fil)
                print(f'{full_Path}{C.ColorOff}')
        if removeCache:
            print(f'removed: {C.BIRed}{full_Path}')
            shutil.rmtree(full_Path)
cc=ClearCache()
