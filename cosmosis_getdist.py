import numpy as np
import getdist
from getdist import MCSamples
from getdist import loadMCSamples
import re

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
        self.get_sampler_type()
        self.get_chains()
        self.index_log,self.index_weight,self.index_samples = self.get_indices()
        self.get_paramnames()
        self.get_samples()
        self.get_loglikes()
        self.get_weights()


    def get_metadata(self):
        metadata = []
        with open(self.chainfile, 'r') as chainfile:
            for line in chainfile:
                if line.startswith("#"):
                    clean_line = line.strip("#")
                    metadata.append(clean_line)
        self.metadata = metadata   

    def get_columnnames(self):
        if self.metadata == None:
            self.metadata = self.get_metadata(self)
        colnames = self.metadata[0].split("\t")
        self.colnames = colnames
    
    def get_indices(self):
        index_log = np.where(np.array(self.colnames) == "post")[0]
        index_all = np.arange(len(self.colnames))
        index_weight = np.where(np.array(self.colnames) == "weight\n")[0]
        index_samples = list(np.array(np.delete(index_all,[index_log,index_weight]).astype(int)))
        return index_log,index_weight,index_samples
    
    def get_samples(self):
        self.samples = self.chains[:, self.index_samples]

    def get_chains(self):
        chains = np.loadtxt(self.chainfile,comments="#")
        self.chains = chains

    def get_sampler_type(self):
        for i in self.metadata:
            if "sampler" in i:
                sampler = re.sub("sampler = ","",i)
                if sampler == "polychord":
                    self.sampler_type = "nested"
    


    def get_weights(self):
        self.weights = self.chains[:,self.index_weight]
    
    def get_loglikes(self):
        self.log = self.chains[:,self.index_log]
        
    def get_paramnames(self):
        print(type(self.index_samples[0]))
        self.paramnames = self.colnames[self.index_samples]
    
    def get_labels(self):
        return 0

    def get_ranges(self):
        return 0
    
    def make_sampler(self):
        self.mc_samples = MCSamples(samples=self.samples, weights=self.weights,
                           loglikes=-2.*loglike,
                           sampler=sampler, names=param_names,
                           labels=param_labels, ranges=ranges,
                           ignore_rows=0, name_tag=name_tag,
                           settings=settings)
        return 0


    #samples = MCSamples
    #return #samples
