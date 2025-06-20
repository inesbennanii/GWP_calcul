import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from PIL import Image
import base64
from streamlit_option_menu import option_menu

if 'total_liste' not in st.session_state:
    st.session_state.total_liste = []
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()
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

with st.sidebar:
    selected_menu = option_menu(
        menu_title='Menu',
        options=['Calcul GWP', 'Total GWP'],
        icons=['calculator', 'clipboard-data'],
        menu_icon='menu-app',
        default_index=0,
        styles={
            'container': {'padding': '5px', 'background-color': '#485744'},
            'nav-link': {'font-size': '16px', 'text-align': 'left'},
        }
)


if selected_menu=='Calcul GWP':
    selected = option_menu(
        menu_title=None,
        options=['Cables', 'Transformateurs', 'Cellules','Coffret'],
        icons=['lightning-charge', 'battery-full', 'battery-full','lightning-charge', 'lightning-charge', 'battery-full'],
        menu_icon='cast',
        default_index=0,
        orientation='horizontal',
        styles={
            'container': {
                'padding': '5px',
                'background-color': '#485744',
                'border-radius': '10px',
                'text-align': 'center',
                'box-shadow': '0 2px 5px rgba(0,0,0,0.1)',
            },
            'nav-link': {
                'font-size': '18px',
                'text-align': 'center',
                'margin': '0px 10px',
                '--hover-color': '#eee',
                'border-radius': '5px',
            },
            'nav-link-selected': {
                'background-color': '#BFC7CA',
                'border-radius': '5px',
            },
        },
    )

    if selected == 'Cables':

        st.markdown(
            "<h1 style='color: #4D5D48;'>Estimez le matériau le plus éco-responsable pour votre projet</h1>",
            unsafe_allow_html=True)


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
            use1=0
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
            use2=0
            fdv2 = H42 * masse_totale2 + I42

            if poids2==1786:
                fab2 = 3890
                distrib2 = 340
                installation2 = 189
                use2=1,98
                fdv2 = 131
                total2= distance2*4370
            else:
                total2 = fab2 + distrib2 + installation2 + fdv2
    
            if total1 > total2:
                materiau = 'le cuivre'
            else:
                materiau = "l'aluminium"

            GWP1 = round(abs(total1), 2)
            GWP2 = round(abs(total2), 2)
            st.session_state.GWP1 = GWP1
            st.session_state.GWP2 = GWP2
            st.session_state.fab1 = fab1
            st.session_state.distrib1 = distrib1
            st.session_state.installation1 = installation1
            st.session_state.use1 = use1
            st.session_state.fdv1 = fdv1
            
            st.session_state.fab2 = fab2
            st.session_state.distrib2 = distrib2
            st.session_state.installation2 = installation2
            st.session_state.use2 = use2
            st.session_state.fdv2 = fdv2

            st.success(f"Le matériau à utiliser est **{materiau}**")
            st.metric(label="Total GWP de l'aluminium", value=f"{GWP1} kg CO₂")
            st.metric(label="Total GWP du cuivre", value=f"{GWP2} kg CO₂")
        
        if "GWP1" in st.session_state and st.button("Choisir l'aluminium", key="alu"):
            st.session_state.total_liste.append({f'Aluminium {section1}': st.session_state.GWP1})
            d = {
                '': [f'Aluminium {section1}'],
                'Fabrication': [abs(st.session_state.fab1)],
                'Distribution': [st.session_state.distrib1],
                'Installation': [st.session_state.installation1],
                'Utilisation': [0],
                'Fin de vie': [st.session_state.fdv1],
                'Global warming': [st.session_state.GWP1]
            }
            df1 = pd.DataFrame(d)
            st.session_state.df = pd.concat([st.session_state.df, df1], ignore_index=True)
            st.success("Ajouté à la liste !")

        if "GWP2" in st.session_state and st.button("Choisir le cuivre",key="cuivre"):
            st.session_state.total_liste.append({f'Cuivre {section2}' : st.session_state.GWP2})
            d = {
                '': [f'Cuivre {section2}'],
                'Fabrication': [st.session_state.fab2],
                'Distribution': [st.session_state.distrib2],
                'Installation': [st.session_state.installation2],
                'Utilisation': [0],
                'Fin de vie': [st.session_state.fdv2],
                'Global warming': [st.session_state.GWP2]
            }
            df1 = pd.DataFrame(d)
            st.session_state.df = pd.concat([st.session_state.df, df1], ignore_index=True)
            st.success("Ajouté à la liste !")
        
        if not st.session_state.df.empty:
            st.dataframe(st.session_state.df)
        
    elif selected == 'Transformateurs':

        st.markdown(
            "<h1 style='color: #4D5D48;'>Estimez le bilan carbone de votre transformateur</h1>",
            unsafe_allow_html=True
            )


        st.markdown(
            "<span style='color: #4D5D48; font-size: 18px;'>Choisissez la section pour l'aluminium :</span>",
            unsafe_allow_html=True
            )  
        
        section1 = st.selectbox("", (100, 160, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150), key="section1")

        section1 = int(section1)
        Fabrication_coeff = {100: 0.30, 160: 0.32, 250: 0.42, 315: 0.48, 400: 0.52, 500: 0.57, 630: 0.65, 800: 0.79, 1000: 1, 1250: 1.14, 1600: 1.36, 2000: 1.67, 2500: 2.03, 3150: 2.5}.get(section1, 0)
        Distribution_coeff = Fabrication_coeff
        Installation_coeff = 1
        Utilisation_coeff = {100: 0.19, 160: 0.27, 250: 0.35, 315: 0.41, 400: 0.49, 500: 0.6, 630: 0.74, 800: 0.86, 1000: 1, 1250: 1.18, 1600: 1.43, 2000: 1.71, 2500: 2.04, 3150: 2.45}.get(section1, 0)
        fin_coeff = Fabrication_coeff

        Fabrication = 17300 * Fabrication_coeff
        Distribution = 482 * Distribution_coeff
        Installation = 0.282 * Installation_coeff
        Utilisation = 189000 * Utilisation_coeff
        Fin = 196 * fin_coeff

        total = Fabrication + Distribution + Installation + Utilisation + Fin
        GWP3 = round(abs(total), 2)
        st.session_state.GWP3 = GWP3


        if st.button("Valider"):
            st.metric(label="Total GWP du transformateur sélectionné", value=f"{GWP3} kg CO₂")

        if st.button("Ajouter à la liste"):
            st.session_state.total_liste.append({f'Transformateur {section1}' : GWP3})
            d = {
                '': [f'Transformateur {section1}'],
                'Fabrication': [Fabrication],
                'Distribution': [Distribution],
                'Installation': [Installation],
                'Utilisation': [Utilisation],
                'Fin de vie': [Fin],
                'Global warming': [GWP3]
            }
            df1 = pd.DataFrame(d)
            st.session_state.df = pd.concat([st.session_state.df, df1], ignore_index=True)
            st.success("Ajouté à la liste !")


        if not st.session_state.df.empty:
            st.dataframe(st.session_state.df)
        

    elif selected == 'Cellules':
        st.markdown(
            "<h1 style='color: #4D5D48;'>Estimez le bilan carbone de vos cellules</h1>",
            unsafe_allow_html=True
        )
        types1 = st.selectbox("", ('TH1', 'TH2', 'TH4', 'TH5', 'TH6', 'TH7'), key="section1")
        
        types1 = str(types1)
        types = {
            'TH1': 'SM AirSeT 24kV - IM375 - IAC 12,5kA 1s AFL CD2 motorisée 48Vcc verrouillage P1',
            'TH2': 'SM AirSeT 24kV - IM375 - IAC 12,5kA 1s AFL CD2 motorisée 48Vcc verrouillage P1',
            'TH4': 'SM6-24 DM1A - Air Insulated Switchgear with SF6 breaking technology',
            'TH5': 'SM AirSeT 24kV - IM375 - IAC 12,5kA 1s AFL CD2 motorisée 48Vcc verrouillage P1',
            'TH6': 'SM AirSeT 24kV - IM375 - IAC 12,5kA 1s AFL CD2 motorisée 48Vcc verrouillage P1',
            'TH7': 'SM AirSeT 24kV - IM375 - IAC 12,5kA 1s AFL CD2 motorisée 48Vcc verrouillage P1'
        }.get(types1, 1)

        if st.button("Valider"):
            if types1== 'TH4':
                GWP4=8460
            else:
                GWP4=899
            st.session_state.GWP4 = GWP4
            st.metric(
                label=f"Total GWP de la cellule {types1}: {types}",
                value=f"{GWP4} kg CO₂",
            )
        if st.button("Ajouter à la liste"):
            if types1== 'TH4':
                GWP4=8460
            else:
                GWP4=899
            st.session_state.GWP4 = GWP4
            st.session_state.total_liste.append({f'Cellule {types1}' : st.session_state.GWP4})
            if types1== 'TH4':
                d = {
                    '': [f'Cellule {types1}'],
                    'Fabrication': [6030],
                    'Distribution': [36.8],
                    'Installation': [18.1],
                    'Utilisation': [2310],
                    'Fin de vie': [64.9],
                    'Global warming': [8460]
                }
                df1 = pd.DataFrame(d)
                st.session_state.df = pd.concat([st.session_state.df, df1], ignore_index=True)
            else:
                d = {
                    '': [f'Cellule {types1}'],
                    'Fabrication': [385],
                    'Distribution': [11.6],
                    'Installation': [10.2],
                    'Utilisation': [472],
                    'Fin de vie': [20],
                    'Global warming': [899]
                }
                df1 = pd.DataFrame(d)
                st.session_state.df = pd.concat([st.session_state.df, df1], ignore_index=True)
            st.success("Ajouté à la liste !")
        if not st.session_state.df.empty:
            st.dataframe(st.session_state.df)

    elif selected == 'Coffret':
        st.markdown(
            "<h1 style='color: #4D5D48;'>Estimez le bilan carbone de votre coffret</h1>",
            unsafe_allow_html=True
            )
        st.markdown(
            "<span style='color: #4D5D48; font-size: 18px;'>Choisissez le coffret :</span>",
            unsafe_allow_html=True
            )  
        
        section1 = st.selectbox("", ('CSAP POSTE HT','CSAP POSTE TGBT',"COFFRET D'ISOLEMENT 125A", "COFFRET DE COMPTAGE", "COFFRET HQ"), key="section1")

        section1 = str(section1)
        Fabrication1 = [('COFFRET PRISMASet G IP30 H:1080 L:600 P:205', 255), ('PORTE PLEINE', 255), ('BLOC INSERT TYPE PAPILLON', 255), ('PATTES DE FIXATION', 255), ('PORTE SCHEMA A4', 471),  ('Répartiteur 1/2 rangée - 4P 160A - (Multiclip) - Courant CRETE 20kA ', 255), ( 'VOYANT TRICOLOR 400V', 0.261),  ('TELECOMMANDE BAES URA', 2.90), ('VIGI 30mA', 1.03),  ('DISJONCTEUR IC60N 3X2A COURBE C 50kA', 0.835),('DISJONCTEUR IC60N 3X2A COURBE C 50kA', 0.835),('DISJONCTEUR IC60N 2X2A COURBE C 20kA', 0.835),  ('DISJONCTEUR IC60N 3X2A COURBE C 20kA', 0.835), ('DISJONCTEUR IC60H 2X10A COURBE C 30kA', 0.835),  ('DISJONCTEUR IC60H 2X16A COURBE C 30kA', 0.835), ('DISJONCTEUR IC60L 3X16A COURBE C 25kA', 0.835), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.835),('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.835), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.835), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.835), ('DISJONCTEUR IC60H 2X10A COURBE C 30kA',0.835), ('VIGI 30mA', 1.03), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.835), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.835), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.835)]
        Distribution1 = [ ('COFFRET PRISMASet G IP30 H:1080 L:600 P:205', 9.4),  ('PORTE PLEINE', 9.47),  ('BLOC INSERT TYPE PAPILLON', 9.47),  ('PATTES DE FIXATION', 9.47),  ('PORTE SCHEMA A4', 215), ('Répartiteur 1/2 rangée - 4P 160A - (Multiclip) - Courant CRETE 20kA ', 9.47), ('VOYANT TRICOLOR 400V', 0.00471), ('TELECOMMANDE BAES URA', 0.0067), ('VIGI 30mA', 0.032),  ('DISJONCTEUR IC60N 3X2A COURBE C 50kA', 0.0156),('DISJONCTEUR IC60N 3X2A COURBE C 50kA', 0.0156),('DISJONCTEUR IC60N 2X2A COURBE C 20kA', 0.0156),  ('DISJONCTEUR IC60N 3X2A COURBE C 20kA', 0.0156),  ('DISJONCTEUR IC60H 2X10A COURBE C 30kA', 0.0156),  ('DISJONCTEUR IC60H 2X16A COURBE C 30kA', 0.0156), ('DISJONCTEUR IC60L 3X16A COURBE C 25kA', 0.0156), ( 'DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.0156), ( 'DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.0156), ( 'DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.0156), ( 'DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.0156), ( 'DISJONCTEUR IC60H 2X10A COURBE C 30kA',0.0156), ('VIGI 30mA', 0.032), ( 'DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.0156), ( 'DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.0156), ( 'DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.0156)]
        Installation1 = [ ('COFFRET PRISMASet G IP30 H:1080 L:600 P:205', 9.11), ('PORTE PLEINE', 9.11), ('BLOC INSERT TYPE PAPILLON', 9.11), ('PATTES DE FIXATION', 9.11),  ('PORTE SCHEMA A4', 15.4),  ('Répartiteur 1/2 rangée - 4P 160A - (Multiclip) - Courant CRETE 20kA ', 9.11), ( 'VOYANT TRICOLOR 400V', 0.014),  ('TELECOMMANDE BAES URA', 0.0172),  ('VIGI 30mA', 0.0327),  ('DISJONCTEUR IC60N 3X2A COURBE C 50kA', 0.0104), ('DISJONCTEUR IC60N 3X2A COURBE C 50kA', 0.0104),('DISJONCTEUR IC60N 2X2A COURBE C 20kA', 0.0104),  ('DISJONCTEUR IC60N 3X2A COURBE C 20kA', 0.0104),  ('DISJONCTEUR IC60H 2X10A COURBE C 30kA', 0.0104),  ('DISJONCTEUR IC60H 2X16A COURBE C 30kA', 0.0104),  ('DISJONCTEUR IC60L 3X16A COURBE C 25kA', 0.0104), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.0104),  ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.0104), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.0104), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.0104), ('DISJONCTEUR IC60H 2X10A COURBE C 30kA',0.0104), ('VIGI 30mA', 0.0327), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.0104),  ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.0104), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.0104)]
        Utilisation1 = [ ('COFFRET PRISMASet G IP30 H:1080 L:600 P:205', 253),  ('PORTE PLEINE', 253),  ('BLOC INSERT TYPE PAPILLON', 253),  ('PATTES DE FIXATION', 253),  ('PORTE SCHEMA A4', 0),  ('Répartiteur 1/2 rangée - 4P 160A - (Multiclip) - Courant CRETE 20kA ', 253),  ('VOYANT TRICOLOR 400V', 13.7),  ('TELECOMMANDE BAES URA', 61.5),  ('VIGI 30mA', 2.41),  ('DISJONCTEUR IC60N 3X2A COURBE C 50kA', 12.9),('DISJONCTEUR IC60N 3X2A COURBE C 50kA', 12.9),('DISJONCTEUR IC60N 2X2A COURBE C 20kA', 12.9),  ('DISJONCTEUR IC60N 3X2A COURBE C 20kA', 12.9),  ('DISJONCTEUR IC60H 2X10A COURBE C 30kA', 12.9),  ('DISJONCTEUR IC60H 2X16A COURBE C 30kA', 12.9),  ('DISJONCTEUR IC60L 3X16A COURBE C 25kA', 12.9), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',12.9), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',12.9), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',12.9), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',12.9), ('DISJONCTEUR IC60H 2X10A COURBE C 30kA',12.9), ('VIGI 30mA', 2.41), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',12.9), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.0104), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.0104)]
        Fin1 = [ ('COFFRET PRISMASet G IP30 H:1080 L:600 P:205', 107),  ('PORTE PLEINE', 107),  ('BLOC INSERT TYPE PAPILLON', 107),  ('PATTES DE FIXATION', 107),  ('PORTE SCHEMA A4', 267),  ('Répartiteur 1/2 rangée - 4P 160A - (Multiclip) - Courant CRETE 20kA ', 107),  ('VOYANT TRICOLOR 400V', 0.0625),  ('TELECOMMANDE BAES URA', 0.248),  ('VIGI 30mA', 0.3),  ('DISJONCTEUR IC60N 3X2A COURBE C 50kA', 0.328),('DISJONCTEUR IC60N 3X2A COURBE C 50kA', 0.328),('DISJONCTEUR IC60N 2X2A COURBE C 20kA', 0.328),  ('DISJONCTEUR IC60N 3X2A COURBE C 20kA', 0.328),  ('DISJONCTEUR IC60H 2X10A COURBE C 30kA', 0.328),  ('DISJONCTEUR IC60H 2X16A COURBE C 30kA', 0.328),  ('DISJONCTEUR IC60L 3X16A COURBE C 25kA', 0.328), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.328), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.328), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.328), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.328), ('DISJONCTEUR IC60H 2X10A COURBE C 30kA',0.328), ('VIGI 30mA', 0.3), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.328), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.328), ('DISJONCTEUR IC60H 2X16A COURBE C 30kA',0.328)]
        fab=0
        dis=0
        ins=0
        use=0
        fin=0
        for (nom,valeur) in Fabrication1:
            fab += float(valeur)
        for (nom,valeur) in Distribution1:
            dis+=float(valeur)
        for (nom,valeur) in Installation1:
            ins+=float(valeur)
        for (nom,valeur) in Utilisation1:
            use+=float(valeur)
        for (nom,valeur) in Fin1:
            fin+=float(valeur)  
        total1 = fab + dis + ins + use + fin
        
        Fabrication2 = [('COFFRET PRISMASet G IP30 H:1080 L:600 P:205', 255), ('PORTE PLEINE', 255), ('BLOC INSERT TYPE PAPILLON', 255), ('PATTES DE FIXATION', 255), ('PORTE SCHEMA A4', 471),('PrimaSet G - Auvent coffret ou armoire - IP41 - L600', 255),('INTERRUPTEUR SECTIONNEUR INS63 4P 63A', 16.6), ('Répartiteur 1/2 rangée - 4P 160A - (Multiclip) - Courant CRETE 20kA ', 255),('DISJONCTEUR IC60N 4X2A COURBE C PDC 50kA', 0.835), ('VOYANT TRICOLOR 400V', 0.261), ('DISJONCTEUR IC60N 2X2A COURBE C PDC 50kA', 0.835),('CONTACT DE PORTE', 0.0000511),('ECLAIRAGE LED 230V 5W', 0.000491) ,('DISJONCTEUR IC60N 2X2A COURBE C  PDC 50kA', 0.835), ('TELECOMMANDE BAES URA', 2.90),('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 0.835), ('DISJONCTEUR IC60N 2X16A COURBE C PDC 20kA', 0.835), ('VIGI 30mA', 1.03), ('DISJONCTEUR IC60H 3X25A COURBE C PDC 15kA', 0.835), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 0.835), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 0.835), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 0.835),  ('DISJONCTEUR IC60N 2X6A COURBE C PDC 20kA', 0.835), ('VIGI 30mA', 1.03), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 0.835),  ('DISJONCTEUR IC60N 2X16A COURBE C PDC 20kA', 0.835),('DISJONCTEUR IC60N 2X16A COURBE C PDC 20kA', 0.835)]
        Distribution2 = [('COFFRET PRISMASet G IP30 H:1080 L:600 P:205', 9.47), ('PORTE PLEINE', 9.47), ('BLOC INSERT TYPE PAPILLON', 9.47), ('PATTES DE FIXATION', 9.47), ('PORTE SCHEMA A4', 215),('PrimaSet G - Auvent coffret ou armoire - IP41 - L600', 9.47),('INTERRUPTEUR SECTIONNEUR INS63 4P 63A', 0.369), ('Répartiteur 1/2 rangée - 4P 160A - (Multiclip) - Courant CRETE 20kA ', 9.47),('DISJONCTEUR IC60N 4X2A COURBE C PDC 50kA', 0.0156), ('VOYANT TRICOLOR 400V', 0.00471),('DISJONCTEUR IC60N 2X2A COURBE C PDC 50kA', 0.0156),('CONTACT DE PORTE', 0.00000000661),('ECLAIRAGE LED 230V 5W', 0),('DISJONCTEUR IC60N 2X2A COURBE C  PDC 50kA', 0.0156), ('TELECOMMANDE BAES URA', 0.0067),('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 0.0156), ('DISJONCTEUR IC60N 2X16A COURBE C PDC 20kA', 0.0156), ('VIGI 30mA', 0.032), ('DISJONCTEUR IC60H 3X25A COURBE C PDC 15kA', 0.0156), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 0.0156), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 0.0156), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 0.0156),  ('DISJONCTEUR IC60N 2X6A COURBE C PDC 20kA', 0.0156), ('VIGI 30mA', 0.032), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 0.0156), ('DISJONCTEUR IC60N 2X16A COURBE C PDC 20kA', 0.0156), ('DISJONCTEUR IC60N 2X16A COURBE C PDC 20kA', 0.0156)]
        Installation2 = [('COFFRET PRISMASet G IP30 H:1080 L:600 P:205', 9.11), ('PORTE PLEINE', 9.11), ('BLOC INSERT TYPE PAPILLON', 9.11), ('PATTES DE FIXATION', 9.11), ('PORTE SCHEMA A4', 15.4),('PrimaSet G - Auvent coffret ou armoire - IP41 - L600', 9.11),('INTERRUPTEUR SECTIONNEUR INS63 4P 63A', 0.129), ('Répartiteur 1/2 rangée - 4P 160A - (Multiclip) - Courant CRETE 20kA ', 9.11),('DISJONCTEUR IC60N 4X2A COURBE C PDC 50kA', 0.0104), ('VOYANT TRICOLOR 400V', 0.014),('DISJONCTEUR IC60N 2X2A COURBE C PDC 50kA', 0.0104),('CONTACT DE PORTE', 0), ('ECLAIRAGE LED 230V 5W', 0),('DISJONCTEUR IC60N 2X2A COURBE C  PDC 50kA', 0.0104),('TELECOMMANDE BAES URA', 0.0172),('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 0.0104), ('DISJONCTEUR IC60N 2X16A COURBE C PDC 20kA', 0.0104), ('VIGI 30mA', 0.0327), ('DISJONCTEUR IC60H 3X25A COURBE C PDC 15kA', 0.0104), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 0.0104), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 0.0104), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 0.0104),  ('DISJONCTEUR IC60N 2X6A COURBE C PDC 20kA', 0.0104), ('VIGI 30mA', 0.0327), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 0.0104), ('DISJONCTEUR IC60N 2X16A COURBE C PDC 20kA', 0.0104), ('DISJONCTEUR IC60N 2X16A COURBE C PDC 20kA', 0.0104)]
        Utilisation2 = [('COFFRET PRISMASet G IP30 H:1080 L:600 P:205', 253), ('PORTE PLEINE', 253), ('BLOC INSERT TYPE PAPILLON', 253), ('PATTES DE FIXATION', 253), ('PORTE SCHEMA A4', 0), ('PrimaSet G - Auvent coffret ou armoire - IP41 - L600', 253),('INTERRUPTEUR SECTIONNEUR INS63 4P 63A', 436),('Répartiteur 1/2 rangée - 4P 160A - (Multiclip) - Courant CRETE 20kA ', 253),('DISJONCTEUR IC60N 4X2A COURBE C PDC 50kA', 12.9), ('VOYANT TRICOLOR 400V', 13.7),('DISJONCTEUR IC60N 2X2A COURBE C PDC 50kA', 12.9),('CONTACT DE PORTE', 0),('ECLAIRAGE LED 230V 5W', 0.00000941),('DISJONCTEUR IC60N 2X2A COURBE C  PDC 50kA', 12.9),('TELECOMMANDE BAES URA', 61.5),('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 12.9), ('DISJONCTEUR IC60N 2X16A COURBE C PDC 20kA', 12.9), ('VIGI 30mA', 2.41), ('DISJONCTEUR IC60H 3X25A COURBE C PDC 15kA', 12.9), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 12.9), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 12.9), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 12.9),  ('DISJONCTEUR IC60N 2X6A COURBE C PDC 20kA', 12.9), ('VIGI 30mA', 2.41), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 12.9),('DISJONCTEUR IC60N 2X16A COURBE C PDC 20kA', 12.9), ('DISJONCTEUR IC60N 2X16A COURBE C PDC 20kA', 12.9)]
        Fin2 = [('COFFRET PRISMASet G IP30 H:1080 L:600 P:205', 107), ('PORTE PLEINE', 107), ('BLOC INSERT TYPE PAPILLON', 107), ('PATTES DE FIXATION', 107), ('PORTE SCHEMA A4', 267),('PrimaSet G - Auvent coffret ou armoire - IP41 - L600', 107),('INTERRUPTEUR SECTIONNEUR INS63 4P 63A', 4.33), ('Répartiteur 1/2 rangée - 4P 160A - (Multiclip) - Courant CRETE 20kA ', 107),('DISJONCTEUR IC60N 4X2A COURBE C PDC 50kA', 0.328), ('VOYANT TRICOLOR 400V', 0.0625),('DISJONCTEUR IC60N 2X2A COURBE C PDC 50kA', 0.328), ('CONTACT DE PORTE', 0), ('ECLAIRAGE LED 230V 5W', 0),('DISJONCTEUR IC60N 2X2A COURBE C  PDC 50kA', 0.328), ('TELECOMMANDE BAES URA', 0.248), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 0.328), ('DISJONCTEUR IC60N 2X16A COURBE C PDC 20kA', 0.328), ('VIGI 30mA', 0.3), ('DISJONCTEUR IC60H 3X25A COURBE C PDC 15kA', 0.328), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 0.328), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 0.328), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 0.328),  ('DISJONCTEUR IC60N 2X6A COURBE C PDC 20kA', 0.328), ('VIGI 30mA', 0.3), ('DISJONCTEUR IC60N 2X10A COURBE C PDC 20kA', 0.328),('DISJONCTEUR IC60N 2X16A COURBE C PDC 20kA', 0.328),('DISJONCTEUR IC60N 2X16A COURBE C PDC 20kA', 0.328)]
        fab2=0
        dis2=0
        ins2=0
        use2=0
        fin2=0
        for (nom1,valeur1) in Fabrication2:
            fab2 += float(valeur1)
        for (nom1,valeur1) in Distribution2:
            dis2+=float(valeur1)
        for (nom1,valeur1) in Installation2:
            ins2+=float(valeur1)
        for (nom1,valeur1) in Utilisation2:
            use2+=float(valeur1)
        for (nom1,valeur1) in Fin2:
            fin2+=float(valeur1)
        total2 = fab2 + dis2 + ins2 + use2 + fin2
        
        Fabrication3= [('PanelSeT S3D - Enveloppe acier - H1200xL1200xP400 - 2 portes pleines IP 55',47.8 ), ('Rail de fixation',47.8 ), ('PORTE SCHEMA A4', 471 ), ('Auvent pour coffret L1200XP400mm', 47.8), ('PanelSeT - Thalassa - insert triangle - 8mm - coffret mural', 471), ('Interrupteur sectionneur 3P 400A commande extérieure latérale + poignée IP 55 Noire', 37.6), ('Axe pour poignée extérieure', 0.91 ),('VOYANT TRICOLOR 400V', 0.261), ('Linergy BS - JdB de fond 400A - barres taraudées 20x5 - L=1000 mm', 224), ('DISJONCTEUR IC60N 3x2A Courbe C PDC 50 KA', 0.835),('Contact Auxiliaire 1 OF/SD', 0.289),  ('DISJONCTEUR IC60N 3x2A Courbe C PDC 50 KA', 0.835),('Contact Auxiliaire 1 OF/SD', 0.289),  ('DISJONCTEUR IC60N 3x4A Courbe C PDC 50 KA', 0.835),('Contact Auxiliaire 1 OF/SD', 0.289),  ('DISJONCTEUR IC60N 3x2A Courbe C PDC 50 KA', 0.835),('Contact Auxiliaire 1 OF/SD', 0.289),('TRANSFORMATEUR 400V/230V - 630VA', 49), ('ClimaSys - thermostat - à fermeture - bleu - °F', 101), ('ClimaSys - thermostat - à ouverture - rouge - °F',101),('ClimaSys - ventilateur 85m3/h - 230V - IP54 - avec grille et filtre G2',6.05 ), ('ClimaSys - résistance chauffante - 55W - 110..250V', 105), ('ComPacT NSX160F - Disjoncteur - MicroLogic 2.2 160A - 3P3D - 36kA - montage fixe', 16), ('Contact Auxiliaire 1 OF', 0.124), ('Contact Auxiliaire 1 SD', 0.124), ('Epanouisseur - séparateur de phase - 3P', 2.03)]
        Distribution3=[('PanelSeT S3D - Enveloppe acier - H1200xL1200xP400 - 2 portes pleines IP 55', 19.5), ('Rail de fixation', 19.5 ), ('PORTE SCHEMA A4', 215), ('Auvent pour coffret L1200XP400mm', 19.5), ('PanelSeT - Thalassa - insert triangle - 8mm - coffret mural',215 ), ('Interrupteur sectionneur 3P 400A commande extérieure latérale + poignée IP 55 Noire',1.11 ), ('Axe pour poignée extérieure', 0.0294), ('VOYANT TRICOLOR 400V', 0.00471), ('Linergy BS - JdB de fond 400A - barres taraudées 20x5 - L=1000 mm', 2.16), ('DISJONCTEUR IC60N 3x2A Courbe C PDC 50 KA',0.0156 ), ('Contact Auxiliaire 1 OF/SD', 0.00577), ('DISJONCTEUR IC60N 3x2A Courbe C PDC 50 KA',0.0156 ), ('Contact Auxiliaire 1 OF/SD', 0.00577), ('DISJONCTEUR IC60N 3x4A Courbe C PDC 50 KA',0.0156 ), ('Contact Auxiliaire 1 OF/SD', 0.00577), ('DISJONCTEUR IC60N 3x4A Courbe C PDC 50 KA',0.0156 ), ('Contact Auxiliaire 1 OF/SD', 0.00577),('TRANSFORMATEUR 400V/230V - 630VA', 1.38),('ClimaSys - thermostat - à fermeture - bleu - °F', 0.143), ('ClimaSys - thermostat - à ouverture - rouge - °F',0.143), ('ClimaSys - ventilateur 85m3/h - 230V - IP54 - avec grille et filtre G2',0 ), ('ClimaSys - résistance chauffante - 55W - 110..250V', 1.19), ('ComPacT NSX160F - Disjoncteur - MicroLogic 2.2 160A - 3P3D - 36kA - montage fixe', 0.602), ('Contact Auxiliaire 1 OF',0.00408 ), ('Contact Auxiliaire 1 SD',0.00408 ), ('Epanouisseur - séparateur de phase - 3P', 0.106)]
        Installation3=[('PanelSeT S3D - Enveloppe acier - H1200xL1200xP400 - 2 portes pleines IP 55', 1.93), ('Rail de fixation',  1.93), ('PORTE SCHEMA A4', 15.4), ('Auvent pour coffret L1200XP400mm',1.93 ), ('PanelSeT - Thalassa - insert triangle - 8mm - coffret mural', 15.4), ('Interrupteur sectionneur 3P 400A commande extérieure latérale + poignée IP 55 Noire', 0.481 ), ('Axe pour poignée extérieure',0.0380), ('VOYANT TRICOLOR 400V', 0.0140), ('Linergy BS - JdB de fond 400A - barres taraudées 20x5 - L=1000 mm', 1.58), ('DISJONCTEUR IC60N 3x2A Courbe C PDC 50 KA', 0.0104), ('Contact Auxiliaire 1 OF/SD', 0.000688),  ('DISJONCTEUR IC60N 3x2A Courbe C PDC 50 KA', 0.0104), ('Contact Auxiliaire 1 OF/SD', 0.000688),  ('DISJONCTEUR IC60N 3x4A Courbe C PDC 50 KA', 0.0104), ('Contact Auxiliaire 1 OF/SD', 0.000688), ('DISJONCTEUR IC60N 3x4A Courbe C PDC 50 KA', 0.0104), ('Contact Auxiliaire 1 OF/SD', 0.000688),('TRANSFORMATEUR 400V/230V - 630VA ', 0), ('ClimaSys - thermostat - à fermeture - bleu - °F', 0), ('ClimaSys - thermostat - à ouverture - rouge - °F',0), ('ClimaSys - ventilateur 85m3/h - 230V - IP54 - avec grille et filtre G2',0 ), ('ClimaSys - résistance chauffante - 55W - 110..250V', 0), ('ComPacT NSX160F - Disjoncteur - MicroLogic 2.2 160A - 3P3D - 36kA - montage fixe', 0.174), ('Contact Auxiliaire 1 OF', 0.0197),  ('Contact Auxiliaire 1 SD', 0.0197), ('Epanouisseur - séparateur de phase - 3P', 0.0196)]
        Utilisation3=[('PanelSeT S3D - Enveloppe acier - H1200xL1200xP400 - 2 portes pleines IP 55', 0), ('Rail de fixation',0 ), ('PORTE SCHEMA A4', 0), ('Auvent pour coffret L1200XP400mm', 0), ('PanelSeT - Thalassa - insert triangle - 8mm - coffret mural',0 ), ('Interrupteur sectionneur 3P 400A commande extérieure latérale + poignée IP 55 Noire', 666), ('Axe pour poignée extérieure', 0), ('VOYANT TRICOLOR 400V', 13.7), ('Linergy BS - JdB de fond 400A - barres taraudées 20x5 - L=1000 mm', 1100), ('DISJONCTEUR IC60N 3x2A Courbe C PDC 50 KA', 12.9), ('Contact Auxiliaire 1 OF/SD', 0.644), ('DISJONCTEUR IC60N 3x2A Courbe C PDC 50 KA', 12.9), ('Contact Auxiliaire 1 OF/SD', 0.644), ('DISJONCTEUR IC60N 3x4A Courbe C PDC 50 KA', 12.9), ('Contact Auxiliaire 1 OF/SD', 0.644), ('DISJONCTEUR IC60N 3x4A Courbe C PDC 50 KA', 12.9), ('Contact Auxiliaire 1 OF/SD', 0.644),('TRANSFORMATEUR 400V/230V - 630VA ', 5470), ('ClimaSys - thermostat - à fermeture - bleu - °F', 259), ('ClimaSys - thermostat - à ouverture - rouge - °F',259), ('ClimaSys - ventilateur 85m3/h - 230V - IP54 - avec grille et filtre G2', 1480), ('ClimaSys - résistance chauffante - 55W - 110..250V', 262), ('ComPacT NSX160F - Disjoncteur - MicroLogic 2.2 160A - 3P3D - 36kA - montage fixe', 284), ('Contact Auxiliaire 1 OF', 16.2), ('Contact Auxiliaire 1 SD', 16.2), ('Epanouisseur - séparateur de phase - 3P', 16)]
        Fin3=[('PanelSeT S3D - Enveloppe acier - H1200xL1200xP400 - 2 portes pleines IP 55', 23.1), ('Rail de fixation',23.1 ), ('PORTE SCHEMA A4', 267), ('Auvent pour coffret L1200XP400mm',23.1 ), ('PanelSeT - Thalassa - insert triangle - 8mm - coffret mural', 267), ('Interrupteur sectionneur 3P 400A commande extérieure latérale + poignée IP 55 Noire', 2.39), ('Axe pour poignée extérieure', 0.0103), ('VOYANT TRICOLOR 400V', 0.0625), ('Linergy BS - JdB de fond 400A - barres taraudées 20x5 - L=1000 mm', 7.53), ('DISJONCTEUR IC60N 3x2A Courbe C PDC 50 KA', 0.328), ('Contact Auxiliaire 1 OF/SD', 0.0066), ('DISJONCTEUR IC60N 3x2A Courbe C PDC 50 KA', 0.328), ('Contact Auxiliaire 1 OF/SD', 0.0066), ('DISJONCTEUR IC60N 3x4A Courbe C PDC 50 KA', 0.328), ('Contact Auxiliaire 1 OF/SD', 0.0066), ('DISJONCTEUR IC60N 3x4A Courbe C PDC 50 KA', 0.328), ('Contact Auxiliaire 1 OF/SD', 0.0066),('TRANSFORMATEUR 400V/230V - 630VA', 0.748), ('ClimaSys - thermostat - à fermeture - bleu - °F',0), ('ClimaSys - thermostat - à ouverture - rouge - °F',0), ('ClimaSys - ventilateur 85m3/h - 230V - IP54 - avec grille et filtre G2', 0.193), ('ClimaSys - résistance chauffante - 55W - 110..250V', 0.0501), ('ComPacT NSX160F - Disjoncteur - MicroLogic 2.2 160A - 3P3D - 36kA - montage fixe', 3.52), ('Contact Auxiliaire 1 OF', 0.0387), ('Contact Auxiliaire 1 SD', 0.0387), ('Epanouisseur - séparateur de phase - 3P', 1.02)]
        fab3=0
        dis3=0
        ins3=0
        use3=0
        fin3=0
        for (nom2,valeur2) in Fabrication3:
            fab3 += float(valeur2)
        for (nom2,valeur2) in Distribution3:
            dis3+=float(valeur2)
        for (nom2,valeur2) in Installation3:
            ins3+=float(valeur2)
        for (nom2,valeur2) in Utilisation3:
            use3+=float(valeur2)
        for (nom2,valeur2) in Fin3:
            fin3+=float(valeur2)
        total3 = fab3 + dis3 + ins3 + use3 + fin3
        
        Fabrication4 = [('Interrupteur-Sectionneur SIRCO M - Comande Extérieure (3x20A)', 1.96), ('Répartiteur Bipolaire (100A)',1.46 ),('Acti9 iC60N - Disjoncteur Courbe C 2x2A', 0.835), ('Voyant led Banc 230v + support rail DIN', 0.261),('Acti9 iC60N - Disjoncteur Courbe C 2x10A + Vigi 30mA', 1.87), ('Acti9 iC60N - Disjoncteur Courbe C 2x10A', 0.835),('Alimentation 230VAC/24VDC-72W-3A',32.7), ('Interrupteur iSW 2x40A', 2.29), ('Acti9 iC60N - Disjoncteur Courbe C 2x10A', 0.835), ('Acti9 iC60H-DC - Disjoncteur Courbe C 2x2A', 0.85)]
        Distribution4= [('Interrupteur-Sectionneur SIRCO M - Comande Extérieure (3x20A)', 0.0968), ('Répartiteur Bipolaire (100A)', 0.0256), ('Acti9 iC60N - Disjoncteur Courbe C 2x2A', 0.0156), ('Voyant led Banc 230v + support rail DIN', 0.00471), ('Acti9 iC60N - Disjoncteur Courbe C 2x10A + Vigi 30mA', 0.0476), ('Acti9 iC60N - Disjoncteur Courbe C 2x10A', 0.0156), ('Alimentation 230VAC/24VDC-72W-3A',0.195), ('Interrupteur iSW 2x40A', 0.0321), ('Acti9 iC60N - Disjoncteur Courbe C 2x10A', 0.0156), ('Acti9 iC60H-DC - Disjoncteur Courbe C 2x2A', 0.0152)]
        Installation4= [('Interrupteur-Sectionneur SIRCO M - Comande Extérieure (3x20A)', 0.0757), ('Répartiteur Bipolaire (100A)', 0.0549), ('Acti9 iC60N - Disjoncteur Courbe C 2x2A', 0.0104), ('Voyant led Banc 230v + support rail DIN', 0.0140), ('Acti9 iC60N - Disjoncteur Courbe C 2x10A + Vigi 30mA', 0.0431), ('Acti9 iC60N - Disjoncteur Courbe C 2x10A', 0.0104), ('Alimentation 230VAC/24VDC-72W-3A',0), ('Interrupteur iSW 2x40A', 0.0226), ('Acti9 iC60N - Disjoncteur Courbe C 2x10A', 0.0104), ('Acti9 iC60H-DC - Disjoncteur Courbe C 2x2A', 0.00837)]
        Utilisation4= [('Interrupteur-Sectionneur SIRCO M - Comande Extérieure (3x20A)', 24.2), ('Répartiteur Bipolaire (100A)', 17.5), ('Acti9 iC60N - Disjoncteur Courbe C 2x2A', 12.9), ('Voyant led Banc 230v + support rail DIN', 13.7), ('Acti9 iC60N - Disjoncteur Courbe C 2x10A + Vigi 30mA', 15.3), ('Acti9 iC60N - Disjoncteur Courbe C 2x10A', 12.9), ('Alimentation 230VAC/24VDC-72W-3A',991), ('Interrupteur iSW 2x40A', 4.33), ('Acti9 iC60N - Disjoncteur Courbe C 2x10A', 12.9), ('Acti9 iC60H-DC - Disjoncteur Courbe C 2x2A', 9.69)]
        Fin4= [('Interrupteur-Sectionneur SIRCO M - Comande Extérieure (3x20A)', 0.131), ('Répartiteur Bipolaire (100A)', 0.454), ('Acti9 iC60N - Disjoncteur Courbe C 2x2A', 0.328), ('Voyant led Banc 230v + support rail DIN', 0.0625), ('Acti9 iC60N - Disjoncteur Courbe C 2x10A + Vigi 30mA', 0.628), ('Acti9 iC60N - Disjoncteur Courbe C 2x10A', 0.328), ('Alimentation 230VAC/24VDC-72W-3A',1.11), ('Interrupteur iSW 2x40A', 0.912), ('Acti9 iC60N - Disjoncteur Courbe C 2x10A', 0.328), ('Acti9 iC60H-DC - Disjoncteur Courbe C 2x2A', 0.302)]
        fab4=0
        dis4=0
        ins4=0
        use4=0
        fin4=0
        for (nom1,valeur1) in Fabrication4:
            fab4 += float(valeur1)
        for (nom1,valeur1) in Distribution4:
            dis4+=float(valeur1)
        for (nom1,valeur1) in Installation4:
            ins4+=float(valeur1)
        for (nom1,valeur1) in Utilisation4:
            use4+=float(valeur1)
        for (nom1,valeur1) in Fin4:
            fin4+=float(valeur1)
        total4 = fab4 + dis4 + ins4 + use4 + fin4
        
        
        Fabrication5=[('DISJONCTEUR IC60N 2x3A Courbe C', 0.835), ('Contact Auxiliaire OF/SD', 0.289), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.835), ('Contact Auxiliaire OF/SD', 0.289), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.835), ('Contact Auxiliaire OF/SD', 0.289), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.835), ('Contact Auxiliaire OF/SD', 0.289), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.835), ('Contact Auxiliaire OF/SD', 0.289), ('ALIMENTATION REGULEE à DECOUPAGE TRI 480W/20A', 23.1), ('Disjoncteur  C60HDC 2x2A Courbe C', 0.85), ('REPARTITEUR BIPOLAIRES A BORNES EQUIPES DE 2 BARREAUX - 2x40A', 1.08), ('Disjoncteur  C60HDC 2x2A Courbe C', 0.85), ('VOYANT BLANC A COLLERETTE 22mm 24VDC', 0.261), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.85), ('Contact Auxiliaire OF', 0.289), ('Disjoncteur  C60HDC 2x16A Courbe C', 0.85), ('Contact Auxiliaire OF/SD', 0.289), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.85), ('Contact Auxiliaire OF/SD', 0.289), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.85), ('Contact Auxiliaire OF/SD', 0.289)]
        Distribution5=[('DISJONCTEUR IC60N 2x3A Courbe C', 0.0156), ('Contact Auxiliaire OF/SD', 0.00577), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.0156), ('Contact Auxiliaire OF/SD', 0.00577), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.0156), ('Contact Auxiliaire OF/SD', 0.00577), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.0156), ('Contact Auxiliaire OF/SD', 0.00577), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.0156), ('Contact Auxiliaire OF/SD', 0.00577), ('ALIMENTATION REGULEE à DECOUPAGE TRI 480W/20A', 0.363), ('Disjoncteur  C60HDC 2x2A Courbe C', 0.0152), ('REPARTITEUR BIPOLAIRES A BORNES EQUIPES DE 2 BARREAUX - 2x40A', 0.0204), ('Disjoncteur  C60HDC 2x2A Courbe C', 0.0152), ('VOYANT BLANC A COLLERETTE 22mm 24VDC', 0.00471), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.0152), ('Contact Auxiliaire OF', 0.00577), ('Disjoncteur  C60HDC 2x16A Courbe C', 0.0152), ('Contact Auxiliaire OF/SD', 0.00577), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.0152), ('Contact Auxiliaire OF/SD', 0.00577), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.0152), ('Contact Auxiliaire OF/SD', 0.00577)]
        Installation5=[('DISJONCTEUR IC60N 2x3A Courbe C', 0.0104), ('Contact Auxiliaire OF/SD', 0.000688), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.0104), ('Contact Auxiliaire OF/SD', 0.000688), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.0104), ('Contact Auxiliaire OF/SD', 0.000688), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.0104), ('Contact Auxiliaire OF/SD', 0.000688), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.0104), ('Contact Auxiliaire OF/SD', 0.000688), ('ALIMENTATION REGULEE à DECOUPAGE TRI 480W/20A', 0), ('Disjoncteur  C60HDC 2x2A Courbe C', 0.00837), ('REPARTITEUR BIPOLAIRES A BORNES EQUIPES DE 2 BARREAUX - 2x40A', 0), ('Disjoncteur  C60HDC 2x2A Courbe C', 0.00837), ('VOYANT BLANC A COLLERETTE 22mm 24VDC', 0.014), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.00837), ('Contact Auxiliaire OF', 0.000688), ('Disjoncteur  C60HDC 2x16A Courbe C', 0.00837), ('Contact Auxiliaire OF/SD', 0.000688), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.00837), ('Contact Auxiliaire OF/SD', 0.000688), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.00837), ('Contact Auxiliaire OF/SD', 0.000688)]
        Utilisation5=[('DISJONCTEUR IC60N 2x3A Courbe C', 12.9), ('Contact Auxiliaire OF/SD', 0.644), ('DISJONCTEUR IC60N 2x10A Courbe C', 12.9), ('Contact Auxiliaire OF/SD', 0.644), ('DISJONCTEUR IC60N 2x10A Courbe C', 12.9), ('Contact Auxiliaire OF/SD', 0.644), ('DISJONCTEUR IC60N 2x10A Courbe C', 12.9), ('Contact Auxiliaire OF/SD', 0.644), ('DISJONCTEUR IC60N 2x10A Courbe C', 12.9), ('Contact Auxiliaire OF/SD', 0.644), ('ALIMENTATION REGULEE à DECOUPAGE TRI 480W/20A', 1350), ('Disjoncteur  C60HDC 2x2A Courbe C', 9.69), ('REPARTITEUR BIPOLAIRES A BORNES EQUIPES DE 2 BARREAUX - 2x40A', 33.5), ('Disjoncteur  C60HDC 2x2A Courbe C', 9.69), ('VOYANT BLANC A COLLERETTE 22mm 24VDC', 13.7), ('Disjoncteur  C60HDC 2x10A Courbe C', 9.69), ('Contact Auxiliaire OF', 0.644), ('Disjoncteur  C60HDC 2x16A Courbe C', 9.69), ('Contact Auxiliaire OF/SD', 0.644), ('Disjoncteur  C60HDC 2x10A Courbe C', 9.69), ('Contact Auxiliaire OF/SD', 0.644), ('Disjoncteur  C60HDC 2x10A Courbe C', 9.69), ('Contact Auxiliaire OF/SD', 0.644)]
        Fin5=[('DISJONCTEUR IC60N 2x3A Courbe C', 0.328), ('Contact Auxiliaire OF/SD', 0.0066), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.328), ('Contact Auxiliaire OF/SD', 0.0066), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.328), ('Contact Auxiliaire OF/SD', 0.0066), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.328), ('Contact Auxiliaire OF/SD', 0.0066), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.328), ('Contact Auxiliaire OF/SD', 0.0066), ('ALIMENTATION REGULEE à DECOUPAGE TRI 480W/20A', 0.14), ('Disjoncteur  C60HDC 2x2A Courbe C', 0.302), ('REPARTITEUR BIPOLAIRES A BORNES EQUIPES DE 2 BARREAUX - 2x40A', 0.011), ('Disjoncteur  C60HDC 2x2A Courbe C', 0.302), ('VOYANT BLANC A COLLERETTE 22mm 24VDC', 0.0625), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.302), ('Contact Auxiliaire OF',0.0066),('Disjoncteur  C60HDC 2x16A Courbe C', 0.302), ('Contact Auxiliaire OF/SD',0.0066), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.302), ('Contact Auxiliaire OF/SD',0.0066), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.302), ('Contact Auxiliaire OF/SD',0.0066)]
        fab5=0
        dis5=0
        ins5=0
        use5=0
        fin5=0
        for (nom1,valeur1) in Fabrication5:
            fab5 += float(valeur1)
        for (nom1,valeur1) in Distribution5:
            dis5+=float(valeur1)
        for (nom1,valeur1) in Installation5:
            ins5+=float(valeur1)
        for (nom1,valeur1) in Utilisation5:
            use5+=float(valeur1)
        for (nom1,valeur1) in Fin5:
            fin5+=float(valeur1)
        total5 = fab5 + dis5 + ins5 + use5 + fin5
        
        if section1=='CSAP POSTE HT':
            GWP5 = round(abs(total1), 2)
            st.session_state.GWP5 = GWP5
        elif section1=='CSAP POSTE TGBT':
            GWP5 = round(abs(total2), 2)
        elif section1=="COFFRET D'ISOLEMENT 125A":
            GWP5 = round(abs(total3), 2)
            st.session_state.GWP5 = GWP5
        elif section1=="COFFRET DE COMPTAGE":
            GWP5 = round(abs(total4), 2)
            st.session_state.GWP5 = GWP5
        elif section1=="COFFRET HQ":
            GWP5 = round(abs(total5), 2)
            st.session_state.GWP5 = GWP5
        if st.button("Valider"):
            st.metric(label="Total GWP du coffret choisi", value=f"{GWP5} kg CO₂")
        if st.button("Ajouter à la liste"):
            st.session_state.total_liste.append({f'Coffret {section1}' : GWP5})
            if section1=='CSAP POSTE HT':
                d = {
                    '': [f'{section1}'],
                    'Fabrication': [fab],
                    'Distribution': [dis],
                    'Installation': [ins],
                    'Utilisation': [use],
                    'Fin de vie': [fin],
                    'Global warming': [GWP5]
                }
            elif section1=='CSAP POSTE TGBT':
                d = {
                    '': [f'{section1}'],
                    'Fabrication': [fab2],
                    'Distribution': [dis2],
                    'Installation': [ins2],
                    'Utilisation': [use2],
                    'Fin de vie': [fin2],
                    'Global warming': [GWP5]
                }
            elif section1=="COFFRET D'ISOLEMENT 125A":
                d = {
                    '': [f'{section1}'],
                    'Fabrication': [fab3],
                    'Distribution': [dis3],
                    'Installation': [ins3],
                    'Utilisation': [use3],
                    'Fin de vie': [fin3],
                    'Global warming': [GWP5]
                }
            elif section1=="COFFRET DE COMPTAGE":
                d = {
                    '': [f'{section1}'],
                    'Fabrication': [fab4],
                    'Distribution': [dis4],
                    'Installation': [ins4],
                    'Utilisation': [use4],
                    'Fin de vie': [fin4],
                    'Global warming': [GWP5]
                }
            elif section1=="COFFRET HQ":
                d = {
                    '': [f'{section1}'],
                    'Fabrication': [fab5],
                    'Distribution': [dis5],
                    'Installation': [ins5],
                    'Utilisation': [use5],
                    'Fin de vie': [fin5],
                    'Global warming': [GWP5]
                }
            df1 = pd.DataFrame(d)
            st.session_state.df = pd.concat([st.session_state.df, df1], ignore_index=True)
            st.dataframe(st.session_state.df)
            st.success("Ajouté à la liste !")
        detail_button_container = st.empty()
        detail_button_container2 = st.empty()
        if detail_button_container.button("Voir le détail", key="detail_button_418"):
            st.session_state.df_co = pd.DataFrame()
            t=0
            w=0
            q=0
            z=0
            e=0
            for i, row in st.session_state.df.iterrows():
                if row[''] == 'CSAP POSTE HT':
                    t += 1
                elif row[''] == 'CSAP POSTE TGBT':
                    w += 1
                elif row[''] == "COFFRET D'ISOLEMENT 125A":
                    q += 1
                elif row[''] == "COFFRET DE COMPTAGE":
                    z += 1
                elif row[''] == "COFFRET HQ":
                    e += 1
            details = []
            if t>0:
                for x in range(len(Fabrication1)):
                        tot = (float(Fabrication1[x][1]) + float(Distribution1[x][1]) + float(Installation1[x][1]) + float(Utilisation1[x][1]) + float(Fin1[x][1]))
                        ligne = {'': f"{t} X {Fabrication1[x][0]}",
                            "Fabrication": float(Fabrication1[x][1]*t),
                            "Distribution": float(Distribution1[x][1]*t),
                            "Installation": float(Installation1[x][1]*t),
                            "Utilisation": float(Utilisation1[x][1]*t),
                            "Fin de vie": float(Fin1[x][1]*t),
                            'Global warming': float(tot*t)
                        }
                        details.append(ligne)
            if w>0:
                for y in range(len(Fabrication2)):
                        tot2 = (float(Fabrication2[y][1]) + float(Distribution2[y][1]) + float(Installation2[y][1]) + float(Utilisation2[y][1]) + float(Fin2[y][1]))
                        ligne2 = {'': f"{w} X {Fabrication2[y][0]}",
                            "Fabrication": float(Fabrication2[y][1]*w),
                            "Distribution": float(Distribution2[y][1]*w),
                            "Installation": float(Installation2[y][1]*w),
                            "Utilisation": float(Utilisation2[y][1]*w),
                            "Fin de vie": float(Fin2[y][1]*w),
                            'Global warming': float(tot2*w)
                        }
                        details.append(ligne2)
            if q>0:
                for a in range(len(Fabrication3)):
                        tot3 = (float(Fabrication3[a][1]) + float(Distribution3[a][1]) + float(Installation3[a][1]) + float(Utilisation3[a][1]) + float(Fin3[a][1]))
                        ligne3 = {'': f"{q} X {Fabrication3[a][0]}",
                            "Fabrication": float(Fabrication3[a][1]*q),
                            "Distribution": float(Distribution3[a][1]*q),
                            "Installation": float(Installation3[a][1]*q),
                            "Utilisation": float(Utilisation3[a][1]*q),
                            "Fin de vie": float(Fin3[a][1]*q),
                            'Global warming': float(tot3*q)
                        }
                        details.append(ligne3)
            if z>0:
                for s in range(len(Fabrication4)):
                        tot4 = (float(Fabrication4[s][1]) + float(Distribution4[s][1]) + float(Installation4[s][1]) + float(Utilisation4[s][1]) + float(Fin4[s][1]))
                        ligne4 = {'': f"{z} X {Fabrication4[s][0]}",
                            "Fabrication": float(Fabrication4[s][1]*z),
                            "Distribution": float(Distribution4[s][1]*z),
                            "Installation": float(Installation4[s][1]*z),
                            "Utilisation": float(Utilisation4[s][1]*z),
                            "Fin de vie": float(Fin4[s][1]*z),
                            'Global warming': float(tot4*z)
                        }
                        details.append(ligne4)
            if e>0:
                for b in range(len(Fabrication5)):
                        tot5 = (float(Fabrication5[b][1]) + float(Distribution5[b][1]) + float(Installation5[b][1]) + float(Utilisation5[b][1]) + float(Fin5[b][1]))
                        ligne5 = {'': f"{e} X {Fabrication5[b][0]}",
                            "Fabrication": float(Fabrication5[b][1]*e),
                            "Distribution": float(Distribution5[b][1]*e),
                            "Installation": float(Installation5[b][1]*e),
                            "Utilisation": float(Utilisation5[b][1]*e),
                            "Fin de vie": float(Fin5[b][1]*e),
                            'Global warming': float(tot5*e)
                        }
                        details.append(ligne5)
            df1 = pd.DataFrame(details)
            st.session_state.df_co = pd.concat([st.session_state.df_co, df1], ignore_index=True)
            st.dataframe(st.session_state.df_co)
            detail_button_container.empty()
            if detail_button_container.button("Voir moins", key="detail_button_419"):
                if not st.session_state.df.empty:
                    st.dataframe(st.session_state.df)
                    detail_button_container.empty()
            
                
elif selected_menu == 'Total GWP':
    st.markdown("<h1 style='color: #4D5D48;'>TOTAL GWP</h1>", unsafe_allow_html=True)
    total_liste = st.session_state.total_liste
    total=0
    if total_liste: 
        for x in total_liste:
            for s in x.keys():
                total += x[s]
                total= round(total,2)
        st.metric(label="Total GWP", value=f"{total} kg CO₂")
        st.subheader("Liste des éléments")
        for x in total_liste:
            for s in x.keys():
                st.write(f"{s}: {x[s]} kg CO₂")
        df= st.session_state.df.copy()
        tot= df.sum(numeric_only=True).to_frame().T
        tot.index=['Total']
        df_tot= pd.concat([df,tot])
        if not st.session_state.df.empty:
            st.dataframe(df_tot)
        csv = st.session_state.df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger",
            data=csv,
            file_name="GWP.csv",
            mime="text/csv"
        )
        if st.button("Réinitialiser la liste"):
            st.session_state.total_liste = []
            st.session_state.df = pd.DataFrame()
            st.rerun()
    else:
        st.info("Aucun élément n'a été ajouté à la liste")
