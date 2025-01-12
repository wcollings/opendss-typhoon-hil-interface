from .constants import *

def map_component(comp_type):
    """ Translate from TSE comp_type to corresponding component(s) in the output format """

    mappings = {
        DSS_BUS: ["BUS"],
        DSS_VSOURCE: ["VSOURCE"],
        DSS_ISOURCE: ["ISOURCE"],
        DSS_FAULT: ["FAULT"],
        DSS_CAPACITOR: ["CAPACITOR"],
        DSS_LINE: ["LINE"],
        DSS_MANUAL_SWITCH: ["SWLINE"],
        DSS_CTRL_SWITCH: ["CSWLINE"],
        DSS_SP_TRANSFORMER: ["TRANSFORMER1P"],
        DSS_TP_TRANSFORMER: ["TRANSFORMER3P"],
        DSS_LOAD: ["LOAD"],
        DSS_GENERATOR: ["GENERATOR"],
        DSS_VSCONVERTER: ["VSCONVERTER"],
        DSS_STORAGE: ["STORAGE"],
        DSS_CONTAINER: ["CONTAINER"]
    }

    if comp_type in mappings.keys():
        return mappings.get(comp_type)


def ignore_component(comp_type):
    """ Merge terminals of supported ignored components
        Dictionary key is a terminal and the value is the list of terminals that are being merged to it.
    """

    merge_dict = {
        "Current Measurement": {"p_node": ["n_node"]},
        "Current RMS": {"p_node": ["n_node"]},
        "Three-phase Meter": {"A-": ["A+"], "B-": ["B+"], "C-": ["C+"]},
        "Three Phase Core Coupling":
                {"a_in": ["a_out"], "b_in": ["b_out"], "c_in": ["c_out"]},
        "Three Phase TLM Core Coupling":
            {"a_in": ["a_out"], "b_in": ["b_out"], "c_in": ["c_out"]},
        "Three Phase Device Coupling":
            {"a_in": ["a_out"], "b_in": ["b_out"], "c_in": ["c_out"]},
        "Three Phase TLM Device Coupling":
            {"a_in": ["a_out"], "b_in": ["b_out"], "c_in": ["c_out"]},
        "Four Phase Core Coupling":
            {"a_in": ["a_out"], "b_in": ["b_out"], "c_in": ["c_out"], "d_in": ["d_out"]},
        "Four Phase TLM Core Coupling":
            {"a_in": ["a_out"], "b_in": ["b_out"], "c_in": ["c_out"], "d_in": ["d_out"]},
        "Four Phase Device Coupling":
            {"a_in": ["a_out"], "b_in": ["b_out"], "c_in": ["c_out"], "d_in": ["d_out"]},
        "Four Phase TLM Device Coupling":
            {"a_in": ["a_out"], "b_in": ["b_out"], "c_in": ["c_out"], "d_in": ["d_out"]},
    }

    return merge_dict.get(comp_type)
