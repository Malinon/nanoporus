import data_reader as dr


INPUT_DIRECTORY = "../results_topo/"#"../simulation_results/"
OUTPUT_TMPL = "cub_complex_topo_"



def save_complex(i):
    input_path = INPUT_DIRECTORY  + "lmp_data_topo_" + str(i)
    data = dr.read_material_from_file(input_path, grid_step=2.023, i=i)
for i in range(75):
    if save_complex(i):
        print(i)
    
