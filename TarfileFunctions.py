from __future__ import absolute_import
from IPython.display import clear_output
from BashColors import C
import glob, os, shutil, tarfile
from os.path import abspath

class TarfileFunctions(object):
    # from IPython.display import clear_output
    # from BashColors import C
    # import glob, os, shutil, tarfile
    # from os.path import abspath
    
    def __init__(self):
        print(f"{C.BIGreen}AllInstalls4{C.ColorOff}")
        self.__all__ = self.getMethodList()
        self.contentPath = os.getcwd()
        
        self.tff = TarfileFunctions
        self.tarfileList=[]
        self.tarfilePathList=[]
        super(object, self).__init__()

    def __iter__(self):
        return self
    def __len__(self):
        return len(self.name)
    def __str__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
    
    def getMethodList(self, silent=True):
        '''List all methods in AllInstalls4\n Print silent = True'''
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
            print(f'{len(method_list)} callable methods in AllInstalls4')
            for method in method_list:
                print(method)
        return method_list
    
    def listTarfiles(self):
        '''List all local tar files'''
        print(f'Available tar files:')
        tarfile_list = glob.glob('**', recursive=True)
        for fil in sorted(tarfile_list):
            if fil.endswith('.gz'):
                fil=os.path.basename(fil)
                fullPth = os.path.abspath(fil)
                print(f'{C.IPurple}{fil}{C.ColorOff}')
                print(f'{C.Green}{fullPth}{C.ColorOff}\n')
                self.tarfileList.append(fil)
                self.tarfilePathList.append(fullPth)
            
    def tarfileFromDirectory(self, output_filename, source_dir):
        '''creates new tar file from given directory'''
        if not output_filename.endswith('.tar.gz'):
            print(f'{output_filename} must endwith .tar.gz')
            return '.tar.gz'
        print(source_dir)
        print(os.path.basename(source_dir))
        with tarfile.open(output_filename, "w:gz") as tar:
            # pass
            tar.add(source_dir, arcname=os.path.basename(source_dir))

    def extractTarfile(self, fileName):
        '''Extracts single tar file'''
        fil=os.path.basename(fileName)
        print(f'extracting: {fil}')
        tar = tarfile.open(fil, 'r:gz')
        tar.extractall()
        tar.close()

    def inspectTarfile(self, named):
        '''Open tar file for inspection'''
        named=str(named)
        named=os.path.basename(named)
        print(named)
        tar = tarfile.open(named, "r:gz")
        for tarinfo in tar:
            print(f'{C.IPurple}{tarinfo.name}{C.ColorOff}')
            print('type:', tarinfo.type)
            print('chksum:', tarinfo.chksum)
            print('size:', tarinfo.size)
            print()
        tar.close()
        
    def extractAllTarfiles(self, fileList:list):
        '''not implemented'''
        print('not implemented')
        print(fileList)
        # fp = tarfile.open(fileName, 'r:gz')''
        # fp.extractall()
        # fp.close()
        
tff = TarfileFunctions()
tff.__all__
