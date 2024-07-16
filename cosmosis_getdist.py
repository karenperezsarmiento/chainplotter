import numpy as np
import getdist
from getdist import MCSamples
from getdist import loadMCSamples

class loadCosmosisMCSamples(filename):
    #load filename
    #do some stuff to the filename like the getdist.loadMCSamples function does
    #package everything into a getdist MCSamples object
    def __init__(self,filename):
        if filename == None:
            return "chainplotter needs a filename"
        self.chainfile = filename+".txt"
        self.get_metadata()
        self.get_paramnames()

    def get_metadata(self):
        metadata = []
        with open(self.chainfile, 'r') as chainfile:
            for line in chainfile:
                if line.startswith("#"):
                    clean_line = line.strip("#")
                    metadata.append(clean_line)
        self.metadata = metadata
        return self.metadata    

    def get_paramnames(self):
        if self.metadata == None:
            self.metadata = self.get_metadata(self)
        paramnames = self.metadata[0].split("\t")
        self.paramnames = paramnames
        return self.paramnames
    
    def get_ranges(self):
        return self.ranges


    #samples = MCSamples
    return #samples
