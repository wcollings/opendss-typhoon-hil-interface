import numpy as np
from itertools import combinations

x0, y0 = (8192, 8192)

def delete_port(mdl, name, parent):
    comp = mdl.get_item(name, parent=parent, item_type="port")
    if comp:
        mdl.delete_item(comp)
        return True

def enable_disable_grounds(mdl, mask_handle):
    grounded_prim_prop = mdl.prop(mask_handle, "grounded_prim")
    grounded_sec1_prop = mdl.prop(mask_handle, "grounded_sec1")
    grounded_sec2_prop = mdl.prop(mask_handle, "grounded_sec2")
    grounded_sec3_prop = mdl.prop(mask_handle, "grounded_sec3")
    num_windings_prop = mdl.prop(mask_handle, "num_windings")
    num_windings = mdl.get_property_disp_value(num_windings_prop)

    if num_windings == "2":
        if not mdl.get_property_disp_value(mdl.prop(mask_handle, "embedded_cpl")) == "None":
            mdl.set_property_disp_value(grounded_prim_prop, False)
            mdl.disable_property(grounded_prim_prop)
            mdl.set_property_disp_value(grounded_sec1_prop, False)
            mdl.disable_property(grounded_sec1_prop)
        else:
            mdl.enable_property(grounded_prim_prop)
            mdl.set_property_disp_value(grounded_prim_prop, mdl.get_property_value(grounded_prim_prop))
            mdl.enable_property(grounded_sec1_prop)
            mdl.set_property_disp_value(grounded_sec1_prop, mdl.get_property_value(grounded_sec1_prop))
    else:
        cpl_props = ["embedded_cpl_12", "embedded_cpl_13", "embedded_cpl_14"]
        gnd_props = [grounded_sec1_prop, grounded_sec2_prop, grounded_sec3_prop]
        for idx in range(int(num_windings) - 1):
            if not mdl.get_property_disp_value(mdl.prop(mask_handle, cpl_props[idx])) == "None":
                mdl.set_property_disp_value(gnd_props[idx], False)
                mdl.disable_property(gnd_props[idx])
            else:
                mdl.set_property_disp_value(gnd_props[idx], mdl.get_property_value(gnd_props[idx]))
                mdl.enable_property(gnd_props[idx])
        # Primary gnd
        enable_prim_gnd = True
        for idx in range(int(num_windings) - 1):
            if mdl.get_property_disp_value(mdl.prop(mask_handle, cpl_props[idx])) == "None":
                pass
            else:
                enable_prim_gnd = False
                break
        if enable_prim_gnd:
            mdl.enable_property(grounded_prim_prop)
            mdl.set_property_disp_value(grounded_prim_prop, mdl.get_property_value(grounded_prim_prop))
        else:
            mdl.disable_property(grounded_prim_prop)
            mdl.set_property_disp_value(grounded_prim_prop, False)


def update_neutrals(mdl, mask_handle, T_handle, created_ports):
    comp_handle = mdl.get_parent(mask_handle)
    num_windings = int(mdl.get_property_value(mdl.prop(mask_handle, "num_windings")))
    conn_dict = ["prim", "sec1", "sec2", "sec3"]
    posY = 346 if num_windings == 4 else 240

    for i in range(1, 5):
        gnd = mdl.get_item("gnd", parent=comp_handle)
        if gnd:
            mdl.delete_item(gnd)

    for idx in range(0, num_windings):
        grounded = mdl.get_property_value(mdl.prop(mask_handle, "grounded_" + conn_dict[idx]))
        conn_prop = mdl.prop(mask_handle, conn_dict[idx] + "_conn")

        if mdl.get_property_value(conn_prop) == "Y" and not str(grounded) == "True" and created_ports:
            if idx == 0:
                new_port_N = created_ports.get("N1")
                # new_port_N = mdl.create_port(
                #     name="N1",
                #     parent=comp_handle,
                #     rotation='up',
                #     position=(x0 + 32, y0 + posY + 64),
                #     terminal_position=(-24, 48 * (num_windings - 1))
                # )
                if not mdl.get_item(f"N1n{str(idx + 1)}", parent=comp_handle, item_type="connection"):
                    mdl.create_connection(mdl.term(T_handle, "n" + str(idx + 1)), new_port_N, name=f"N1n{str(idx + 1)}")
            else:
                new_port_N = created_ports.get("N" + str(idx + 1))
                # new_port_N = mdl.create_port(
                #     name="N" + str(idx + 1),
                #     parent=comp_handle,
                #     flip="flip_horizontal",
                #     rotation='up',
                #     position=(x0 + 300, y0 + posY + 64 * idx),
                #     terminal_position=(24 - 16 * (num_windings - 1) + 16 * idx, 48 * (num_windings - 1))
                # )
                if not mdl.get_item(f"N{str(idx + 1)}n{str(idx + 1)}", parent=comp_handle, item_type="connection"):
                    mdl.create_connection(mdl.term(T_handle, "n" + str(idx + 1)), new_port_N, name=f"N{str(idx + 1)}n{str(idx + 1)}")
        elif mdl.get_property_value(conn_prop) == "Y":
            gnd = mdl.get_item("gnd", parent=comp_handle)
            if not gnd:
                gnd = mdl.create_component(
                    "core/Ground",
                    name="gnd",
                    parent=comp_handle,
                    position=(x0 + 150, y0 + 110 * num_windings)
                )
            if not mdl.get_item(f"gndn{str(idx + 1)}", parent=comp_handle, item_type="connection"):
                mdl.create_connection(mdl.term(gnd, "node"), mdl.term(T_handle, "n" + str(idx + 1)), name=f"gndn{str(idx + 1)}")

