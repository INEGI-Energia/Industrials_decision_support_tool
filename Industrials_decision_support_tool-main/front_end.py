import streamlit as st
import io
import pandas as pd
import base64
from main_WebUI import renewable_gases_introduction_sim_eq_database
from main_WebUI import renewable_gases_introduction_sim_eq_user
from main_WebUI import renewable_gases_introduction_sim_factory_database
from main_WebUI import renewable_gases_introduction_sim_factory_user
from information_page import information_page
from assumptions_page import assumptions_page
from about_project import project_page
from utilization_guide import guide_page
from faq_page import faq_page
    
###Ferramenta de apoio a decisão de consumidores industriais
def energy_consumption_mode():
    st.header("1. Modo de entrada de dados")
    st.write("Selecione se deseja fornecer os consumos energéticos desagregados por equipamento ou o consumo total da fábrica por vetor energético.")

    mode = st.radio(
        "Como pretende fornecer os dados de consumo energético?",
        options=["Desagregado por equipamento", "Consumo total da fábrica"],
        index=0,
        key="energy_mode"
    )

    # Add an empty placeholder for dynamic content
    st.empty()
    return mode


def energy_tariff_knowledge():
    st.header("3. Tarifa dos vetores energéticos")
    st.write("Selecione se deseja fornecer a tarifa de cada um dos vetores energéticos selecionados. Caso contrário serão usados valores padrão.")
    mode = st.radio(
        "Como pretende realizar o estudo?",
        options=["Tarifa inserida pelo utilizador", "Tarifa da base de dados"],
        index=0,
        key="tariff_mode")
    # Add an empty placeholder for dynamic content
    st.empty()
    return mode


def equipments_WebUI():
    st.header("2. Equipamentos térmicos a estudar")
    st.write("Indicação dos equipamentos de queima a ter em consideração para integração de gases renováveis")
    # Use a dictionary to store selected modules
    equipment_data = {}
    n_equipments = int(st.number_input("Número de equipamentos:", value=0, min_value=0, step=1, format='%i'))

    for i in range(n_equipments):
        # Use f-string to create a unique key based on the loop index i
        key_selectBox = f"module_selectBox_{i}"
        key_modules = f"module_{i}"
        key_power = f"Equipment_power_{i}"
        key_combustible = f"Equipment_combustible_{i}"
        key_consumption = f"Equipment_consumption_{i}"
        key_consumption_unit = f"Equipment_consumption_unit_{i}"
        module_options = ["Caldeira", "Forno", "Cogeração"]

        st.markdown(f"<h3 style='text-align: center; color: green;'>Equipamento {i+1}</h3>", unsafe_allow_html=True)
        selected_module = st.selectbox(
            f"Equipamento {i+1}",
            module_options,
            index=module_options.index("Caldeira"),
            key=key_selectBox,
            )
        equipment_data[f"Equipment {i+1}"] = {
            "module_name": st.text_input("Nome do equipamento", value=f"Equipamento {i+1}", key=key_modules),
            "selected_module": selected_module,
            "nomPower": st.number_input("Potência do equipamento [kW]", key=key_power, value=0, min_value=0, step=10),
            "combustible": st.selectbox("Vetor energético em uso", ["Biometano", "Hidrogénio", "Biomassa", "Eletricidade", "Gás natural", "GPL", "Nafta", "Gasóleo", "Fuelóleo", "Coque de petróleo", "Residuos industriais"], index=1, key=key_combustible),
        }
        # Create two columns for "Consumo anual do equipamento" and "Unidade de consumo"
        col2_A, col2_B = st.columns(2)        
        with col2_A:
            equipment_data[f"Equipment {i+1}"]["equipment_consumption"] = st.number_input("Consumo anual do equipamento", key=key_consumption, value=0, min_value=0, step=1000)
        with col2_B:
            possible_units = ["kWh/ano", "ton/ano", "m3/ano"]
            if equipment_data[f"Equipment {i+1}"]["combustible"] == "Eletricidade":
                possible_units = ["kWh/ano"]
            if equipment_data[f"Equipment {i+1}"]["combustible"] == "Biomassa":
                possible_units = ["kWh/ano", "ton/ano"]
            equipment_data[f"Equipment {i+1}"]["consumption_unit"] = st.selectbox("Unidade de consumo", possible_units, key=key_consumption_unit)
    return n_equipments, equipment_data


