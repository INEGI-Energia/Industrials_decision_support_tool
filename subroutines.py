import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import cantera as ct

def data():
    """
    The present function serves to aquire the data necessary to the tool to fucntion.
    Vector - energy vector name
    PCI units - MJ/kg
    Density units - kg/m3 considering PTN conditions
    Emission factor units - kgCO2eq/kWh
    Reference tariff units - €/kWh
    """
    #Data table saving
    data_table = {"Vector":["Biometano", "Hidrogénio", "Biomassa", "Eletricidade", "Gás natural", "GPL", "Nafta", "Gasóleo", "Fuelóleo", "Coque de petróleo", "Residuos industriais"],\
                   "PCI":[48, 120, 17.5 , None, 45, 46.4, 44.4, 42.7, 41.9, 32.5, 18.5], \
                   "Density":[0.7, 0.0899, None, None, 0.84, 2.43, 680, 837, 944, 800, 200], \
                    "Emission factor":[0.039996, 0, 0, 0.151, 0.20305, 0.22718, 0.26496, 0.26676, 0.28296, 0.33696, 0.52164], \
                    "Reference tariff":[0.112, 0.195, 0.010, 0.126, 0.078, 0.109, 0.056, 0.161, 0.103, 0.040, None],\
                    "Specific gravity":[0.554, 0.0696, None, None, 0.7, None, None, None, None, None, None],\
                    "Minimum ignition energy": [0.20, 0.02, None, None, 0.20, None, None, None, None, None, None]}
    
    
    #convert data_table to DataFrame for future use
    df = pd.DataFrame(data_table)
    
    return df

def flammablity_data():
    #Flammability limits calculation
    flammabality_data = {"Vector":["Hidrogénio", "Biometano", "Gás natural"],\
                         "LFL":[4, 4, 4.13],
                         "HFL":[75, 16, 15.77]}
    df_flammability = pd.DataFrame(flammabality_data)

    return df_flammability

#Load DataFrame
data_df = data()
flammablity_df = flammablity_data()
#Emission tax
emissions_tax = 77.210 #€/tonCO2eq


"""
In order to make the code abler to be implemented in web it will be created an object for each equipment to be inserted
Equipment will be selected between a list of possibilities
Nominal power units - kW
Energy vector will be selected between a list of possibilities
Anual consumption is inserted and then the unit will be chosen  
"""
class Equipment():
    #class variable containing allowed options for object creation
    allowed_equipments = ["Forno", "Caldeira", "Cogeração", "Queimador (Dedicado a estufas ou banhos térmicos)"]
    allowed_vector = data_df["Vector"].tolist()
    allowed_consumption_unit = ["kWh/ano", "ton/ano", "m3/ano"]
    
    tariffs = {}  # Static variable to hold tariffs for energy vectors
    
    def __init__(self, equipment, nominal_power, energy_vector, anual_consumption=None, consumption_unit=None):
        self.name = None
        self.equipment = equipment
        self.nominal_power = nominal_power
        self.energy_vector = energy_vector
        self.anual_consumption = anual_consumption
        self.consumption_unit = consumption_unit

        if equipment not in self.allowed_equipments:
            raise ValueError(f"(equipment) is not a valid one. Choose from {self.allowed_equipments}")
        
        if energy_vector not in self.allowed_vector and energy_vector != None:
            raise ValueError(f"(vector) is not a valid one. Choose from {self.allowed_vector}")
        
        if consumption_unit not in self.allowed_consumption_unit and consumption_unit != None:
            raise ValueError(self.consumption_unit, f" is not a valid one. Choose from {self.allowed_consumption_unit}")
        
        if energy_vector == "Eletricidade" and consumption_unit != "kWh/ano":
            raise ValueError(consumption_unit, f" is not a valid one. It could only be kWh/ano for electricity")
          
    def energy_consumption_calc(self):
        """
        Calculation of anual energy consumption. For cases where the specified unit is not in energy basis (kWh/year) it is realized a conversion that takes into
        account the values presented in the dataFrame.
        """
        if self.consumption_unit == "kWh/ano":
            self.anual_energy_consumption = self.anual_consumption

        elif self.consumption_unit == "ton/ano":
            self.vector_pci = data_df.loc[data_df['Vector'] == self.energy_vector, 'PCI'].values[0]
            self.anual_energy_consumption = self.anual_consumption * (self.vector_pci/3.6*1000)

        elif self.consumption_unit == "m3/ano":
            self.vector_pci = data_df.loc[data_df['Vector'] == self.energy_vector, 'PCI'].values[0]
            vector_density = data_df.loc[data_df['Vector'] == self.energy_vector, 'Density'].values[0]
            self.anual_energy_consumption = self.anual_consumption * (self.vector_pci*vector_density/3.6)
        return self.anual_energy_consumption

    def base_emissions_calculation(self):
        """Calculation of anual emissions of each equipment based on the anual energy consumption."""
        vector_emission_factor = data_df.loc[data_df['Vector'] == self.energy_vector, 'Emission factor'].values[0]
        self.base_emissions = vector_emission_factor * self.anual_energy_consumption
        return self.base_emissions
    
    def energy_costs_calculation(self):
        """Calculation of energy costs of each equipment based on anual energy consumption"""
        self.vector_tariff = data_df.loc[data_df['Vector'] == self.energy_vector, 'Reference tariff'].values[0]
        self.energy_costs = self.vector_tariff * self.anual_energy_consumption


