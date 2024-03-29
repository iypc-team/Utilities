from __future__ import absolute_import, unicode_literals
from BashColors import C

from subprocess import check_output, CalledProcessError, STDOUT
import concurrent.futures, glob, json, pip, os, shutil, sys, tarfile
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
else: pass

class AllInstalls4(object):
    ''' '''
    def __init__(self):
        print(f'{C.BIGreen}AllInstalls4{C.ColorOff}')
        if pip.__version__ <= '22.0.4':
            print(f'{C.BIPurple}installing pip --update{C.ColorOff}')
            self.systemCall(["pip3", "install", "-q", "-U", "pip"])
            
        self.__all__ = self.getMethodList()

        self.contentPath = os.getcwd()
        self.initialGlobPth = join(self.contentPath, 'initialGlobList.json')
        self.initialGlobList:list
        with open("initialGlobList.json", 'r') as f:
            self.initialGlobList = json.load(f)
            
        self.jsonFilesPath = join(self.contentPath, 'jsonFiles')
        if not os.path.exists(self.jsonFilesPath):
            os.makedirs(self.jsonFilesPath)
            
        print(f'{C.BIYellow}Pre installing modules{C.ColorOff}')
        start = perf_counter()
        if not self.checkPackageAvailability('tfx', silent=False):
            self.systemCall(
                ["pip3", "install", "-q", "-U", "tfx"])
        if not self.checkPackageAvailability('matplotlib', silent=False):
            self.systemCall(
                ["pip3", "install", "-q", "-U", "matplotlib"])
        if not self.checkPackageAvailability('opencv-python-headless', silent=False):
            self.systemCall(
                ["pip3", "install", "-q","-U", "opencv-python-headless"])
        if not self.checkPackageAvailability('numpy', silent=False):
            self.systemCall(
                ["pip3", "install", "-q", "-U", "numpy"])
        self.printTime(start)
        print(f'{C.BIYellow}Pre installs completed…{C.ColorOff}\n')
        
        self.ai4 = AllInstalls4
        
        self.planetsPath = join(self.contentPath, 'planets')
        self.generatorPath = join(self.contentPath, 'DataGenerator')
        self.testPath = join(self.contentPath, 'images')
        if not exists(self.planetsPath):
            self.extractTarfile('OriginalPlanets.tar.gz', silent=False)
        if not exists(self.generatorPath):
            self.extractTarfile('DataGenerator5.tar.gz', silent=False)
        if not exists(self.testPath):
            self.extractTarfile('images.tar.gz', silent=False)
            
            # self.extractTarfile('images.tar.gz'), silent=False)
        
        super(object, self).__init__()

    def __iter__(self):
        return self
    def __len__(self):
        return len(self.name)
    def __str__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
    
    def extractTarfile(self, fileName, silent=True):
        '''Extracts single tar file'''
        fil=os.path.basename(fileName)
        if not silent:
            print(f'extracting: {fil}')
        tar = tarfile.open(fil, 'r:gz')
        tar.extractall()
        tar.close()

    def getMethodList(self, silent=True):
        '''List all methods in AllInstall\n Print silent = True'''
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
            print(f'{len(method_list)} callable methods in AllInstall')
            for method in method_list:
                print(method)
        return method_list

    def listNewFiles(self, deleteNew = False):
        '''Lists newly created files'''
        initial = self.initialGlobList
        currentFilesGlob = glob.glob('**', recursive = True)
        print(f'{C.BICyan}New files...{C.ColorOff}')
        if len(initial) ==  len(currentFilesGlob):
            print(f'{C.BIRed}No new files.\nNothing to see here')
        for fil in currentFilesGlob:
            if not fil in initial:
                if isdir(fil):
                    print(f'{C.BIBlue}{fil}')
                    if deleteNew:
                        shutil.rmtree(fil)
                elif isfile(fil):
                    print(f'{C.ColorOff}{fil}')
                    if deleteNew:
                        os.remove(fil)

    def getDateTime(self, silent=True):
        '''Returns date and time string'''
        import time
        secs = time.time()
        secs = secs - (5 * 60 * 60)
        date = time.ctime(secs)
        if not silent:
            print(date)
        return str(date)

    def listSystemModules(self, silent=True):
        '''List system installed modules'''
        # 233 modules installed at start
        alreadyInstalledSet = set([each.split('.')[0] for each in sys.modules.keys()])
        modul = sys.modules.keys()
        for idx, item in sorted(enumerate(alreadyInstalledSet)):
            if item in sorted(alreadyInstalledSet):
                if not silent:
                    print(f'{idx} {C.BIBlue}{item}{C.ColorOff}')
        print(f'{idx} system modules installed')

    def printTime(self, strt, fin = None):
        '''print execution times '''
        if fin ==  None:
            fin = perf_counter()
        totalTime = fin - strt
        totalTime =  round(totalTime, 0)
        if totalTime < 60.0:
            print(f'completed in: {C.BIPurple}{totalTime} second(s){C.ColorOff}')
        elif totalTime >=  60.0:
            minutes = totalTime//60
            seconds = totalTime - (minutes * 60)
            seconds = round(seconds, 2)
            print(f'completed in: {C.BIPurple}{minutes} minutes {seconds} second(s){C.ColorOff}')
            
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

    def getPip(self):
        '''Should needs to be pip version 22.0.4'''
        print(f'installing: {C.BIPurple}pip{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "U", "pip"])
        print(f'completed: {C.BIGreen}pip{C.ColorOff}')
        # return f'completed: {C.BIGreen}pip{C.ColorOff}'

    def getTensorflow(self):
        ''' '''
        print(f'installing: {C.BIPurple}tensorflow{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "tensorflow"])
        # !pip install -q -U tensorflow
        print(f'completed: {C.BIGreen}tensorflow{C.ColorOff}')
        # return f'completed: {C.BIGreen}tensorflow{C.ColorOff}'

    def getTFX(self):
        ''' '''
        print(f'installing: {C.BIPurple}TFX{C.ColorOff}')
        # output, success = self.systemCall(["pip3", "install", "-q", "-U", "tfx"])
        output, success = self.systemCall(["pip", "install", "-q", "-U", "tfx"])
        # output, success = self.systemCall("pip3 install tfx")
        # !pip install -q -U tfx
        print(f'completed: {C.BIGreen}TFX{C.ColorOff}')
        # return f'completed: {C.BIGreen}TFX{C.ColorOff}'

    def getApache(self):
        ''' '''
        print(f'installing: {C.BIPurple}apache-beam[interactive]{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "apache-beam[interactive]"])
        # !pip install -q -U apache-beam[interactive] # TFX requirement
        print(f'completed: {C.BIGreen}apache-beam[interactive]{C.ColorOff}')
        # return f'completed: {C.BIGreen}apache-beam{C.ColorOff}'

    def getSnappy(self):
        ''' '''
        print(f'installing: {C.BIPurple}snappy{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "python-snappy"])
        # !pip install -q -U python-snappy
        print(f'completed: {C.BIGreen}snappy{C.ColorOff}')
        # return f'completed: {C.BIGreen}snappy{C.ColorOff}'

    def getTensorflowDatasets(self):
        ''' '''
        print(f'installing: {C.BIPurple}tensorflow-datasets{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "tensorflow-datasets"])
        # !pip install -q -U tensorflow-datasets
        print(f'completed: {C.BIGreen}tensorflow-datasets{C.ColorOff}')
        # return f'completed: {C.BIGreen}tensorflow-datasets{C.ColorOff}'

    def getTFLiteModelMaker(self):
        ''' '''
        print(f'installing: {C.BIPurple}tflite-model-maker{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "tflite-model-maker"])
        # !pip install -q -U tflite-model-maker
        print(f'completed: {C.BIGreen}tflite-model-maker{C.ColorOff}')
        # return f'completed: {C.BIGreen}tflite-model-maker{C.ColorOff}'

    def getTFHub(self):
        ''' '''
        print(f'installing: {C.BIPurple}tensorflow-hub{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "tensorflow-hub"])
        # !pip install -q -U tensorflow-hub
        print(f'completed: {C.BIGreen}tensorflow-hub{C.ColorOff}')
        # return f'completed: {C.BIGreen}tensorflow-hub{C.ColorOff}'

    def getTFLiteSupport(self):
        ''' '''
        print(f'installing: {C.BIPurple}tflite-support{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "tflite-support"])
        # !pip install -q -U tflite-support
        print(f'completed: {C.BIGreen}tflite-support{C.ColorOff}')
        # return f'completed: {C.BIGreen}tflite-support{C.ColorOff}'

    def getTFLiteRuntime(self):
        ''' '''
        print(f'installing: {C.BIPurple}tflite-runtime{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "tflite-runtime"])
        # !pip install -q -U tflite-runtime
        print(f'completed: {C.BIGreen}tflite-runtime{C.ColorOff}')
        # return f'completed: {C.BIGreen}tflite-runtime{C.ColorOff}'

    def getNumpy(self):
        ''' '''
        print(f'installing: {C.BIPurple}numpy{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "numpy"])
        # !pip install -q -U numpy
        print(f'completed: {C.BIGreen}numpy{C.ColorOff}')
        # return f'completed: {C.BIGreen}numpy{C.ColorOff}'

    def getCV2(self):
        ''' '''
        print(f'installing: {C.BIPurple}opencv-headless{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "opencv-python-headless"])
        # !pip install -q -U opencv-python-headless # works.
        print(f'completed: {C.BIGreen}opencv-headless{C.ColorOff}')
        # return f'completed: {C.BIGreen}opencv-headless{C.ColorOff}'
        # # !pip install -q -U opencv-contrib-python-headless

    def getMatplotlib(self):
        ''' '''
        print(f'installing: {C.BIPurple}matplotlib{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "matplotlib"])
        # !pip install -q -U matplotlib
        print(f'completed: {C.BIGreen}matplotlib{C.ColorOff}')
        # return f'completed: {C.BIGreen}matplotlib{C.ColorOff}'

    def getSciPi(self):
        ''' '''
        print(f'installing: {C.BIPurple}SciPy{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "SciPy"])
        # !pip install -q -U SciPy
        print(f'completed: {C.BIGreen}SciPy{C.ColorOff}')
        # return f'completed: {C.BIGreen}SciPy{C.ColorOff}'

    def getSeaborn(self):
        ''' '''
        print(f'installing: {C.BIPurple}seaborn{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "seaborn"])
        # !pip install -q -U seaborn
        print(f'completed: {C.BIGreen}seaborn{C.ColorOff}')
        # return f'completed: {C.BIGreen}seaborn{C.ColorOff}'

    def getResults(self):
        ''' '''
        print(f'installing: {C.BIPurple}results{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "results"])
        # !pip install -q -U results
        print(f'completed: {C.BIGreen}results{C.ColorOff}')
        # return f'completed: {C.BIGreen}results{C.ColorOff}'

    def getBeautifulSoup(self):
        ''' '''
        print(f'installing: {C.BIPurple}beautifulsoup4{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "beautifulsoup4"])
        # !pip install -q -U beautifulsoup4
        print(f'completed: {C.BIGreen}beautifulsoup4{C.ColorOff}')
        # return f'completed: {C.BIGreen}beautifulsoup4{C.ColorOff}'

    def getHtmlLib(self):
        '''USED WITH BeautifulSoup'''
        print(f'installing: {C.BIPurple}html5lib{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "html5lib"])
        # !pip install -q -U html5lib
        print(f'completed: {C.BIGreen}html5lib{C.ColorOff}')
        # return f'completed: {C.BIGreen}html5lib{C.ColorOff}'

    def getLXML(self):
        '''USED WITH BeautifulSoup'''
        print(f'installing: {C.BIPurple}lxml{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "lxml"])
        # !pip install -q -U lxml
        print(f'completed: {C.BIGreen}lxml{C.ColorOff}')
        # return f'completed: {C.BIGreen}lxml{C.ColorOff}'

    def getImutils(self):
        '''Image processing utility '''
        print(f'installing: {C.BIPurple}imutils{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "imutils"])
        # !pip install -q -U imutils
        print(f'completed: {C.BIGreen}imutils{C.ColorOff}')
        # return f'completed: {C.BIGreen}imutils{C.ColorOff}'

    def getPillow(self):
        '''Image processing utility '''
        print(f'installing: {C.BIPurple}pillow{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "pillow"])
        # !pip install -q -U pillow
        print(f'completed: {C.BIGreen}pillow{C.ColorOff}')
        # return f'completed: {C.BIGreen}pillow{C.ColorOff}'

    def getTQDM(self):
        '''Progress bar module'''
        print(f'installing: {C.BIPurple}tqdm{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "tqdm"])
        # !pip install -q -U tqdm
        print(f'completed: {C.BIGreen}tqdm{C.ColorOff}')
        # return f'completed: {C.BIGreen}tqdm{C.ColorOff}'

    def getPSUtil(self):
        '''system monitoring, profiling and limiting process resources'''
        print(f'installing: {C.BIPurple}psutil{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "psutil"])
        # !pip install -q -U psutil
        print(f'completed: {C.BIGreen}psutil{C.ColorOff}')
        # return f'completed: {C.BIGreen}psutil{C.ColorOff}'

    def getSwiftClient(self):
        ''' '''
        print(f'installing: {C.BIPurple}SwiftClient{C.ColorOff}')
        output, success = self.systemCall(["pip3", "install", "-q", "-U", "python-swiftclient"])
        # !pip install -q -U python-swiftclient
        print(f'completed: {C.BIGreen}SwiftClient{C.ColorOff}')
        # return f'completed: {C.BIGreen}Swift client{C.ColorOff}
        
    def listInstalledModules(self):
        '''List installed modules with version number'''
        installed_packages = pkg_resources.working_set
        installedPackagesList = sorted(
            ["%s==%s" % (i.key, i.version) for i in installed_packages])

        packageCount=0
        for package in installedPackagesList:
            packageCount+=1
            print(packageCount, package)

    def checkPackageAvailability(self, packageName:str, silent=True):
        packageName=str(packageName)
        '''checks for package availability returns:boolean True/False'''
        installed_packages = pkg_resources.working_set
        packagesList = sorted(
            ["%s" % i.key for i in installed_packages]
        )
        if not packageName in packagesList:
            if  not silent:
                print(f'{C.BIPurple}{packageName} is not installed{C.ColorOff}')
            return False
        else:
            if not silent:
                print(f'{C.BICyan}{packageName} is installed{C.ColorOff}')
            return True
ai4 = AllInstalls4()