def update_subsystem_components(mdl, mask_handle, created_ports):
    comp_handle = mdl.get_parent(mask_handle)
    num_windings = int(mdl.get_property_value(mdl.prop(mask_handle, "num_windings")))

    trafo_tag_names = [f"TagT{phase}{winding}" for winding in "1234" for phase in "ABCN"]
    # Delete trafo tags
    for tag in trafo_tag_names:
        tag_handle = mdl.get_item(tag, parent=comp_handle, item_type="tag")
        if tag_handle:
            mdl.delete_item(tag_handle)

    T_handle = mdl.get_item("T1", parent=comp_handle)

    # Delete 3P transformer
    if T_handle:
        mdl.delete_item(T_handle)

    tr_dict = {2: "core/Three Phase Two Winding Transformer",
               3: "core/Three Phase Three Winding Transformer",
               4: "core/Three Phase Four Winding Transformer"}

    # Create new 3P transformer
    T_handle = mdl.create_component(
        tr_dict[num_windings],
        parent=comp_handle,
        name="T1",
        position=(x0 + 256, y0)
    )
    mdl.set_property_value(mdl.prop(T_handle, "input"), "SI")

    # Y positions
    if num_windings == 2:
        posA = [-96, -96]
        posA_term = -32
        posB = [0, 0]
        posB_term = 0
        posC = [96, 96]
        posC_term = 32
    else:
        posA = [-96, -346, -96, 154] if num_windings == 4 else [-96, -240, 48]
        posB = [y + 96 for y in posA]
        posC = [y + 96 for y in posB]

    # Create transformer tags
    trafo_tag_labels = [f"T_{phase}{winding}" for winding in "1234" for phase in "ABCN"]

    for idx in range(1, num_windings + 1):
        # A
        new_tag_A = mdl.create_tag(
            name=trafo_tag_names[4*(idx-1)],
            value=trafo_tag_labels[4*(idx-1)],
            scope='local',
            parent=comp_handle,
            flip="none" if idx == 1 else "flip_horizontal",
            rotation='up',
            position=(x0 + 60 if idx == 1 else x0 + 408, y0 - 96 if idx == 1 else y0 + posA[idx - 1])
        )

        if idx == 1:
            mdl.create_connection(mdl.term(T_handle, "prm_1"), new_tag_A)
        else:
            mdl.create_connection(mdl.term(T_handle, "sec_" + str(3 * (idx - 2) + 1)), new_tag_A)
        # B
        new_tag_B = mdl.create_tag(
            name=trafo_tag_names[4*(idx-1)+1],
            value=trafo_tag_labels[4*(idx-1)+1],
            scope='local',
            parent=comp_handle,
            flip="none" if idx == 1 else "flip_horizontal",
            rotation='up',
            position=(x0 + 60 if idx == 1 else x0 + 408, y0 if idx == 1 else y0 + posB[idx - 1])
        )
        if idx == 1:
            mdl.create_connection(mdl.term(T_handle, "prm_2"), new_tag_B)
        else:
            mdl.create_connection(mdl.term(T_handle, "sec_" + str(3 * (idx - 2) + 2)), new_tag_B)
        # C
        new_tag_C = mdl.create_tag(
            name=trafo_tag_names[4*(idx-1)+2],
            value=trafo_tag_labels[4*(idx-1)+2],
            scope='local',
            parent=comp_handle,
            flip="none" if idx == 1 else "flip_horizontal",
            rotation='up',
            position=(x0 + 60 if idx == 1 else x0 + 408, y0 + 96 if idx == 1 else y0 + posC[idx - 1])
        )
        if idx == 1:
            mdl.create_connection(mdl.term(T_handle, "prm_3"), new_tag_C)
        else:
            mdl.create_connection(mdl.term(T_handle, "sec_" + str(3 * (idx - 2) + 3)), new_tag_C)
        # N
        if not idx == 1:
            new_tag_N = mdl.create_tag(
                name=trafo_tag_names[4 * (idx - 1) + 3],
                value=trafo_tag_labels[4 * (idx - 1) + 3],
                scope='local',
                parent=comp_handle,
                flip="none" if idx == 1 else "flip_horizontal",
                rotation='up',
                position=(x0 + 60 if idx == 1 else x0 + 408, y0 + 48*(idx) + 90*(num_windings))
            )
            mdl.create_connection(mdl.term(T_handle, f"n{idx}"), new_tag_N)

    # Right ports and tags
    port_names = [f"{phase}{winding}" for winding in "234" for phase in "ABC"]
    tag_names = [f"Tag{phase}{winding}" for winding in "234" for phase in "ABC"]
    tag_labels = [f"T_{phase}{winding}" for winding in "234" for phase in "ABC"]

    # Delete tags
    for t in tag_names:
        t_handle = mdl.get_item(t, parent=comp_handle)
        if t_handle:
            mdl.delete_item(t_handle)

    porty0 = y0 - 48 * 3 * (num_windings - 1)
    for idx in range(1, 3 * (num_windings - 1) + 1):
        # A
        new_tag = mdl.create_tag(
            name=tag_names[idx - 1],
            value=tag_labels[idx - 1],
            scope='local',
            parent=comp_handle,
            flip="none",
            rotation='up',
            position=(x0 + 1080, porty0 + idx * 96)
        )
        new_port = created_ports.get(port_names[idx - 1])
        mdl.create_connection(new_tag, new_port)

    update_neutrals(mdl, mask_handle, T_handle, created_ports)
    vreg_connection(mdl, mask_handle)

