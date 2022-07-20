from __future__ import absolute_import, unicode_literals
from AllInstalls_4 import *
from BashColors import C
from TarfileFunctions import *

from subprocess import check_output, CalledProcessError, STDOUT
import glob, json, os, pprint
try: 
    import numpy
    import numpy as np
except ModuleNotFoundError:
    ai4.getNumpy()
    import numpy
    import numpy as np
from json import JSONEncoder, JSONDecoder, JSONDecodeError
from os.path import *

class Parent(object):
    def __init__(self):
        print(f"{C.BIGreen}Parent{C.ColorOff}")
        self.pp = pprint.PrettyPrinter()
        try: self.created=self.inspectJsonFile(
            'JsonUtilsCreationDate.json')
        except: pass
        self.contentPath = os.getcwd()
        self.jsonFileSet = {'q'}
        self.jsonFileSet.remove('q')
        self.listJsonFiles()
        self.jsonFilesPath=join(self.contentPath, 'jsonFiles')
        if not os.path.exists(self.jsonFilesPath):
            os.makedirs(self.jsonFilesPath)
        self.checksum = self.getCheckSum()
        self.jnu = JsonNumpyUtils
        super(object, self).__init__()
        
    def __iter__(self):
        return self
    def __len__(self):
        return len(self.name)
    def __str__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
    
    def getDateTime(self, silent=True):
        '''Returns date and time string'''
        import time
        secs = time.time()
        secs = secs - (5 * 60 * 60)
        date = time.ctime(secs)
        if not silent:
            print(date)
        return str(date)

    def listJsonFiles(self, silent=True):
        json_files = glob.glob('*.json', recursive = True)
        if len(json_files) !=  0:
            if not silent:
                print('\nJson files...')
            for fil in sorted(json_files):
                fil = os.path.abspath(fil)
                fil = str(fil)
                self.jsonFileSet.add(fil)
                if not silent:
                    print(f'{C.ColorOff}{fil}{C.ColorOff}')
        else: print(f'{C.BIRed}No JSON files exist.{C.ColorOff}')
        return json_files
            
    def createJsonFile(self, name:str, input_data:any):
            ''' '''
            from BashColors import C
            from os.path import join
            # import json
            if not name.endswith('.json'):
                name = name + '.json'
                fullPath=join(self.contentPath, name)
            with open(name, 'w') as f:
                newFile=json.dump(input_data, f, indent='\t')
                print(f'{C.BIGreen}{name}{C.ColorOff} file is created')
                return newFile

    def inspectJsonFile(self, existingPath:str, silent=True):
        ''' '''
        with open(existingPath, 'r') as fil:
            newFile = json.load(fil)
            if not silent:
                self.pp.pprint(newFile)
            return newFile

    def gzipJsonTarFile(self, silent=True):
        '''collects json files and creates a tar.gz file\nsilent=True'''
        # from TarfileFunctions import tarfileFromDirectory, listTarfiles
        import glob, shutil
        jsonGlob=glob.glob('*.json')
        if exists(self.jsonFilesPath): # and isdir(jnu.jsonFilesPath):
            for fil in sorted(jsonGlob):
                fullPath=abspath(fil)
                copyToPath=join(jnu.jsonFilesPath, fil)
                if not silent:
                    print(fil)
                    print(fullPath)
                    print(copyToPath)
                if not exists(copyToPath):
                    shutil.copy2(src=fullPath, dst=copyToPath)
                    print(f'copied: {C.BIGreen}{fil}{C.ColorOff}')
                else: print(f'copied: {C.BIRed}{fil} already exists.{C.ColorOff}')
                # jnu.jsonFileSet.update(fil)

        print(f'creating: {C.BIGreen}JsonFiles.tar.gz{C.ColorOff}')
        tff.tarfileFromDirectory(output_filename='JsonFiles.tar.gz',
                                source_dir=jnu.jsonFilesPath)
        
    def getCheckSum(
        file_path='JsonNumpyUtils.py', compare_to=None, silent=True):
        ''' '''
        # Import hashlib library (md5 method is part of it)
        import hashlib
        # File to check
        file_path = 'JsonNumpyUtils.py'
        # Correct original md5 goes here
        original_md5 = str(compare_to)
        # Open,close, read file and calculate MD5 on its contents 
        with open(file_path, 'rb') as file_to_check:
            # read contents of the file
            data = file_to_check.read()    
            # pipe contents of the file through
            md5_returned = hashlib.md5(data).hexdigest()
            if silent:
                return md5_returned
            elif not silent:
                # print(md5_returned)
                # Finally compare original MD5 with freshly calculated
                if original_md5 == md5_returned:
                    print(f"{C.BIGreen}MD5 verified{C.ColorOff}")
                else: print(f"{C.BIRed}MD5 verification failed!{C.ColorOff}")
                return md5_returned
        
        super(Parent, self).__init__()

class NumpyArrayEncoder(Parent):
    """
    - Serializes python/Numpy objects via customizing json encoder.
    - **Usage**
        - `json.dumps(python_dict, cls=EncodeFromNumpy)` to get json string.
        - `json.dump(*args, cls=EncodeFromNumpy)` to create a file.json.
    """
    def __init__(self):
        print(f"{C.BIGreen}{'NumpyArrayEncoder'}{C.ColorOff}")
        super(NumpyArrayEncoder, self).__init__()
        
    def encodeNumpy(self, obj):
        if isinstance(obj, np.str):
            return str(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyArrayEncoder, self).default(obj)
        

class DecodeToNumpy(Parent):
    """
    - Serializes python/Numpy objects via customizing json encoder.
    - **Usage**
        - `json.dumps(python_dict, cls=EncodeFromNumpy)` to get json string.
        - `json.dump(*args, cls=EncodeFromNumpy)` to create a file.json.
    """
    def __init__(self, *args, **kwargs):
        print(f"{C.BIGreen}DecodeToNumpy{C.ColorOff}")
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
        super(DecodeToNumpy, self).__init__()

    def object_hook(self, obj):
        import numpy
        if '_kind_' not in obj:
            return obj
        kind = obj['_kind_']
        if kind == 'ndarray':
            return numpy.array(obj['_value_'])
        elif kind == 'range':
            value = obj['_value_']
            return range(value[0],value[-1])
        return obj

class JsonNumpyUtils(NumpyArrayEncoder, DecodeToNumpy):
    def __init__(self):
        print(f"{C.BIGreen}JsonNumpyUtils{C.ColorOff}")
        self.__all__ = self.getMethodList()
        self.mro = 'Class Resolution order: JsonNumpyUtils left right Parent'
        super(JsonNumpyUtils, self).__init__()
        
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
    
    def sleepyTime(self):
        from IPython.display import clear_output
        import time
        count=0
        try:
            while count <= 120:
                print(f'sleeping for {count} minutes')
                time.sleep(60)
                count+=1
                if count % 5 == 0:
                    clear_output()
        except KeyboardInterrupt:
            clear_output()
        
jnu=JsonNumpyUtils()
