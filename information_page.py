import streamlit as st
import io
import pandas as pd
import base64

def information_page():
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
    
    st.title('Infomação relevante à integração de gases renováveis em processos industriais')
    # Dados organizados
    data_tubes_fittings = {
        "Norma": [
            "ANSI B31.1", "ASME B31.3", "ASME B31.12", "ASME B31.12", "ANSI B16.5",
            "ANSI B16.20", "ANSI B16.34", "ANSI B16.10", "ANSI B16.104", "ANSI 16.9",
            "ANSI / ASME B 16.10 M", "ANSI B 2.1", "API 520", "API 521", 
            "ASME VII Div. 1", "ASME/AWWA D100", "API Std 650", "API Std 620", 
            "EN 14.620", "EN 10208-1", "EN 13480", "ISO 7", "ISO 228", "ISO 3419",
            "ISO 13623", "ISO 3183", "DIN 30675", "DIN 30677",
            "ASME IX", "ASME V", "AWS D1.1-10", "API Std. 1104", "EN 12732",
            "ISO 1680", "ISO 7919", "ISO 1940", "ISO 11342", "ISO 3746", 
            "ISO 22734", "ISO 15916", "ISO 1940/1", "ISO 2372", "VDI 2056"],
        "Descrição": [
            "Power piping", "Process piping", "Hydrogen piping and pipelines",
            "Hydrogen piping and pipelines", "Steel pipe flanges and flanged fittings",
            "Ring-joint gaskets and grooves for steel pipe flanges", "Steel butt-weld end valves",
            "Face to face end to end dimensions of ferrous valves", "Control valve seat leakage",
            "Wrought steel butt - welding fittings", "Wekded and seamless wrought steel pipe",
            "Pipe threads (except dryseal)", "Sizing, selection, and installation of pressure-relieving devices in refineries",
            "Pressure-relieving and depressuring systems", "Design, construction, and inspection of tanks and pressure vessels",
            "Welded steel tanks for water storage", "Welded tanks for oil storage", 
            "Design and construction of large, welded low-pressure storage tanks",
            "Design and manufacture of site built, vertical, cylindrical, flatt-bottomed steel tanks for the storage of refrigerated, liquified gases with operating temperatures between 0 °C and -165 °C",
            "Steel pipes for pipelines for combustible fluids", "Metallica industrial piping",
            "Pipe threads where pressure-tight joints are made on the threads",
            "Pipe threads where pressure-tight joints are not made on the threads",
            "Non alloy and alloy steel buttwelding fittings", "Pipeline transportation systems",
            "Steel pipe for pipeline transportation systems", "External corrosion protection of buried steel pipes",
            "Design and application of cathodic protection", "Welding and brazing qualification",
            "Boiler and pressure vessel code, section V: Non-destructive examination",
            "Structural welding code - vessels", "Standard for welding pipeline and related facilities",
            "Gas infrastructures - Welding steel pipework",
            "Mechanical Vibration", "Mechanical vibrations of non-reciprocating machines - Measurement on rotating shafts and evaluation criteria",
            "Balance quality requirements for robots in a constant (rigid) state",
            "Mechanical vibration - Methods and criteria for the mechanical balancing of flexible rotors",
            "Acoustics - Determination of sound power levels of noise sources using sound pressure - Survey method using an enveloping measurement surface over a reflecting plane",
            "Hydrogen Electrolyser", "Hydrogen Production Plant",
            "Mechanical vibration - Balance quality requirements of rigid motors",
            "Mechanical vibration of machines with operating speeds from 10 to 200 rev/s",
            "Criteria for assessing mechanical vibrations of machines"]
        }
    
    data_reservoirs = {
    "Norma": [
        "Decreto-Lei nº. 131/2019 de 30 de agosto",
        "Despacho nº. 1859/2003, de 30 da janeiro"
    ],
    "Descrição": [
        "Aprova o Regulamento de Instalação e de Funcionamento de Recipientes sob Pressão Simples e de Equipamentos sob Pressão",
        "Aprova e publica, em anexo, a Instrução Técnica Complementar para Recipientes Sob Pressão de Ar Comprimido"
    ]}

    #Ambiente e Segurança – Enquadramento Legal
    data_environment_safety = {
    "Norma": [
        "Decreto-Lei nº. 30-A/2022 de 18 de abril",
        "Decreto-Lei nº. 151-B/2013 de 31 de outubro",
        "Decreto-Lei nº. 150/2015 de 5 de agosto",
        "Decreto-Lei nº. 220/2008 de 12 de novembro",
        "Portaria nº. 1532/2008 de 29 de dezembro",
        "Decreto-Lei nº. 236/2003 de 30 de dezembro",
        "Decreto-Lei nº. 111-C/2017 de 31 de agosto",
        "Decreto-Regulamentar nº. 1/1992 de 18 de fevereiro",
        "Decreto-Lei nº. 9/2007 de 17 de janeiro",
        "API RP 505",
        "IEC 60079",
        "IEC 60529",
        "NFPA 2",
        "NFPA 11",
        "NFPA 13",
        "NFPA 14",
        "NFPA 15",
        "NFPA 20",
        "NFPA 22",
        "NFPA 24",
        "NFPA 55",
        "NFPA 72",
        "EN 1866",
        "EN 694",
        "EN 13565",
        "EN 3"],
    "Descrição": [
        "Aprova medidas excecionais que visam assegurar a simplificação dos procedimentos de produção de energia a partir de fontes renováveis",
        "Estabelece o regime jurídico da avaliação de impacte ambiental (AIA) dos projetos públicos e privados suscetíveis de produzirem efeitos significativos no ambiente",
        "Estabelece o regime de prevenção de acidentes graves que envolvem substâncias perigosas e de limitação das suas consequências para a saúde humana e para o ambiente",
        "Estabelece o regime jurídico da segurança contra incêndios em edifícios",
        "Aprova o Regulamento Técnico de Segurança contra Incêndio em Edifícios (SCIE)",
        "Estabelece os preceitos mínimos para promover a segurança e saúde dos trabalhadores expostos a atmosferas explosivas (ATEX). Transpõe a Diretiva nº 1999/92/EC",
        "Estabelece as regras de segurança para aparelhos e sistemas de proteção utilizados em atmosferas potencialmente explosivas, transpondo a Diretiva nº 2014/34/UE",
        "Aprova o Regulamento de Segurança para Linhas Elétricas de Alta Voltagem",
        "Aprova o Regulamento Geral do Ruído e revoga o regime legal da poluição sonora",
        "Recommended Practice for Classification of Locations for Electrical Installation at Petroleum Facilities as Class I, Zone 0, Zone 1 and Zone 2",
        "Explosive atmospheres",
        "Degrees of protection provided by enclosures (IP Code)",
        "Hydrogen Technologies Code",
        "Standard for Low-, Medium-, and High-Expansion Foam",
        "Installation of Sprinkler Systems",
        "Standard for the Installation of Standpipe, Private Hydrant and Hose Systems",
        "Standard for Water Spray Fixed Systems for Fire Protection",
        "Standard for the Installation of Stationary Pumps for Fire Protection",
        "Standard for Water Tanks for Private Fire Protection",
        "Installation of Private Fire Service Mains and Their Appurtenances",
        "Compressed Gases and Cryogenic Fluids Code",
        "National Fire Alarm Code",
        "Mobile Fire Extinguishers",
        "Fire-fighting hoses. Semi-rigid hoses for fixed systems",
        "Foams",
        "Requirements for portable fire extinguishers"
    ]}
    # Criar dataframe
    df_tubes = pd.DataFrame(data_tubes_fittings)
    df_reservoir = pd.DataFrame(data_reservoirs)
    df_data_environment_safety = pd.DataFrame(data_environment_safety)

    # Exibir tabela no Streamlit
    st.header("Normas Técnicas")
    st.write("As tabelas abaixo apresentam uma sistematização de normas técnicas por categoria:")
    with st.expander("Tubagens de gás, transições e acessórios"):
        st.dataframe(df_tubes, use_container_width=True)
    with st.expander("Reservatórios pressurizados"):
        st.dataframe(df_reservoir, use_container_width=True)
    with st.expander("Segurança e Ambiente"):
        st.dataframe(df_data_environment_safety, use_container_width=True)
    
    st.write("Poder-se-á ainda aceder a mais informação relacionada com normas e regulamentações ou boas práticas associadas à introdução de gases renováveis através dos seguintes links:")
    st.write("- https://observatory.clean-hydrogen.europa.eu/hydrogen-landscape/policies-and-standards")
    st.write("- https://h2tools.org/hydrogen-fuel-cell-codes-standards")
    st.write("- https://h2tools.org/bestpractices/best-practices-overview")
    

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
