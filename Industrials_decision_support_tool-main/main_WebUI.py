import streamlit as st
import pandas as pd

### Call core code
from subroutines import *

def renewable_gases_introduction_sim_eq_database(n_equipments, equipment_data, n_objectives, scenario_data):
    factory = Factory()
    flowchart = Flowchart(factory)
    post_processing = Post_processing(flowchart)
    target_cost = None
    
    #### Modules definition
    equipments = {}
    objectives = {}

    for i in range(n_equipments):
        id = f"Equipment_{i+1}"
        equipments[id] = Equipment(equipment_data[f"Equipment {i+1}"]["selected_module"],
                               equipment_data[f"Equipment {i+1}"]["nomPower"],
                               equipment_data[f"Equipment {i+1}"]["combustible"],
                               equipment_data[f"Equipment {i+1}"]["equipment_consumption"],
                               equipment_data[f"Equipment {i+1}"]["consumption_unit"])

        equipments[id].name = equipment_data[f"Equipment {i+1}"]["module_name"]
        flowchart.add_equipment(equipments[id])

    for i in range(n_objectives):
        id = f"Objective_{i+1}"
        hydrogen_quantity = scenario_data[f"Objectivo {i+1}"]["hydrogen_quantity"]
        biomethane_quantity = scenario_data[f"Objectivo {i+1}"]["biomethane_quantity"]
        cele_mode = scenario_data[f"Objectivo {i+1}"]["cele_mode"]
        if "target_cost" in scenario_data[f"Objectivo {i+1}"]:
            target_cost = scenario_data[f"Objectivo {i+1}"]["target_cost"]
        # Retrieve Equipment instances by their names
        objective_equipments_definition = [
            equipment for equipment_name in scenario_data[f"Objectivo {i+1}"]["equipments"]
            for equipment in equipments.values()
            if equipment.name == equipment_name
        ]
        
        objectives[id] = Objective(hydrogen_quantity, biomethane_quantity, objective_equipments_definition, cele_mode, target_cost)
        
        objectives[id].name = f"Objectivo {i+1}"
        flowchart.add_objective(objectives[id])

    flowchart.simulate()


def renewable_gases_introduction_sim_eq_user(n_equipments, equipment_data, n_objectives, scenario_data, vector_tariffs):
    factory = Factory()
    flowchart = Flowchart(factory)
    post_processing = Post_processing(flowchart)
    
    #### Modules definition
    equipments = {}
    objectives = {}
    vectors = {}

    for i in range(n_equipments):
        id = f"Equipment_{i+1}"
        equipments[id] = Equipment(equipment_data[f"Equipment {i+1}"]["selected_module"],
                               equipment_data[f"Equipment {i+1}"]["nomPower"],
                               equipment_data[f"Equipment {i+1}"]["combustible"],
                               equipment_data[f"Equipment {i+1}"]["equipment_consumption"],
                               equipment_data[f"Equipment {i+1}"]["consumption_unit"])

        equipments[id].name = equipment_data[f"Equipment {i+1}"]["module_name"]
        flowchart.add_equipment(equipments[id])
    
    for i in range(n_objectives):
        id = f"Objective_{i+1}"
        target_cost = None
        hydrogen_quantity = scenario_data[f"Objectivo {i+1}"]["hydrogen_quantity"]
        biomethane_quantity = scenario_data[f"Objectivo {i+1}"]["biomethane_quantity"]
        cele_mode = scenario_data[f"Objectivo {i+1}"]["cele_mode"]
        if "target_cost" in scenario_data[f"Objectivo {i+1}"]:
            target_cost = scenario_data[f"Objectivo {i+1}"]["target_cost"]
        # Retrieve Equipment instances by their names
        objective_equipments_definition = [
            equipment for equipment_name in scenario_data[f"Objectivo {i+1}"]["equipments"]
            for equipment in equipments.values()
            if equipment.name == equipment_name]
        objectives[id] = Objective(hydrogen_quantity, biomethane_quantity, objective_equipments_definition, cele_mode, target_cost)
        objectives[id].name = f"Objectivo {i+1}"
        flowchart.add_objective(objectives[id])
    
    for vector, vector_information in vector_tariffs.items():
        id = f"Energy_vector_{i+1}"
        selected_vector = vector
        tariff_value = vector_information["tariff_value"]
        tariff_unit = vector_information["tariff_unit"]

        vectors[vector] = Energy_vector(selected_vector, tariff_value, tariff_unit)
        flowchart.add_energy_vector(vectors[vector])

    flowchart.simulate()


