def inv_control_mode_value_edited(mdl, container_handle, new_value):
    if new_value == "PQ":
        mdl.set_property_disp_value(mdl.prop(container_handle, 'V_ref_str'), "Converter nominal")
        mdl.set_property_disp_value(mdl.prop(container_handle, 'vdc_ref_str'), "Converter nominal")
        mdl.set_property_disp_value(mdl.prop(container_handle, 'fs_ref_str'), "Converter nominal")
        mdl.disable_property(mdl.prop(container_handle, "V_ref_str"))
        mdl.disable_property(mdl.prop(container_handle, "V_kp"))
        mdl.disable_property(mdl.prop(container_handle, "V_ki"))
        mdl.disable_property(mdl.prop(container_handle, "vdc_ref_str"))
        mdl.disable_property(mdl.prop(container_handle, "vdc_kp"))
        mdl.disable_property(mdl.prop(container_handle, "vdc_ki"))
        mdl.disable_property(mdl.prop(container_handle, "fs_ref_str"))
        mdl.enable_property(mdl.prop(container_handle, "Q_ref_str"))
        mdl.enable_property(mdl.prop(container_handle, "Q_kp"))
        mdl.enable_property(mdl.prop(container_handle, "Q_ki"))
        mdl.enable_property(mdl.prop(container_handle, "P_ref_str"))
        mdl.enable_property(mdl.prop(container_handle, "P_kp"))
        mdl.enable_property(mdl.prop(container_handle, "P_ki"))
    elif new_value == "PV":
        mdl.set_property_disp_value(mdl.prop(container_handle, 'Q_ref_str'), "Converter nominal")
        mdl.set_property_disp_value(mdl.prop(container_handle, 'vdc_ref_str'), "Converter nominal")
        mdl.set_property_disp_value(mdl.prop(container_handle, 'fs_ref_str'), "Converter nominal")
        mdl.disable_property(mdl.prop(container_handle, "Q_ref_str"))
        mdl.disable_property(mdl.prop(container_handle, "Q_kp"))
        mdl.disable_property(mdl.prop(container_handle, "Q_ki"))
        mdl.disable_property(mdl.prop(container_handle, "vdc_ref_str"))
        mdl.disable_property(mdl.prop(container_handle, "vdc_kp"))
        mdl.disable_property(mdl.prop(container_handle, "vdc_ki"))
        mdl.disable_property(mdl.prop(container_handle, "fs_ref_str"))
        mdl.enable_property(mdl.prop(container_handle, "V_ref_str"))
        mdl.enable_property(mdl.prop(container_handle, "V_kp"))
        mdl.enable_property(mdl.prop(container_handle, "V_ki"))
        mdl.enable_property(mdl.prop(container_handle, "P_ref_str"))
        mdl.enable_property(mdl.prop(container_handle, "P_kp"))
        mdl.enable_property(mdl.prop(container_handle, "P_ki"))
    elif new_value == "Vdc-Vac":
        mdl.set_property_disp_value(mdl.prop(container_handle, 'P_ref_str'), "Converter nominal")
        mdl.set_property_disp_value(mdl.prop(container_handle, 'Q_ref_str'), "Converter nominal")
        mdl.set_property_disp_value(mdl.prop(container_handle, 'fs_ref_str'), "Converter nominal")
        mdl.disable_property(mdl.prop(container_handle, "P_ref_str"))
        mdl.disable_property(mdl.prop(container_handle, "P_kp"))
        mdl.disable_property(mdl.prop(container_handle, "P_ki"))
        mdl.disable_property(mdl.prop(container_handle, "Q_ref_str"))
        mdl.disable_property(mdl.prop(container_handle, "Q_kp"))
        mdl.disable_property(mdl.prop(container_handle, "Q_ki"))
        mdl.disable_property(mdl.prop(container_handle, "fs_ref_str"))
        mdl.enable_property(mdl.prop(container_handle, "V_ref_str"))
        mdl.enable_property(mdl.prop(container_handle, "V_kp"))
        mdl.enable_property(mdl.prop(container_handle, "V_ki"))
        mdl.enable_property(mdl.prop(container_handle, "vdc_ref_str"))
        mdl.enable_property(mdl.prop(container_handle, "vdc_kp"))
        mdl.enable_property(mdl.prop(container_handle, "vdc_ki"))
    elif new_value == "Vdc-Q":
        mdl.set_property_disp_value(mdl.prop(container_handle, 'P_ref_str'), "Converter nominal")
        mdl.set_property_disp_value(mdl.prop(container_handle, 'V_ref_str'), "Converter nominal")
        mdl.set_property_disp_value(mdl.prop(container_handle, 'fs_ref_str'), "Converter nominal")
        mdl.disable_property(mdl.prop(container_handle, "P_ref_str"))
        mdl.disable_property(mdl.prop(container_handle, "P_kp"))
        mdl.disable_property(mdl.prop(container_handle, "P_ki"))
        mdl.disable_property(mdl.prop(container_handle, "V_ref_str"))
        mdl.disable_property(mdl.prop(container_handle, "V_kp"))
        mdl.disable_property(mdl.prop(container_handle, "V_ki"))
        mdl.disable_property(mdl.prop(container_handle, "fs_ref_str"))
        mdl.enable_property(mdl.prop(container_handle, "Q_ref_str"))
        mdl.enable_property(mdl.prop(container_handle, "Q_kp"))
        mdl.enable_property(mdl.prop(container_handle, "Q_ki"))
        mdl.enable_property(mdl.prop(container_handle, "vdc_ref_str"))
        mdl.enable_property(mdl.prop(container_handle, "vdc_kp"))
        mdl.enable_property(mdl.prop(container_handle, "vdc_ki"))
    elif new_value == "Grid Forming":
        mdl.set_property_disp_value(mdl.prop(container_handle, 'P_ref_str'), "Converter nominal")
        mdl.set_property_disp_value(mdl.prop(container_handle, 'Q_ref_str'), "Converter nominal")
        mdl.set_property_disp_value(mdl.prop(container_handle, 'vdc_ref_str'), "Converter nominal")
        mdl.disable_property(mdl.prop(container_handle, "P_ref_str"))
        mdl.disable_property(mdl.prop(container_handle, "P_kp"))
        mdl.disable_property(mdl.prop(container_handle, "P_ki"))
        mdl.disable_property(mdl.prop(container_handle, "Q_ref_str"))
        mdl.disable_property(mdl.prop(container_handle, "Q_kp"))
        mdl.disable_property(mdl.prop(container_handle, "Q_ki"))
        mdl.disable_property(mdl.prop(container_handle, "vdc_ref_str"))
        mdl.disable_property(mdl.prop(container_handle, "vdc_kp"))
        mdl.disable_property(mdl.prop(container_handle, "vdc_ki"))
        mdl.enable_property(mdl.prop(container_handle, "V_ref_str"))
        mdl.enable_property(mdl.prop(container_handle, "V_kp"))
        mdl.enable_property(mdl.prop(container_handle, "V_ki"))
        mdl.enable_property(mdl.prop(container_handle, "fs_ref_str"))
    elif new_value == "External Control":
        mdl.enable_property(mdl.prop(container_handle, "P_ref_str"))
        mdl.enable_property(mdl.prop(container_handle, "P_kp"))
        mdl.enable_property(mdl.prop(container_handle, "P_ki"))
        mdl.enable_property(mdl.prop(container_handle, "Q_ref_str"))
        mdl.enable_property(mdl.prop(container_handle, "Q_kp"))
        mdl.enable_property(mdl.prop(container_handle, "Q_ki"))
        mdl.enable_property(mdl.prop(container_handle, "fs_ref_str"))
        mdl.enable_property(mdl.prop(container_handle, "V_ref_str"))
        mdl.enable_property(mdl.prop(container_handle, "V_kp"))
        mdl.enable_property(mdl.prop(container_handle, "V_ki"))
        mdl.enable_property(mdl.prop(container_handle, "vdc_ref_str"))
        mdl.enable_property(mdl.prop(container_handle, "vdc_kp"))
        mdl.enable_property(mdl.prop(container_handle, "vdc_ki"))
        mdl.set_property_disp_value(mdl.prop(container_handle, 'P_ref_str'), "External input")
        mdl.set_property_disp_value(mdl.prop(container_handle, 'Q_ref_str'), "External input")
        mdl.set_property_disp_value(mdl.prop(container_handle, 'V_ref_str'), "External input")
        mdl.set_property_disp_value(mdl.prop(container_handle, 'vdc_ref_str'), "External input")
        mdl.set_property_disp_value(mdl.prop(container_handle, 'fs_ref_str'), "External input")