def vreg_connection(mdl, mask_handle):
    comp_handle = mdl.get_parent(mask_handle)
    vreg_handle = mdl.get_item("Vreg", parent=comp_handle)

    # Defaults
    trafo_tag_names = [f"TagT{phase}{winding}" for winding in "1234" for phase in "ABC"]
    left_reg_tag_names = ["TagRegA1", "TagRegB1", "TagRegC1"]
    right_reg_tag_names = ["TagRegA2", "TagRegB2", "TagRegC2"]
    port_tag_names = [f"Tag{phase}{winding}" for winding in "1234" for phase in "ABC"]

    trafo_labels = [f"T{phase}_{winding}" for winding in "1234" for phase in "ABC"]

    mdl.disable_items(vreg_handle)

    for idx, tag in enumerate(left_reg_tag_names):
        this_tag = mdl.get_item(tag, parent=comp_handle, item_type="tag")
        if this_tag:
            mdl.set_tag_properties(this_tag, value="not_used", scope='local')
    for idx, tag in enumerate(right_reg_tag_names):
        this_tag = mdl.get_item(tag, parent=comp_handle, item_type="tag")
        if this_tag:
            mdl.set_tag_properties(this_tag, value="not_used", scope='local')
    for idx, tag in enumerate(trafo_tag_names):
        this_tag = mdl.get_item(tag, parent=comp_handle, item_type="tag")
        if this_tag:
            mdl.set_tag_properties(this_tag, value=trafo_labels[idx], scope='local')
    for idx, tag in enumerate(port_tag_names):
        this_tag = mdl.get_item(tag, parent=comp_handle, item_type="tag")
        if this_tag:
            mdl.set_tag_properties(this_tag, value=trafo_labels[idx], scope='local')

    regcontrol_on = mdl.get_property_value(mdl.prop(mask_handle, "regcontrol_on"))

    if regcontrol_on:
        mdl.enable_items(vreg_handle)
        ctrl_winding = mdl.get_property_value(mdl.prop(mask_handle, "ctrl_winding"))
        n_ctrl = ctrl_winding[-1]  # Get number of the ctrl winding
        trafo_tag_names = [f"TagTA{n_ctrl}", f"TagTB{n_ctrl}", f"TagTC{n_ctrl}"]
        port_tag_names = [f"TagA{n_ctrl}", f"TagB{n_ctrl}", f"TagC{n_ctrl}"]

        trafo_labels = [f"TA_{n_ctrl}", f"TB_{n_ctrl}", f"TC_{n_ctrl}"]
        port_labels = [f"Reg_A2", f"Reg_B2", f"Reg_C2"]

        for idx, tag in enumerate(left_reg_tag_names):
            this_tag = mdl.get_item(tag, parent=comp_handle, item_type="tag")
            if this_tag:
                mdl.set_tag_properties(this_tag, value=trafo_labels[idx], scope='local')
        for idx, tag in enumerate(right_reg_tag_names):
            this_tag = mdl.get_item(tag, parent=comp_handle, item_type="tag")
            if this_tag:
                mdl.set_tag_properties(this_tag, value=port_labels[idx], scope='local')
        for idx, tag in enumerate(trafo_tag_names):
            this_tag = mdl.get_item(tag, parent=comp_handle, item_type="tag")
            if this_tag:
                mdl.set_tag_properties(this_tag, value=trafo_labels[idx], scope='local')
        for idx, tag in enumerate(port_tag_names):
            this_tag = mdl.get_item(tag, parent=comp_handle, item_type="tag")
            if this_tag:
                mdl.set_tag_properties(this_tag, value=port_labels[idx], scope='local')

        # Internal Vreg labels (Y or D connection)
        left_autotrafo_tag_names = [f"TagAuto{n}{phase}1" for n in "123" for phase in "B"]
        right_autotrafo_tag_names = [f"TagAuto{n}{phase}2" for n in "123" for phase in "B"]

        for idx, tag in enumerate(left_autotrafo_tag_names):
            this_tag = mdl.get_item(tag, parent=vreg_handle, item_type="tag")
            if this_tag:
                mdl.set_tag_properties(this_tag, value="N", scope='local')
        for idx, tag in enumerate(right_autotrafo_tag_names):
            this_tag = mdl.get_item(tag, parent=vreg_handle, item_type="tag")
            if this_tag:
                mdl.set_tag_properties(this_tag, value=f"N{idx}", scope='local')

