import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from PIL import Image
import base64
from streamlit_option_menu import option_menu

def get_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

encoded_image = get_base64("suss22.jpg")
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_image}");
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

selected = option_menu(
    menu_title= None,
    options= ['Cables', 'Transformateurs', 'Cellules'],
    default_index=0,
    orientation='horizontal',
    styles={
        'container' : {'padding': '0!important', 'background-color' : 'white'},
        'nav-link': {
            'font-size': '25px',
            'text-align':'left',
            'margin': '0px',
            '--hover-color': '#eee'
        },
        'nav-link-selected': {'background-color': 'grey'},
    },
)


if selected == 'Cables':

    st.markdown(
        "<h1 style='color: #4D5D48;'>Estimez le matériau le plus éco-responsable pour votre projet</h1>",
        unsafe_allow_html=True
        )


    st.markdown(
        "<span style='color: #4D5D48; font-size: 18px;'>Choisissez la section pour l'aluminium :</span>",
        unsafe_allow_html=True
        )  
    section1 = st.selectbox("", (25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400, 500, 630), key="section1")

    st.markdown(
        "<span style='color: #4D5D48; font-size: 18px;'>Distance pour l'aluminium :</span>",
        unsafe_allow_html=True
        )
    distance1 = st.text_input("", value="1", key="distance1")

    st.markdown(
        "<span style='color: #4D5D48; font-size: 18px;'>Choisissez la section pour le cuivre :</span>",
        unsafe_allow_html=True
        )
    section2 = st.selectbox("", (25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400, 500, 630), key="section2")

    st.markdown(
        "<span style='color: #4D5D48; font-size: 18px;'>Distance pour le cuivre :</span>",
        unsafe_allow_html=True
        )
    distance2 = st.text_input("", value="1", key="distance2")

    if st.button("Valider"):

        section1 = int(section1)
        distance1 = float(distance1)*0.001
        section2 = int(section2)
        distance2 = float(distance2)*0.001
    
        poids1 = {25: 140, 35: 173, 50: 225, 70: 296, 95: 385, 120: 470, 150: 590, 185: 713, 240: 905, 300: 1118, 400: 1446, 500: 1785, 630: 2294}.get(section1, 0)
        poids2 = {25: 277, 35: 372, 50: 493, 70: 685, 95: 933, 120: 1178, 150: 1428, 185: 1786, 240: 2289, 300: 2899, 400: 3715, 500: 4942, 630: 6234}.get(section2, 0)

        masse_totale1 = poids1 * distance1
        masse_totale2 = poids2 * distance2

        if poids1 > 425.5:
            B39, C39 = 4.1, 24.3
        else:
            B39, C39 = 4.97, -49.4

        wb = load_workbook("Calcul_GWP.xlsx", data_only=True)
        ws = wb.active

        B40 = ws["B40"].value
        C40 = ws["C40"].value
        B41 = ws["B41"].value
        C41 = ws["C41"].value
        B42 = ws["B42"].value
        C42 = ws["C42"].value

        fab1 = B39 * masse_totale1 + C39
        distrib1 = B40 * masse_totale1 + C40
        installation1 = B41 * masse_totale1 + C41
        fdv1 = B42 * masse_totale1 + C42
        total1 = fab1 + distrib1 + installation1 + fdv1

        if masse_totale2 > 2049.5:
            H39, I39 = 2.28, -289
        else:
            H39, I39 = 2.15, 17.4

        H40 = ws["H40"].value
        I40 = ws["I40"].value
        H41 = ws["H41"].value
        I41 = ws["I41"].value
        H42 = ws["H42"].value
        I42 = ws["I42"].value

        fab2 = H39 * masse_totale2 + I39
        distrib2 = H40 * masse_totale2 + I40
        installation2 = H41 * masse_totale2 + I41
        fdv2 = H42 * masse_totale2 + I42

        if poids2==1786:
            total2= distance2*4370
        else:
            total2 = fab2 + distrib2 + installation2 + fdv2
    
        if total1 > total2:
            materiau = 'le cuivre'
        else:
            materiau = "l'aluminium"

        GWP1 = round(abs(total1), 2)
        GWP2 = round(abs(total2), 2)

        st.success(f"Le matériau à utiliser est **{materiau}**")
        st.metric(label="Total GWP de l'aluminium", value=f"{GWP1} kg CO₂")
        st.metric(label="Total GWP du cuivre", value=f"{GWP2} kg CO₂")
        