def cele():
    st.header("Desconto de redução de emissões de CO2")
    st.write("Selecine se a sua empresa se encontra ao abrigo  do CELE.")
    st.write("Em caso afirmativo, será descontado o valor associado às emissões de GEE no custo energético. Caso contrário, este fator não será contabilizado.")
    cele = st.radio(
        "Como pretende realizar o estudo?",
        options=["Abrangido pelo CELE", "Não abrangido pelo CELE"],
        index=0,
        key="tariff_mode")
    
    # Add an empty placeholder for dynamic content
    st.empty()
    return cele


def equipments_general_consumption_WebUI():
    st.header("2. Equipamentos de queima a estudar")
    st.write("Indicação dos equipamentos de queima a ter em consideração para integração de gases renováveis")

    # Use a dictionary to store selected modules
    general_equipment_data = {}

    n_general_equipments = int(st.number_input("Número de equipamentos:", value=0, min_value=0, step=1, format='%i'))

    for i in range(n_general_equipments):
        # Use f-string to create a unique key based on the loop index i
        key_selectBox = f"module_selectBox_{i}"
        key_module_name = f"module_name_{i}"
        key_power = f"Equipment_power_{i}"
        key_combustible = f"Equipment_combustible_{i}"

        module_options = ["Caldeira", "Forno", "Cogeração"]
        st.markdown(f"<h3 style='text-align: center; color: green;'>Equipamento {i+1}</h3>", unsafe_allow_html=True)

        selected_module = st.selectbox(
            f"Equipment {i+1}",
            module_options,
            index=module_options.index("Caldeira"),
            key=key_selectBox,
        )
        general_equipment_data[f"Equipment {i+1}"] = {
            "module_name": st.text_input("Nome do equipamento", value=f"Equipamento {i+1}", key=key_module_name),
            "selected_module": selected_module,
            "nomPower": st.number_input("Potência do equipamento [kW]", key=key_power, value=0, min_value=0, step=10),
            "combustible": st.selectbox("Vetor energético em uso", ["Biometano", "Hidrogénio", "Biomassa", "Eletricidade", "Gás natural", "GPL", "Nafta",\
                                                                     "Gasóleo", "Fuelóleo", "Coque de petróleo", "Residuos industriais"], index=1, key=key_combustible),
        }
    return n_general_equipments, general_equipment_data


