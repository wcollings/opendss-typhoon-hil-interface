import pathlib
import numpy as np

import typhoon.api.hil as hil
from typhoon.api.schematic_editor import model as mdl

# TSE to OpenDSS converter
import tse_to_opendss
from tse_to_opendss.tse2tpt_base_converter import tse2tpt

# OpenDSS API
import opendssdirect as dss

###################################################

def reload_hil_libraries():
    mdl.reload_libraries()

def convert_to_dss(tse_file_path):
    load_tse_model(tse_file_path)
    mdl.export_model_to_json()

    # Paths
    parent_folder = pathlib.Path(tse_file_path).parent
    target_files_path = parent_folder.joinpath(str(pathlib.Path(tse_file_path).stem) + ' Target files')
    json_file_path = target_files_path.joinpath(str(pathlib.Path(tse_file_path).stem) + '.json')
    master_dss_file_path = target_files_path.joinpath("dss").joinpath(
        str(pathlib.Path(tse_file_path).stem) + '_master.dss')

    # Simulation parameters
    simdss_found = False
    for comp in mdl.get_items():
        # SimDSS component must be on the top level and named SimDSS1, otherwise load default parameters
        if mdl.get_name(comp) == "SimDSS1":
            simdss_found = True
            break

    if simdss_found:
        sim_parameters = {"sim_mode": mdl.get_property_disp_value(mdl.prop(comp, "sim_mode")),
                          "algorithm": mdl.get_property_disp_value(mdl.prop(comp, "algorithm")),
                          "voltagebases": mdl.get_property_disp_value(mdl.prop(comp, "voltagebases")),
                          "basefrequency": mdl.get_property_disp_value(mdl.prop(comp, "basefrequency")),
                          "maxiter": mdl.get_property_disp_value(mdl.prop(comp, "maxiter")),
                          "miniterations": mdl.get_property_disp_value(mdl.prop(comp, "miniterations")),
                          "loadmodel": mdl.get_property_disp_value(mdl.prop(comp, "loadmodel")),
                          "stepsize": mdl.get_property_disp_value(mdl.prop(comp, "tsstp")),
                          "number": mdl.get_property_disp_value(mdl.prop(comp, "tspoints"))}
    else:
        sim_parameters = {"sim_mode": "Snap",
                          "basefrequency": "60",
                          "maxiter": "10",
                          "miniterations": "2",
                          "loadmodel": "Power flow",
                          "voltagebases": "[0.480, 12.47]"}

    tse2tpt.start_conversion(json_file_path, tse_to_opendss, simulation_parameters=sim_parameters)

    return master_dss_file_path


def compile_dss_model(dss_file_path):
    comp_result = dss.utils.run_command(f'Compile "{str(dss_file_path)}"')
    return comp_result


def import_dss_model(dss_file_path):
    import importer.scripts.modules as dsm

    dss_file_name = pathlib.Path(dss_file_path).stem
    save_dir = pathlib.Path(dss_file_path).parent.joinpath("importer_output")
    save_dir.mkdir(parents=True, exist_ok=True)

    # Create TSE model using the importer
    comp_dict, circuit_name, loadshapes = dsm.getElements(dss_file_path)
    placement_info = dsm.generatePlacementInfo(comp_dict)
    mdl = dsm.generateSchematic(comp_dict, placement_info)
    output_file_name = str(save_dir.joinpath(f"{dss_file_name}.tse"))
    mdl.save_as(output_file_name)

    # Write loadshapes if they exist in the original DSS model
    if loadshapes:
        dsm.writeLoadShapes(loadshapes, str(save_dir), dss_file_name)

    return output_file_name


def load_tse_model(tse_file_path):
    # Open the converted tse file
    mdl.load(tse_file_path)

def compile_model_and_load_to_hil(tse_file_path, use_vhil=True):
    # Compile the model
    mdl.compile()
    # Load to HIL
    parent_folder = pathlib.Path(tse_file_path).parent
    target_files_path = parent_folder.joinpath(str(pathlib.Path(tse_file_path).stem) + ' Target files')
    cpd_path = target_files_path.joinpath(str(pathlib.Path(tse_file_path).stem) + ".cpd")
    hil.load_model(file=cpd_path, offlineMode=False, vhil_device=use_vhil)

def get_element_current(elem_name, elem_class):
    dss.Circuit.SetActiveClass(elem_class)
    dss.ActiveClass.First()
    for _ in range(dss.ActiveClass.Count()):
        if dss.CktElement.Name().upper() == f"{elem_class.upper()}.{elem_name.upper()}":
            meas = dss.CktElement.CurrentsMagAng()
            currents_dict = {}
            phase_num_dict = {ph: chr(97 + ph//2) for ph in range(2*(dss.CktElement.NumConductors()))}  # {0: a, 1: a, 2: b, ... }
            for idx, _ in enumerate(meas[0:dss.CktElement.NumConductors()]):

                currents_dict.update(
                    {
                        f"mag_{phase_num_dict[2*idx]}": meas[2*idx],
                        f"ang_{phase_num_dict[2*idx+1]}": meas[2*idx+1],
                    }
                )
            return currents_dict
        dss.ActiveClass.Next()

def get_bus_voltage(busname):
    dss.Circuit.SetActiveBus(busname)
    meas = dss.Bus.VMagAngle()
    phase_num_dict = {ph: chr(97 + ph//2) for ph in range(2*dss.Bus.NumNodes())}  # {0: a, 1: a, 2: b, ... }
    voltages_dict = {}
    for idx, _ in enumerate(meas[0:dss.Bus.NumNodes()]):
        voltages_dict.update(
            {
                f"mag_{phase_num_dict[2*idx]}": meas[2*idx],
                f"ang_{phase_num_dict[2*idx+1]}": meas[2*idx+1],
            }
        )
    return voltages_dict

def calculate_line_voltage(v1_mag, v1_phase, v2_mag, v2_phase):

    # Convert to cartesian
    v1_x, v1_y = pol2cart(v1_mag, v1_phase)
    v2_x, v2_y = pol2cart(v2_mag, v2_phase)

    # Subtract the coordinates
    v12_x = v1_x - v2_x
    v12_y = v1_y - v2_y

    # Convert back to polar
    return cart2pol(v12_x, v12_y)


def cart2pol(x, y):
    # From cartesian to polar
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return (rho, phi)

def pol2cart(rho, phi):
    # From polar to cartesian
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return (x, y)





