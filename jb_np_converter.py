import sys
import os
import numpy as np
import joblib

PATH_FILES = sys.argv[1]
FILE_NUM = int(sys.argv[2])

for i in range(FILE_NUM):
    in_name = os.path.join(PATH_FILES, "filtration_" + str(i))
    out_name = os.path.join(PATH_FILES, "arr_fil_" + str(i) + ".npy")
    arr = joblib.load(in_name)
    np.save(out_name, arr)

for fname in os.listdir(PATH_FILES):
    if fname.startswith("filtration_"):
        os.remove(os.path.join(PATH_FILES, fname))