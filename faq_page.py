import streamlit as st
import io
import base64
import pandas as pd

def faq_page():
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
    
    st.title('Questões frequentes')

    # Secção Conceitos Básicos
    st.subheader("🔍 Conceitos Básicos")
    with st.expander("1. O que é o hidrogénio renovável e como é produzido?"):
        st.write("""Existem diferentes métodos de produção de hidrogénio, sendo que nem todos são considerados renováveis. Atualmente, é estimado que cerca de 75% da produção total de H2 é efetuada a partir da \
        reformação de metano, seguida por 23% através da queima de carvão. Apenas uma fração muito reduzida é produzida por vias consideradas renováveis.""")
        st.write("""Neste contexto, na União Europeia, considera-se "hidrogénio renovável" aquele que é produzido através de processos que utilizam energia proveniente de fontes renováveis, nomeadamente a eletrólise \
        da água abastecida por eletricidade renovável, processo que, quando corretamente rastreado, não origina emissões diretas de GEE durante a produção.""")

    with st.expander("2. Que cores do hidrogénio existem e o que significam? "):
        # Lista com as cores e respetivas origens
        dados = [
            ("Verde", "Renovável"),  # Verde
            ("Branco", "Hidrogénio naturalmente presente no subsolo"),  
            ("Azul", "Reformação de metano com captura de carbono"),  
            ("Turquesa", "Pirólise de metano"), 
            ("Rosa", "Energia nuclear"), 
            ("Cinzento", "Reformação de metano sem captura de carbono"),
            ("Preto", "Carvão")]
        # Criar o DataFrame
        df = pd.DataFrame(dados, columns=["Código cor", "Origem de energia"])
        
        st.write("""Como referido anteriormente, o hidrogénio pode ser produzido por diferentes métodos, utilizando fontes de energia renováveis ou combustíveis fósseis. Cada método de produção está associado a \
        diferentes níveis de emissões de gases com efeito de estufa (GEE). Para facilitar a compreensão e comunicação sobre a origem e impacto ambiental do hidrogénio, foi adotado, de forma não oficial,\
        um sistema de codificação por cores. Este esquema associa uma cor ao hidrogénio consoante o método de produção e a fonte energética utilizada.""")
        st.dataframe(df)
        

    # Secção Aplicações Industriais
    st.subheader("🏭 Aplicações Industriais")
    with st.expander("3. Atualmente, quais são os principais usos do hidrogénio?"):
        st.write("""Atualmente, o hidrogénio é utilizado sobretudo como matéria-prima em processos industriais, com destaque para os seguintes setores:""")
        st.write("""- Produção de amoníaco (NH₃), principal componente de fertilizantes agrícolas, através do processo Haber-Bosch.""")
        st.write("""- Refinarias de petróleo, onde é utilizado para o hidrotratamento e a hidrodesulfurização, ajudando a remover impurezas como o enxofre dos combustíveis.""")
        st.write("""- Produção de metanol, utilizado como solvente, combustível e intermediário químico.""")
        st.write("""- Indústria eletrónica e do vidro, como gás de processo de elevada pureza.""")
        st.write("""- Para além destes, há aplicações mais específicas e de menor escala, como o uso de hidrogénio líquido como combustível para foguetões na indústria aeroespacial (por exemplo, pela NASA).""")
        st.write("""Importa salientar que a grande maioria do hidrogénio atualmente consumido a nível mundial é produzido a partir de combustíveis fósseis representando elevadas emissões de gases com efeito de estufa. \
        Por este motivo, a descarbonização da produção de hidrogénio constitui uma prioridade estratégica para a transição energética e para a indústria de base química.""")

    with st.expander("4. Em que processos industriais pode o H2 renovável vir a substituir combustíveis fósseis?"):
        st.write("""O hidrogénio tem potencial para substituir combustíveis fósseis em vários processos industriais intensivos em energia e emissões, contribuindo para a descarbonização do setor. \
        Os principais exemplos incluem:""")
        st.write("""- O hidrogénio pode substituir o carvão (coque) no processo de redução de minério de ferro, dando origem ao chamado ferro de redução direta (DRI) com emissões muito reduzidas. Este \
        processo é central na transição para o aço verde.""")
        st.write("""- Em setores como a cerâmica, vidro, cimento, papel e pasta de papel, o hidrogénio pode ser utilizado como combustível direto nos fornos e caldeiras industriais, substituindo gás natural \
        ou outros combustíveis fósseis.""")
        st.write("""- Além de ser uma matéria-prima tradicional (por exemplo, na produção de amoníaco ou metanol), o hidrogénio renovável pode substituir o H₂ fóssil atualmente utilizado, descarbonizando \
        significativamente estes processos.""")
        st.write("""- O hidrogénio pode ser usado em sistemas de cogeração (produção combinada de calor e eletricidade), como alternativa ao gás natural em motores, turbinas ou células de combustível.""")
        st.write("""- Embora o setor das refinarias utilize hidrogénio sobretudo como reagente, o hidrogénio renovável pode substituir o convencional para reduzir a pegada de carbono dos combustíveis fósseis enquanto\
        estes forem necessários.""")

    # Seção Técnica
    st.subheader("⚙️ Aspectos Técnicos")
    with st.expander("5. Existem desafios técnicos em se introduzir hidrogénio em processos industriais?"):
        st.write("""Podem existir desafios técnicos relevantes relacionados com a introdução de hidrogénio em processos industriais, mas é importante sublinhar desde já que estes \
        variam de processo para processo. A substituição total ou parcial de combustíveis fósseis por hidrogénio deve ser sempre precedida por uma análise técnica cuidadosa, que tenha em conta \
        as especificidades do processo industrial, os equipamentos existentes, os requisitos térmicos e as condições de operação. Alguns destes desafios poderão estar relacionados com:""")
        st.write("""- Adaptação dos queimadores e sistemas de combustão""")
        st.write("""- Elevada temperatura de chama e formação de NOₓ""")
        st.write("""- Segurança e deteção de fugas""")
        st.write("""- Fragilização de materiais""")
        st.write("""- Controlo e monitorização""")

    with st.expander("6. Qual a diferença entre introduzir 20% H2 em base volúmica e introduzir 20% H2 em base mássica numa mistura com gás natural?"):
        st.write("""Introduzir 20% de hidrogénio em base volúmica significa que, em cada unidade de volume da mistura gasosa (por exemplo, 1 m³), 20% corresponde a hidrogénio (H₂) e 80% a gás natural.\
        Já introduzir 20% de hidrogénio em base mássica significa que, em cada unidade de massa total da mistura (por exemplo, 1 kg), 20% corresponde à massa de hidrogénio e 80% à massa do outro gás.
        Como o hidrogénio é um gás menos denso do que o gás natural — tem uma massa molar de 0,0899 kg/m³, contra cerca de 0,8019 kg/m³ para o metano — esta diferença de base (volumétrica vs mássica)\
        tem implicações relevantes:""")
        st.write("""- Ao se introduzir 20% de H₂ em base volúmica, o conteúdo energético da mistura diminui de forma significativa, por se estar a substituir parte do gás com maior densidade energética \
        (gás natural) por outro com menor densidade energética (hidrogénio).""")
        st.write("""- Ao se introduzir 20% de H₂ em base mássica, a fração de hidrogénio em termos de volume será muito maior (cerca de 55-60% em volume, dependendo das condições), porque o H₂ é muito mais leve\
        — o que altera muito mais as propriedades físicas da mistura.""")

    # Secção Segurança
    st.subheader("🛡️ Segurança e Regulamentação")
    with st.expander("7. Quais normas de segurança aplicam-se à introdução de hidrogénio em ambiente industrial?"):
        st.write("""Na página “Informação: Integração de Gases Renováveis” são identificadas várias normas relevantes para as diferentes vertentes associadas à \
        introdução de gases renováveis, entre as quais se destaca a segurança. No contexto da utilização de hidrogénio em ambiente industrial, algumas normas de\
        referência incluem:""")
        st.write("""- IEC 60079 – relativa a atmosferas explosivas (ATEX), abrangendo requisitos para o equipamento e proteção em ambientes com risco de explosão;""")
        st.write("""- NFPA 2 – código da National Fire Protection Association dedicado especificamente ao hidrogénio, com orientações para o seu armazenamento,\
        manuseamento e utilização segura;""")
        st.write("""- API RP 505 – prática recomendada pelo American Petroleum Institute sobre classificação de áreas perigosas em instalações com atmosferas inflamáveis.""")
        st.write("""- Estas normas constituem uma base técnica essencial para garantir a segurança na integração do hidrogénio em ambientes industriais, devendo ser \
        complementadas com a legislação nacional aplicável.""")

    with st.expander("8. Que regulamentos da legislação nacional deve-se considerar para garantir a conformidade legal e segurança operacional na instalação de um sistema de armazenamento de \
    hidrogénio gasoso pressurizado?"):
        st.write("""Tendo em conta a informação apresentada no Decreto-Lei n.º 131/2019, de 30 de agosto, relativa às condições de segurança requeridas para o caso do hidrogénio no estado \
        gasoso deve ser tido em conta o Despacho nº 2957/2022, de 9 de março, onde é aprovada a “instrução técnica complementar que estabelece as regras técnicas relativas à instalação e \
        funcionamento dos recipientes destinados a conter ar, oxigénio ou gases inertes comprimidos”.""")

    # Secção Económica
    st.subheader("💼 Viabilidade Económica")
    with st.expander("9. Que incentivos existem para a implementação de hidrogénio renovável?"):
        st.write("""Tanto a nível nacional como europeu têm sido disponibilizados, nos últimos anos, diversos mecanismos de financiamento para promover a produção e a integração do hidrogénio na economia. Estes incentivos\
        têm-se concentrado maioritariamente no apoio à oferta, isto é, nos produtores, quer através do financiamento de investimentos iniciais, quer através do apoio direto ao custo de produção.\
        Em Portugal, destacam-se os seguintes instrumentos de apoio:""")
        st.write("""- **Compra centralizada de gases renováveis (2024)** – Procedimento nacional que visa apoiar projetos de produção de hidrogénio renovável e biometano, com uma dotação anual de 14 milhões\
        de euros, podendo atingir 140 milhões de euros ao longo de 10 anos. O principal objetivo é mitigar a volatilidade do preço da energia, com um preço máximo de 127 €/MWh para o hidrogénio\
        e 62 €/MWh para o biometano.""")
        st.write("""- **POSEUR-01-2020-19 (2020-2021)** – Programa com uma dotação total de 40 milhões de euros, com um apoio máximo de 5 milhões de euros por operação e por beneficiário, destinado a projetos\
        de produção de hidrogénio renovável.""")
        st.write("""- **PRR – Componente C14: Apoio à Produção de Hidrogénio e Gases Renováveis**:""")
        st.write("""- 1.ª fase (01/C14-i01/2021): 62 milhões de euros de dotação total, com um máximo de 5 milhões de euros por projeto.""")
        st.write("""- 2.ª fase (02/C14-i01/2023): 83 milhões de euros de dotação total, com aumento do apoio máximo por operação para 15 milhões de euros.""")
        st.write("""- **01/RP-C21-i06/2024, Medida reforçada: Hidrogénio renovável e outros gases renováveis**:""")
        st.write("""- Reforço de 70 milhões de euros, também com um limite de 15 milhões de euros por beneficiário, para ampliar a capacidade de produção.""")



    # Seção Sustentabilidade
    st.subheader("🌱 Sustentabilidade")
    with st.expander("10. Qual é a redução de emissões associada à substituição de um combustível por hidrogénio? "):
        # Dados da tabela
        data = {
            "Combustível Substituído": ["Gás Natural", "GPL (butano/propano)", "Gasóleo", "Carvão"],
            "Redução ao substituir por H₂ renovável (kgCO₂/MWh)": [202, "230–250", 266, "340–380"]}
        # Criar DataFrame
        df = pd.DataFrame(data)
        
        st.write("""A redução de emissões de CO₂ ao substituir um combustível por hidrogénio depende do vetor energético substituído e assume-se, neste caso, a utilização de hidrogénio renovável, cujas emissões\
        diretas de CO₂ na utilização são nulas. Considerando apenas as emissões diretas (combustão) e expressando a comparação por MWh de energia útil, as reduções estimadas são as seguintes:""")
        st.dataframe(df, use_container_width=True)
        st.write("""Estes valores podem variar ligeiramente conforme o poder calorífico e características específicas de cada combustível. Em termos práticos, a substituição por hidrogénio renovável pode\
        permitir reduções de 200 a 380 kgCO₂ por MWh de energia substituída.Importa ainda considerar que, se forem incluídas emissões do ciclo de vida completo, estas reduções podem ser ajustadas, dependendo \
        da forma de produção e transporte do hidrogénio e do combustível substituído.""")

    with st.expander("11. Se introduzir 20% H2 em base volúmica numa mistura com gás natural é possível descarbonizar 20% das emissões de um processo industrial?"):
        st.write("""Não, introduzir 20% de hidrogénio em base volúmica não implica uma redução de 20% das emissões de gases com efeito de estufa (GEE) de um processo industrial.\
        A relação entre percentagem volumétrica e descarbonização é não linear, devido às diferentes características físico-químicas do hidrogénio em relação gás natural. Eis porquê:""")
        st.write("""O hidrogénio tem menor densidade energética por unidade de volume - o Poder Calorífico Inferior do hidrogénio é cerca de 10,8 MJ/m³ e do metano (principal constituinte do gás natural) 35,8 MJ/m³.""")
        st.write("""Por outro lado, a redução real de emissões depende da energia substituída. Como o H₂ ocupa mais volume que o gás natural para a mesma energia entregue, a fração de CH₄ que é efetivamente substituída\
        é menor do que 20% da energia, logo a redução de emissões também será inferior a 20%. Assim, em termos práticos, substituir 20% do volume de CH₄ por H₂ pode levar a uma redução de emissões na ordem \
        dos 7 a 10% e não de 20%, dependendo da composição e do tipo de processo.""")


    # Secção Implementação
    st.subheader("🔧 Integração Industrial")
    with st.expander("13. Existem casos de sucesso de integração de hidrogénio em processsos industriais?"):
        st.write("""Sim, existem diversos casos de sucesso de integração de hidrogénio renovável em processos industriais, tanto a nível europeu como internacional.\
        Estes projetos demonstram a viabilidade técnica e económica da substituição de combustíveis fósseis por hidrogénio, sobretudo em setores com emissões difíceis de\
        abater (“hard-to-abate”). Alguns exemplos relevantes incluem:""")
        st.write("""- HYBRIT (Suécia): https://www.hybritdevelopment.se/en/""")
        st.write("""- H2FUTURE (Áustria): https://www.h2future-project.eu/en""")
        st.write("""- GrinHy 2.0 (Alemanha): https://salcos.salzgitter-ag.com/de/grinhy-20.html""")
        st.write("""A nível nacional, também existem projetos relevantes em funcionamento, tanto ao nível da produção como do consumo de hidrogénio, que demonstram a viabilidade\
        técnica desta solução em contexto real. Destacam-se iniciativas como as existentes em Sines, com foco na produção e exportação de hidrogénio verde, e projetos industriais \
        em curso promovidos por diversas empresas a que avaliam a substituição de combustíveis fósseis por hidrogénio nos seus processos.""")
        st.write("""Além disso, têm sido realizados testes e projetos de demonstração em setores como a cerâmica, cimento e metalurgia, suportados por programas de financiamento \
        público. Estes casos reforçam a ideia de que o hidrogénio renovável pode desempenhar um papel estratégico na transição energética da indústria.""")
    

    with st.expander("14. Quais são as tendências futuras para o mercado do hidrogénio?"):
        st.write("""A definir""")
    
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
