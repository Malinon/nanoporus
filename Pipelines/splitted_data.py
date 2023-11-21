import numpy as np

"""
This class represents data splited into train and test data
"""
class SplitedData:
    def get_split_idxs(length, test_size):
        perm = np.random.permutation(length)
        limit = int(test_size * length)
        return perm[:limit], perm[limit:]
    def __init__(self, data, labs_yield, labs_modulus, idxs, transformer, test_size=0.2):
        # Select Data
        data = np.array(data)[idxs]
        labs_yield = np.array(labs_yield)[idxs]
        labs_modulus = np.array(labs_modulus)[idxs]
        # Split Data
        test_sub, train_sub  = SplitedData.get_split_idxs(len(labs_yield), test_size)
        self.test_sub = test_sub
        self.train_labs_yield     = np.array(labs_yield)[train_sub]
        self.test_labs_yield      = np.array(labs_yield)[test_sub]
        self.train_labs_modulus   = np.array(labs_modulus)[train_sub]
        self.test_labs_modulus    = np.array(labs_modulus)[test_sub]
        self.train_dgms           = np.transpose(np.array(data)[train_sub])#[data[i] for i in train_sub]
        transformer.fit(self.train_dgms)
        self.train_dgms           = transformer.transform((self.train_dgms))
        self.test_dgms            = transformer.transform(np.transpose(np.array([data[i] for i in test_sub])))
    def get_labels(self, use_yield):
        if use_yield:
            return self.train_labs_yield, self.test_labs_yield
        else:
            return self.train_labs_modulus, self.test_labs_modulus