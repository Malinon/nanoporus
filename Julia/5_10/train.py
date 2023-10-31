from sklearn.preprocessing   import MinMaxScaler
from sklearn.pipeline        import Pipeline
from sklearn.svm             import SVC
from sklearn.ensemble        import RandomForestClassifier
from sklearn.neighbors       import KNeighborsClassifier
import numpy as np



dgms = []
labs = []
f = open("demofile.txt", "r")
print(f.readlines()) 
labs = [lines[i] for i in range(75)] 




test_size            = 0.2
perm                 = np.random.permutation(len(labs))
limit                = int(test_size * len(labs))
test_sub, train_sub  = perm[:limit], perm[limit:]
train_labs           = np.array(labs)[train_sub]
test_labs            = np.array(labs)[test_sub]
train_dgms           = [dgms[i] for i in train_sub]
test_dgms            = [dgms[i] for i in test_sub]

# Definition of pipeline
pipe = Pipeline([("Separator", gd.representations.DiagramSelector(use=True,limit=np.inf, point_type="finite")),
                 ("Scaler",    gd.representations.DiagramScaler(use=False, scalers=[([0,1], MinMaxScaler())])),
                 ("TDA",       gd.representations.SlicedWassersteinKernel(bandwidth=0.1, num_directions = 10)),
                 ("Estimator", SVC(kernel="precomputed", gamma="auto"))])


pipe.fit(train_dgms, train_labs)