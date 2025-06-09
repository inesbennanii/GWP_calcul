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
        
        section1 = st.selectbox("", ('CSAP-P725-7 POSTE HT','Coffret2'), key="section1")

        section1 = str(section1)
        Fabrication1 = {'COFFRET PRISMASet G IP30 H:1080 L:600 P:205': 255, 'PORTE PLEINE': 255, 'BLOC INSERT TYPE PAPILLON': 255, 'PATTES DE FIXATION': 255, 'PORTE SCHEMA A4': 471, 'Répartiteur 1/2 rangée - 4P 160A - (Multiclip) - Courant CRETE 20kA ': 255, 'VOYANT TRICOLOR 400V': 0.261, 'TELECOMMANDE BAES URA': 2.90, 'VIGI 30mA': 1.03, 'DISJONCTEUR IC60N 3X2A COURBE C 50kA': 0.835, 'DISJONCTEUR IC60N 3X2A COURBE C 20kA': 0.835, 'DISJONCTEUR IC60H 3X10A COURBE C 30kA': 0.835, 'DISJONCTEUR IC60H 3X16A COURBE C 30kA': 0.835,  'DISJONCTEUR IC60L 3X16A COURBE C 25kA': 0.835, 'DISJONCTEUR IC60L 3X10A COURBE C 30kA':0.835}
        Distribution1 = {'COFFRET PRISMASet G IP30 H:1080 L:600 P:205': 9.47, 'PORTE PLEINE': 9.47, 'BLOC INSERT TYPE PAPILLON': 9.47, 'PATTES DE FIXATION': 9.47, 'PORTE SCHEMA A4': 215, 'Répartiteur 1/2 rangée - 4P 160A - (Multiclip) - Courant CRETE 20kA ': 9.47, 'VOYANT TRICOLOR 400V': 0.00471, 'TELECOMMANDE BAES URA': 0.0067, 'VIGI 30mA': 0.032, 'DISJONCTEUR IC60N 3X2A COURBE C 50kA': 0.0156, 'DISJONCTEUR IC60N 3X2A COURBE C 20kA': 0.0156, 'DISJONCTEUR IC60H 3X10A COURBE C 30kA': 0.0156, 'DISJONCTEUR IC60H 3X16A COURBE C 30kA': 0.0156,  'DISJONCTEUR IC60L 3X16A COURBE C 25kA': 0.0156, 'DISJONCTEUR IC60L 3X10A COURBE C 30kA':0.0156}
        Installation1 = {'COFFRET PRISMASet G IP30 H:1080 L:600 P:205': 9.11, 'PORTE PLEINE': 9.11, 'BLOC INSERT TYPE PAPILLON': 9.11, 'PATTES DE FIXATION': 9.11, 'PORTE SCHEMA A4': 15.4, 'Répartiteur 1/2 rangée - 4P 160A - (Multiclip) - Courant CRETE 20kA ': 9.11, 'VOYANT TRICOLOR 400V': 0.014, 'TELECOMMANDE BAES URA': 0.0172, 'VIGI 30mA': 0.0327, 'DISJONCTEUR IC60N 3X2A COURBE C 50kA': 0.0104, 'DISJONCTEUR IC60N 3X2A COURBE C 20kA': 0.0104, 'DISJONCTEUR IC60H 3X10A COURBE C 30kA': 0.0104, 'DISJONCTEUR IC60H 3X16A COURBE C 30kA': 0.0104,  'DISJONCTEUR IC60L 3X16A COURBE C 25kA': 0.0104, 'DISJONCTEUR IC60L 3X10A COURBE C 30kA':0.0104}
        Utilisation1 = {'COFFRET PRISMASet G IP30 H:1080 L:600 P:205': 253, 'PORTE PLEINE': 253, 'BLOC INSERT TYPE PAPILLON': 253, 'PATTES DE FIXATION': 253, 'PORTE SCHEMA A4': 0, 'Répartiteur 1/2 rangée - 4P 160A - (Multiclip) - Courant CRETE 20kA ': 253, 'VOYANT TRICOLOR 400V': 13.7, 'TELECOMMANDE BAES URA': 61.5, 'VIGI 30mA': 2.41, 'DISJONCTEUR IC60N 3X2A COURBE C 50kA': 12.9, 'DISJONCTEUR IC60N 3X2A COURBE C 20kA': 12.9, 'DISJONCTEUR IC60H 3X10A COURBE C 30kA': 12.9, 'DISJONCTEUR IC60H 3X16A COURBE C 30kA': 12.9,  'DISJONCTEUR IC60L 3X16A COURBE C 25kA': 12.9, 'DISJONCTEUR IC60L 3X10A COURBE C 30kA':12.9}
        Fin1 = {'COFFRET PRISMASet G IP30 H:1080 L:600 P:205': 107, 'PORTE PLEINE': 107, 'BLOC INSERT TYPE PAPILLON': 107, 'PATTES DE FIXATION': 107, 'PORTE SCHEMA A4': 267, 'Répartiteur 1/2 rangée - 4P 160A - (Multiclip) - Courant CRETE 20kA ': 107, 'VOYANT TRICOLOR 400V': 0.0625, 'TELECOMMANDE BAES URA': 0.248, 'VIGI 30mA': 0.3, 'DISJONCTEUR IC60N 3X2A COURBE C 50kA': 0.328, 'DISJONCTEUR IC60N 3X2A COURBE C 20kA': 0.328, 'DISJONCTEUR IC60H 3X10A COURBE C 30kA': 0.328, 'DISJONCTEUR IC60H 3X16A COURBE C 30kA': 0.328,  'DISJONCTEUR IC60L 3X16A COURBE C 25kA': 0.328, 'DISJONCTEUR IC60L 3X10A COURBE C 30kA':0.328}
        fab=0
        dis=0
        ins=0
        use=0
        fin=0
        for x in Fabrication1.keys():
            fab += float(Fabrication1[x])
        for x in Distribution1.keys():
            dis+=float(Distribution1[x])
        for x in Installation1.keys():
            ins+=float(Installation1[x])
        for x in Utilisation1.keys():
            use+=float(Utilisation1[x])
        for x in Fin1.keys():
            fin+=float(Fin1[x])        
        total1 = fab + dis + ins + use + fin
        if section1=='CSAP-P725-7 POSTE HT':
            GWP5 = round(abs(total1), 2)
            st.session_state.GWP5 = GWP5
        if st.button("Valider"):
            st.metric(label="Total GWP du coffret choisi", value=f"{GWP5} kg CO₂")
        if st.button("Ajouter à la liste"):
            st.session_state.total_liste.append({f'Coffret {section1}' : GWP5})
            d = {
                '': [f'{section1}'],
                'Fabrication': [fab],
                'Distribution': [dis],
                'Installation': [ins],
                'Utilisation': [use],
                'Fin de vie': [fin],
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
            for i, row in st.session_state.df.iterrows():
                if row[''] == 'CSAP-P725-7 POSTE HT':
                    t += 1
            details = []
            for s in Fabrication1.keys():
                    tot = (float(Fabrication1[s]) + float(Distribution1[s]) + float(Installation1[s]) + float(Utilisation1[s]) + float(Fin1[s]))
                    ligne = {'': f"{t} X {s}",
                        "Fabrication": float(Fabrication1[s]),
                        "Distribution": float(Distribution1[s]),
                        "Installation": float(Installation1[s]),
                        "Utilisation": float(Utilisation1[s]),
                        "Fin de vie": float(Fin1[s]),
                        'Global warming': float(tot)
                    }
                    details.append(ligne)
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