def define_icon(mdl, mask_handle):
    dc_cap = mdl.get_property_value(mdl.prop(mask_handle, "dc_cap_en"))
    if dc_cap:
        mdl.set_component_icon_image(mask_handle, 'images/vsc_cap.svg')
    else:
        mdl.set_component_icon_image(mask_handle, 'images/vsc_nocap.svg')

def toggle_frequency_prop(mdl, mask_handle, init=False):
    frequency_prop = mdl.prop(mask_handle, "Fs")
    global_frequency_prop = mdl.prop(mask_handle, "global_basefreq")
    use_global = mdl.get_property_disp_value(global_frequency_prop)

    if use_global:
        if "simdss_basefreq" in mdl.get_ns_vars():
            mdl.set_property_value(frequency_prop, mdl.get_ns_var("simdss_basefreq"))
            mdl.hide_property(frequency_prop)
        else:
            mdl.set_property_disp_value(global_frequency_prop, False)
            mdl.info("Add a SimDSS component to define the global frequency value.")
    else:
        mdl.show_property(frequency_prop)

def port_dynamics(mdl, mask_handle, caller_prop_handle=None, init=False):
    pass

def update_frequency_property(mdl, mask_handle, init=False):

    frequency_prop = mdl.prop(mask_handle, "Fs")
    global_frequency_prop = mdl.prop(mask_handle, "global_basefreq")
    use_global = mdl.get_property_value(global_frequency_prop)

    if init:
        mdl.hide_property(frequency_prop)
    else:
        if use_global:
            if "simdss_basefreq" in mdl.get_ns_vars():
                mdl.set_property_value(frequency_prop, mdl.get_ns_var("simdss_basefreq"))
            else:
                mdl.set_property_value(global_frequency_prop, False)
        toggle_frequency_prop(mdl, mask_handle, init)