def update_regctrl_combo(mdl, mask_handle):
    num_windings = mdl.get_property_disp_value(mdl.prop(mask_handle, "num_windings"))
    combo_vals = [f"Winding {n}" for n in range(1, int(num_windings) + 1)]
    mdl.set_property_combo_values(mdl.prop(mask_handle, "ctrl_winding"), combo_vals)


def validate_properties(mdl, mask_handle):
    # Validate lengths
    comp_handle = mdl.get_parent(mask_handle)
    num_windings = int(mdl.get_property_value(mdl.prop(comp_handle, "num_windings")))

    prop_names = ["KVs", "KVAs", "percentRs", "XArray"]

    for prop_name in prop_names:
        prop_handle = mdl.prop(mask_handle, prop_name)
        prop_value = mdl.get_property_value(prop_handle)

        base_str = mdl.get_name(comp_handle) + " -- Incorrect number of array elements for the"

        if not prop_name == "XArray":
            if not len(prop_value) == num_windings:
                mdl.info(f'{base_str} {prop_name} property: {len(prop_value)} ({num_windings} expected)')
        else:
            if type(prop_value) == float or type(prop_value) == int:
                prop_value = [prop_value]
            if not len(prop_value) == num_windings:
                mdl.info(f'{base_str} {prop_name} property: {len(prop_value)} ({num_windings} expected)')


