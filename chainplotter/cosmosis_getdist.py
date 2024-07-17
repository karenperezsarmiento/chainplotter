import numpy as np
import getdist
from getdist import MCSamples
from getdist import loadMCSamples
import re

class loadCosmosisMCSamples:
    """Loads cosmosis output chains and returns a getdist.MCSamples object that can be plotted using getdist.

    Attributes:
        chainfile (str): File name of cosmosis output chains.
        metadata (:obj:`list` of :obj:`str`): Metadata from cosmosis file.
        columnnames (:obj:`np.array` of :obj:`str`): List of columns names (first line in cosmosis metadata)
        sampler_type (str): Sampler used to generate chains. Currently only supports nested sampling.
        chains (:obj:`np.array`): Array with the chains from cosmosis file
        indices (:obj:`np.array`): Indices of the columns that correspond to the loglikelihood, weights and sampled variables.
        paramnames (:obj:`np.array of :obj:`str`): Array of the parameter names.
        samples (:obj:`np.array`): Array with the sampled parameters from the chains.
        loglikes (:obj:`np.array`): Array with the log likelihood from the chains.
        weights (:obj:`np.array`): Array with the weights.
        labels (:obj:`list`): List of the labels for the parameters.
        ranges (:obj: `dict`): Dictionary for each parameters and its corresponding minimum and maximum values.
    """
    def __init__(self,filename):
        """ Initializes the loadCosmosisMCSamples class

        Args:
            filename (str): File name of cosmosis chains (must not contain`.txt`).

        """
        if filename == None:
            raise ValueError("chainplotter needs a filename")
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
        self.get_labels()
        self.get_ranges()


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
        self.colnames = np.array(colnames)
    
    def get_indices(self):
        index_log = np.where(np.array(self.colnames) == "post")[0]
        index_all = np.arange(len(self.colnames))
        index_weight = np.where(np.array(self.colnames) == "weight\n")[0]
        index_samples = np.array(np.delete(index_all,[index_log,index_weight]).astype(int))
        return index_log,index_weight,index_samples
    
    def get_samples(self):
        self.samples = self.chains[:, self.index_samples]

    def get_chains(self):
        chains = np.loadtxt(self.chainfile,comments="#")
        self.chains = chains

    def get_sampler_type(self):
        for i in self.metadata:
            if "polychord" in i:
                self.sampler_type = "nested"

    def get_weights(self):
        self.weights = self.chains[:,self.index_weight]
    
    def get_loglikes(self):
        self.log = self.chains[:,self.index_log]
        
    def get_paramnames(self):
        self.paramnames = self.colnames[self.index_samples]
    
    def get_labels(self):
        labels = []
        for i,p in enumerate(self.paramnames):
            p_new = re.sub(r".*--","",p)
            labels.append(p_new)
        self.labels = labels
        categories = []
        for i,p in enumerate(self.paramnames):
            p_new = re.sub(r"--.*","",p)
            categories.append(p_new)
        self.categories = categories

        chi2_ind = self.labels.index("2PT_CHI2")
        self.labels.pop(chi2_ind)
        self.categories.pop(chi2_ind)
        prior_ind = self.labels.index("prior")
        self.labels.pop(prior_ind)
        self.categories.pop(prior_ind)
        like_ind = self.labels.index("like")
        self.labels.pop(like_ind)
        self.categories.pop(like_ind)
        return self.labels,self.categories

    def get_ranges(self):
        for i,s in enumerate(self.metadata):
            if "START_OF_VALUES_INI" in s:
                start_of_ranges = i
            if "END_OF_VALUES_INI" in s:
                end_of_ranges = i
        ranges_chunk = self.metadata[start_of_ranges+1:end_of_ranges]
        unique_cat = np.unique(np.array(list(map(str.lower,self.categories))))
        cat_array = np.array(self.categories)
        lab_array = np.array(self.labels)
        cat_index = []
        for i,s in enumerate(ranges_chunk):
            for j in unique_cat:
                if j in s:
                    id = ranges_chunk.index(s)
                    cat_index.append(id)
        ranges_dict = {}
        for i,n in enumerate(cat_index[:-1]):
            cat_chunk = ranges_chunk[cat_index[i]:cat_index[i+1]]
            this_cat = unique_cat[i]

            these_labels = lab_array[np.array(cat_array)==this_cat]
            for c,j in enumerate(cat_chunk):
                for lab in these_labels:
                    if lab in j:
                        to_delete = lab+" = "
                        numbers = re.sub(to_delete,"", j)
                        numbers = numbers.split()
                        numbers = np.array(numbers).astype(float)
                        if len(numbers)==1:
                            min_val = None
                            max_val = no=np.max(numbers)
                        elif len(numbers)==3:
                            min_val = np.min(numbers)
                            max_val = np.max(numbers)
                        else:
                            min_val = None
                            max_val = None
                        key_name = this_cat+"__"+lab
                        ranges_dict[key_name] = {"min": min_val, "max": max_val}
        self.ranges = ranges_dict
        return self.ranges
    
    def make_sampler(self):
        self.mc_samples = MCSamples(samples=self.samples, weights=self.weights,
                           loglikes=-2.*self.log,
                           sampler=self.sampler_type, names=self.paramnames,
                           labels=param_labels, ranges=ranges,
                           ignore_rows=0)
                           #settings=settings)
        return 


    #samples = MCSamples
    #return #samples
