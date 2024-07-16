import numpy as np
import getdist
from getdist import MCSamples
from getdist import loadMCSamples

class loadCosmosisMCSamples:
    #load filename
    #do some stuff to the filename like the getdist.loadMCSamples function does
    #package everything into a getdist MCSamples object
    def __init__(self,filename):
        if filename == None:
            return "chainplotter needs a filename"
        self.chainfile = filename+".txt"
        self.get_metadata()
        self.get_columnnames()
        self.get_chains()

    def get_metadata(self):
        metadata = []
        with open(self.chainfile, 'r') as chainfile:
            for line in chainfile:
                if line.startswith("#"):
                    clean_line = line.strip("#")
                    metadata.append(clean_line)
        self.metadata = metadata
        return self.metadata    

    def get_columnnames(self):
        if self.metadata == None:
            self.metadata = self.get_metadata(self)
        colnames = self.metadata[0].split("\t")
        self.colnames = colnames
        return self.colnames
    
    def get_samples(self):
        samples = []
        self.samples = samples
        return self.samples

    def get_chains(self):
        chains = np.loadtxt(self.chainfile,comments="#")
        self.chains = chains
        return self.chains
    
    def get_weights(self):
        for i,cn in enumerate(self.colnames):
            if "weight" in cn:
                weight_ind = i

        return self.weights
    
    def get_loglikes(self):
        return 0
        
    def get_paramnames(self):
        return 0
    
    def get_labels(self):
        return 0

    def get_sampler(self):
        return 0

    def get_ranges(self):
        return 0


    #samples = MCSamples
    #return #samples