def objective(equipment_data):
    st.header("4. Cenário objetivo")
    st.write("Definição dos cenários de descarbonização a estudar")
    scenario_data = {}

    if not equipment_data:
        st.warning("Nenhum equipamento disponível. Por favor, insira dados de equipamentos.")
        return 0, {}
    
    cele = st.radio(
        "Selecine se a sua empresa se encontra ao abrigo  do CELE",
        options=["Abrangido pelo CELE", "Não abrangido pelo CELE"],
        index=0,
        key="cele_mode")
    st.warning("Em caso afirmativo, será descontado o valor associado às emissões de GEE no custo energético. Caso contrário, este fator não será contabilizado.")
    # Add an empty placeholder for dynamic content
    st.empty()

    equipment_names = [equipment_data[key]["module_name"] for key in equipment_data]
    n_objectives = int(st.number_input("Número de cenários de estudo", value=0, min_value=0, step=1, format='%i', key="n_scenarios"))
    
    
    for i in range(n_objectives):
        st.markdown(f"<h3 style='text-align: center; color: green;'>Cenário {i+1}</h3>", unsafe_allow_html=True)

        equipments_mode = st.radio(
        "Pretende indicar que equipamentos considerar no cenário ou selecionar todos?",
        options=["Selecionar todos", "Escolha personalizada"],
        index=0,
        key=f"equipments_mode_{i}")
        if equipments_mode == "Selecionar todos":
            scenario_data[f"Objectivo {i+1}"] = {"equipments": []}
            scenario_data[f"Objectivo {i+1}"]["module_name"] = f"Cenário {i+1}"

            for eq in equipment_names:
                scenario_data[f"Objectivo {i+1}"]["equipments"].append(eq)

        if equipments_mode == "Escolha personalizada":
            objective_equipments_list = int(st.number_input(f"Número de equipamentos no cenário {i+1}", value=0, min_value=0, step=1, format='%i', key=f"n_objective_equipments_{i}"))
            
            scenario_data[f"Objectivo {i+1}"] = {"equipments": []}
            scenario_data[f"Objectivo {i+1}"]["module_name"] = f"Cenário {i+1}"

            # Track selected equipment for this scenario
            selected_equipment_for_scenario = []
            
            for k in range(objective_equipments_list):
                # Filter available equipment names
                available_equipment = [eq for eq in equipment_names if eq not in selected_equipment_for_scenario]

                # Display the dropdown with the filtered options
                selected_equipment = st.selectbox(
                    f"Equipamento a considerar no Cenário {i+1}",
                    available_equipment,
                    key=f"objective_equipment_{i}_{k}"
                )

                # Add selected equipment to the scenario and update the used list
                scenario_data[f"Objectivo {i+1}"]["equipments"].append(selected_equipment)
                selected_equipment_for_scenario.append(selected_equipment)
        scenario_data[f"Objectivo {i+1}"]["cele_mode"] = cele
        col3_A, col3_B = st.columns(2)
        with col3_A:
            scenario_data[f"Objectivo {i+1}"]["hydrogen_quantity"] = st.number_input(f"Percentagem de Hidrogénio no Cenário {i+1} [%vol]", value=0, min_value=0, max_value=100, step=5, key=f"hydrogen_percentage_{i}")
        with col3_B:
            scenario_data[f"Objectivo {i+1}"]["biomethane_quantity"] = st.number_input(f"Percentagem de Biometano no Cenário {i+1} [%vol]", value=0, min_value=0, max_value=100, step=5, key=f"biomethane_percentage_{i}")
        st.warning("É considerado que a fração remanescente da mistura de gases, para além das percentagens de gases renováveis introduzidas, será composta por **gás natural**.")
        if (scenario_data[f"Objectivo {i+1}"]["hydrogen_quantity"] + scenario_data[f"Objectivo {i+1}"]["biomethane_quantity"]) > 100:
            st.error("A soma das percentagens de Hidrogénio e Biometano não pode exceder 100%. Por favor, ajuste os valores.")
        
        objective_cost_mode = st.radio(
        "Pretende definir o custo da mistura objetivo? Caso não o pretenda irão ser considerados valores da base de dados.",
        options=["Sim", "Não"],
        index=0,
        key=f"objective_cost_mode_{i}")

        if objective_cost_mode == "Sim":
            scenario_data[f"Objectivo {i+1}"]["target_cost"] = st.number_input(f"Custo do vetor energético do cenário {i+1} [€/kWh]", value=0.0, min_value=0.0, step=0.01, key=f"target_cost_{i}")

    
    return n_objectives, scenario_data


def factory_consumption_input(general_equipment_data):
    st.header("Consumo total da fábrica por vetor energético")
    st.write("Indique os consumos energéticos totais da fábrica para cada vetor energético utilizado.")

    # Extract unique energy vectors from the provided equipment data
    energy_vectors = set(
        general_equipment_data[key]["combustible"]
        for key in general_equipment_data
    )

    factory_consumption = {}
    for i, vector in enumerate(energy_vectors):
        key_energy_consumption = f"Energy_consumption_{i}"
        key_unit = f"Energy_unit_{i}"

        st.markdown(f"<h3 style='text-align: center; color: green;'>Consumo da fábrica de {vector}</h3>", unsafe_allow_html=True)

        col4_A, col4_B = st.columns(2)
        with col4_A:
            factory_consumption[vector] = {"energy_consumption":st.number_input("Consumo anual do equipamento", key=key_energy_consumption, value=0, min_value=0, step=1000)}
        with col4_B:
            possible_units = ["kWh/ano", "ton/ano", "m3/ano"]
            factory_consumption[vector]["consumption_unit"] = st.selectbox("Unidade de consumo", possible_units, key=key_unit)
    n_vectors = len(energy_vectors)

    return n_vectors, factory_consumption


