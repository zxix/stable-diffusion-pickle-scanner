import pickle as python_pickle
from types import ModuleType
from functools import partial


def _check_list(what, where):
    for s in where:
        if s == what or (s.endswith('*') and what.startswith(s[:-1])):
            return True
    return False


class InspectorResult:
    def __init__(self):
        self.classes = []
        self.calls = []
        self.structure = {}


class UnpickleConfig:
    def __init__(self, blacklist = [], whitelist = [], tracklist = []):
        self.blacklist = blacklist
        self.whitelist = whitelist
        self.tracklist = tracklist
        self.record = True
        self.verbose = False
        self.strict = False


class StubBase:
    def __init__(self, module, name, result, config, *args, **kwargs):
        self.module = module
        self.name = name
        self.full_name = f'{module}.{name}'
        self.args = {'__init__': [args]}
        self.kwargs = {'__init__': [kwargs]}
        self.config = config
        self.result = result
        if config.record or self.full_name in config.tracklist:
            result.calls.append(f'{self.full_name}({args}, {kwargs})')

    def __repr__(self):
        return f'{self.full_name}({self.args["__init__"]}, {self.kwargs["__init__"]})'
        
    def __getattr__(self, attr):
        return partial(self._call_tracer, attr)

    def __setitem__(self,*args, **kwargs):
        self._call_tracer('__setitem__', *args, **kwargs)

    def _call_tracer(self, attr, *args, **kwargs):
        if attr not in self.args:
            self.args[attr] = []
            self.kwargs[attr] = []
        self.args[attr].append(args)
        self.kwargs[attr].append(kwargs)
        self.result.calls.append(f'{self.full_name}.{attr}({args}, {kwargs})')


class UnpickleBase(python_pickle.Unpickler):
    config = UnpickleConfig()
    def _print(self, *_):
        if self.config.verbose:
            print(*_)


class UnpickleInspector(UnpickleBase):
    def find_class(self, result, module, name):
        full_name = f'{module}.{name}'
        self._print(f'STUBBED {full_name}')
        in_tracklist = _check_list(full_name, self.config.tracklist)
        if self.config.record or in_tracklist:
           result.classes.append(full_name)
        config = self.config
        class Stub(StubBase):
            def __init__(self, *args, **kwargs):
                super().__init__(module, name, result, config, *args, **kwargs)
        return Stub

    def load(self):
        result = InspectorResult()
        self.persistent_load = lambda *_: None # torch
        self.find_class = partial(UnpickleInspector.find_class, self, result)
        result.structure = super().load()
        return result


class BlockedException(Exception):
    def __init__(self, msg):
        self.msg = msg


class UnpickleControlled(UnpickleBase):
    def find_class(self, result, module, name):
        full_name = f'{module}.{name}'
        in_blacklist = _check_list(full_name, self.config.blacklist)
        in_whitelist = _check_list(full_name, self.config.whitelist)
        if (in_blacklist and not in_whitelist) or (len(self.config.blacklist) < 1 and len(self.config.whitelist) > 0 and not in_whitelist):
            if self.config.strict:
                raise BlockedException(f'strict mode: {full_name} blocked')
            else:
                return UnpickleInspector.find_class(self, result, module, name)
        self._print(full_name)
        in_tracklist = _check_list(full_name, self.config.tracklist)
        if self.config.record or full_name in self.config.tracklist:
            result.classes.append(full_name)
        return super().find_class(module, name)
        
    def load(self):
        result = InspectorResult()
        self.find_class = partial(UnpickleControlled.find_class, self, result)
        result.structure = super().load()
        return result


def build(unpickler, conf = None):
    if conf is not None:
        class ConfiguredUnpickler(unpickler):
            config = conf
        unpickler = ConfiguredUnpickler
            
    class PickleModule(ModuleType):
        Unpickler = unpickler
    
    return PickleModule('pickle')


pickle = build(UnpickleInspector)
