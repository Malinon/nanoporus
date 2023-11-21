import load_and_preprocess
import joblib
import cv_model_select
import raport_generator

def get_data_file_name(filt_params, isTopo):
    if isTopo:
        return "../../Persistances/ConeFiltration/cone_" + str(filt_params.radius) + "_" + str(filt_params.height) + "_topo"
    else:
        return "../../Persistances/ConeFiltration/cone_" + str(filt_params.radius) + "_" + str(filt_params.height) + "_rand"

class ConeZFiltParams:
    def __init__(self, radius, height):
        self.radius = radius
        self.height = height

params = ConeZFiltParams(3,6)
labels_path ="../../"

def test_out(a):
    return "out_test"

#load_and_preprocess.prepare_data(params, get_data_file_name, labels_path, test_out)
datas = joblib.load("out_test")

best_mod = cv_model_select.find_best_model_rf(datas, use_yield=True)

raport_generator.generate_report(best_mod.best_estimator_, datas, True, raport_generator.DataType.WHOLE, False)