"""
For the cases where each specific equipment consumption isn't known the Factory class enters
The whole consumption per vector is given and it distributes this per equipment
"""
class Factory:
    def __init__(self, vector_information=None):
        """
        total_energy_by_vector: Dictionary with total energy by vector
        Example: "Gás natural": 30000, kwh/ano
        """
        self.equipments = []
        self.vector_information = vector_information

        """
        Adds or updates an energy vector with its consumption and units.

        Parameters:
        vector_name (str): Name of the energy vector (e.g., "Gás natural").
        consumption (float): Total energy consumption (e.g., 30000).
        units (str): Unit of measurement for the consumption (e.g., "kWh/year").
        """
    
    def info_analysis(self):
        for vector_name, details in self.vector_information.items():
            consumption = details["energy_consumption"]
            units = details["consumption_unit"]
            if vector_name not in Equipment.allowed_vector:
                raise ValueError(f"{vector_name} is not a valid energy vector. Choose from {Equipment.allowed_vector}")
            if consumption <= 0:
                raise ValueError(f"{vector_name} has not a valid energy consumption. It should be greater than 0")
            if units not in Equipment.allowed_consumption_unit:
                raise ValueError(f"{units} is not a valid unit. Choose from {Equipment.allowed_consumption_unit}")           
            if vector_name == "Eletricidade" and units != "kWh/ano":
                raise ValueError(units, f" is not a valid one. It could only be kWh/ano for electricity")
            
            # Store vector info as a nested dictionary
            self.vector_information[vector_name] = {"energy_consumption": consumption, "consumption_unit": units}                   

    def add_equipment(self, equipment: Equipment):
        """Add equipment to the factory."""
        self.equipments.append(equipment)
    
    def energy_consumption_calc(self):
        #Converts the energy consumption per vector to kWh/year so that all calculations are made the same way
        for vector, details in self.vector_information.items():
            if details['consumption_unit'] == 'kWh/ano':
                details['Real Consumption'] = details['energy_consumption']

            if details['consumption_unit'] == 'm3/ano':
                self.vector_pci = data_df.loc[data_df['Vector'] == vector, 'PCI'].values[0]
                vector_density = data_df.loc[data_df['Vector'] == vector, 'Density'].values[0]
                details['Real Consumption'] = details['energy_consumption'] * (self.vector_pci*vector_density/3.6)

            if details['consumption_unit'] == 'ton/ano':
                self.vector_pci = data_df.loc[data_df['Vector'] == vector, 'PCI'].values[0]
                self.anual_energy_consumption = details['energy_consumption'] * (self.vector_pci/3.6*1000)    

    def energy_distribuiton(self):
        # Iterate over each energy vector and its details
        for vector, details in self.vector_information.items():
            vector_power = 0
            # Calculate the total nominal power for all equipment that use the current vector
            for equipment in self.equipments:
                if vector == equipment.energy_vector:
                    vector_power += equipment.nominal_power
            # Distribute the vector's total power proportionally to each relevant equipment
            for equipment in self.equipments:
                if vector == equipment.energy_vector:
                    equipment.anual_energy_consumption = (equipment.nominal_power / vector_power) * details["energy_consumption"]

    def equipment_base_emissions_calculation(self):
        """Calculation of anual emissions of each equipment based on the anual energy consumption."""
        for equipment in self.equipments:
            vector_emission_factor = data_df.loc[data_df['Vector'] == equipment.energy_vector, 'Emission factor'].values[0]
            equipment.base_emissions = vector_emission_factor * equipment.anual_energy_consumption            
        
    def energy_costs_calculation(self):
        """Calculation of energy costs of each equipment based on anual energy consumption"""
        for equipment in self.equipments:
            self.vector_tariff = data_df.loc[data_df['Vector'] == equipment.energy_vector, 'Reference tariff'].values[0]
            equipment.energy_costs = self.vector_tariff * equipment.anual_energy_consumption


class Energy_vector():
    ##class variable containing allowed options for object creation
    allowed_vector = data_df["Vector"].tolist()
    allowed_cost_unit = ["€/kWh", "€/ton", "€/m3"]
    
    def __init__(self, energy_vector, vector_tariff, tariff_unit):
        self.energy_vector = energy_vector
        self.vector_tariff = vector_tariff
        self.tariff_unit = tariff_unit
    
        if energy_vector not in self.allowed_vector:
                raise ValueError(energy_vector, f" is not a valid one. Choose from {self.allowed_vector}")        
        if vector_tariff < 0:
                raise ValueError(vector_tariff, f" is not a valid one. It must be higher than 0.")        
        if tariff_unit not in self.allowed_cost_unit:
                raise ValueError(tariff_unit, f" is not a valid one. Choose from {self.allowed_cost_unit}")
        if energy_vector == "Eletricidade" and tariff_unit != "€/kWh":
                raise ValueError(tariff_unit, f" is not a valid one. It could only be €/kWh for electricity")

    def tariff_conversion(self):
        if self.tariff_unit == "€/kWh":
            self.vector_tariff = self.vector_tariff
        if self.tariff_unit == "€/ton":
            self.vector_pci = data_df.loc[data_df['Vector'] == self.energy_vector, 'PCI'].values[0]
            self.vector_tariff = self.vector_tariff/1000 /(self.vector_pci/3.6)
        if self.tariff_unit == "€/m3":
            self.vector_pci = data_df.loc[data_df['Vector'] == self.energy_vector, 'PCI'].values[0]
            vector_density = data_df.loc[data_df['Vector'] == self.energy_vector, 'Density'].values[0]
            self.vector_tariff = self.vector_tariff/ vector_density/ (self.vector_pci/3.6)