def convert_all_properties(mdl, mask_handle, prop_names=None):
    comp_handle = mdl.get_parent(mask_handle)
    num_windings = int(mdl.get_property_value(mdl.prop(mask_handle, "num_windings")))
    T_inner = mdl.get_item("T1", parent=comp_handle)
    regcontrol_on = mdl.get_property_value(mdl.prop(mask_handle, "regcontrol_on"))

    if not prop_names:
        prop_names = ["KVs", "KVAs", "Basefreq", "percentRs", "percentNoloadloss", "percentimag", "XArray"]

    try:
        for prop_name in prop_names:
            prop_handle = mdl.prop(mask_handle, prop_name)
            prop_value = mdl.get_property_value(prop_handle)

            if type(prop_value) == float or type(prop_value) == int:
                prop_value = [prop_value]

            # Power
            if prop_name == "KVAs":
                Sn_prop = mdl.prop(T_inner, "Sn")
                converted_value = prop_value[0] * 1000
                mdl.set_property_value(Sn_prop, converted_value)
            # Frequency
            elif prop_name == "Basefreq":
                prop_value = prop_value[0]
                f_prop = mdl.prop(T_inner, "f")
                converted_value = prop_value
                mdl.set_property_value(f_prop, converted_value)
            # Nominal voltages
            elif prop_name == "KVs":
                for num in range(1, num_windings + 1):
                    V_prop = mdl.prop(T_inner, "V" + str(num))
                    converted_value = 1000 * prop_value[num - 1]
                    mdl.set_property_value(V_prop, converted_value)
            # Resistances
            elif prop_name == "percentRs":
                KVs_prop = mdl.prop(comp_handle, "KVs")
                KVAs_prop = mdl.prop(comp_handle, "KVAs")
                KVs = mdl.get_property_value(KVs_prop)
                KVAs = mdl.get_property_value(KVAs_prop)
                for num in range(1, num_windings + 1):
                    R_prop = mdl.prop(T_inner, "R" + str(num))
                    a = KVs[0] / KVs[num - 1]
                    baseR = KVs[0] * KVs[0] / KVAs[0] * 1000
                    ''' Account for winding type '''
                    conn = 'prim_conn' if num == 1 else f'sec{num - 1}_conn'
                    YD = mdl.get_property_value(mdl.prop(comp_handle, conn))
                    factor = 1 if YD == 'Y' else 3
                    ''' ------------------------ '''
                    converted_value = factor * (
                                baseR / 100 * prop_value[num - 1]) / a ** 2
                    # if regcontrol_on:
                    #     converted_value = converted_value*0.99
                    mdl.set_property_value(R_prop, converted_value)
            # Magnetization
            elif prop_name in ["percentNoloadloss", "percentimag"]:
                prop_value = prop_value[0]
                KVs_prop = mdl.prop(comp_handle, "KVs")
                KVAs_prop = mdl.prop(comp_handle, "KVAs")
                KVs = mdl.get_property_value(KVs_prop)
                KVAs = mdl.get_property_value(KVAs_prop)
                baseV = KVs[0] * 1000
                baseP = KVAs[0] * 1000
                if prop_name == "percentNoloadloss":
                    try:
                        ''' Account for winding type '''
                        YD = mdl.get_property_value(mdl.prop(comp_handle, 'prim_conn'))
                        factor = 1 if YD == 'Y' else 3
                        ''' ------------------------ '''
                        converted_value = factor * ((baseV * baseV) / baseP) / (
                                    prop_value / 100)  # baseV*baseV/(baseP*prop_value/100)
                        # if converted_value >= 0.99e5:
                        #    converted_value = "inf"
                    except ZeroDivisionError:
                        converted_value = "inf"
                    Rm_prop = mdl.prop(T_inner, "Rm")
                    mdl.set_property_value(Rm_prop, converted_value)
                elif prop_name == "percentimag":
                    ''' Account for winding type '''
                    YD = mdl.get_property_value(mdl.prop(comp_handle, 'prim_conn'))
                    factor = 1 if YD == 'Y' else 3
                    ''' ------------------------ '''
                    baseI = baseP / baseV
                    Lm_prop = mdl.prop(T_inner, "Lm")
                    Basefreq = mdl.get_property_value(mdl.prop(mask_handle, "Basefreq"))
                    if not prop_value <= 0:
                        converted_value = factor * ((baseV * baseV) / baseP) / (prop_value / 100) / (
                                    2 * np.pi * Basefreq)
                    else:
                        converted_value = "inf"
                    mdl.set_property_value(Lm_prop, converted_value)
            # Inductances
            elif prop_name == "XArray":
                KVs_prop = mdl.prop(comp_handle, "KVs")
                KVAs_prop = mdl.prop(comp_handle, "KVAs")
                KVs = mdl.get_property_value(KVs_prop)
                KVAs = mdl.get_property_value(KVAs_prop)
                Basefreq = mdl.get_property_value(mdl.prop(mask_handle, "Basefreq"))
                reactances_pct = prop_value
                xsc_array = []

                for num in range(1, num_windings + 1):
                    base_prim = KVs[0] * KVs[0] / KVAs[0] * 1000

                    ''' Account for winding type '''
                    conn = 'prim_conn' if num == 1 else f'sec{num - 1}_conn'
                    YD = mdl.get_property_value(mdl.prop(comp_handle, conn))
                    factor = 1 if YD == 'Y' else 3
                    ''' ------------------------ '''

                    a = KVs[0] / KVs[num - 1]
                    ind = factor*reactances_pct[num - 1] * base_prim / 100 / 2 / np.pi / Basefreq / a ** 2
                    # if regcontrol_on:
                    #     ind = ind*0.99
                    L_prop = mdl.prop(T_inner, "L" + str(num))
                    converted_value = ind
                    mdl.set_property_value(L_prop, converted_value)

                xsc_idxs = list(combinations(range(num_windings), 2))
                for idx in xsc_idxs:
                    xsc_array.append(reactances_pct[idx[0]] + reactances_pct[idx[1]])

                mdl.set_property_value(mdl.prop(comp_handle, "XscArray"), str(xsc_array))
        set_autotrafo_properties(mdl, mask_handle)

    except IndexError:
        mdl.error(f"Make sure the arrays match the size required for {num_windings} windings.")

