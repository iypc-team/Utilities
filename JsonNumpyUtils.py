from BashColors import C
import glob, json, numpy, os, pprint
class EncodeFromNumpy(json.JSONEncoder):
    """
    - Serializes python/Numpy objects via customizing json encoder.
    - **Usage**
        - `json.dumps(python_dict, cls = EncodeFromNumpy)` to get json string.
        - `json.dump(*args, cls = EncodeFromNumpy)` to create a file.json.
    """
    from  BashColors import C
    import json, numpy
    
    def default(self, obj):
        import numpy
        if isinstance(obj, numpy.ndarray):
            return {
                "_kind_": "ndarray",
                "_value_": obj.tolist()
            }
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj,range):
            value = list(obj)
            return {
                "_kind_" : "range",
                "_value_" : [value[0],value[-1]+1]
            }
        return super(EncodeFromNumpy, self).default(obj)
    
class DecodeToNumpy(json.JSONDecoder):
    """
    - Deserilizes JSON object to Python/Numpy's objects.
    - **Usage**
        - `json.loads(json_string,cls = DecodeToNumpy)` from string, use `json.load()` for file.
    """
    import json
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook = self.object_hook, *args, **kwargs)
        # self.jsonFileSet = {'q'}
        # self.jsonFileSet.remove('q')
        # self.listJsonFiles()

    def object_hook(self, obj):
        import numpy
        if '_kind_' not in obj:
            return obj
        kind = obj['_kind_']
        if kind == 'ndarray':
            return numpy.array(obj['_value_'])
        elif kind ==  'range':
            value = obj['_value_']
            return range(value[0],value[-1])
        return obj

class JsonNumpyUtils(EncodeFromNumpy, DecodeToNumpy):
    ''' '''
    from BashColors import C
    import glob, json # , os, pprint
    # os.environ['TZ']
    
    def __init__(self):
        """init"""
        self.pp = pprint.PrettyPrinter()
        self.created=self.inspectJsonFile(
            'JsonUtilsCreationDate.json')
        self.contentPath = os.getcwd()
        self.jsonFileSet = {'q'}
        self.jsonFileSet.remove('q')
        self.jnu = JsonNumpyUtils
        
    def __iter__(self):
        """iter"""
        return self
    
    def getDate(self, silent=True):
        '''Returns date and time string'''
        import time
        secs = time.time()
        secs = secs - (5 * 60 * 60)
        date = time.ctime(secs)
        if not silent:
            print(date)
        return str(date)

    def listJsonFiles(self, C=C):
        json_files = glob.glob('*.json', recursive = True)
        if len(json_files) !=  0:
            print('\nJson files...')
            for fil in sorted(json_files):
                fil = os.path.abspath(fil)
                self.jsonFileSet.add(fil)
                print(f'{C.BICyan}{fil}{C.ColorOff}')
        else: print(f'{C.BIRed}No JSON files exist.{C.ColorOff}')
            

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

    def inspectJsonFile(self, existing:str, silent=True):
        ''' '''
        with open(existing, 'r') as fil:
            newFile = json.load(fil)
            if not silent:
                self.pp.pprint(newFile)
            return newFile
        
    def getMethodList(self, silent=True):
        '''List all methods in JsonNumpyUtils.\n Print silent = True'''
        methodList=[]
        for item in dir(jnu):
            if not item.__contains__('__'):
                methodList.append(item)
                if not silent:
                    print(item)
        return methodList
jnu=JsonNumpyUtils()
