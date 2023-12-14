from fpdf import FPDF
from enum import Enum

import seaborn as sns
import matplotlib.pylab as plt

from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

import numpy as np
from consts import *

METRICS_DICT = {"R2": r2_score, "MAE": mean_absolute_error, "MSE ": mean_squared_error, "MAPE ": mean_absolute_percentage_error}

TOPO_COLOR = "red"
RAND_COLOR  = "blue"

IMG_WIDTH = 200

def get_impact_heat_map_from_rf(forest, dim, name):
    plt.clf()
    plt.cla()
    img_size = PERSISTENCE_IMAGE_RESOLUTION[0] * PERSISTENCE_IMAGE_RESOLUTION[1]
    importances = forest[0].feature_importances_
    datas = np.copy(importances[dim*img_size:img_size*(dim+1)]).reshape(PERSISTENCE_IMAGE_RESOLUTION)
    ax = sns.heatmap(datas, linewidth=0.5)
    plt.title("Impact in dim=" + str(dim))
    plt.savefig(name)

def get_impact_heat_map_from_lasso(lasso_reg, dim, name):
    plt.clf()
    plt.cla()
    img_size = PERSISTENCE_IMAGE_RESOLUTION[0] * PERSISTENCE_IMAGE_RESOLUTION[1]
    datas = np.copy(lasso_reg[0].coef_[dim * img_size:img_size*(dim+1)]).reshape(PERSISTENCE_IMAGE_RESOLUTION)
    ax = sns.heatmap(datas, linewidth=0.5)
    plt.title("Coefficients in dim=" + str(dim))
    plt.savefig(name)

class ResultReport:
    def __init__(self, model, splited_data, use_yield, data_type, is_lasso, filt_params):
        self.model = model
        self.prediction_test = self.model.predict(splited_data.test_dgms)
        self.splited_data = splited_data
        self.use_yield = use_yield
        self.data_type = data_type
        self.is_lasso = is_lasso
        self.filt_params = filt_params
    def get_intro(self):
        return ("The best model for " + str(self.data_type) + " dataset is " + str(self.model.best_estimator_['Estimator'])
                + "\n Filtration: radius " + str(self.filt_params.radius) +", height " + str(self.filt_params.height))
    def get_metrics_results(self):
        output_dict = {}
        _, test_labs = self.splited_data.get_labels(self.use_yield)
        print(len(test_labs), " Labs" )
        for met in METRICS_DICT:
            output_dict[met] = str(METRICS_DICT[met](test_labs, self.prediction_test))
        return output_dict
    def get_importances_img_by_path(self):
        names = [ str(self.data_type) + "_importance_dim_" + str(dim) + ".png"  for dim in range(3)]
        if self.is_lasso:
            for dim in range(3):
                get_impact_heat_map_from_lasso(self.model.best_estimator_, dim, names[dim]) 
        else:
            for dim in range(3):
                get_impact_heat_map_from_rf(self.model.best_estimator_, dim, names[dim])
        return names
    def get_result_img_by_path(self):
        name = str(self.data_type) + "_result.png"
        self.plot_scatter_result(name)
        return name

    def plot_scatter_result(self, name):
        fig, ax = plt.subplots()
        _, test_labs = self.splited_data.get_labels(self.use_yield)
        color = None
        if self.data_type == DataType.TOPO:
            color = TOPO_COLOR
        elif self.data_type == DataType.RAND:
            color = RAND_COLOR
        else:
            color =[TOPO_COLOR  if idx < NUMBER_OF_OK_TOPO_SAMPLES else RAND_COLOR for idx in self.splited_data.test_sub]
        ax.scatter(test_labs, self.prediction_test, s=25, c = color, zorder=10)
        lims = [
            np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
            np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
        ]

        ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
        ax.set_aspect('equal')
        ax.set_xlim(lims)
        ax.set_ylim(lims)
        ax.set_xlabel("real")
        ax.set_ylabel("prediction")
        plt.savefig(name)

def add_header(pdf, title):
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, h = 10, txt = title, border = 0, ln = 2)

def set_default_font(pdf):
    pdf.set_font('Arial', style = '', size = 12)
def print_report_to_pdf(result_report):
    pdf = FPDF()
    pdf.add_page()
    add_header(pdf, "Introduction")
    pdf.set_auto_page_break(True)
    set_default_font(pdf)
    pdf.write(h=10, txt = result_report.get_intro() + "\n")
    pdf.set_x(0)
    add_header(pdf, "Basic metrics")
    set_default_font(pdf)
    res_metrics = result_report.get_metrics_results()
    for metrics_name in res_metrics.keys():
        pdf.cell(0, h = 10, txt = metrics_name +': ' + str(res_metrics[metrics_name]), border = 0, ln = 2)
    add_header(pdf, "Results")
    set_default_font(pdf)
    pdf.image(result_report.get_result_img_by_path(), w = IMG_WIDTH)
    add_header(pdf, "Feature importances")
    set_default_font(pdf)
    paths = result_report.get_importances_img_by_path()
    for path in paths:
        pdf.image(path,  w = IMG_WIDTH)
    pdf.output('/home/xardas/best_'+ str(result_report.use_yield) + str(result_report.data_type) + '.pdf', 'F')

def generate_report(model, splited_data, use_yield, data_type, is_lasso, filt_params):
    report = ResultReport(model, splited_data, use_yield, data_type, is_lasso, filt_params)
    print_report_to_pdf(report)

def plot_score_for_filtration(best_for_filtration, filtrations_params, name):
    plt.clf()
    plt.cla()
    fig, ax = plt.subplots()
    ax.plot([a.radius for a in filtrations_params], best_for_filtration)
    ax.set_xlabel("radius")
    ax.set_ylabel("score")
    plt.savefig("/home/xardas/" + name)