def set_autotrafo_properties(mdl, mask_handle):
    comp_handle = mdl.get_parent(mask_handle)
    regcontrol_on = mdl.get_property_value(mdl.prop(mask_handle, "regcontrol_on"))
    if regcontrol_on:
        vreg_handle = mdl.get_item("Vreg", parent=comp_handle)
        t_inner_handle = mdl.get_item("T1", parent=comp_handle)
        autotrafo_handle = mdl.get_item("Auto1", parent=vreg_handle)

        for prop_name in ["R1", "R2", "L1", "L2", "Rm", "Lm", "n_taps", "reg_range"]:
            at_prop = mdl.prop(autotrafo_handle, prop_name)

            if prop_name == "n_taps":
                numtaps = mdl.get_property_value(mdl.prop(mask_handle, "numtaps"))
                mdl.set_property_value(at_prop, int(numtaps))
            elif prop_name == "reg_range":
                maxtap = mdl.get_property_value(mdl.prop(mask_handle, "maxtap"))
                mintap = mdl.get_property_value(mdl.prop(mask_handle, "mintap"))
                regrange = max((float(maxtap)-1), (1-float(mintap)))*100
                mdl.set_property_value(at_prop, regrange)
            elif prop_name in ["Rm", "Lm"]:
                t_prop = mdl.prop(t_inner_handle, prop_name)
                t_prop_value = mdl.get_property_value(t_prop)
                mdl.set_property_value(at_prop, t_prop_value)
            else:
                ctrl_winding = mdl.get_property_value(mdl.prop(mask_handle, "ctrl_winding"))
                n_ctrl = ctrl_winding[-1]  # Get number of the ctrl winding
                orig_prop_name = prop_name[0] + str(n_ctrl)
                t_prop = mdl.prop(t_inner_handle, orig_prop_name)
                t_prop_value = mdl.get_property_value(t_prop)
                mdl.set_property_value(at_prop, float(t_prop_value/1000))

def show_hide_ground(mdl, prop_handle, mask_handle):
    prop_name = mdl.get_name(prop_handle)
    grd_prop = mdl.prop(mask_handle, "grounded_" + prop_name[:4]);
    if mdl.get_property_disp_value(mdl.prop(mask_handle, prop_name)) == "Y":
        mdl.show_property(grd_prop)
    else:
        mdl.hide_property(grd_prop)
        mdl.set_property_value(grd_prop, False)


def show_hide_conn(mdl, mask_handle):
    num_windings = int(mdl.get_property_disp_value(mdl.prop(mask_handle, "num_windings")))

    p = ["prim", "sec1", "sec2", "sec3"]

    for idx in range(4):
        conn_prop = mdl.prop(mask_handle, p[idx] + "_conn");
        grd_prop = mdl.prop(mask_handle, "grounded_" + p[idx])
        if idx < num_windings:
            if not mdl.is_property_visible(conn_prop):
                mdl.show_property(conn_prop)
                conn_value = mdl.get_property_value(conn_prop)
                if conn_value == "Y":
                    mdl.show_property(grd_prop)
                else:
                    mdl.hide_property(grd_prop)
        else:
            mdl.hide_property(conn_prop)
            mdl.hide_property(grd_prop)


def show_hide_couplings(mdl, mask_handle):
    num_windings = int(mdl.get_property_disp_value(mdl.prop(mask_handle, "num_windings")))

    if num_windings == 2:
        coup_prop = mdl.prop(mask_handle, "embedded_cpl")
        mdl.show_property(coup_prop)
        for n in range(2, 5):
            coup_prop = mdl.prop(mask_handle, "embedded_cpl_1" + str(n))
            mdl.hide_property(coup_prop)
    else:
        coup_prop = mdl.prop(mask_handle, "embedded_cpl")
        mdl.hide_property(coup_prop)
        for n in range(2, 5):
            coup_prop = mdl.prop(mask_handle, "embedded_cpl_1" + str(n))
            if n < num_windings + 1:
                mdl.show_property(coup_prop)
            else:
                mdl.hide_property(coup_prop)


