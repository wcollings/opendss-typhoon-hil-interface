from .base import *
from ...output_functions import *

class Line(TwoTerminal):
    """ Converted component class. """

    def __init__(self, converted_comp_type, name, circuit, tse_properties, tse_component):
        self.type = converted_comp_type
        self.name = name
        self.circuit = circuit

        # Some TSE components require more than one instance/class
        self.created_instances_list = [self]

        # Number of phases
        self.num_phases = self.define_number_of_phases(self, tse_properties, tse_component)
        # Number of buses
        self.num_buses = self.define_number_of_buses(self, tse_properties, tse_component)
        # Floating neutral
        self.floating_neutral = self.is_neutral_floating(self, tse_properties, tse_component)

        # Get bus connections list
        self.buses = return_bus_connections(tse_component, self.num_buses, self.num_phases, self.floating_neutral)

        # Filter unused TSE properties and create new ones
        self.new_format_properties = self.create_new_format_properties_dict(self, tse_properties, tse_component)

        # Run parent initialization code
        super().__init__(name, circuit, self.buses, dss_properties=self.new_format_properties)

        # Create monitoring lines
        create_monitors(self, tse_properties, tse_component)

        # Apply extra necessary conversion steps
        self.extra_conversion_steps(self, tse_properties, tse_component)

    @staticmethod
    def create_new_format_properties_dict(self, tse_properties, tse_component):
        """ Filters unused TSE properties and creates new ones. Returns a dictionary with the new properties. """

        if tse_properties['input_type'] == "LineCode":
            new_format_properties = {"LineCode": tse_properties['selected_object'],
                                     "Length": tse_properties['Length']}

        elif tse_properties['input_type'] == "Matrix":
            tse_props_copy = dict(tse_properties)
            for p in ["rmatrix", "xmatrix", "cmatrix"]:
                tse_props_copy[p] = convert_matrix_format(tse_props_copy[p], self.num_phases)
            new_format_properties = {k: v for k, v in tse_props_copy.items() if
                                     k in ["Length", "rmatrix", "xmatrix", "cmatrix"]}
        else:
            new_format_properties = {k: v for k, v in tse_properties.items() if
                                     k in ["Length", "R1", "R0", "X1", "X0", "C1", "C0"]}

        # Specify the base frequency if not inheriting the global value

        if tse_properties['global_basefreq'] == "False":
            new_format_properties["BaseFreq"] = tse_properties['BaseFreq']
        return new_format_properties

    @staticmethod
    def define_number_of_phases(self, tse_properties, tse_component):
        """ Returns the number of phases of the component. """

        phases = int(tse_properties.get('phases'))

        num_phases = phases if phases else 3

        return num_phases

    @staticmethod
    def define_number_of_buses(self, tse_properties, tse_component):
        """ Returns the number of buses the component is connected to. """

        num_buses = 2

        return num_buses

    @staticmethod
    def is_neutral_floating(self, tse_properties, tse_component):
        """ Floating neutrals connect to an unused bus node """

        return False

    @staticmethod
    def extra_conversion_steps(self, tse_properties, tse_component):
        """ Applies extra necessary conversion steps. """

        pass

    def output_line(self):
        """ Overrides parent output_line method. """

        if not self.num_phases == 3:
            params = [f'{param}={self.new_format_properties.get(param)}' for param in self.new_format_properties]
            return f'new {self.identifier()} phases={self.num_phases} Bus1={self.buses[0]}' \
                   f'{" Bus2=" + self.buses[1] if len(self.buses) == 2 else ""} {" ".join(params)}\n'
        else:
            return super().output_line()

    def created_component_instances(self):
        """ Some TSE components may result in multiple converted components. """

        return self.created_instances_list