def renewable_gases_introduction_sim_factory_database(n_general_equipments, general_equipment_data, n_objectives, scenario_data, factory_consumption):
    factory = Factory()
    flowchart = Flowchart(factory)
    post_processing = Post_processing(flowchart)
    
    #### Modules definition
    equipments = {}
    objectives = {}
    vector_information = {}

    for i in range(n_general_equipments):
        id = f"Equipment_{i+1}"
        equipments[id] = Equipment(general_equipment_data[f"Equipment {i+1}"]["selected_module"],
                               general_equipment_data[f"Equipment {i+1}"]["nomPower"],
                               general_equipment_data[f"Equipment {i+1}"]["combustible"])

        equipments[id].name = general_equipment_data[f"Equipment {i+1}"]["module_name"]
        flowchart.add_equipment(equipments[id])

    vector_information = factory_consumption[1]
    factory.vector_information = vector_information
    flowchart.add_factory(factory)
    
    for i in range(n_objectives):
        id = f"Objective_{i+1}"
        hydrogen_quantity = scenario_data[f"Objectivo {i+1}"]["hydrogen_quantity"]
        biomethane_quantity = scenario_data[f"Objectivo {i+1}"]["biomethane_quantity"]
        cele_mode = scenario_data[f"Objectivo {i+1}"]["cele_mode"]
        if "target_cost" in scenario_data[f"Objectivo {i+1}"]:
            target_cost = scenario_data[f"Objectivo {i+1}"]["target_cost"]
        # Retrieve Equipment instances by their names
        objective_equipments_definition = [
            equipment for equipment_name in scenario_data[f"Objectivo {i+1}"]["equipments"]
            for equipment in equipments.values()
            if equipment.name == equipment_name]
        objectives[id] = Objective(hydrogen_quantity, biomethane_quantity, objective_equipments_definition, cele_mode, target_cost)       
        objectives[id].name = f"Objectivo {i+1}"
        flowchart.add_objective(objectives[id])

    flowchart.simulate()


def renewable_gases_introduction_sim_factory_user(n_general_equipments, general_equipment_data, n_objectives, scenario_data, factory_consumption, vector_tariffs):
    factory = Factory()
    flowchart = Flowchart(factory)
    post_processing = Post_processing(flowchart)
    
    #### Modules definition
    equipments = {}
    objectives = {}
    vector_information = {}
    vectors = {}

    for i in range(n_general_equipments):
        id = f"Equipment_{i+1}"
        equipments[id] = Equipment(general_equipment_data[f"Equipment {i+1}"]["selected_module"],
                               general_equipment_data[f"Equipment {i+1}"]["nomPower"],
                               general_equipment_data[f"Equipment {i+1}"]["combustible"])

        equipments[id].name = general_equipment_data[f"Equipment {i+1}"]["module_name"]
        flowchart.add_equipment(equipments[id])
    vector_information = factory_consumption[1]
    factory.vector_information = vector_information
    flowchart.add_factory(factory)
    
    for i in range(n_objectives):
        id = f"Objective_{i+1}"
        hydrogen_quantity = scenario_data[f"Objectivo {i+1}"]["hydrogen_quantity"]
        biomethane_quantity = scenario_data[f"Objectivo {i+1}"]["biomethane_quantity"]
        cele_mode = scenario_data[f"Objectivo {i+1}"]["cele_mode"]
        if "target_cost" in scenario_data[f"Objectivo {i+1}"]:
            target_cost = scenario_data[f"Objectivo {i+1}"]["target_cost"]
        # Retrieve Equipment instances by their names
        objective_equipments_definition = [
            equipment for equipment_name in scenario_data[f"Objectivo {i+1}"]["equipments"]
            for equipment in equipments.values()
            if equipment.name == equipment_name]
        objectives[id] = Objective(hydrogen_quantity, biomethane_quantity, objective_equipments_definition, cele_mode, target_cost)       
        objectives[id].name = f"Objectivo {i+1}"
        flowchart.add_objective(objectives[id])

    for vector, vector_information in vector_tariffs.items():
        id = f"Energy_vector_{i+1}"
        selected_vector = vector
        tariff_value = vector_information["tariff_value"]
        tariff_unit = vector_information["tariff_unit"]

        vectors[vector] = Energy_vector(selected_vector, tariff_value, tariff_unit)
        flowchart.add_energy_vector(vectors[vector])

    flowchart.simulate()