def update_winding_configs(mdl, prop_handle, mask_handle, created_ports):
    comp_handle = mdl.get_parent(mask_handle)
    num_windings = int(mdl.get_property_value(mdl.prop(mask_handle, "num_windings")))
    T_inner = mdl.get_item("T1", parent=comp_handle)

    wdg_num_dict = {"prim": "1", "sec1": "2", "sec2": "3", "sec3": "4"}
    wdg_conn_dict = {"Y": "Y", "Δ": "D"}
    wdg_clock_dict = {"Y": "0", "Δ": "1"}

    YorD_prim = mdl.get_property_value(mdl.prop(comp_handle, "prim_conn"))

    wdg_name = mdl.get_name(prop_handle)[:4]
    if wdg_name == "grou":
        # Passed by grounded property
        wdg_name = mdl.get_name(prop_handle)[-4:]
        YorD = mdl.get_property_value(mdl.prop(mask_handle, wdg_name + "_conn"))
    else:
        # Passed by conn property
        YorD = mdl.get_property_value(prop_handle)

    if int(wdg_num_dict[wdg_name]) <= num_windings:
        inner_conn_prim_prop = mdl.prop(T_inner, "winding_1_connection")
        inner_conn_prop = mdl.prop(T_inner, "winding_" + wdg_num_dict[wdg_name] + "_connection")

        mdl.set_property_value(inner_conn_prop, wdg_conn_dict[YorD])

        if int(wdg_num_dict[wdg_name]) > 1:  # Secondaries
            if num_windings == 2:
                inner_clock_prop = mdl.prop(T_inner, "clock_number")
                if not YorD == YorD_prim:
                    mdl.set_property_value(inner_clock_prop, "1")
                else:
                    mdl.set_property_value(inner_clock_prop, "0")
            else:
                inner_clock_prop = mdl.prop(T_inner, "clk_num_1" + wdg_num_dict[wdg_name])
                if not YorD == YorD_prim:
                    mdl.set_property_value(inner_clock_prop, "1")
                else:
                    mdl.set_property_value(inner_clock_prop, "0")
        else:  # Primary
            # Update all others
            prop_names = ["sec1_conn", "sec2_conn", "sec3_conn"]
            for p in prop_names:
                update_winding_configs(mdl, mdl.prop(mask_handle, p), mask_handle, created_ports)

    update_neutrals(mdl, mask_handle, T_inner, created_ports=created_ports)

    mdl.refresh_icon(mask_handle)


def update_all_windings(mdl, mask_handle, created_ports):
    prop_names = ["prim_conn", "sec1_conn", "sec2_conn", "sec3_conn"]
    for p in prop_names:
        update_winding_configs(mdl, mdl.prop(mask_handle, p), mask_handle, created_ports)

def calculate_winding_voltage(mdl, mask_handle):

    winding_voltage_prop = mdl.prop(mask_handle, "winding_voltage")

    vreg_prop = mdl.prop(mask_handle, "vreg")
    vreg = mdl.get_property_disp_value(vreg_prop)

    ptratio_prop = mdl.prop(mask_handle, "ptratio")
    ptratio = mdl.get_property_disp_value(ptratio_prop)

    def try_calculation(vreg, ptratio):

        try:
            vreg = float(vreg)
        except:
            try:
                vreg = float(mdl.get_ns_var(vreg))
            except:
                mdl.set_property_disp_value(winding_voltage_prop, f"Variable {vreg} is invalid (make sure to compile once)")
                return

        try:
            ptratio = float(ptratio)
        except:
            try:
                ptratio = float(mdl.get_ns_var(ptratio))
            except:
                mdl.set_property_disp_value(winding_voltage_prop, f"Variable {ptratio} is invalid (make sure to compile once)")
                return

        mdl.set_property_disp_value(winding_voltage_prop, str(vreg * ptratio * np.sqrt(3)))
        mdl.set_property_value(winding_voltage_prop, str(vreg * ptratio * np.sqrt(3)))

        return

    try_calculation(vreg, ptratio)


def toggle_regcontrol_props(mdl, mask_handle):

    regcontrol_on_prop = mdl.prop(mask_handle, "regcontrol_on")
    regcontrol_on = mdl.get_property_disp_value(regcontrol_on_prop)

    props_list = ["ctrl_winding", "vreg", "ptratio", "winding_voltage", "band", "delay", "mintap",
                  "maxtap", "numtaps", "execution_rate"]

    if regcontrol_on:
        for i in range(len(props_list)):
            prop = mdl.prop(mask_handle, props_list[i])
            mdl.enable_property(prop)
    else:
        for i in range(len(props_list)):
            prop = mdl.prop(mask_handle, props_list[i])
            mdl.disable_property(prop)