"""
The Objective class relates to the objective scenario(s). In this sense it is intended to identify what the 
renewable gas mixture wanted cis and then all the calculations are elaborated.
"""
class Objective():
    def __init__(self, hydrogen_quantity, biomethane_quantity, objective_equipments, cele_mode=None, target_cost=None):
        self.name = None
        self.cele_mode = cele_mode
        self.target_cost = target_cost
        """
        objective_mixture: User indicates hydrogen and biomethane percentages in (%). 
        If hydrogen + biomethane is less than 100% the rest is natural gas.

        objective_equipment: List of the equipments that it is intended to convert to a certain energy vector - objects selection
        """
        self.hydrogen_quantity = hydrogen_quantity
        self.biomethane_quantity = biomethane_quantity
        # Ensure `equipments` is always a list, even if a single object is passed
        if isinstance(objective_equipments, Equipment):
            self.objective_equipments = [objective_equipments]
        else:
            self.objective_equipments = objective_equipments
        
        self.objective_vectors = []
        self.objective_percentages = []
        self.base_scenario_energy_consumption = []
        self.total_base_emissions = 0
        self.total_base_costs = 0

        # Ensure inputs are valid percentages
        if not (0 <= hydrogen_quantity <= 100):
            raise ValueError("Hydrogen percentage must be between 0 and 100.")
        if not (0 <= biomethane_quantity <= 100):
            raise ValueError("Biomethane percentage must be between 0 and 100.")
        if hydrogen_quantity + biomethane_quantity > 100:
            raise ValueError("O total de hidrogénio e biometano não pode exceder os 100%. Será necessário corrigir as percentagens de gases renováveis da mistura de estudo")
        
        #Calculates natural gas percentage
        self.natural_gas_quantity = 100 - (self.hydrogen_quantity + self.biomethane_quantity)

        #Initialize gas mixture
        self.objective_vectors = ["Biometano", "Hidrogénio","Gás natural"]
        self.objective_percentages = [self.biomethane_quantity, self.hydrogen_quantity, self.natural_gas_quantity]
        
        # Validate that the total percentage equals 100%
        self.validate_mixture()

    def validate_mixture(self):
        """Ensure that the total percentage adds up to 100%."""
        total_percentage = sum(self.objective_percentages)
        if total_percentage != 100:
            raise ValueError(f"The total percentage of the mixture must be 100%. Current total is {total_percentage}%")

    def get_mixture(self):
        """Return the mixture of energy vectors and their percentages."""
        return list(zip(self.objective_vectors, self.objective_percentages))
        
    def emissions_reduction(self):
        """Compares the emissions of an objective scenario with the base one."""
        total_mixture_emission_factor_vol = 0  # Initialize sum of emission factors
        self.objective_anual_energy_consumption = 0 #Initialize sum of energy
        self.objective_base_emissions = 0 #Initialize sum of base emissions
        self.objective_pci_vol = 0
        self.objective_density = 0

        #Calculation of emissions of base scenario for the equipments considered in the objective
        for object in self.objective_equipments:
            self.objective_base_emissions += object.base_emissions

        #Zip the vectors and percentages into tuples and iterate through them - Calculation of objective emission factor
        objective_mixture = list(zip(self.objective_vectors, self.objective_percentages))
        # Objective mixture density calculation
        for vector, percentage in objective_mixture:
            vector_density = data_df.loc[data_df['Vector'] == vector, 'Density'].values[0]
            self.objective_density += vector_density * (percentage / 100)
        # Objective mixture pci calculation
        for vector, percentage in objective_mixture:
            vector_density = data_df.loc[data_df['Vector'] == vector, 'Density'].values[0]
            vector_pci = data_df.loc[data_df['Vector'] == vector, 'PCI'].values[0]
            self.objective_pci_vol += (vector_pci/3.6) * vector_density * (percentage/100)
        self.objective_pci = self.objective_pci_vol / self.objective_density
        # Objective mixture emission factor calculation
        for vector, percentage in objective_mixture:
            pci = data_df.loc[data_df['Vector'] == vector, 'PCI'].values[0] / 3.6
            density = data_df.loc[data_df['Vector'] == vector, 'Density'].values[0]
            emission_factor = data_df.loc[data_df['Vector'] == vector, 'Emission factor'].values[0]

            emission_factor_vol = emission_factor * density * pci
            total_mixture_emission_factor_vol += emission_factor_vol * (percentage / 100)
        self.total_mixture_emission_factor = total_mixture_emission_factor_vol / self.objective_density / self.objective_pci
        # Objective mixture total emissions calculation
        for object in self.objective_equipments:
            self.objective_anual_energy_consumption += object.anual_energy_consumption 
            self.total_mixture_emissions = self.objective_anual_energy_consumption * self.total_mixture_emission_factor
        self.relative_emissions_reduction = (1 - self.total_mixture_emissions/self.objective_base_emissions) * 100
        #Objective total hydrogen consumption calculation
        for vector, percentage in objective_mixture:
            if vector == 'Hidrogénio':
                density = data_df.loc[data_df['Vector'] == vector, 'Density'].values[0]
                pci = data_df.loc[data_df['Vector'] == vector, 'PCI'].values[0] / 3.6
                hydrogen_annual_consumption_vol = self.objective_anual_energy_consumption / self.objective_pci / self.objective_density * (percentage/100)
                self.objective_hydrogen_annual_consumption = hydrogen_annual_consumption_vol * density * pci


    def objective_energy_cost_calc(self):
        """Calculates the energy costs of the objective scenario and compares it with the base one."""
        self.objective_reference_tariff = 0
        objective_anual_energy_cost = 0
        #Calculation of energy costs of base scenario for the equipments considered in the objective
        for object in self.objective_equipments:
            self.total_base_costs += object.energy_costs

        objective_mixture = list(zip(self.objective_vectors, self.objective_percentages))
        for vector, percentage in objective_mixture:
            reference_tariff = data_df.loc[data_df['Vector'] == vector, 'Reference tariff'].values[0]
            self.objective_reference_tariff += reference_tariff * (percentage / 100)
        if self.target_cost != None:
            self.objective_reference_tariff = self.target_cost
        if self.cele_mode == "Abrangido pelo CELE":
            for object in self.objective_equipments:
                objective_anual_energy_cost += self.objective_anual_energy_consumption * self.objective_reference_tariff
            self.final_anual_energy_cost = objective_anual_energy_cost - ((self.objective_base_emissions - self.total_mixture_emissions)/1000 * emissions_tax)
            self.relative_cost_variation = ((self.final_anual_energy_cost - self.total_base_costs) / self.total_base_costs) * 100
        else:
            for object in self.objective_equipments:
                objective_anual_energy_cost += self.objective_anual_energy_consumption * self.objective_reference_tariff
            self.final_anual_energy_cost = objective_anual_energy_cost
            self.relative_cost_variation = ((self.final_anual_energy_cost - self.total_base_costs) / self.total_base_costs) * 100

        
    def objective_vector_properties(self):
        """Calculation of objective energy vector properties to inform the user."""
        objective_mixture = list(zip(self.objective_vectors, self.objective_percentages))
        self.objective_pci_vol = 0
        self.objective_density = 0
        self.objective_sg = 0
        self.objective_mie = 0
        air_density = 1.204

        #Mixture density
        for vector, percentage in objective_mixture:
            vector_density = data_df.loc[data_df['Vector'] == vector, 'Density'].values[0]
            self.objective_density += vector_density * (percentage / 100)

        #Mixture PCI
        for vector, percentage in objective_mixture:
            vector_density = data_df.loc[data_df['Vector'] == vector, 'Density'].values[0]
            vector_pci = data_df.loc[data_df['Vector'] == vector, 'PCI'].values[0]
            self.objective_pci_vol += (vector_pci/3.6) * vector_density * (percentage/100)
        self.objective_pci = self.objective_pci_vol / self.objective_density

        #Mixture Wobbe Index
        self.objective_sg = self.objective_density / air_density
        self.wobbe_index = self.objective_pci_vol/(self.objective_sg**(1/2))

        #Mixture Minimum ignition energy
        for vector, percentage in objective_mixture:
            vector_minimum_ign = data_df.loc[data_df['Vector'] == vector, 'Minimum ignition energy'].values[0]
            self.objective_mie += vector_minimum_ign * (percentage / 100)

        #Flammability limits
        self.vector_lfl = 0
        self.vector_hfl = 0
        for vector, percentage in objective_mixture:
            lfl = flammablity_df.loc[flammablity_df['Vector'] == vector, 'LFL'].values[0]
            hfl = flammablity_df.loc[flammablity_df['Vector'] == vector, 'HFL'].values[0]
            self.vector_lfl += lfl * (percentage/100)
            self.vector_hfl += hfl * (percentage/100)

        #Adiabatic flame temperature
        flame_temperature_data = {"vector":[], "percentage": []}
        for vector, percentage in objective_mixture:
            if vector == "Biometano":
                fuel = "CH4"
                fuel_percentage = percentage/100
                flame_temperature_data["vector"].append(fuel)
                flame_temperature_data["percentage"].append(fuel_percentage)
            if vector =="Hidrogénio":
                fuel = "H2"
                fuel_percentage = percentage/100
                flame_temperature_data["vector"].append(fuel)
                flame_temperature_data["percentage"].append(fuel_percentage)
            if vector == "Gás natural":
                mixture = ["CH4", "C2H6", "C3H8"]
                mixture_percentage = [0.9, 0.0601, 0.0399]
                for fuel, value in zip(mixture, mixture_percentage):
                    flame_temperature_data["vector"].append(fuel)
                    flame_temperature_data["percentage"].append(value*(percentage/100))
        flame_temperature_final = {"vector":[], "percentage": []}
        # Runs throught flame_temperature_data to verify if some species is repeated
        for i in range(len(flame_temperature_data["vector"])):
            gas = flame_temperature_data["vector"][i]
            percentage = flame_temperature_data["percentage"][i]
            # Check if the gas is already in the dictionary
            if gas in flame_temperature_final["vector"]:
                # Find the index of the existing gas and update the percentage
                index = flame_temperature_final["vector"].index(gas)
                flame_temperature_final["percentage"][index] += percentage
            else:
                # If the gas is not in the unique_data, add it along with its percentage
                flame_temperature_final["vector"].append(gas)
                flame_temperature_final["percentage"].append(percentage)
        # Define the gas mixture
        fuel_mixture = ""
        for item, number in zip(flame_temperature_final['vector'], flame_temperature_final['percentage']):
            fuel_mixture += f"{item}:{number:.3f}, "
        fuel_composition = fuel_mixture[:-2]
        oxidizer = 'O2:1.0, N2:3.76'  # Air composition
        equivalence_ratio = 1.0  # Stoichiometric combustion
        # Create the gas mixture
        gas = ct.Solution('gri30.yaml')  # Load GRI-3.0 mechanism
        gas.set_equivalence_ratio(equivalence_ratio, fuel_composition, oxidizer)
        # Set the initial temperature and pressure
        initial_temperature = 273.15  # in Kelvin
        initial_pressure = ct.one_atm  # in Pascals
        gas.TP = initial_temperature, initial_pressure
        # Perform an adiabatic, constant-pressure equilibrium calculation
        gas.equilibrate('HP')
        # Retrieve the adiabatic flame temperature
        self.adiabatic_flame_temperature = gas.T - 273.15

    def hydrogen_production(self):
        hydrogen_lhv = 120/3.6 #kWh/kg
        electrolyser_input_energy = self.objective_hydrogen_annual_consumption / 0.65 #kWh
        self.working_hours = 3000 #hours/year
        self.electrolyser_power = electrolyser_input_energy / self.working_hours
        electrolyser_specific_cost = 4841 * (self.electrolyser_power**-0.198) #€/kW
        self.electrolyser_cost = electrolyser_specific_cost * self.electrolyser_power #€
        consumed_hydrogen = electrolyser_input_energy / hydrogen_lhv
        water_consumption_ratio = 18 #kg H2O/kg H2
        self.consumed_water = consumed_hydrogen * water_consumption_ratio / 1000 #m3

