import streamlit as st
import io
import base64
import pandas as pd

def guide_page():
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
    
    st.title('Guia de utilização')

    # Show data table of all energy vectors in Streamlit
    st.header("Inserção de inputs")
    st.write("A ferramenta de apoio à decisão para integração de gases renováveis em processos industriais consiste no tratamento de dados tendo em conta as características associadas a cada \
             um dos equipamentos em estudo e ao vetor energético (ou mistura de vetores) para o qual se pretende transitar.")
    st.write("Em primeiro lugar, dever-se-á descrever as informações associadas \
             aos equipamentos. Para isto será fundamental indicar qual o modo de entrada dos dados pretendido (Figura 1).")
    
    #Figura 1
    image_path_fig1 = r"Modo_entrada_dados.PNG"
    # Exibir a imagem no Streamlit
    st.image(image_path_fig1, caption="Figura 1 - Modo de entrada dos dados", width=400)

    st.write("Caso se possua os consumos energéticos desagregados por equipamento é aconselhado que se selecione essa opção dado garantir uma maior proximidade à realidade dos resultados\
              obtidos relativamente aos fatores de descarbonização e económicos. Caso contrário bastará indicar que apenas se possui conhecimento do consumo total da fábrica, aparecendo \
             de seguida o espaço na tela para que se possa fazê-lo (Figura 2).")
    
    #Figura 2
    image_path_fig2 = r"Indicacao_consumo_fabrica.PNG"
    # Exibir a imagem no Streamlit
    st.image(image_path_fig2, caption="Figura 2 - Indicação do consumo total da fábrica", width=400)

    st.write("De seguida é dada a possibilidade ao utilizador de definir o número de equipamentos que pretende estudar e preencher as informações acerca de cada um deles (Figura 3). \
             Para cada um deles deverá definir o tipo de equipamento, o nome que lhe pretende atribuir, a sua potência nominal, o vetor energético em uso e, caso possua os consumos \
             desagregados, o seu consumo energético.")
    
    #Figura 3
    image_path_fig3 = r"Equipamentos_a_estudar.PNG"
    # Exibir a imagem no Streamlit
    st.image(image_path_fig3, caption="Figura 3 - Indicação do número de equipamentos a estudar", width=400)
    #Figura 4
    image_path_fig4 = r"Preenchimento_equipamento.PNG"
    # Exibir a imagem no Streamlit
    st.image(image_path_fig4, caption="Figura 4 - Indicação das características de cada equipamento", width=400)

    st.write("O utilizador poderá ainda definir a tarifa associada a cada um dos vetores energéticos em uso, ou caso não o pretenda poderá realizar as simulações tendo em conta os \
             valores estipulados na base de dados.")
    
    #Figura 5
    image_path_fig5 = r"Modo_tarifa_vetores.PNG"
    # Exibir a imagem no Streamlit
    st.image(image_path_fig5, caption="Figura 5 - Modos de inserção das tarifas dos vetores energéticos", width=400)
    #Figura 6
    image_path_fig6 = r"Tarifa_vetores.PNG"
    # Exibir a imagem no Streamlit
    st.image(image_path_fig6, caption="Figura 6 - Indicação da tarifa de cada vetor energético", width=400)

    st.write("Por fim, o utilizador poderá definir cada um dos cenários objetivos que pretende simular. Para isso em primeiro lugar deverá indicar se a sua instituição é abrangida pelo \
             CELE (Comércio Europeu de Licenças de Emissão) dado este input impactar os resultados financeiros associados à venda de licenças das emissões de carbono evitadas com a \
             modificação dos vetores energéticos em uso.")
    st.write("De seguida deverá indicar os equipamentos que pretende selecionar para cada um dos cenários e as percentagens de hidrogénio e biometano na mistura de gás a ser \
             usada – Figura 7.")
    
    #Figura 7
    image_path_fig7 = r"Preenchimento_cenarios.PNG"
    # Exibir a imagem no Streamlit
    st.image(image_path_fig7, caption="Figura 7 - Indicação das características de cada cenário", width=400)
    
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
