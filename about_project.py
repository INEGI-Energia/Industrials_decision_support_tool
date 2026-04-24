import streamlit as st
import io
import base64
import pandas as pd

def project_page():
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
    
    st.title('Acerca do projeto')
    st.write("A Aliança para a Transição Energética visa o reforço da competitividade e resiliência das empresas do setor energético como resultado da criação de produtos e soluções \
             inovadoras e de cariz exportador, tendo por base tecnologia e know-how desenvolvido e consolidado no sector, colocando Portugal na liderança da descarbonização e \
             potenciando uma efetiva transição energética.")
    st.divider()

    # Show data table of all energy vectors in Streamlit
    st.header("ATE PPS 39")
    st.write("O PPS 39 visa desenvolver sistemas avançados de apoio à decisão e planeamento para a injeção de gases renováveis na rede, assegurando assegurando uma integração eficiente e segura dos gases renováveis no processo de descarbonização dos diferentes setores. \
    A iniciativa inclui o mapeamento espacial e temporal da penetração do H₂, disponibilizando uma ferramenta para consumidores industriais que oferece um guia metodológico para a descarbonização de processos,\
    um guia tecnológico que promove o setor produtivo nacional e a sua internacionalização, e uma ferramenta de autodiagnóstico para a indústria.Além disso, o projeto desenvolve soluções para a adaptação de motores \
    de cogeração ao uso de H₂, otimizados para reduzir emissões de NOₓ, e avalia o impacto da injeção gradual deste gás em centrais de cogeração, analisando materiais, processos de combustão, segurança e condições \
    operacionais. O objetivo final é definir requisitos e especificações técnicas para garantir o funcionamento eficiente e seguro destas centrais num cenário de crescente integração de hidrogénio.")
    st.divider()
    
    # Show assumptions related with hydrogen production calculations
    st.header('Ferramenta de apoio à decisão de consumidores industriais para integração de gases renováveis')
    st.write("**Objetivos**")
    st.write("📌    Facilitar o autodiagnóstico energético para a indústria (Equipamentos térmicos)") 
    st.write("📌    Comparar impactos tecno-económicos e ambientais da integração de vetores descarbonizados e novas tecnologias")
    
    st.write("**Tecnologia**")
    st.write("📌    Streamlit (Python) - Interface gráfica dinâmica e intuitiva")

    st.write("**Funcionalidades Principais**")

    st.write("📌    Análise Personalizada - Adaptação a diferentes perfis industriais")

    st.write("📌    Comparação de Cenários Avaliação de alternativas sustentáveis")

    st.write("📌    Interface Intuitiva Facilidade de uso para o utilizador")
    

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