class Post_processing():
    def __init__(self, flowchart):
        self.flowchart = flowchart  # Access Flowchart data
        self.data = {}

    def process(self):
        """"Method to trigger post processing operations"""
        self.gather_data()
        st.header("Comparação de emissões")
        self.plot_emissions_comparison()
        st.header("Variação de custos")
        self.cost_variation()
        self.plot_costs_comparison()
        st.header("Propriedades da mistura de gases objetivo")
        self.properties_calculator()
        ### st.header("Considerações técnicas")
        self.info_system()
        self.warning_system()
        st.header('Soluções H2 ready')
        self.h2ready_equipments()

    def gather_data(self):
        # Collect data for each objective and equipment
        for objective in self.flowchart.objectives:
            self.data[objective.name] = {
                "base_emissions": objective.objective_base_emissions,                
                "objective_emissions": objective.total_mixture_emissions,
                "emissions_reduction": objective.relative_emissions_reduction,
                "base_costs": objective.total_base_costs,
                "objective_costs": objective.final_anual_energy_cost,
                "cost_variation": objective.relative_cost_variation,
                "objective_density": objective.objective_density,
                "objective_PCI": objective.objective_pci
            }
    
    def info_system(self):
        for objective in self.flowchart.objectives:
            objective_mixture = list(zip(objective.objective_vectors, objective.objective_percentages))
            
            #Info related to hydrogen production
            for vector, percentage in objective_mixture:
                if vector == 'Hidrogénio' and percentage > 0:
                    st.header("Considerações técnicas")
                    st.write(f"**Informações para o: {objective.name}**")
                    st.write(f"Para o caso do {objective.name}, para o **fornecimento de {objective.objective_anual_energy_consumption:,.0f} kWh/ano** à fábrica seria necessário instalar \
                                um eletrolisador com uma **potência nominal de {objective.electrolyser_power:,.1f} kW**, tendo em conta {objective.working_hours} horas de funcionamento anual. \
                        O **investimento** para a aquisição deste equipamento rondará os **{objective.electrolyser_cost:,.2f} €**. \
                        Tendo em conta a quantidade de hidrogénio necessária, estima-se o **consumo de {objective.consumed_water:,.1f} m³ de água por ano**.")

    def warning_system(self):
        more_than_10_percent_hydrogen = False
        more_than_20_percent_hydrogen = False
        objectives_more_than_10H2 = []
        objectives_more_than_20H2 = []
        for objective in self.flowchart.objectives:
            objective_mixture = list(zip(objective.objective_vectors, objective.objective_percentages))
            for vector, percentage in objective_mixture:
                if vector == 'Hidrogénio' and percentage >= 10 and percentage < 20:
                    objectives_more_than_10H2.append(objective.name)
                if vector == 'Hidrogénio' and percentage >= 20:
                    objectives_more_than_20H2.append(objective.name)

        if objectives_more_than_10H2 or objectives_more_than_20H2:
                st.write("#### Outras considerações")
        
        for objective in self.flowchart.objectives:
            objective_mixture = list(zip(objective.objective_vectors, objective.objective_percentages))            
            #Technical considerations
            for vector, percentage in objective_mixture:
                if vector == 'Hidrogénio' and percentage >= 10 and percentage < 20:
                    if more_than_10_percent_hydrogen == False:
                        st.write(f'O facto da mistura de gases pretendida para o caso do(s) {objectives_more_than_10H2} possuir mais que 10% de H₂ resulta na necessidade de atenção a alguns tópicos técnicos:')
                        st.write('- A percentagem de hidrogénio é contemplada na legislação nacional, conforme abordado no Despacho n.º 2791/2025, de 28 de fevereiro (Regulamento da Rede Nacional de Distribuição de Gás)\
                                no qual se estabelece o limite máximo de 20% H2 a veicular na RNDG. Deste modo, para a generalidade dos casos, não será expectável que haja alterações operacionais com a alteração\
                                da mistura de gás a usar.')
                        st.write('Na página **Informação: Integração de gases renováveis** encontra-se uma listagem de algumas normas relacionadas com a introdução de hidrogénio\
                                em diversas valências')
                        st.markdown('')
                        more_than_10_percent_hydrogen = True

                if vector == 'Hidrogénio' and percentage >= 20:
                    if more_than_20_percent_hydrogen == False:
                        st.write(f'O facto da mistura de gases pretendida para o caso do(s) {objectives_more_than_20H2} possuir mais que 20% de H₂ resulta na necessidade de atenção a alguns tópicos técnicos:')
                        st.write('- Será importante mencionar que a mistura se encontra fora do limite máximo estabelecido legalmente para veicular nas infraestruturas do Sistema Nacional de Gás. Deste modo será \
                                 necessário o utilizador adquirir parte do hidrogénio por meios próprios de forma a atingir esta percentagem.')
                        st.write('- A inclusão  de hidrogénio na mistura de gás resulta também na modificação das propriedades fisico-quimicas da mesma. Assim, será \
                                fundamental proceder ao contacto com os fornecedores dos equipamentos de queima para a garantia de que não existe risco de situações como retorno de chama.')         
                        st.write('Na página **Informação: Integração de gases renováveis** encontra-se uma listagem de algumas normas relacionadas com a introdução de hidrogénio\
                                em diversas valências')
                        st.markdown('')
                        st.markdown('')
                        more_than_20_percent_hydrogen = True

    def h2ready_equipments(self):
        caldeira_has_been_called = False
        forno_has_been_called = False
        cogeracao_has_been_called = False
        queimador_has_been_called = False
        caldeira_objects_list = []
        forno_objects_list = []
        cogeracao_objects_list = []
        queimador_objects_list = []

        for equipment in self.flowchart.equipments:
            if equipment.equipment == 'Caldeira':
                caldeira_objects_list.append(equipment.name)
            if equipment.equipment == 'Forno':
                forno_objects_list.append(equipment.name)
            if equipment.equipment == 'Cogeração':
                cogeracao_objects_list.append(equipment.name)
            if equipment.equipment == 'Queimador (Dedicado a estufas ou banhos térmicos)':
                queimador_objects_list.append(equipment)
        
        for equipment in self.flowchart.equipments:
            if caldeira_has_been_called == False:
                if equipment.equipment == "Caldeira":
                    st.subheader('**Caldeira**')
                    st.write('De acordo com a pesquisa realizada foram identificadas as seguintes referências de caldeiras relacionadas com a introdução de gases renováveis em **caldeiras**:')
                    st.write('Há diferentes empresas que, de momento, afirmam desenvolver caldeiras tecnicamente preparadas para o funcionamento regular com misturas de\
                             gás natural e gases renováveis (H2). No entanto, será importante referir que em grande parte dos casos apenas é considerada a possibilidade de mistura parcial com H2,\
                             podendo este atingir, os 20% em volume.')
                    st.write('- Babcock & Wilcox - https://www.babcock.com/home/environmental/decarbonization/hydrogen-combustion/') 
                    st.write('- Bosch - https://www.bosch-industrial.com/gb/en/ocs/commercial-industrial/hydrogen-boilers-20753156-c/')
                    st.write('- Viessmann - https://www.viessmann.pt/pt/produtos/caldeiras-industriais/vitomax-hs.html')                       
                    st.write('Informa-se que na página **Informação: Integração de gases renováveis** encontra-se uma listagem de algumas normas relacionadas com a introdução de hidrogénio\
                            em diversas valências.')
                    st.markdown('')
                    caldeira_has_been_called = True

        for equipment in self.flowchart.equipments:
            if forno_has_been_called == False:
                if equipment.equipment == "Forno":
                    st.subheader('**Forno**')
                    st.write('De acordo com a pesquisa realizada foram identificadas as seguintes referências de fornos que se encontram preparados para a \
                             utilização de diferentes misturas de gases renováveis:')
                    st.write('Há diferentes empresas que, de momento, afirmam desenvolver fornos tecnicamente preparadss para o funcionamento regular com misturas de\
                             gás natural e gases renováveis (H2). No entanto, será importante referir que em grande parte dos casos apenas é considerada a possibilidade de mistura parcial com H2,\
                             podendo este atingir, regularmente, os 20% em volume.')
                    st.write('- Induzir - https://www.induzir.pt/pt')
                    st.write('- Fives - https://www.fivesgroup.com/energy-combustion/reducing-carbon-footprint/hydrogen-combustion-solutions')
                    st.markdown('**Projetos de demonstração**')
                    st.write('- H2AL - Projeto com o principal objetivo de impulsionar a adoção de tecnologias de combustão de hidrogénio em várias indústrias')
                    st.write('https://h2al.ulb.be/')
                    st.write('- H2 Glass - O consórcio H2GLASS tem o objetivo de acelerar a descarbonização da indústria do vidro, desenvolvendo tecnologias para a combustão total a hidrogénio.')
                    st.write('https://h2-glass.eu/')
                    st.write('- TwinGhy - O consórcio TwinGhy pretende introduzir o hidrogénio como combustível para substituir o gás natural nos fornos de reaquecimento do sector siderúrgico.')
                    st.write('https://twinghy.eu/')
                    st.write('- Saint-Gobain - A Saint-Gobain desenvolveu iniciativas de descarbonização na indústria do vidro, destacando-se pela produção de vidro plano utilizando mais de 30% de hidrogénio no seu forno na Alemanha.')
                    st.write('https://www.saint-gobain.com/en/magazine/hydrogen-driving-green-revolution')
                    st.write('- ECP - A ECP tem como objetivo reforçar a competitividade das indústrias de cerâmica e cristalaria a nível nacional com investimentos em todas as etapas da cadeia de valor do setor e sustentados pela melhoria das qualificações dos seus ativos.')
                    st.write('https://agendaecp.pt/pt/atividades/wp1')
                    st.write('- HYBRIT - O projeto HYBRIT, liderado por empresas suecas, visa eliminar o uso de carvão na produção de aço, substituindo-o por hidrogénio verde. ')
                    st.write('https://www.hybritdevelopment.se/en/')
                    st.write('Na página **Informação: Integração de gases renováveis** encontra-se uma listagem de algumas normas relacionadas com a introdução de hidrogénio\
                            em diversas valências')
                    
                    st.markdown('')
                    forno_has_been_called = True
        
        for equipment in self.flowchart.equipments:
            if cogeracao_has_been_called == False:
                if equipment.equipment == "Cogeração":
                    st.subheader('**Cogeração**')
                    st.write('De acordo com a pesquisa realizada foram identificadas as seguintes referências de turbinas que se encontram preparadas para a \
                             utilização de diferentes misturas de gases renováveis:')
                    st.write('Há diferentes empresas que, de momento, afirmam desenvolver turbinas tecnicamente preparadas para o funcionamento regular com misturas de\
                             gás natural e gases renováveis (H2). No entanto, será importante referir que em grande parte dos casos apenas é considerada a possibilidade de mistura parcial com H2,\
                             podendo este atingir, regularmente, os 20% em volume.')
                    st.write('- Ansaldo Energia - https://www.ansaldoenergia.com/offering/solutions-for-the-transition/hydrogen')
                    st.write('- Baker Hughes - https://www.bakerhughes.com/gas-turbines')
                    st.write('- General Electric - https://www.gevernova.com/gas-power/future-of-energy/hydrogen-fueled-gas-turbines')
                    st.write('- Mitsubishi Power - https://power.mhi.com/regions/amer/products/hydrogen-gas-turbine')
                    st.write('- Siemens Energy - https://www.siemens-energy.com/global/en/home/products-services/product/hydrogen-power-plants.html')
                    st.markdown('**Projetos de demonstração**')
                    st.write('- HyFlexPower - Projeto europeu finalizado cujo objetivo consistiu na demonstração do retrofit de um sistema de cogeração de gás natural para hidrogénio.')
                    st.write('https://www.hyflexpower.eu/')
                    st.write('- ZEHTEC - Projeto europeu finalizado cujo objetivo foi a demonstração da viabilidade da integração entre o \
                             hidrogénio e as turbinas a gás, a produção de energias renováveis e o armazenamento de energia em conjunto num futuro sistema energético flexível e sustentável.')
                    st.write('https://www.zehtc.org/')
                    st.write('- HyPowerGT - Projeto europeu finalizado cujo objetivo consistiu no desenvolvimento de turbinas a gás que funcionem com hidrogénio, \
                             garantindo baixas emissões de NOx sem recurso a catalisadores, diluentes ou redução da eficiência termodinâmica. ')
                    st.write('https://hypowergt.eu/')
                    st.write('- Flex4H2 - O projeto europeu cujo objetivo incide na continuação do desenvolvimento de uma tecnologia de combustão própria, conhecida como \
                             combustão sequencial a pressão constante (CPSC) utilizando misturas de H2 com gás natural em qualquer concentração, até 100%.')
                    st.write('https://flex4h2.eu/')
                    st.write('Informa-se que na página **Informação: Integração de gases renováveis** encontra-se uma listagem de algumas normas relacionadas com a introdução de hidrogénio\
                            em diversas valências.')
                    st.markdown('')
                    cogeracao_has_been_called = True
        
        for equipment in self.flowchart.equipments:
            if queimador_has_been_called == False:
                if equipment.equipment == "Queimador (Dedicado a estufas ou banhos térmicos)":
                    st.subheader('**Queimador**')
                    st.write('De acordo com a pesquisa realizada foram identificadas as seguintes referências de queimadores que se encontram preparados para a \
                             utilização de diferentes misturas de gases renováveis:')
                    st.write('Na página **Informação: Integração de gases renováveis** encontra-se uma listagem de algumas normas relacionadas com a introdução de hidrogénio\
                            em diversas valências')
                    st.markdown('')
                    queimador_has_been_called = True

    def properties_calculator(self):
        data = []
        natural_gas_density = data_df.loc[data_df['Vector'] == "Gás natural", 'Density'].values[0]
        natural_gas_PCI = data_df.loc[data_df['Vector'] == "Gás natural", "PCI"].values[0]/3.6
        natural_gas_PCI_vol = (data_df.loc[data_df['Vector'] == "Gás natural", "PCI"].values[0]/3.6)*data_df.loc[data_df['Vector'] == "Gás natural", "Density"].values[0]
        natural_gas_WI = natural_gas_PCI_vol/((natural_gas_density/1.204)**(1/2))
        natural_gas_lfl = flammablity_df.loc[flammablity_df['Vector'] == "Gás natural", 'LFL'].values[0]
        natural_gas_hfl = flammablity_df.loc[flammablity_df['Vector'] == "Gás natural", 'HFL'].values[0]
        natural_gas_limits = f"{natural_gas_lfl:.2f}% - {natural_gas_hfl:.2f}%"
        natural_gas_mie = data_df.loc[data_df['Vector'] == "Gás natural", 'Minimum ignition energy'].values[0]
        fuel = 'CH4:0.9, C2H6:0.0601, C3H8:0.0399' #Natural gas composition
        oxidizer = 'O2:1.0, N2:3.76'  # Air composition
        equivalence_ratio = 1.0  # Stoichiometric combustion
        # Create the gas mixture
        gas = ct.Solution('gri30.yaml')  # Load GRI-3.0 mechanism
        gas.set_equivalence_ratio(equivalence_ratio, fuel, oxidizer)
        # Set the initial temperature and pressure
        initial_temperature = 273.15  # in Kelvin
        initial_pressure = ct.one_atm  # in Pascals
        gas.TP = initial_temperature, initial_pressure
        # Perform an adiabatic, constant-pressure equilibrium calculation
        gas.equilibrate('HP')
        # Retrieve the adiabatic flame temperature
        adiabatic_flame_temperature = gas.T - 273.15

        natural_gas_properties = {
                "Gas": "Gás natural",
                "Massa volumica (kg/Nm³)": f"{natural_gas_density:.3f}",
                "PCI [kWh/kg]": f"{natural_gas_PCI:.2f}",
                "PCI [kWh/Nm³]": f"{natural_gas_PCI_vol:.2f}",
                "Índice de Wobbe [kWh/m³]": f"{natural_gas_WI:.2f}",
                "Energia mínima de ignição [mJ]": f"{natural_gas_mie:.2f}",
                "Temperatura adiabática de chama [°C]": round(adiabatic_flame_temperature,0),
                "Limites de inflamabilidade [%]": natural_gas_limits,
                "Fator de emissão [kg CO₂/kWh]": data_df.loc[data_df['Vector'] == "Gás natural", 'Emission factor'].values[0]}
        data.append(natural_gas_properties)
        
        for objective in self.flowchart.objectives:
            # Create a string that combines each gas with its percentage
            gas_mixture = ", ".join(
            f"{gas} [{percentage:.0f}%]"
            for gas, percentage in zip(objective.objective_vectors, objective.objective_percentages)
            if percentage > 0)
            flammability_limits = f"{objective.vector_lfl:.2f}% - {objective.vector_hfl:.2f}%"
            
            properties = {
                "Gas": gas_mixture,
                "Massa volumica (kg/Nm³)": round(objective.objective_density,3),
                "PCI [kWh/kg]": round(objective.objective_pci,2),
                "PCI [kWh/Nm³]":round(objective.objective_pci_vol, 2),
                "Índice de Wobbe [kWh/m³]": round(objective.wobbe_index, 2),
                "Energia mínima de ignição [mJ]": round(objective.objective_mie, 2),
                "Temperatura adiabática de chama [°C]": round(objective.adiabatic_flame_temperature,0),
                "Limites de inflamabilidade [%]": flammability_limits,
                "Fator de emissão [kg CO₂/kWh]": objective.total_mixture_emission_factor,
            }
            data.append(properties)
        # Convert to DataFrame and display/save
        properties_df = pd.DataFrame(data)
        st.dataframe(properties_df.reset_index(drop=True))

    def cost_variation(self):
        cost_data = []
        for objective, details in self.data.items():
            costs = {"Cenário": objective,
            "Custos energéticos base [€/ano]": f"{details['base_costs']:,.2f}",
            "Custos energéticos cenário estudo [€/ano]": f"{details['objective_costs']:,.2f}",
            "Variação dos custos [%]": f"{details['cost_variation']:,.2f}"}
            cost_data.append(costs)
        # Convert to DataFrame and display/save
        cost_data_df = pd.DataFrame(cost_data)
        st.write("Na presente figura são apresentados os dados económicos para cada um dos cenários de estudo.")
        #st.dataframe(cost_data_df.reset_index(drop=True))


    def plot_costs_comparison(self):
        fig = go.Figure()
    
        x_values = []
        base_costs = []
        study_costs = []
    
        # Collect data for each objective
        for objective_name, values in self.data.items():
            x_values.append(objective_name)
            base_costs.append(values["base_costs"])
            study_costs.append(values["objective_costs"])
    
        fig.add_trace(go.Bar(
            name="Custos Base",
            x=x_values,
            y=base_costs,
            text=[f"{value:,.2f} €" for value in base_costs],
            textposition='auto',))
    
        fig.add_trace(go.Bar(
            name="Custos do Cenário de Estudo",
            x=x_values,
            y=study_costs,
            text=[f"{value:,.2f} €" for value in study_costs],
            textposition='auto',))
    
        # Update layout for grouped bars
        fig.update_layout(
            yaxis_title="Custos Energéticos (€/ano)",
            barmode='group',
            xaxis=dict(categoryorder='category ascending'),)
    
        st.plotly_chart(fig)
        for objective_name, values in self.data.items():
            if values["cost_variation"] > 0:
                st.write(f"Para o {objective_name}, os **custos energéticos aumentam** em cerca de **{values['cost_variation']:,.2f}%** face à situação base.")
            elif values["cost_variation"] < 0:
                st.write(f"O {objective_name} resulta numa **redução de custos energéticos** de aproximadamente **{abs(values['cost_variation']):,.2f}%**.")
            else:
                st.write(f"Para o {objective_name}, os custos mantêm-se **inalterados** face ao cenário base.")
    
    def plot_emissions_comparison(self):
        fig = go.Figure()

        # Prepare data for grouped visualization
        x_values = []
        base_emissions = []
        study_emissions = []
        # Collect data for each objective
        for objective_name, values in self.data.items():
            x_values.append(objective_name)  # Add objective name
            base_emissions.append(values["base_emissions"])  # Base emissions
            study_emissions.append(values["objective_emissions"])  # Study emissions
        # Add Base Emissions bar
        fig.add_trace(go.Bar(
            name="Emissões Base",
            x=x_values,
            y=base_emissions,
            text=[f"{value:,.2f}" for value in base_emissions],
            textposition='auto',))
        # Add Study Emissions bar
        fig.add_trace(go.Bar(
            name="Emissões do Cenário de Estudo",
            x=x_values,
            y=study_emissions,
            text=[f"{value:,.2f}" for value in study_emissions],
            textposition='auto',))
        # Update layout for grouped bars
        fig.update_layout(
            yaxis_title="Emissões (kg CO2eq)",
            barmode='group',  # Group bars for each objective
            xaxis=dict(
                categoryorder='category ascending'  # Keep objectives in order
            )
        )
        st.plotly_chart(fig)
        for objective_name, values in self.data.items():

            if values["emissions_reduction"] == float('inf'):
                    st.write(f"Para o {objective_name}, a redução de emissões é **total** devido à troca de vetor energético.")
            elif values["emissions_reduction"] == float('-inf'):
                    st.write(f"O {objective_name} representa um **aumento total** das emissões.")
            else:
                if values["emissions_reduction"] > 0:
                    st.write(f"Para o {objective_name} a **redução de emissões** devido à troca de vetor energético corresponderá a cerca de **{values["emissions_reduction"]:,.2f}%**. ")
                if values["emissions_reduction"] < 0:
                    st.write(f"O {objective_name} representa um aumento de cerca de **{values["emissions_reduction"]:,.2f}%**. das emissões quando comparado com o base.")