def vector_cost_input(equipment_data):

    st.header("Tarifa associada a cada vetor energético")
    st.write("Indique as tarifas associadas a cada vetor energético utilizado nos equipamentos.")

    # Extract unique energy vectors from the provided equipment data
    energy_vectors = set(
        equipment_data[key]["combustible"]
        for key in equipment_data
    )

    # Dictionary to store tariffs for each vector
    vector_tariffs = {}

    for i, vector in enumerate(energy_vectors):
        key_tariff = f"tariff_{i}"
        key_unit = f"tariff_unit_{i}"

        st.markdown(f"<h3 style='text-align: center; color: green;'>Tarifa para {vector}</h3>", unsafe_allow_html=True)

        col_tariff_A, col_tariff_B = st.columns(2)
        with col_tariff_A:
            vector_tariffs[vector] = {
                "tariff_value": st.number_input(
                    f"Tarifa do vetor {vector} [€/unit]",
                    key=key_tariff,
                    value=0.0,
                    min_value=0.0,
                    step=0.01,
                )
            }
        with col_tariff_B:
            vector_tariffs[vector]["tariff_unit"] = st.selectbox(
                "Unidade da tarifa",
                ["€/kWh", "€/ton", "€/m3"],
                key=key_unit,
            )

    n_vector_tariffs = len(energy_vectors)
    return n_vector_tariffs, vector_tariffs


