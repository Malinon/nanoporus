from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import joblib
import sys
import os.path
NANPOR_REPO_PATH = "/home/xardas/Dokumenty/Nanoporous/nanoporus"
sys.path.append(NANPOR_REPO_PATH  + '/Pipelines')

import load_and_preprocess
from cv_model_select import find_best_model_rf, find_best_model_lasso
from report_generator import generate_report, plot_score_for_filtration
from consts import *

class CvResults:
    def __init__(self, filt_params, is_lasso, use_yield):
        self.filt_params = filt_params
        self.is_lasso = is_lasso
        self.use_yield = use_yield
    def set_estim(self, estim):
        self.estimator = estim
    def get_name(self):
        return "result_"+str(self.filt_params.radius) + "_" + str(self.filt_params.height) + str(self.is_lasso) + str(self.use_yield)
    def dump(self):
        name = self.get_name()
        joblib.dump(self, name)
        return name

def get_data_file_name(filt_params, isTopo):
    if isTopo:
        return NANPOR_REPO_PATH + "/Persistances/ConeFiltration/cone_" + str(filt_params.radius) + "_" + str(filt_params.height) + "_topo"
    else:
        return NANPOR_REPO_PATH + "/Persistances/ConeFiltration/cone_" + str(filt_params.radius) + "_" + str(filt_params.height) + "_rand"

def get_label_name(use_yield):
    if use_yield:
        return "yield"
    else:
        return "modulus"

labels_path ="/home/xardas/Dokumenty/Nanoporous/nanoporus/"

def output_name_generator(filt_params):
    return "/home/xardas/data_" + str(filt_params.radius) + "_" + str(filt_params.height)

def prepare_data(filt_params):
    load_and_preprocess.prepare_data(filt_params, get_data_file_name, labels_path, output_name_generator)

filtrations_params = [ConeZFiltParams(3, 6),
                      ConeZFiltParams(5, 10),
                      ConeZFiltParams(10, 20),
                      ConeZFiltParams(20, 40)]

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 24),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'schedule_interval': None,
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('pers_kub', default_args=default_args)

def get_all_data_sets(filt_params):
    print("USed dataset ",output_name_generator(filt_params))
    basic_name = output_name_generator(filt_params)# "/home/xardas/data_5_10"
    return (joblib.load(basic_name), joblib.load(basic_name + "_topo"), joblib.load(basic_name + "_rand"))

def find_best(filt_params, real_searcher, use_yield, is_lasso):
    whole_data, topo_data, rand_data = get_all_data_sets(filt_params)
    cv_results = CvResults(filt_params, is_lasso, use_yield)
    cv_resuls_name = cv_results.get_name()
    if not os.path.isfile(cv_resuls_name):
        cv_results.set_estim([real_searcher(splited_data=data, use_yield=use_yield) for data in get_all_data_sets(filt_params)])
        joblib.dump(cv_results, cv_resuls_name)
    else:
        print("Skip")
    return cv_resuls_name

def create_search_ops(searcher, use_yield, is_lasso):
    return [PythonOperator(task_id='search_cv_' + str(filt_params) + "_" + get_label_name(use_yield) + str(is_lasso), dag = dag,
                            python_callable = find_best, op_args=[filt_params, searcher, use_yield, is_lasso]) for filt_params in filtrations_params]

def find_best_res(results, idx, filter_func=(lambda x: True)):
    max_score = 0.0
    best_mod = None
    for res in filter(filter_func, results):
        if res.estimator[idx].best_score_ > max_score:
            best_mod = res
            max_score = res.estimator[idx].best_score_
    print("Max score", max_score, "Len: ", len(list(filter(filter_func, results))))
    return best_mod

def gen_rep_best(ti, dependencies, name_score, use_yield=True):
    results = [joblib.load(name) for name in ti.xcom_pull(task_ids=[op.task_id for op in dependencies])]
    for rest in results:
        print(rest.filt_params, " : ", rest.estimator[0].best_score_)
    best_models = [find_best_res(results, idx) for idx in range(3)]
    idx = 0

    for data_type in DataType:
        datas = get_all_data_sets(best_models[idx].filt_params)
        print("Best ", best_models[idx].filt_params, " ", str(data_type))
        generate_report(best_models[idx].estimator[idx], datas[idx], use_yield, data_type, best_models[idx].is_lasso, best_models[idx].filt_params)
        idx += 1
    
    best_for_filtration = []
        
    for filt in filtrations_params:
        print(filt)
        filter_func = lambda x: x.filt_params == filt
        best_for_filtration.append(find_best_res(results, 0, filter_func).estimator[0].best_score_)
    plot_score_for_filtration(best_for_filtration, filtrations_params, name_score)

# Define tasks

load_data_ops = [PythonOperator(task_id='prepareDataa' + str(filt_params), dag = dag,
                            python_callable = prepare_data, op_args=[filt_params]) for filt_params in filtrations_params]

cv_search_yield = create_search_ops(find_best_model_rf, True, False) + create_search_ops(find_best_model_lasso, True, True)
cv_search_modulus = create_search_ops(find_best_model_rf, False, False)+ create_search_ops(find_best_model_lasso, False, True)

gen_rep_best_yields = lambda ti: gen_rep_best(ti, cv_search_yield, name_score="yield_score.png")
gen_rep_best_modulus = lambda ti: gen_rep_best(ti, cv_search_modulus,  name_score="modulus_score.png", use_yield=False)

generate_report_for_best_yield = PythonOperator(task_id='report_yield', python_callable = gen_rep_best_yields, provide_context=True, dag = dag)
generate_report_for_best_modulus = PythonOperator(task_id='report_modulus', python_callable = gen_rep_best_modulus, provide_context=True, dag = dag)

# Set dependencies
for i in range(len(filtrations_params)):
    load_data_ops[i] >> cv_search_yield[i]
    load_data_ops[i] >> cv_search_modulus[i]
cv_search_yield  >> generate_report_for_best_yield
cv_search_modulus >> generate_report_for_best_modulus
