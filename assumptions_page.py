import streamlit as st
import io
import pandas as pd
import base64
from subroutines import data


def assumptions_page():
    data_table = data()
    data_table_trimmed = data_table.iloc[:, :-2]
    data_table_trimmed = data_table_trimmed.fillna("Não considerado")
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
    

    # Create dataframe
    df = pd.DataFrame(data_table_trimmed)
    df.columns = ["Vector","PCI [MJ/kg]","Density [kg/m³]","Emission factor [kgCO₂/MJ]","Reference tariff [€/kWh]"]

    # Show data table of all energy vectors in Streamlit
    st.header("Pressupostos da ferramenta")
    st.write("A tabela abaixo apresenta as propriedades consideradas para os dos vetores energéticos disponíveis na ferramenta:")
    st.markdown(
    """
    <div style="font-size:20px;">
        Propriedades dos vetores energéticos
    </div>
    """,
    unsafe_allow_html=True,)
    st.dataframe(df)

    # Show assumptions related with hydrogen production calculations
    st.header('Pressupostos assumidos quanto à produção de hidrogénio')
    st.write(" Para os cálculos efetuados relativos à produção de hidrogénio foi necessário recorrer-se à definição de pressupostos que os fundamentassem. Estes são apresentados de seguida:")
    st.write("- Custo do eletrolisador: 4841 x P⁻⁰.¹⁹⁸ €/MW")
    st.write("- Eficiência do eletrolisador: 65%")
    st.write("- Consumo de água: 18 kg H₂O/ kgH₂")
    st.write("- Taxa de emissão de carbono: 68.368 €/tonCO₂eq")
    st.write("")
    st.write("P = potência nominal do eletrolisador")

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
