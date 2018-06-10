from importlib import import_module


class Engine(object):

    # TODO: Some form of chaining here

    def __init__(self, instruct, keys):
        self.start = self.get_component(instruct['input']['platform'])
        self.end = self.get_component(instruct['output']['platform'])
        self.start.component.get_data(keys,instruct['input']['input'])

    def run(self):
        pass

    @staticmethod
    def get_component(comp):
        return import_module('platforms.' + comp)