def main_page():

    # Load and encode the image as base64
    with open("Picture1.png", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    # CSS for styling the background image container and title
    custom_css = f"""
        <style>
            .custom-background {{
                background-image: url("https://tice.pt/sites/default/files/projetos/imagem/ate_logo_color_rgb.png");
                background-size: 300px 181px;
                background-position: top center;
                background-repeat: no-repeat;
                height: 200px;
            }}
            .title-container {{
                text-align: center;
                margin-top: 1rem;
            }}
            .main-content {{
                padding: 2rem;
            }}
            .footer {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                height: 70px;
                padding: 0 2rem;
                background-color: transparent;
            }}
            .footer-left, .footer-right {{
                height: 100%;
                width: auto;
                background-repeat: no-repeat;
                background-size: contain;
            }}
            .footer-left img, .footer-right img {{
                height: 100%;
                object-fit: contain;
            }}
        </style>
        """

    # Apply CSS
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # Background image container
    st.markdown(
        """
        <div class="custom-background">
        </div>
        """,
        unsafe_allow_html=True)

    # Title container
    st.markdown(
        """
        <div class="title-container">
            <h1>Ferramenta de apoio à decisão para integração de gases renováveis em processos industriais</h1>
        </div>
        """,
        unsafe_allow_html=True)

    # Divider to separate sections
    st.divider()

    # Place "Modo de entrada de dados" at the top
    col8, col9 = st.columns([7, 7])
    with col8:
        energy_mode = energy_consumption_mode()
    with col9:
        tariff_mode = energy_tariff_knowledge()

    # Use columns for dynamic content to prevent layout shifts
    col1, buff, col2 = st.columns([7, 0.5, 7])

    if energy_mode == "Desagregado por equipamento":
        if tariff_mode == "Tarifa da base de dados":
            with col1:
                n_equipments, equipment_data = equipments_WebUI()
            with col2:
                n_objectives, scenario_data = objective(equipment_data)
            if st.button("Simulate"):
                if equipment_data and scenario_data:
                    renewable_gases_introduction_sim_eq_database(n_equipments, equipment_data, n_objectives, scenario_data)
                elif not equipment_data:
                    st.warning("Nenhum equipamento disponível. Por favor, insira dados de equipamentos.")
                elif not scenario_data:
                    st.warning("Nenhum cenário de estudo disponível. Por favor, insira dados de cenários.")

        if tariff_mode == "Tarifa inserida pelo utilizador":
            with col1:
                n_equipments, equipment_data = equipments_WebUI()
            with col2:
                n_vector_tariffs, vector_tariffs = vector_cost_input(equipment_data)
                n_objectives, scenario_data = objective(equipment_data)
            
            for vector in vector_tariffs:
                if vector_tariffs[vector]["tariff_value"] == 0:
                    st.warning(f"Aviso: Não foi inserido qualquer tarifa do(s) vetor(es) energético(s): {vector}. Caso não proceda \
                    ao preenchimento dos mesmos será considerado que os mesmos não dispõem de custo de aquisição.")                    
            if st.button("Simulate"):
                if equipment_data and scenario_data:
                    renewable_gases_introduction_sim_eq_user(n_equipments, equipment_data, n_objectives, scenario_data, vector_tariffs)
                elif not equipment_data:
                    st.warning("Nenhum equipamento disponível. Por favor, insira dados de equipamentos.")
                elif not scenario_data:
                    st.warning("Nenhum cenário de estudo disponível. Por favor, insira dados de cenários.")

    else:
        if tariff_mode == "Tarifa da base de dados":
            with col1:
                n_general_equipments, general_equipment_data = equipments_general_consumption_WebUI()
            factory_consumption = factory_consumption_input(general_equipment_data)
            with col2:
                n_objectives, scenario_data = objective(general_equipment_data)
            
            if st.button("Simulate"):
                if equipment_data and scenario_data:
                    renewable_gases_introduction_sim_factory_database(n_general_equipments, general_equipment_data, n_objectives, scenario_data,  factory_consumption)
                elif not general_equipment_data:
                    st.warning("Nenhum equipamento disponível. Por favor, insira dados de equipamentos.")
                elif not scenario_data:
                    st.warning("Nenhum cenário de estudo disponível. Por favor, insira dados de cenários.")
        
        if tariff_mode == "Tarifa inserida pelo utilizador":
            with col1:
                n_general_equipments, general_equipment_data = equipments_general_consumption_WebUI()
            with col2:
                n_vector_tariffs, vector_tariffs = vector_cost_input(general_equipment_data)
                n_objectives, scenario_data = objective(general_equipment_data)
            factory_consumption = factory_consumption_input(general_equipment_data)
            for vector in vector_tariffs:
                if vector_tariffs[vector]["tariff_value"] == 0:
                    st.warning(f"Aviso: Não foi inserido qualquer tarifa do(s) vetor(es) energético(s): {vector}. Caso não proceda \
                    ao preenchimento dos mesmos será considerado que os mesmos não dispõem de custo de aquisição.")
            if st.button("Simulate"):
                if equipment_data and scenario_data:
                    renewable_gases_introduction_sim_factory_user(n_general_equipments, general_equipment_data, n_objectives, scenario_data, factory_consumption, vector_tariffs)
                elif not equipment_data:
                    st.warning("Nenhum equipamento disponível. Por favor, insira dados de equipamentos.")
                elif not scenario_data:
                    st.warning("Nenhum cenário de estudo disponível. Por favor, insira dados de cenários.")

    # Divider to separate sections
    st.divider()

    st.caption("O presente trabalho foi elaborado no âmbito da ATE Agenda – Aliança para a Transição Energética. O seu conteúdo, incluindo análises, \
               opiniões, interpretações e conclusões, é da exclusiva responsabilidade do(s) autor(es) e não reflete necessariamente a posição oficial da \
               ATE, das suas entidades parceiras, membros associados ou de quaisquer entidades financiadoras. A ATE Agenda e o(s) autor(es) declinam qualquer \
               responsabilidade por eventuais erros, omissões ou consequências decorrentes da utilização da informação aqui contida, quer de forma direta, quer indireta.")
    
    # Footer image
    st.markdown(
    f"""
    <div class="footer">
        <div class="footer-left">
            <img src="data:image/png;base64,{encoded_image}" style="height:100%;"/>
        </div>
        <div class="footer-right">
            <img src="https://recuperarportugal.gov.pt/wp-content/uploads/2024/03/footer.webp" style="height:100%;"/>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


if __name__ == "__main__":
    st.set_page_config(page_title="Ferramenta de apoio à decisão de consumidores industriais para introdução GR", layout="wide")
    # Create a sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Páginas disponíveis", ["Ferramenta de apoio", "Informação: Integração de gases renováveis", "Pressupostos","Acerca do Projeto", "Guia de utilização", "FAQ's"]) #Possivelmente ter uma página about, contactos, user guide ou possivelmente FAQ?
    
    if page == "Ferramenta de apoio":
        main_page()
    if page == "Informação: Integração de gases renováveis":
        information_page()
    if page == "Pressupostos":
        assumptions_page()
    if page == "Acerca do Projeto":
        project_page()
    if page == "Guia de utilização":
        guide_page()
    if page == "FAQ's":
        faq_page()