class Flowchart():
    """
    Class that manages all the flowchart
    """
    def __init__(self, factory):
        self.equipments = []
        self.objectives = []
        self.factory = factory # Store a reference to the Factory
        self.factories = []
        self.energy_vectors = []
        self.global_tariffs = {}  # {"Electricity": 0.12, "Natural Gas": 0.08}
    
    """
    Factory creation
    """
    def add_factory(self, factory):
        self.factories.append(factory)
    
    """
    Equipment creation
    """
    def add_equipment(self, equipment):
        self.equipments.append(equipment)
        self.factory.add_equipment(equipment)  # Add to Factory too

    """
    Energy vector tariff creation
    """
    def add_energy_vector(self, energy_vector):
        self.energy_vectors.append(energy_vector) 

    """
    Objective creation
    """
    def add_objective(self, objective):
        self.objectives.append(objective)

    """
    Post processing trigger - It isn´t needed to define it in main
    """
    def trigger_post_processing(self):
        self.post_processing = Post_processing(self)
        self.post_processing.process()

    """
    Firstly, the calculation for the base scenarios are made - From this we get the data that will be compared with the objective scenario.
    """
    def simulate(self):
        if self.energy_vectors != []:
            for vector in self.energy_vectors:
                for equipment in self.equipments:
                    if vector.energy_vector == equipment.energy_vector:
                        vector.tariff_conversion()
                        data_df.loc[data_df["Vector"] == vector.energy_vector, "Reference tariff"] = vector.vector_tariff

        for equipment in self.equipments:
            if equipment.anual_consumption is not None:
                equipment.energy_consumption_calc()
                equipment.base_emissions_calculation()
                equipment.energy_costs_calculation() #Verificar se este loop também está a ser fechado.

            else:       
                for factory in self.factories:
                    factory.info_analysis()
                    factory.energy_consumption_calc()
                    factory.energy_distribuiton()
                    factory.equipment_base_emissions_calculation()
                    factory.energy_costs_calculation()
          
        for objective in self.objectives:
            objective.validate_mixture()
            objective.get_mixture()
            objective.emissions_reduction()
            objective.objective_energy_cost_calc()
            objective.objective_vector_properties()
            objective.hydrogen_production()

        self.trigger_post_processing()

if __name__ == "__main__":
    pass