def toggle_frequency_prop(mdl, mask_handle, init=False):
    frequency_prop = mdl.prop(mask_handle, "Basefreq")
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


def update_frequency_property(mdl, mask_handle, init=False):

    frequency_prop = mdl.prop(mask_handle, "Basefreq")
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

def mask_dialog_dynamics(mdl, mask_handle, caller_prop_handle=None, init=False):
    toggle_frequency_prop(mdl, mask_handle)

def port_dynamics(mdl, mask_handle, caller_prop_handle=None, init=False):
    comp_handle = mdl.get_parent(mask_handle)
    deleted_ports = []
    created_ports = {}

    comp_handle = mdl.get_parent(mask_handle)
    num_windings = int(mdl.get_property_value(mdl.prop(mask_handle, "num_windings")))
    conn_dict = ["prim", "sec1", "sec2", "sec3"]
    posY = 346 if num_windings == 4 else 240

    for i in range(1, 5):
        if delete_port(mdl, "N" + str(i), comp_handle):
            deleted_ports.append("N" + str(i))

    port_names = [f"{phase}{winding}" for winding in "234" for phase in "ABC"]
    if caller_prop_handle and mdl.get_name(caller_prop_handle) == "num_windings":
        # Delete ports
        for p in port_names:
            if delete_port(mdl, p, comp_handle):
                deleted_ports.append(p)
    for idx in range(0, num_windings):
        grounded = mdl.get_property_value(mdl.prop(mask_handle, "grounded_" + conn_dict[idx]))
        conn_prop = mdl.prop(mask_handle, conn_dict[idx] + "_conn")

        if mdl.get_property_value(conn_prop) == "Y" and not str(grounded) == "True":
            if idx == 0:
                new_port_N = mdl.create_port(
                    name="N1",
                    parent=comp_handle,
                    rotation='up',
                    position=(x0 + 32, y0 + posY + 64),
                    terminal_position=(-24, 48 * (num_windings - 1))
                )
                created_ports.update({"N1": new_port_N})
            else:
                new_port_n = mdl.get_item("N" + str(idx + 1), parent=comp_handle, item_type="port")
                if not new_port_n:
                    new_port_n = mdl.create_port(
                        name="N" + str(idx + 1),
                        parent=comp_handle,
                        flip="flip_horizontal",
                        rotation='up',
                        position=(x0 + 300, y0 + posY + 64 * idx),
                        terminal_position=(24 - 16 * (num_windings - 1) + 16 * idx, 48 * (num_windings - 1))
                    )
                    created_ports.update({"N" + str(idx + 1): new_port_n})

    porty0 = y0 - 48 * 3 * (num_windings - 1)
    for idx in range(1, 3 * (num_windings - 1) + 1):
        new_port = mdl.get_item(port_names[idx - 1], parent=comp_handle, item_type="port")
        if not new_port:
            new_port = mdl.create_port(
                name=port_names[idx - 1],
                parent=comp_handle,
                flip="flip_horizontal",
                rotation='up',
                position=(x0 + 1180, porty0 + idx * 96),
                terminal_position=(32, - 16 - 16 * 3 * (num_windings - 1) + idx * 32)
            )
        created_ports.update({port_names[idx - 1]: new_port})
    return created_ports, deleted_ports

def define_icon(mdl, mask_handle):
    images = {
        "2": "t_3p2w.svg",
        "3": "t_3p3w.svg",
        "4": "t_3p4w.svg"
    }
    num_windings = mdl.get_property_value(mdl.prop(mask_handle, "num_windings"))

    mdl.set_component_icon_image(mask_handle, "images/" + images[num_windings])

    mdl.set_color(mask_handle, "blue")
    wdg_names = ["prim", "sec1", "sec2", "sec3"]
    for wdg_name in wdg_names[:int(num_windings)]:
        conn_prop = mdl.prop(mask_handle, wdg_name + "_conn")
        conn_value = mdl.get_property_value(conn_prop)
        if wdg_name == "prim":
            mdl.disp_component_icon_text(mask_handle, conn_value, rotate="rotate", relpos_x=0.2,
                                         relpos_y=(48 * (int(num_windings) - 2) + 8) / (
                                                     96 + 96 * (int(num_windings) - 2)), size=8, trim_factor=0.7)
        else:
            sec_num = int(wdg_name[-1])
            mdl.disp_component_icon_text(mask_handle, conn_value, rotate="rotate", relpos_x=0.8,
                                         relpos_y=(96 * (sec_num - 1) + 8) / (96 * (int(num_windings) - 1)), size=8,
                                         trim_factor=0.7)