if selected == 'Transformateurs':

    st.markdown(
        "<h1 style='color: #4D5D48;'>Estimez le bilan carbone de votre transformateur</h1>",
        unsafe_allow_html=True
        )


    st.markdown(
        "<span style='color: #4D5D48; font-size: 18px;'>Choisissez la section pour l'aluminium :</span>",
        unsafe_allow_html=True
        )  
    
    section1 = st.selectbox("", (100, 160, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150), key="section1")

    if st.button("Valider"):

        section1 = int(section1)
    
        Fabrication_coeff = {100: 0.30, 160: 0.32, 250: 0.42, 315: 0.48, 400: 0.52, 500: 0.57, 630: 0.65, 800: 0.79, 1000: 1, 1250: 1.14, 1600: 1.36, 2000: 1.67, 2500: 2.03, 3150 : 2.5 }.get(section1, 0)
        Distribution_coeff= {100: 0.30, 160: 0.32, 250: 0.42, 315: 0.48, 400: 0.52, 500: 0.57, 630: 0.65, 800: 0.79, 1000: 1, 1250: 1.14, 1600: 1.36, 2000: 1.67, 2500: 2.03, 3150 : 2.5 }.get(section1, 0)
        Installation_coeff= {100: 1, 160: 1, 250: 1, 315: 1, 400: 1, 500: 1, 630: 1, 800: 1, 1000: 1, 1250: 1, 1600: 1, 2000: 1, 2500: 1, 3150 : 1 }.get(section1, 0)
        Utilisation_coeff= {100: 0.19, 160: 0.27, 250: 0.35, 315: 0.41, 400: 0.49, 500: 0.6, 630: 0.74, 800: 0.86, 1000: 1, 1250: 1.18, 1600: 1.43, 2000: 1.71, 2500: 2.04, 3150 : 2.45 }.get(section1, 0)
        fin_coeff= {100: 0.30, 160: 0.32, 250: 0.42, 315: 0.48, 400: 0.52, 500: 0.57, 630: 0.65, 800: 0.79, 1000: 1, 1250: 1.14, 1600: 1.36, 2000: 1.67, 2500: 2.03, 3150 : 2.5 }.get(section1, 0)
        
        Fabrication= 17300* Fabrication_coeff
        Distribution= 482*Distribution_coeff
        Installation= 0.282*Installation_coeff
        Utilisation= 189000*Utilisation_coeff
        Fin= 196*fin_coeff
        
        total= Fabrication+Distribution+Installation+Utilisation+Fin
        
        GWP1 = round(abs(total), 2)

        st.metric(label="Total GWP du transformeur séléctionné", value=f"{GWP1} kg CO₂")

if selected == 'Cellules':

    st.markdown(
        "<h1 style='color: #4D5D48;'>Estimez le bilan carbone de vos cellules</h1>",
        unsafe_allow_html=True
        )
    
    cellules_selectionnees=[]
    if "cellule_count" not in st.session_state:
        st.session_state.cellule_count = 1

    for i in range(st.session_state.cellule_count):
        section = st.selectbox(
            f"Choisissez la cellule n°{i+1} :", 
            ('TH1', 'TH2', 'TH4', 'TH5', 'TH6', 'TH7'), 
            key=f"cellule_{i}"
        )
        cellules_selectionnees.append(section)
    if st.button("Ajouter une cellule"):
        st.session_state.cellule_count += 1

    

    if st.button("Valider"):

        section1 = str(section1)
    
        types = {'TH1': 'SM AirSeT 24kV - IM375 - IAC 12,5kA 1s AFL CD2 motorisée 48Vcc verrouillage P1', 'TH2': 'SM AirSeT 24kV - IM375 - IAC 12,5kA 1s AFL CD2 motorisée 48Vcc verrouillage P1', 'TH4': 'SM AirSeT - DMVLS - CDTS - MX220 - 20kV - IAC 12,5 kA 1s AFL - verr. C4 - VIP45', 'TH5': 'SM AirSeT 24kV - IM375 - IAC 12,5kA 1s AFL CD2 motorisée 48Vcc verrouillage P1', 'TH6': 'SM AirSeT 24kV - IM375 - IAC 12,5kA 1s AFL CD2 motorisée 48Vcc verrouillage P1', 'TH7': 'SM AirSeT 24kV - IM375 - IAC 12,5kA 1s AFL CD2 motorisée 48Vcc verrouillage P1' }.get(section1, 0)

        st.write("Vous avez sélectionné les cellules suivantes :")
        for x, y in enumerate(cellules_selectionnees, start=1):
            st.write(f"Cellule {x} : {y}")
            
        GWP1= 899

        st.metric(label="Total GWP du transformeur séléctionné", value=f"{GWP1} kg CO₂")
