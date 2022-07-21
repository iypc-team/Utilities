from __future__ import absolute_import, unicode_literals
from BashColors import C

from subprocess import check_output, CalledProcessError, STDOUT
import concurrent.futures, glob, json, pip, os, sys, tarfile
import pkg_resources
from concurrent.futures import ThreadPoolExecutor
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '5'
from os.path import *
from time import perf_counter, sleep

contentPath=os.getcwd()
jsonPath=join(contentPath, 'initialGlobList.json')

if not exists(jsonPath):
    initialGlobList=glob.glob('**', recursive=True)
    initialGlobList=glob.glob('**', recursive=True)
    if not 'initialGlobList.json' in initialGlobList:
        # initialGlobList.append('initialGlobList.json')
        pass
    with open('initialGlobList.json', 'w', encoding='utf-8') as f:
        json.dump(initialGlobList, f, ensure_ascii=False, indent='\t')
else:
    pass

class TarfileFunctions(object):
    '''tarfile utilities'''
    def __init__(self):
        print(f"{C.BIGreen}TarfileFunctions{C.ColorOff}")
        if pip.__version__ <= '22.0.4':
            print(f'{C.BIPurple}installing pip --update{C.ColorOff}')
            self.systemCall(["pip3", "install", "-q", "-U", "pip"])
        self.__all__ = self.getMethodList()
        self.contentPath = os.getcwd()
        self.tff = TarfileFunctions
        self.tarfileList=[]
        self.tarfilePathList=[]
        self.listTarfiles()
        
        self.planetsPath = join(self.contentPath, 'planets')
        self.generatorPath = join(self.contentPath, 'DataGenerator')
        self.testPath = join(self.contentPath, 'images')
        if not exists(self.planetsPath):
            self.extractTarfile('OriginalPlanets.tar.gz')
        if not exists(self.generatorPath):
            self.extractTarfile('DataGenerator5.tar.gz')
        if not exists(self.testPath):
            self.extractTarfile('images.tar.gz')
        
        super(object, self).__init__()

    def __iter__(self):
        return self
    def __len__(self):
        return len(self.name)
    def __str__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
    
    def silentSystemCall(self, command, silent=True):
        """
        params:
            command: list of strings, `["pip3", "install", "-q", "-U", "pip"]`
            if not silent...
            returns: output, success
        """
        try:
            output = check_output(command, stderr=STDOUT).decode()
            success = True 
        except CalledProcessError as e:
            output = e.output.decode()
            success = False
        if not silent:
            print(command)
            if success:
                print(f'success: {C.BIGreen}{success}{C.ColorOff}\n{output}')
            elif not success:
                print(f'success: {C.BIRed}{success}{C.ColorOff}\n{output}')
            return output, success
        
    def systemCall(self, command):
        """ 
        params:
            command: list of strings, ex. `["pip3", "install", "-q", "-U", "pip"]`
        returns: output, success
        """
        try:
            output = check_output(command, stderr=STDOUT).decode()
            success = True 
        except CalledProcessError as e:
            output = e.output.decode()
            success = False
        print(command)
        if success:
            print(f'success: {C.BIGreen}{success}{C.ColorOff}\n{output}')
        elif not success:
            print(f'success: {C.BIRed}{success}{C.ColorOff}\n{output}')
        return output, success
    
    def getMethodList(self, silent=True):
        '''List all methods in TarfileFunctions\n Print silent = True'''
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
            print(f'{len(method_list)} methods in TarfileFunctions')
            for method in method_list:
                print(method)
        return method_list
    
    def listTarfiles(self, silent=True):
        '''List all local tar files'''
        if not silent:
            print(f'Available tar files:')
        tarfile_list = glob.glob('**', recursive=True)
        for fil in sorted(tarfile_list):
            if fil.endswith('.gz'):
                fil=os.path.basename(fil)
                fullPth = os.path.abspath(fil)
                if not silent:
                    print(f'{C.IPurple}{fil}{C.ColorOff}')
                    print(f'{C.Green}{fullPth}{C.ColorOff}\n')
                self.tarfileList.append(fil)
                self.tarfilePathList.append(fullPth)
                
    def tarfileFromDirectory(self, output_filename, source_dir):
        '''creates new tar file from given directory'''
        if not output_filename.__contains__('.'):
            output_filename = output_filename + '.tar.gz'
        if not output_filename.endswith('.tar.gz'):
            print(f'{C.BIRed}{output_filename} must endwith .tar.gz{C.ColorOff}')
            return '.tar.gz'
        if source_dir == self.contentPath:
            print(f'{C.BIRed}can not tar from directory:{C.ColorOff} {source_dir}')
            return
        # print('source_dir:', source_dir)
        # print('basename(source_dir)', os.path.basename(source_dir))
        file_name = os.path.basename(source_dir) + '.tar.gz'
        # print(file_name)
        
        with tarfile.open(output_filename, "w:gz") as tar:
            # pass
            tar.add(source_dir, arcname=os.path.basename(source_dir))
        if exists(join(tff.contentPath, file_name)):
                  print(f'{C.BIGreen}created: {file_name}{C.ColorOff}')

    def extractTarfile(self, fileName, silent=True):
        '''Extracts single tar file'''
        fil=os.path.basename(fileName)
        if not silent:
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
