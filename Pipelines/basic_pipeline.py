from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import load_and_preprocess
from cv_model_select import find_best_model_rf, find_best_model_lasso
from report_generator import generate_report
from consts import *

class ConeZFiltParams:
    def __init__(self, radius, height):
        self.radius = radius
        self.height = height

def get_data_file_name(filt_params, isTopo):
    if isTopo:
        return "../Persistances/ConeFiltration/cone_" + str(filt_params.radius) + "_" + str(filt_params.height) + "_topo"
    else:
        return "../Persistances/ConeFiltration/cone_" + str(filt_params.radius) + "_" + str(filt_params.height) + "_rand"

def get_label_name(use_yield):
    if use_yield:
        return "yield"
    else:
        return "modulus"

labels_path ="../"

def otput_name_generator(filt_params):
    return "data_" + str(filt_params.radius) + "_" + str(filt_params.height)

def prepare_data(filt_params):
    load_and_preprocess.prepare_data(filt_params, get_data_file_name, labels_path, output_name_generator)

filtrations_params = [ConeZFiltParams(3, 6),
                      ConeZFiltParams(5, 10),
                      ConeZFiltParams(10, 20),
                      ConeZFiltParams(20, 40)]

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'schedule_interval': '@once',
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('tutorial', default_args=default_args)

def get_all_data_sets(filt_params):
    return (joblib.load(), joblib.load(), joblib.load())

def find_best(filt_params, real_searcher, use_yield, is_lasso):
    whole_data, topo_data, rand_data = 
    return tuple((real_searcher(filt_params, data) for data in get_all_data_sets(filt_params)), filt_params, is_lasso)

def create_search_ops(searcher, use_yield, is_lasso):
    return [PythonOperator(task_id='search_cv_' + str(filt_params) "_" + get_label_name(use_yield) + str(is_lasso),
                            python_callable = find_best, op_args=[filt_params, searcher, use_yield, is_lasso]) for filt_params in filtrations_params]

load_data_ops = [PythonOperator(task_id='prepare_data_' + str(filt_params),
                            python_callable = prepare_data, op_args=[filt_params]) for filt_params in filtrations_params]

cv_search_yield = create_search_ops(find_best_model_rf, True, False) + create_search_ops(find_best_model_lasso, True, True)
cv_search_modulus = create_search_ops(find_best_model_rf, False, False)+ create_search_ops(ind_best_model_lasso, False, True)

generate_report_for_best_yield = PythonOperator(task_id='report_yield', python_callable = gen_rep_best_yields, provide_context=True)
generate_report_for_best_modulus = PythonOperator(task_id='report_yield', python_callable = gen_rep_best_modulus, provide_context=True)

def find_best_res(results, idx):
    max_score = 0.0
    best_mod = None
    for res in results:
        if res[0][idx].best_score_ > max_score:
            best_mod = res[0][idx]
            max_score = res[0][idx].best_score_
    return best_mod


def gen_rep_best_yields(ti):
    results = ti.xcom_pull(task_ids=[op.task_id for op in cv_search_yield])
    best_models = [find_best_res(results, idx) for idx in range(3)]
    idx = 0

    for data_type in DataType:
        datas = get_all_data_sets(best_models[idx][1])
        generate_report(best_models[idx][0], datas[idx], True, data_type, best_models[idx][2])

load_data_ops >> cv_search_yield  >> generate_report_for_best_yield
load_data_ops >> cv_search_modulus >> generate_report_for_best_modulus