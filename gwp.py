import streamlit as st
import pandas as pd
from PIL import Image
import base64
from openpyxl import load_workbook
from streamlit_option_menu import option_menu
from streamlit_scroll_navigation import scroll_navbar


if 'total_liste' not in st.session_state:
    st.session_state.total_liste = []
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()
def get_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

st.markdown("""
    <style>
    html, body, .main, .block-container {
        font-family: Georgia, serif !important;
    }

    h1, h2, h3, h4, h5, h6, p, div, span, label, input, textarea, select, button {
        font-family: Georgia, serif !important;
    }
    </style>
""", unsafe_allow_html=True)

anchor_ids = ["Calcul GWP", "Total GWP"]
anchor_icons = ["calculator", "clipboard-data"]
anchor_ids1 = ['Armoire','Armoire Maitre', 'Armoire Esclave', "Câbles","Cellules","Chargeur 48", "Coffrets",'Gaine à barre','Onduleur','TB1',"TGBT", "Tiroirs","Transformateurs"]
anchor_icons1 = ["1", "2", " ", " ", " ", " ","1", "2", " ", " ", " ", " ", " "]

image = Image.open("vinci.png")
left_col, right_col = st.columns([2, 1])  
with right_col:
    st.image(image, width=150)

selected_menu = option_menu(
        menu_title=None,
        options=anchor_ids,
        icons=anchor_icons,
        menu_icon='cast',
        default_index=0,
        orientation='horizontal',
        styles={
            'container': {
                'padding': '5px',
                'background-color': '#084288',
                'border-radius': '10px',
                'text-align': 'center',
                'box-shadow': '0 2px 5px rgba(0,0,0,0.1)',
            },
            'nav-link': {
                'font-size': '18px',
                'text-align': 'center',
                'margin': '0px 10px',
                'color': 'white',
                '--hover-color': '#BE162F',
                'border-radius': '5px',
            },
            'nav-link-selected': {
                'background-color': '#BE162F',
                'color': 'white',
                'border-radius': '5px',
            },
        },
    )
       

if selected_menu=='Calcul GWP':
    with st.sidebar:
        page = option_menu(
            menu_title=' ',
            options=anchor_ids1,
            icons=anchor_icons1,
            default_index=0,
            styles={
                'container': {'padding': '5px', 'background-color': '#084288', 'color': 'white'},
                'nav-link': {'font-size': '16px', 'text-align': 'left', 'color': 'white'},
                'nav-link-selected': {
                'background-color': '#BE162F',
                'color': 'white',
                'border-radius': '5px',
            },
            }
    )
    if page == 'Câbles':

        st.markdown(
            "<h1 style='color: #BE162F;'>Estimez le matériau le plus éco-responsable pour votre projet</h1>",
            unsafe_allow_html=True)


        st.markdown(
            "<span style='color: #084288; font-size: 18px;'>Choisissez la section pour l'aluminium :</span>",
            unsafe_allow_html=True
            )  
        section1 = st.selectbox("", (25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400, 500, 630), key="section1")

        st.markdown(
            "<span style='color: #084288; font-size: 18px;'>Distance pour l'aluminium :</span>",
            unsafe_allow_html=True
            )
        distance1 = st.text_input("", value="1", key="distance1")

        st.markdown(
            "<span style='color: #084288; font-size: 18px;'>Choisissez la section pour le cuivre :</span>",
            unsafe_allow_html=True
            )
        section2 = st.selectbox("", (25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400, 500, 630), key="section2")

        st.markdown(
            "<span style='color: #084288; font-size: 18px;'>Distance pour le cuivre :</span>",
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
                
            B40 = 0.0594
            C40 = 2.79
            B41 = 0.27
            C41 = 0.651
            B42 = 0.883
            C42 = 17

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

            H40 = 0.191
            I40 = 6.67
            H41 = 0
            I41 = 0
            H42 = 0.0713
            I42 = 2.29

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

            st.info(f"Le matériau à utiliser est **{materiau}**")
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
            st.info("Ajouté à la liste !")

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
            st.info("Ajouté à la liste !")
        
        if not st.session_state.df.empty:
            st.dataframe(st.session_state.df)
        
    elif page == 'Transformateurs':

        st.markdown(
            "<h1 style='color: #BE162F;'>Bilan carbone de votre transformateur</h1>",
            unsafe_allow_html=True
            )


        st.markdown(
            "<span style='color: #084288; font-size: 18px;'>Choisissez la section du transformateur :</span>",
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
            st.info("Ajouté à la liste !")


        if not st.session_state.df.empty:
            st.dataframe(st.session_state.df)
        

    elif page == 'Cellules':
        st.markdown(
            "<h1 style='color: #BE162F;'>Bilan carbone de vos cellules</h1>",
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
                    st.info("Ajouté à la liste !")
            if not st.session_state.df.empty:
               st.dataframe(st.session_state.df)
        
        st.markdown(
            "<h1 style='color: #BE162F;'>Bilan carbone de vos coffrets</h1>",
            unsafe_allow_html=True
        )
        section2 = st.selectbox("", ('TH1', 'TH2', 'TH4', 'TH5', 'TH6'), key="section2")
        
        section2 = str(section2)
        Fabrication1= [('Interrupteur HTA 630A - Jeu de barre calibré 630A', 2220), ('3 x interrupteur de commande 2P 20A', 1.39),('5 x relais miniature LED 40F 48Vcc', 1.61), ('BP affleurant rouge - déclenchement', 0.598), ('BP affleurant vert - enclenchement', 0.598), ('Bouton tournant 2 positions 2NO', 0.664), ('BLOC DE CONTACT  "1 NF', 0.336), ('BP affleurant bleu - essai lampes', 0.598), ('BLOC DE CONTACT 1NO', 0.112), ('RELAIS TEMPORISÉ MULTIFONCTION 1s-100h 12-240Vca/cc 10F', 1.43), ('RESISTANCE 50W - 230V', 105), ('THERMOSTAT', 101)]
        Distribution1= [('Interrupteur HTA 630A - Jeu de barre calibré 630A', 80.5), ('3 x interrupteur de commande 2P 20A', 0.0287),('5 x relais miniature LED 40F 48Vcc', 0.0263),  ('BP affleurant rouge - déclenchement', 0.011), ('BP affleurant vert - enclenchement', 0.011), ('Bouton tournant 2 positions 2NO', 0.013), ('BLOC DE CONTACT  "1 NF', 0.00759), ('BP affleurant bleu - essai lampes', 0.011), ('BLOC DE CONTACT 1NO', 0.00253), ('RELAIS TEMPORISÉ MULTIFONCTION 1s-100h 12-240Vca/cc 10F', 0.0106), ('RESISTANCE 50W - 230V', 1.19), ('THERMOSTAT', 0.143)]
        Installation1= [('Interrupteur HTA 630A - Jeu de barre calibré 630A', 8.74), ('3 x interrupteur de commande 2P 20A', 0.0184), ('5 x relais miniature LED 40F 48Vcc', 0),('BP affleurant rouge - déclenchement', 0.0169), ('BP affleurant vert - enclenchement', 0.0169), ('Bouton tournant 2 positions 2NO', 0.0161), ('BLOC DE CONTACT  "1 NF', 0.0381), ('BP affleurant bleu - essai lampes', 0.0169), ('BLOC DE CONTACT 1NO', 0.0127), ('RELAIS TEMPORISÉ MULTIFONCTION 1s-100h 12-240Vca/cc 10F', 0), ('RESISTANCE 50W - 230V', 0), ('THERMOSTAT', 0)]
        Utilisation1= [('Interrupteur HTA 630A - Jeu de barre calibré 630A', 2340), ('3 x interrupteur de commande 2P 20A', 2.42),('5 x relais miniature LED 40F 48Vcc', 85 ), ('BP affleurant rouge - déclenchement', 0.0618), ('BP affleurant vert - enclenchement', 0.0618), ('Bouton tournant 2 positions 2NO', 0.0619), ('BLOC DE CONTACT  "1 NF', 0.0837), ('BP affleurant bleu - essai lampes', 0.0618), ('BLOC DE CONTACT 1NO', 0.0279), ('RELAIS TEMPORISÉ MULTIFONCTION 1s-100h 12-240Vca/cc 10F', 39.6), ('RESISTANCE 50W - 230V', 262), ('THERMOSTAT', 259)]
        Fin1= [('Interrupteur HTA 630A - Jeu de barre calibré 630A', 1000), ('3 x interrupteur de commande 2P 20A', 0.576), ('5 x relais miniature LED 40F 48Vcc', 0.0266), ('BP affleurant rouge - déclenchement', 0.209), ('BP affleurant vert - enclenchement', 0.209), ('Bouton tournant 2 positions 2NO', 0.253), ('BLOC DE CONTACT  "1 NF', 0.0981), ('BP affleurant bleu - essai lampes', 0.209), ('BLOC DE CONTACT 1NO', 0.0327), ('RELAIS TEMPORISÉ MULTIFONCTION 1s-100h 12-240Vca/cc 10F', 0.0411), ('RESISTANCE 50W - 230V', 0.0501), ('THERMOSTAT', 0)]
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
        
        Fabrication2= [('2 x Interrupteur HTA 630A', 33.2),('CENTRALE DE MESURE POWERLOGIC', 36), ('PORTE FUSIBLE SECTIONNABLE 1 P +N ', 0.486),('3 x PORTE FUSIBLE SECTIONNABLE  3P +N ',1.46 ), ('3 x interrupteur de commande 2P 20A', 1.39),('4 x relais miniature LED 40F 48Vcc', 1.29), ("Moteur d'armement disjoncteur 48Vcc",8.48), ('BP affleurant rouge - déclenchement', 0.598), ('BP affleurant vert - enclenchement', 0.598), ('Bouton tournant 2 positions 2NO', 0.664), ('BLOC DE CONTACT  "1 NF', 0.336), ('BP affleurant bleu - essai lampes', 0.598), ('BLOC DE CONTACT 1NO', 0.112), ('RESISTANCE 50W - 230V', 105), ('THERMOSTAT', 101)]
        Distribution2= [('2 x Interrupteur HTA 630A', 0.738),('CENTRALE DE MESURE POWERLOGIC', 0.26), ('PORTE FUSIBLE SECTIONNABLE 1 P +N ',0.00616),('3 x PORTE FUSIBLE SECTIONNABLE  3P +N ', 0.0185),  ('3 x interrupteur de commande 2P 20A', 0.0287), ('4 x relais miniature LED 40F 48Vcc', 0.021),("Moteur d'armement disjoncteur 48Vcc", 0.226), ('BP affleurant rouge - déclenchement', 0.011), ('BP affleurant vert - enclenchement', 0.011), ('Bouton tournant 2 positions 2NO', 0.013), ('BLOC DE CONTACT  "1 NF', 0.00759), ('BP affleurant bleu - essai lampes', 0.011), ('BLOC DE CONTACT 1NO', 0.00253),('RESISTANCE 50W - 230V', 1.19), ('THERMOSTAT', 0.143)]
        Installation2= [('2 x Interrupteur HTA 630A', 0.258),('CENTRALE DE MESURE POWERLOGIC', 0.0479), ('PORTE FUSIBLE SECTIONNABLE 1 P +N ', 0.00465),('3 x PORTE FUSIBLE SECTIONNABLE  3P +N ', 0.014), ('3 x interrupteur de commande 2P 20A', 0.0184),('4 x relais miniature LED 40F 48Vcc', 0) ,("Moteur d'armement disjoncteur 48Vcc", 0.346), ('BP affleurant rouge - déclenchement', 0.0169), ('BP affleurant vert - enclenchement', 0.0169), ('Bouton tournant 2 positions 2NO', 0.0161), ('BLOC DE CONTACT  "1 NF', 0.0381), ('BP affleurant bleu - essai lampes', 0.0169), ('BLOC DE CONTACT 1NO', 0.0127),('RESISTANCE 50W - 230V', 0), ('THERMOSTAT', 0)]
        Utilisation2= [('2 x Interrupteur HTA 630A', 872),('CENTRALE DE MESURE POWERLOGIC', 290), ('PORTE FUSIBLE SECTIONNABLE 1 P +N ', 22.8),('3 x PORTE FUSIBLE SECTIONNABLE  3P +N ', 68.4),('3 x interrupteur de commande 2P 20A', 2.42),('4 x relais miniature LED 40F 48Vcc', 68),("Moteur d'armement disjoncteur 48Vcc", 0.084) ,('BP affleurant rouge - déclenchement', 0.0618), ('BP affleurant vert - enclenchement', 0.0618), ('Bouton tournant 2 positions 2NO', 0.0619), ('BLOC DE CONTACT  "1 NF', 0.0837), ('BP affleurant bleu - essai lampes', 0.0618), ('BLOC DE CONTACT 1NO', 0.0279),('RESISTANCE 50W - 230V', 262), ('THERMOSTAT', 259)]
        Fin2= [('2 x Interrupteur HTA 630A', 8.66),('CENTRALE DE MESURE POWERLOGIC', 1.3), ('PORTE FUSIBLE SECTIONNABLE 1 P +N ', 0.16),('3 x PORTE FUSIBLE SECTIONNABLE  3P +N ', 0.48), ('3 x interrupteur de commande 2P 20A', 0.576), ('4 x relais miniature LED 40F 48Vcc', 0.0213),("Moteur d'armement disjoncteur 48Vcc", 3.78), ('BP affleurant rouge - déclenchement', 0.209),('BP affleurant vert - enclenchement', 0.209), ('Bouton tournant 2 positions 2NO', 0.253), ('BLOC DE CONTACT  "1 NF', 0.0981), ('BP affleurant bleu - essai lampes', 0.209), ('BLOC DE CONTACT 1NO', 0.0327),('RESISTANCE 50W - 230V', 0.0501), ('THERMOSTAT', 0)]
        fab2=0
        dis2=0
        ins2=0
        use2=0
        fin2=0
        for (nom,valeur) in Fabrication2:
            fab2 += float(valeur)
        for (nom,valeur) in Distribution2:
            dis2+=float(valeur)
        for (nom,valeur) in Installation2:
            ins2+=float(valeur)
        for (nom,valeur) in Utilisation2:
            use2+=float(valeur)
        for (nom,valeur) in Fin2:
            fin2+=float(valeur)  
        total2 = fab2 + dis2 + ins2 + use2 + fin2
        
        Fabrication3= [('Interrupteur HTA 630A - Jeu de barre calibré 630A', 2220), ('3 x interrupteur de commande 2P 20A', 1.39),('5 x relais miniature LED 40F 48Vcc', 1.61), ('BP affleurant rouge - déclenchement', 0.598), ('BP affleurant vert - enclenchement', 0.598), ('Bouton tournant 2 positions 2NO', 0.664), ('BLOC DE CONTACT  "1 NF', 0.336), ('BP affleurant bleu - essai lampes', 0.598), ('BLOC DE CONTACT 1NO', 0.112),("Moteur d'armement disjoncteur 48Vcc", 8.48), ('RELAIS TEMPORISÉ MULTIFONCTION 1s-100h 12-240Vca/cc 10F', 1.43), ('RESISTANCE 50W - 230V', 105), ('THERMOSTAT', 101)]
        Distribution3= [('Interrupteur HTA 630A - Jeu de barre calibré 630A', 80.5), ('3 x interrupteur de commande 2P 20A', 0.0287),('5 x relais miniature LED 40F 48Vcc', 0.0263),  ('BP affleurant rouge - déclenchement', 0.011), ('BP affleurant vert - enclenchement', 0.011), ('Bouton tournant 2 positions 2NO', 0.013), ('BLOC DE CONTACT  "1 NF', 0.00759), ('BP affleurant bleu - essai lampes', 0.011), ('BLOC DE CONTACT 1NO', 0.00253),("Moteur d'armement disjoncteur 48Vcc", 0.226),('RELAIS TEMPORISÉ MULTIFONCTION 1s-100h 12-240Vca/cc 10F', 0.0106), ('RESISTANCE 50W - 230V', 1.19), ('THERMOSTAT', 0.143)]
        Installation3= [('Interrupteur HTA 630A - Jeu de barre calibré 630A', 8.74), ('3 x interrupteur de commande 2P 20A', 0.0184), ('5 x relais miniature LED 40F 48Vcc', 0),('BP affleurant rouge - déclenchement', 0.0169), ('BP affleurant vert - enclenchement', 0.0169), ('Bouton tournant 2 positions 2NO', 0.0161), ('BLOC DE CONTACT  "1 NF', 0.0381), ('BP affleurant bleu - essai lampes', 0.0169), ('BLOC DE CONTACT 1NO', 0.0127),("Moteur d'armement disjoncteur 48Vcc", 0.346), ('RELAIS TEMPORISÉ MULTIFONCTION 1s-100h 12-240Vca/cc 10F', 0), ('RESISTANCE 50W - 230V', 0), ('THERMOSTAT', 0)]
        Utilisation3= [('Interrupteur HTA 630A - Jeu de barre calibré 630A', 2340), ('3 x interrupteur de commande 2P 20A', 2.42),('5 x relais miniature LED 40F 48Vcc', 85 ), ('BP affleurant rouge - déclenchement', 0.0618), ('BP affleurant vert - enclenchement', 0.0618), ('Bouton tournant 2 positions 2NO', 0.0619), ('BLOC DE CONTACT  "1 NF', 0.0837), ('BP affleurant bleu - essai lampes', 0.0618), ('BLOC DE CONTACT 1NO', 0.0279),("Moteur d'armement disjoncteur 48Vcc", 0.084), ('RELAIS TEMPORISÉ MULTIFONCTION 1s-100h 12-240Vca/cc 10F', 39.6), ('RESISTANCE 50W - 230V', 262), ('THERMOSTAT', 259)]
        Fin3= [('Interrupteur HTA 630A - Jeu de barre calibré 630A', 1000), ('3 x interrupteur de commande 2P 20A', 0.576), ('5 x relais miniature LED 40F 48Vcc', 0.0266), ('BP affleurant rouge - déclenchement', 0.209), ('BP affleurant vert - enclenchement', 0.209), ('Bouton tournant 2 positions 2NO', 0.253), ('BLOC DE CONTACT  "1 NF', 0.0981), ('BP affleurant bleu - essai lampes', 0.209), ('BLOC DE CONTACT 1NO', 0.0327),("Moteur d'armement disjoncteur 48Vcc", 0.0213), ('RELAIS TEMPORISÉ MULTIFONCTION 1s-100h 12-240Vca/cc 10F', 0.0411), ('RESISTANCE 50W - 230V', 0.0501), ('THERMOSTAT', 0)]
        fab3=0
        dis3=0
        ins3=0
        use3=0
        fin3=0
        for (nom,valeur) in Fabrication3:
            fab3 += float(valeur)
        for (nom,valeur) in Distribution3:
            dis3+=float(valeur)
        for (nom,valeur) in Installation3:
            ins3+=float(valeur)
        for (nom,valeur) in Utilisation3:
            use3+=float(valeur)
        for (nom,valeur) in Fin3:
            fin3+=float(valeur)  
        total3 = fab3 + dis3 + ins3 + use3 + fin3
        
        if section2=='TH1' or section2=='TH2':
            GWP5 = round(abs(total1), 2)
            st.session_state.GWP5 = GWP5
        if section2=='TH4':
            GWP5 = round(abs(total2), 2)
            st.session_state.GWP5 = GWP5
        if section2=='TH5' or section2=='TH6':
            GWP5 = round(abs(total3), 2)
            st.session_state.GWP5 = GWP5
        if st.button("Valider coffret"):
            st.metric(label="Total GWP du coffret choisi", value=f"{GWP5} kg CO₂")
        if st.button("Ajouter le coffret à la liste"):
            st.session_state.total_liste.append({f'Coffret {section2}' : GWP5})
            if section2=='TH1'or section2=='TH2':
                d = {
                    '': [f'Coffret {section2}'],
                    'Fabrication': [fab],
                    'Distribution': [dis],
                    'Installation': [ins],
                    'Utilisation': [use],
                    'Fin de vie': [fin],
                    'Global warming': [GWP5]
                }
            elif section2=='TH3'or section2=='TH4':
                d = {
                    '': [f'Coffret {section2}'],
                    'Fabrication': [fab2],
                    'Distribution': [dis2],
                    'Installation': [ins2],
                    'Utilisation': [use2],
                    'Fin de vie': [fin2],
                    'Global warming': [GWP5]
                }
            elif section2=='TH5'or section2=='TH6':
                d = {
                    '': [f'Coffret {section2}'],
                    'Fabrication': [fab3],
                    'Distribution': [dis3],
                    'Installation': [ins3],
                    'Utilisation': [use3],
                    'Fin de vie': [fin3],
                    'Global warming': [GWP5]
                }
            df1 = pd.DataFrame(d)
            st.session_state.df = pd.concat([st.session_state.df, df1], ignore_index=True)
            st.dataframe(st.session_state.df)
            st.info("Ajouté à la liste !")
        detail_button_container = st.empty()
        detail_button_container2 = st.empty()
        if detail_button_container.button("Voir le détail", key="detail_button_418"):
            st.session_state.df_co = pd.DataFrame()
            t=0
            q=0
            w=0
            for i, row in st.session_state.df.iterrows():
                if row[''] == 'Coffret TH1' or row[''] == 'Coffret TH2':
                    t += 1
                elif row[''] == 'Coffret TH4' :
                    q += 1
                elif row[''] == 'Coffret TH5' or row[''] == 'Coffret TH6' :
                    w += 1
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
            if q>0:
                for x in range(len(Fabrication2)):
                        tot = (float(Fabrication2[x][1]) + float(Distribution2[x][1]) + float(Installation2[x][1]) + float(Utilisation2[x][1]) + float(Fin2[x][1]))
                        ligne = {'': f"{q} X {Fabrication2[x][0]}",
                            "Fabrication": float(Fabrication2[x][1]*q),
                            "Distribution": float(Distribution2[x][1]*q),
                            "Installation": float(Installation2[x][1]*q),
                            "Utilisation": float(Utilisation2[x][1]*q),
                            "Fin de vie": float(Fin2[x][1]*q),
                            'Global warming': float(tot*q)
                        }
                        details.append(ligne)
            if w>0:
                for x in range(len(Fabrication3)):
                        tot = (float(Fabrication3[x][1]) + float(Distribution3[x][1]) + float(Installation3[x][1]) + float(Utilisation3[x][1]) + float(Fin3[x][1]))
                        ligne = {'': f"{w} X {Fabrication3[x][0]}",
                            "Fabrication": float(Fabrication3[x][1]*w),
                            "Distribution": float(Distribution3[x][1]*w),
                            "Installation": float(Installation3[x][1]*w),
                            "Utilisation": float(Utilisation3[x][1]*w),
                            "Fin de vie": float(Fin3[x][1]*w),
                            'Global warming': float(tot*w)
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
    elif page == 'Coffrets':
        st.markdown(
            "<h1 style='color: #BE162F;'>Bilan carbone de votre coffret</h1>",
            unsafe_allow_html=True
            )
        st.markdown(
            "<span style='color: #084288; font-size: 18px;'>Choisissez le coffret :</span>",
            unsafe_allow_html=True
            )  
        
        section1 = st.selectbox("", ('CSAP POSTE HT','CSAP POSTE TGBT',"COFFRET D'ISOLEMENT 125A", "COFFRET DE COMPTAGE", "COFFRET HQ", "COFFRET REPORT", "COFFRET CONTROLE D'ACCES", "COFFRET RCEI"), key="section1")

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
        
        
        Fabrication5=[('ARMOIRE ACIER SPACIAL', 471), ('SOCLE 200mm', 942), ('PORTE SCHEMA A4', 471),('Interrupteur iSW 2x40A', 2.29),("ARRET D'URGENCE", 1.69), ('DISJONCTEUR IC60N 4x2A Courbe C', 0.835),("VOYANT TRICOLOR 400V", 0.261), ("DISJONCTEUR IC60N 2x2A Courbe C", 0.835),("CONTACT DE PORTE", 0.0000511),("ECLAIRAGE LED 230V 5W", 0.000491),("4 x Disjoncteur  C60HDC 2x10A Courbe C", 3.34),("4 x Contact Auxiliaire OF/SD", 1.16),("DISJONCTEUR IC60N 3x2A Courbe C", 0.835),("Contact Auxiliaire OF/SD", 0.289), ('DISJONCTEUR IC60N 2x3A Courbe C', 0.835), ('Contact Auxiliaire OF/SD', 0.289), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.835), ('Contact Auxiliaire OF/SD', 0.289), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.835), ('Contact Auxiliaire OF/SD', 0.289), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.835), ('Contact Auxiliaire OF/SD', 0.289), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.835), ('Contact Auxiliaire OF/SD', 0.289), ('ALIMENTATION REGULEE à DECOUPAGE TRI 480W/20A', 23.1), ('Disjoncteur  C60HDC 2x2A Courbe C', 0.85), ('REPARTITEUR BIPOLAIRES A BORNES EQUIPES DE 2 BARREAUX - 2x40A', 1.08), ('Disjoncteur  C60HDC 2x2A Courbe C', 0.85), ('VOYANT BLANC A COLLERETTE 22mm 24VDC', 0.261), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.85), ('Contact Auxiliaire OF', 0.289), ('Disjoncteur  C60HDC 2x16A Courbe C', 0.85), ('Contact Auxiliaire OF/SD', 0.289), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.85), ('Contact Auxiliaire OF/SD', 0.289), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.85), ('Contact Auxiliaire OF/SD', 0.289)]
        Distribution5=[('ARMOIRE ACIER SPACIAL', 215), ('ARMOIRE ACIER SPACIAL', 430), ('PORTE SCHEMA A4', 215),('Interrupteur iSW 2x40A', 0.0321),("ARRET D'URGENCE", 0.0206),('DISJONCTEUR IC60N 4x2A Courbe C', 0.0156), ("VOYANT TRICOLOR 400V", 0.00471),("DISJONCTEUR IC60N 2x2A Courbe C", 0.0156),("CONTACT DE PORTE", 0.00000000661),("ECLAIRAGE LED 230V 5W", 0),("4 x Disjoncteur  C60HDC 2x10A Courbe C", 0.0624),("4 x Contact Auxiliaire OF/SD", 0.0231),("DISJONCTEUR IC60N 3x2A Courbe C", 0.0156),("Contact Auxiliaire OF/SD", 0.00577),('DISJONCTEUR IC60N 2x3A Courbe C', 0.0156), ('Contact Auxiliaire OF/SD', 0.00577), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.0156), ('Contact Auxiliaire OF/SD', 0.00577), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.0156), ('Contact Auxiliaire OF/SD', 0.00577), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.0156), ('Contact Auxiliaire OF/SD', 0.00577), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.0156), ('Contact Auxiliaire OF/SD', 0.00577), ('ALIMENTATION REGULEE à DECOUPAGE TRI 480W/20A', 0.363), ('Disjoncteur  C60HDC 2x2A Courbe C', 0.0152), ('REPARTITEUR BIPOLAIRES A BORNES EQUIPES DE 2 BARREAUX - 2x40A', 0.0204), ('Disjoncteur  C60HDC 2x2A Courbe C', 0.0152), ('VOYANT BLANC A COLLERETTE 22mm 24VDC', 0.00471), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.0152), ('Contact Auxiliaire OF', 0.00577), ('Disjoncteur  C60HDC 2x16A Courbe C', 0.0152), ('Contact Auxiliaire OF/SD', 0.00577), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.0152), ('Contact Auxiliaire OF/SD', 0.00577), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.0152), ('Contact Auxiliaire OF/SD', 0.00577)]
        Installation5=[('ARMOIRE ACIER SPACIAL', 15.4), ('SOCLE 200mm', 30.8), ('PORTE SCHEMA A4', 15.4),('Interrupteur iSW 2x40A', 0.0226),("ARRET D'URGENCE", 0.000691), ("DISJONCTEUR IC60N 4x2A Courbe C", 0.0104),("VOYANT TRICOLOR 400V", 0.014), ("DISJONCTEUR IC60N 2x2A Courbe C", 0.0104),("CONTACT DE PORTE", 0),("ECLAIRAGE LED 230V 5W", 0),("4 x Disjoncteur  C60HDC 2x10A Courbe C", 0.0416),("4 x Contact Auxiliaire OF/SD", 0.00275),("DISJONCTEUR IC60N 3x2A Courbe C", 0.0104),("Contact Auxiliaire OF/SD", 0.000688),('DISJONCTEUR IC60N 2x3A Courbe C', 0.0104), ('Contact Auxiliaire OF/SD', 0.000688), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.0104), ('Contact Auxiliaire OF/SD', 0.000688), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.0104), ('Contact Auxiliaire OF/SD', 0.000688), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.0104), ('Contact Auxiliaire OF/SD', 0.000688), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.0104), ('Contact Auxiliaire OF/SD', 0.000688), ('ALIMENTATION REGULEE à DECOUPAGE TRI 480W/20A', 0), ('Disjoncteur  C60HDC 2x2A Courbe C', 0.00837), ('REPARTITEUR BIPOLAIRES A BORNES EQUIPES DE 2 BARREAUX - 2x40A', 0), ('Disjoncteur  C60HDC 2x2A Courbe C', 0.00837), ('VOYANT BLANC A COLLERETTE 22mm 24VDC', 0.014), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.00837), ('Contact Auxiliaire OF', 0.000688), ('Disjoncteur  C60HDC 2x16A Courbe C', 0.00837), ('Contact Auxiliaire OF/SD', 0.000688), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.00837), ('Contact Auxiliaire OF/SD', 0.000688), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.00837), ('Contact Auxiliaire OF/SD', 0.000688)]
        Utilisation5=[('ARMOIRE ACIER SPACIAL', 0),('SOCLE 200mm', 0),('PORTE SCHEMA A4', 0),('Interrupteur iSW 2x40A', 4.33) ,("ARRET D'URGENCE",0), ("DISJONCTEUR IC60N 4x2A Courbe C", 12.9),("VOYANT TRICOLOR 400V", 13.7),("DISJONCTEUR IC60N 2x2A Courbe C", 12.9),("CONTACT DE PORTE", 0),("ECLAIRAGE LED 230V 5W", 0.00000941),("4 x Disjoncteur  C60HDC 2x10A Courbe C", 51.6),("4 x Contact Auxiliaire OF/SD", 2.58),("DISJONCTEUR IC60N 3x2A Courbe C", 12.9),("Contact Auxiliaire OF/SD", 0.644),('DISJONCTEUR IC60N 2x3A Courbe C', 12.9), ('Contact Auxiliaire OF/SD', 0.644), ('DISJONCTEUR IC60N 2x10A Courbe C', 12.9), ('Contact Auxiliaire OF/SD', 0.644), ('DISJONCTEUR IC60N 2x10A Courbe C', 12.9), ('Contact Auxiliaire OF/SD', 0.644), ('DISJONCTEUR IC60N 2x10A Courbe C', 12.9), ('Contact Auxiliaire OF/SD', 0.644), ('DISJONCTEUR IC60N 2x10A Courbe C', 12.9), ('Contact Auxiliaire OF/SD', 0.644), ('ALIMENTATION REGULEE à DECOUPAGE TRI 480W/20A', 1350), ('Disjoncteur  C60HDC 2x2A Courbe C', 9.69), ('REPARTITEUR BIPOLAIRES A BORNES EQUIPES DE 2 BARREAUX - 2x40A', 33.5), ('Disjoncteur  C60HDC 2x2A Courbe C', 9.69), ('VOYANT BLANC A COLLERETTE 22mm 24VDC', 13.7), ('Disjoncteur  C60HDC 2x10A Courbe C', 9.69), ('Contact Auxiliaire OF', 0.644), ('Disjoncteur  C60HDC 2x16A Courbe C', 9.69), ('Contact Auxiliaire OF/SD', 0.644), ('Disjoncteur  C60HDC 2x10A Courbe C', 9.69), ('Contact Auxiliaire OF/SD', 0.644), ('Disjoncteur  C60HDC 2x10A Courbe C', 9.69), ('Contact Auxiliaire OF/SD', 0.644)]
        Fin5=[('ARMOIRE ACIER SPACIAL', 267),('SOCLE 200mm', 534), ('PORTE SCHEMA A4', 267), ('Interrupteur iSW 2x40A', 0.912),("ARRET D'URGENCE", 0.0186), ("DISJONCTEUR IC60N 4x2A Courbe C", 0.328),("VOYANT TRICOLOR 400V", 0.0625),("DISJONCTEUR IC60N 2x2A Courbe C", 0.328),("CONTACT DE PORTE", 0),("ECLAIRAGE LED 230V 5W", 0),("4 x Disjoncteur  C60HDC 2x10A Courbe C", 1.31),("4 x Contact Auxiliaire OF/SD", 0.0264),("DISJONCTEUR IC60N 3x2A Courbe C", 0.328),("Contact Auxiliaire OF/SD", 0.0066),('DISJONCTEUR IC60N 2x3A Courbe C', 0.328), ('Contact Auxiliaire OF/SD', 0.0066), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.328), ('Contact Auxiliaire OF/SD', 0.0066), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.328), ('Contact Auxiliaire OF/SD', 0.0066), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.328), ('Contact Auxiliaire OF/SD', 0.0066), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.328), ('Contact Auxiliaire OF/SD', 0.0066), ('ALIMENTATION REGULEE à DECOUPAGE TRI 480W/20A', 0.14), ('Disjoncteur  C60HDC 2x2A Courbe C', 0.302), ('REPARTITEUR BIPOLAIRES A BORNES EQUIPES DE 2 BARREAUX - 2x40A', 0.011), ('Disjoncteur  C60HDC 2x2A Courbe C', 0.302), ('VOYANT BLANC A COLLERETTE 22mm 24VDC', 0.0625), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.302), ('Contact Auxiliaire OF',0.0066),('Disjoncteur  C60HDC 2x16A Courbe C', 0.302), ('Contact Auxiliaire OF/SD',0.0066), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.302), ('Contact Auxiliaire OF/SD',0.0066), ('Disjoncteur  C60HDC 2x10A Courbe C', 0.302), ('Contact Auxiliaire OF/SD',0.0066)]
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
        
        Fabrication6=[('COFFRET ACIER SPACIAL S3D IP66 H:600 L:400 P:250', 47.8), ('PORTE SCHEMA A4', 471), ('JEU DE 4 PATTES DE FIXATION', 47.8), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.835), ('ALIMENTATION 230VCA/24VCC 5A', 10.1), ('DISJONCTEUR IC60H-DC 2x2A Courbe C', 0.85), ('BATTERIE 12V 7.2AH', 10.5), ('TETE DE STATION STANDARD ETHERNET MB TCP IP NIM', 10400), ('ALIMENTATION 24VDC PDM STANDARD KIT CO ', 7.3), ('CARTE ENTREES TOR 24VDC IN 6PT BASIC KIT', 7.3)]
        Distribution6=[('COFFRET ACIER SPACIAL S3D IP66 H:600 L:400 P:250', 19.5), ('PORTE SCHEMA A4', 215), ('JEU DE 4 PATTES DE FIXATION', 19.5), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.0156), ('ALIMENTATION 230VCA/24VCC 5A', 0.233), ('DISJONCTEUR IC60H-DC 2x2A Courbe C', 0.0152), ('BATTERIE 12V 7.2AH', 0.391), ('TETE DE STATION STANDARD ETHERNET MB TCP IP NIM', 9.45), ('ALIMENTATION 24VDC PDM STANDARD KIT CO ', 0.0181), ('CARTE ENTREES TOR 24VDC IN 6PT BASIC KIT', 0.0181)]
        Installation6=[('COFFRET ACIER SPACIAL S3D IP66 H:600 L:400 P:250', 1.93), ('PORTE SCHEMA A4', 15.4), ('JEU DE 4 PATTES DE FIXATION', 1.93), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.0104), ('ALIMENTATION 230VCA/24VCC 5A', 0), ('DISJONCTEUR IC60H-DC 2x2A Courbe C', 0.00837), ('BATTERIE 12V 7.2AH', 0.191), ('TETE DE STATION STANDARD ETHERNET MB TCP IP NIM', 0), ('ALIMENTATION 24VDC PDM STANDARD KIT CO ', 0), ('CARTE ENTREES TOR 24VDC IN 6PT BASIC KIT', 0)]
        Utilisation6=[('COFFRET ACIER SPACIAL S3D IP66 H:600 L:400 P:250', 0), ('PORTE SCHEMA A4', 0), ('JEU DE 4 PATTES DE FIXATION',0), ('DISJONCTEUR IC60N 2x10A Courbe C', 12.9), ('ALIMENTATION 230VCA/24VCC 5A', 1080), ('DISJONCTEUR IC60H-DC 2x2A Courbe C', 9.69), ('BATTERIE 12V 7.2AH', 4.53), ('TETE DE STATION STANDARD ETHERNET MB TCP IP NIM', 110000), ('ALIMENTATION 24VDC PDM STANDARD KIT CO ', 103), ('CARTE ENTREES TOR 24VDC IN 6PT BASIC KIT', 103)]
        Fin6=[('COFFRET ACIER SPACIAL S3D IP66 H:600 L:400 P:250', 23.1), ('PORTE SCHEMA A4', 267), ('JEU DE 4 PATTES DE FIXATION', 23.1), ('DISJONCTEUR IC60N 2x10A Courbe C', 0.328), ('ALIMENTATION 230VCA/24VCC 5A', 0.124), ('DISJONCTEUR IC60H-DC 2x2A Courbe C', 0.302), ('BATTERIE 12V 7.2AH', 0.314), ('TETE DE STATION STANDARD ETHERNET MB TCP IP NIM', 0), ('ALIMENTATION 24VDC PDM STANDARD KIT CO ', 0.0417), ('CARTE ENTREES TOR 24VDC IN 6PT BASIC KIT', 0.0417)]
        fab6=0
        dis6=0
        ins6=0
        use6=0
        fin6=0
        for (nom1,valeur1) in Fabrication6:
            fab6 += float(valeur1)
        for (nom1,valeur1) in Distribution6:
            dis6+=float(valeur1)
        for (nom1,valeur1) in Installation6:
            ins6+=float(valeur1)
        for (nom1,valeur1) in Utilisation6:
            use6+=float(valeur1)
        for (nom1,valeur1) in Fin6:
            fin6+=float(valeur1)
        total6 = fab6 + dis6 + ins6 + use6 + fin6
        
        Fabrication7=[('COFFRET ACIER SPACIAL S3D IP66 H:600 L:400 P:250', 47.8),('JEU DE 4 PATTES DE FIXATION', 47.8), ('DISJONCTEUR IC60N 2x4A Courbe C', 0.835), ('ALIMENTATION 230VCA/24VCC 5A', 10.1), ('BATTERIE 12V 7.2AH', 10.5)]
        Distribution7=[('COFFRET ACIER SPACIAL S3D IP66 H:600 L:400 P:250', 19.5), ('JEU DE 4 PATTES DE FIXATION', 19.5), ('DISJONCTEUR IC60N 2x4A Courbe C', 0.0156), ('ALIMENTATION 230VCA/24VCC 5A', 0.233), ('BATTERIE 12V 7.2AH', 0.391)]
        Installation7=[('COFFRET ACIER SPACIAL S3D IP66 H:600 L:400 P:250', 1.93), ('JEU DE 4 PATTES DE FIXATION', 1.93), ('DISJONCTEUR IC60N 2x4A Courbe C', 0.0104), ('ALIMENTATION 230VCA/24VCC 5A', 0), ('BATTERIE 12V 7.2AH', 0.191)]
        Utilisation7=[('COFFRET ACIER SPACIAL S3D IP66 H:600 L:400 P:250', 0), ('JEU DE 4 PATTES DE FIXATION',0), ('DISJONCTEUR IC60N 2x4A Courbe C', 12.9), ('ALIMENTATION 230VCA/24VCC 5A', 1080), ('BATTERIE 12V 7.2AH', 4.53)]
        Fin7=[('COFFRET ACIER SPACIAL S3D IP66 H:600 L:400 P:250', 23.1), ('JEU DE 4 PATTES DE FIXATION', 23.1), ('DISJONCTEUR IC60N 2x4A Courbe C', 0.328), ('ALIMENTATION 230VCA/24VCC 5A', 0.124), ('BATTERIE 12V 7.2AH', 0.314)]
        fab7=0
        dis7=0
        ins7=0
        use7=0
        fin7=0
        for (nom1,valeur1) in Fabrication7:
            fab7 += float(valeur1)
        for (nom1,valeur1) in Distribution7:
            dis7+=float(valeur1)
        for (nom1,valeur1) in Installation7:
            ins7+=float(valeur1)
        for (nom1,valeur1) in Utilisation7:
            use7+=float(valeur1)
        for (nom1,valeur1) in Fin7:
            fin7+=float(valeur1)
        total7 = fab7 + dis7 + ins7 + use7 + fin7
        
        Fabrication8=[('ACIER SPACIAL S3D IP66 PORTE VITREE H:600 L:600 P:300', 47.8), ('CHASSIS TELEQUICK', 0.0000511), ('JEU DE 4 PATTES DE FIXATION', 47.8), ('INTER GENERAL ISW 2x20A', 0.464), ('REPARTITEUR BIPOLAIRE 2x40A', 1.46), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 0.85), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 0.85), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 0.85), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 0.85), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 0.85), ('CONVERTISSEUR DE MEDIA ETHERNET VERS FIBRE', 17.4)]
        Distribution8=[('ACIER SPACIAL S3D IP66 PORTE VITREE H:600 L:600 P:300', 19.5), ('CHASSIS TELEQUICK', 0.00000000661), ('JEU DE 4 PATTES DE FIXATION', 19.5), ('INTER GENERAL ISW 2x20A', 0.00955), ('REPARTITEUR BIPOLAIRE 2x40A', 0.0256), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 0.0152), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 0.0152), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 0.0152), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 0.0152), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 0.0152), ('CONVERTISSEUR DE MEDIA ETHERNET VERS FIBRE', 0.0334)]
        Installation8=[('ACIER SPACIAL S3D IP66 PORTE VITREE H:600 L:600 P:300', 1.93), ('CHASSIS TELEQUICK', 0), ('JEU DE 4 PATTES DE FIXATION', 1.93), ('INTER GENERAL ISW 2x20A', 0.00612), ('REPARTITEUR BIPOLAIRE 2x40A', 0.0549), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 0.00837),('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 0.00837), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 0.00837), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 0.00837), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 0.00837), ('CONVERTISSEUR DE MEDIA ETHERNET VERS FIBRE', 0.102)]
        Utilisation8=[('ACIER SPACIAL S3D IP66 PORTE VITREE H:600 L:600 P:300', 0), ('CHASSIS TELEQUICK', 0), ('JEU DE 4 PATTES DE FIXATION', 0), ('INTER GENERAL ISW 2x20A', 0.808), ('REPARTITEUR BIPOLAIRE 2x40A', 17.1), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 9.69), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 9.69), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 9.69), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 9.69), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 9.69), ('CONVERTISSEUR DE MEDIA ETHERNET VERS FIBRE', 184)]
        Fin8=[('ACIER SPACIAL S3D IP66 PORTE VITREE H:600 L:600 P:300', 23.1), ('CHASSIS TELEQUICK', 0), ('JEU DE 4 PATTES DE FIXATION', 23.1), ('INTER GENERAL ISW 2x20A', 0.192), ('REPARTITEUR BIPOLAIRE 2x40A', 0.454), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 0.302), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 0.302), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 0.302), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 0.302), ('DISJONCTEUR IC60H-DC 2x0.5A Courbe C', 0.302), ('CONVERTISSEUR DE MEDIA ETHERNET VERS FIBRE', 0.412)]
        fab8=0
        dis8=0
        ins8=0
        use8=0
        fin8=0
        for (nom1,valeur1) in Fabrication8:
            fab8 += float(valeur1)
        for (nom1,valeur1) in Distribution8:
            dis8+=float(valeur1)
        for (nom1,valeur1) in Installation8:
            ins8+=float(valeur1)
        for (nom1,valeur1) in Utilisation8:
            use8+=float(valeur1)
        for (nom1,valeur1) in Fin8:
            fin8+=float(valeur1)
        total8 = fab8 + dis8 + ins8 + use8 + fin8
        
        
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
        elif section1=="COFFRET REPORT":
            GWP5 = round(abs(total6), 2)
            st.session_state.GWP5 = GWP5
        elif section1=="COFFRET CONTROLE D'ACCES":
            GWP5 = round(abs(total7), 2)
            st.session_state.GWP5 = GWP5
        elif section1=="COFFRET RCEI":
            GWP5 = round(abs(total8), 2)
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
            elif section1=="COFFRET REPORT":
                d = {
                    '': [f'{section1}'],
                    'Fabrication': [fab6],
                    'Distribution': [dis6],
                    'Installation': [ins6],
                    'Utilisation': [use6],
                    'Fin de vie': [fin6],
                    'Global warming': [GWP5]
                }
            elif section1=="COFFRET CONTROLE D'ACCES":
                d = {
                    '': [f'{section1}'],
                    'Fabrication': [fab7],
                    'Distribution': [dis7],
                    'Installation': [ins7],
                    'Utilisation': [use7],
                    'Fin de vie': [fin7],
                    'Global warming': [GWP5]
                }
            elif section1=="COFFRET RCEI":
                d = {
                    '': [f'{section1}'],
                    'Fabrication': [fab7],
                    'Distribution': [dis7],
                    'Installation': [ins7],
                    'Utilisation': [use7],
                    'Fin de vie': [fin7],
                    'Global warming': [GWP5]
                }
            df1 = pd.DataFrame(d)
            st.session_state.df = pd.concat([st.session_state.df, df1], ignore_index=True)
            st.dataframe(st.session_state.df)
            st.info("Ajouté à la liste !")
        detail_button_container = st.empty()
        detail_button_container2 = st.empty()
        if detail_button_container.button("Voir le détail", key="detail_button_418"):
            st.session_state.df_co = pd.DataFrame()
            t=0
            w=0
            q=0
            z=0
            e=0
            r=0
            p=0
            i=0
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
                elif row[''] == "COFFRET REPORT":
                    r += 1
                elif row[''] == "COFFRET CONTROLE D'ACCES":
                    p += 1
                elif row[''] == "COFFRET RCEI":
                    i += 1
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
            if r>0:
                for b in range(len(Fabrication6)):
                        tot6 = (float(Fabrication6[b][1]) + float(Distribution6[b][1]) + float(Installation6[b][1]) + float(Utilisation6[b][1]) + float(Fin6[b][1]))
                        ligne6 = {'': f"{r} X {Fabrication6[b][0]}",
                            "Fabrication": float(Fabrication6[b][1]*r),
                            "Distribution": float(Distribution6[b][1]*r),
                            "Installation": float(Installation6[b][1]*r),
                            "Utilisation": float(Utilisation6[b][1]*r),
                            "Fin de vie": float(Fin6[b][1]*r),
                            'Global warming': float(tot6*r)
                        }
                        details.append(ligne6)
            if p>0:
                for b in range(len(Fabrication7)):
                        tot7 = (float(Fabrication7[b][1]) + float(Distribution7[b][1]) + float(Installation7[b][1]) + float(Utilisation7[b][1]) + float(Fin7[b][1]))
                        ligne7 = {'': f"{p} X {Fabrication7[b][0]}",
                            "Fabrication": float(Fabrication7[b][1]*p),
                            "Distribution": float(Distribution7[b][1]*p),
                            "Installation": float(Installation7[b][1]*p),
                            "Utilisation": float(Utilisation7[b][1]*p),
                            "Fin de vie": float(Fin7[b][1]*p),
                            'Global warming': float(tot7*p)
                        }
                        details.append(ligne7)
            if i>0:
                for b in range(len(Fabrication8)):
                        tot8 = (float(Fabrication8[b][1]) + float(Distribution8[b][1]) + float(Installation8[b][1]) + float(Utilisation8[b][1]) + float(Fin8[b][1]))
                        ligne8 = {'': f"{i} X {Fabrication8[b][0]}",
                            "Fabrication": float(Fabrication8[b][1]*i),
                            "Distribution": float(Distribution8[b][1]*i),
                            "Installation": float(Installation8[b][1]*i),
                            "Utilisation": float(Utilisation8[b][1]*i),
                            "Fin de vie": float(Fin8[b][1]*i),
                            'Global warming': float(tot8*i)
                        }
                        details.append(ligne8)
            df1 = pd.DataFrame(details)
            st.session_state.df_co = pd.concat([st.session_state.df_co, df1], ignore_index=True)
            st.dataframe(st.session_state.df_co)
            detail_button_container.empty()
            if detail_button_container.button("Voir moins", key="detail_button_419"):
                if not st.session_state.df.empty:
                    st.dataframe(st.session_state.df)
                    detail_button_container.empty()
    elif page == 'Chargeur 48':
        st.markdown(
            "<h1 style='color: #BE162F;'>Bilan carbone de votre chargeur 48</h1>",
            unsafe_allow_html=True
            )
        st.markdown(
            "<span style='color: #084288; font-size: 18px;'>Choisissez le coffret :</span>",
            unsafe_allow_html=True
            )  
        
        section1 = st.selectbox("", ("COFFRET DISTRIBUTION 48Vcc"), key="section1")

        section1 = str(section1)
        Fabrication1 = [('COFFRET PRISMASet G IP30 H:1080 L:600 P:205', 255), ('PORTE PLEINE', 255), ('BLOC INSERT TYPE PAPILLON', 255), ('PATTES DE FIXATION', 255), ('PORTE SCHEMA A4', 471),  ('Répartiteur modulaire monobloc bipolaire à bornes 40A ', 1.46), ('Disjoncteur  C60HDC 2x2A Courbe C PDC 20KA', 0.85), ('Contact Auxiliaire OF/SD', 0.289), ('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.85), ('Contact Auxiliaire OF/SD', 0.289), ('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.85), ('Contact Auxiliaire OF/SD', 0.289),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.85), ('Contact Auxiliaire OF/SD', 0.289),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.85), ('Contact Auxiliaire OF/SD', 0.289),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.85), ('Contact Auxiliaire OF/SD', 0.289),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.85), ('Contact Auxiliaire OF/SD', 0.289),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.85), ('Contact Auxiliaire OF/SD', 0.289),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.85), ('Contact Auxiliaire OF/SD', 0.289),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.85), ('Contact Auxiliaire OF/SD', 0.289),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.85), ('Contact Auxiliaire OF/SD', 0.289),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.85), ('Contact Auxiliaire OF/SD', 0.289),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.85), ('Contact Auxiliaire OF/SD', 0.289),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.85), ('Contact Auxiliaire OF/SD', 0.289),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.85), ('Contact Auxiliaire OF/SD', 0.289),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.85), ('Contact Auxiliaire OF/SD', 0.289)]
        Distribution1 = [ ('COFFRET PRISMASet G IP30 H:1080 L:600 P:205', 9.4),  ('PORTE PLEINE', 9.47),  ('BLOC INSERT TYPE PAPILLON', 9.47),  ('PATTES DE FIXATION', 9.47),  ('PORTE SCHEMA A4', 215), ('Répartiteur modulaire monobloc bipolaire à bornes 40A ', 0.0256), ('Disjoncteur  C60HDC 2x2A Courbe C PDC 20KA', 0.0152),('Contact Auxiliaire OF/SD', 0.00577), ('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.0152),('Contact Auxiliaire OF/SD', 0.00577), ('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.0152),('Contact Auxiliaire OF/SD', 0.00577), ('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.0152),('Contact Auxiliaire OF/SD', 0.00577), ('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.0152),('Contact Auxiliaire OF/SD', 0.00577), ('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.0152),('Contact Auxiliaire OF/SD', 0.00577), ('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.0152),('Contact Auxiliaire OF/SD', 0.00577), ('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.0152),('Contact Auxiliaire OF/SD', 0.00577), ('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.0152),('Contact Auxiliaire OF/SD', 0.00577), ('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.0152),('Contact Auxiliaire OF/SD', 0.00577), ('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.0152),('Contact Auxiliaire OF/SD', 0.00577), ('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.0152),('Contact Auxiliaire OF/SD', 0.00577), ('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.0152),('Contact Auxiliaire OF/SD', 0.00577), ('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.0152),('Contact Auxiliaire OF/SD', 0.00577), ('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.0152),('Contact Auxiliaire OF/SD', 0.00577), ('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.0152),('Contact Auxiliaire OF/SD', 0.00577)]
        Installation1 = [ ('COFFRET PRISMASet G IP30 H:1080 L:600 P:205', 9.11), ('PORTE PLEINE', 9.11), ('BLOC INSERT TYPE PAPILLON', 9.11), ('PATTES DE FIXATION', 9.11),  ('PORTE SCHEMA A4', 15.4),  ('Répartiteur modulaire monobloc bipolaire à bornes 40A ', 0.0549), ('Disjoncteur  C60HDC 2x2A Courbe C PDC 20KA', 0.00837),('Contact Auxiliaire OF/SD', 0.000688),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.00837),('Contact Auxiliaire OF/SD', 0.000688),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.00837),('Contact Auxiliaire OF/SD', 0.000688),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.00837),('Contact Auxiliaire OF/SD', 0.000688),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.00837),('Contact Auxiliaire OF/SD', 0.000688),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.00837),('Contact Auxiliaire OF/SD', 0.000688),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.00837),('Contact Auxiliaire OF/SD', 0.000688),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.00837),('Contact Auxiliaire OF/SD', 0.000688),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.00837),('Contact Auxiliaire OF/SD', 0.000688),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.00837),('Contact Auxiliaire OF/SD', 0.000688),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.00837),('Contact Auxiliaire OF/SD', 0.000688),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.00837),('Contact Auxiliaire OF/SD', 0.000688),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.00837),('Contact Auxiliaire OF/SD', 0.000688),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.00837),('Contact Auxiliaire OF/SD', 0.000688),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.00837),('Contact Auxiliaire OF/SD', 0.000688),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.00837),('Contact Auxiliaire OF/SD', 0.000688)]
        Utilisation1 = [ ('COFFRET PRISMASet G IP30 H:1080 L:600 P:205', 253),  ('PORTE PLEINE', 253),  ('BLOC INSERT TYPE PAPILLON', 253),  ('PATTES DE FIXATION', 253),  ('PORTE SCHEMA A4', 0),  ('Répartiteur modulaire monobloc bipolaire à bornes 40A ', 17.5), ('Disjoncteur  C60HDC 2x2A Courbe C PDC 20KA', 9.69),('Contact Auxiliaire OF/SD', 0.644),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 9.69),('Contact Auxiliaire OF/SD', 0.644),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 9.69),('Contact Auxiliaire OF/SD', 0.644),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 9.69),('Contact Auxiliaire OF/SD', 0.644),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 9.69),('Contact Auxiliaire OF/SD', 0.644),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 9.69),('Contact Auxiliaire OF/SD', 0.644),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 9.69),('Contact Auxiliaire OF/SD', 0.644),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 9.69),('Contact Auxiliaire OF/SD', 0.644),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 9.69),('Contact Auxiliaire OF/SD', 0.644),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 9.69),('Contact Auxiliaire OF/SD', 0.644),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 9.69),('Contact Auxiliaire OF/SD', 0.644),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 9.69),('Contact Auxiliaire OF/SD', 0.644),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 9.69),('Contact Auxiliaire OF/SD', 0.644),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 9.69),('Contact Auxiliaire OF/SD', 0.644),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 9.69),('Contact Auxiliaire OF/SD', 0.644),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 9.69),('Contact Auxiliaire OF/SD', 0.644)]
        Fin1 = [ ('COFFRET PRISMASet G IP30 H:1080 L:600 P:205', 107),  ('PORTE PLEINE', 107),  ('BLOC INSERT TYPE PAPILLON', 107),  ('PATTES DE FIXATION', 107),  ('PORTE SCHEMA A4', 267),  ('Répartiteur modulaire monobloc bipolaire à bornes 40A ', 0.454), ('Disjoncteur  C60HDC 2x2A Courbe C PDC 20KA', 0.302), ('Contact Auxiliaire OF/SD', 0.0066), ('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.302), ('Contact Auxiliaire OF/SD', 0.0066),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.302), ('Contact Auxiliaire OF/SD', 0.0066),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.302), ('Contact Auxiliaire OF/SD', 0.0066),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.302), ('Contact Auxiliaire OF/SD', 0.0066),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.302), ('Contact Auxiliaire OF/SD', 0.0066),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.302), ('Contact Auxiliaire OF/SD', 0.0066),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.302), ('Contact Auxiliaire OF/SD', 0.0066),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.302), ('Contact Auxiliaire OF/SD', 0.0066),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.302), ('Contact Auxiliaire OF/SD', 0.0066),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.302), ('Contact Auxiliaire OF/SD', 0.0066),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.302), ('Contact Auxiliaire OF/SD', 0.0066),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.302), ('Contact Auxiliaire OF/SD', 0.0066),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.302), ('Contact Auxiliaire OF/SD', 0.0066),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.302), ('Contact Auxiliaire OF/SD', 0.0066),('Disjoncteur  C60HDC 2x16A Courbe C PDC 20KA', 0.302), ('Contact Auxiliaire OF/SD', 0.0066)] 
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
        if section1=='COFFRET DISTRIBUTION 48Vcc':
            GWP5 = round(abs(total1), 2)
            st.session_state.GWP5 = GWP5
        if st.button("Valider"):
            st.metric(label="Total GWP du coffret choisi", value=f"{GWP5} kg CO₂")
        if st.button("Ajouter à la liste"):
            st.session_state.total_liste.append({f'Coffret {section1}' : GWP5})
            if section1=='COFFRET DISTRIBUTION 48Vcc':
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
                st.info("Ajouté à la liste !")
        detail_button_container = st.empty()
        detail_button_container2 = st.empty()
        if detail_button_container.button("Voir le détail", key="detail_button_418"):
            st.session_state.df_co = pd.DataFrame()
            t=0
            for i, row in st.session_state.df.iterrows():
                if row[''] == 'COFFRET DISTRIBUTION 48Vcc':
                    t += 1
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
            df1 = pd.DataFrame(details)
            st.session_state.df_co = pd.concat([st.session_state.df_co, df1], ignore_index=True)
            st.dataframe(st.session_state.df_co)
            detail_button_container.empty()
            if detail_button_container.button("Voir moins", key="detail_button_419"):
                if not st.session_state.df.empty:
                    st.dataframe(st.session_state.df)
                    detail_button_container.empty()
    elif page == 'TGBT':
        st.markdown(
            "<h1 style='color: #BE162F;'>Bilan carbone de votre TGBT</h1>",
            unsafe_allow_html=True
            )
        Fabrication1= [('interrupteur MTZ2 HA 2000A 3P débrochable', 537), ('6 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,2mm2 - 6mm2, AWG: 24 - 10', 0.0707*6), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 0.618), ('ZELIO CONTROL, ORDRE ET ABSENCE DE PHASE, TRIPHASE, 208-480VAC', 1.72), ('interrupteur MTZ2 HA 2000A 3P débrochable', 537), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 0.618), ('ZELIO CONTROL, ORDRE ET ABSENCE DE PHASE, TRIPHASE, 208-480VAC', 1.72), ('6 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,2mm2 - 6mm2, AWG: 24 - 10', 0.0707*6), ('CENTRALE DE MESURE POWER METER PM5561',36), ('ACTI9, IC60L DISJONCTEUR 2P 4A COURBE C', 0.835), ('ACTI9, VIGI IC60, BLOC DIFFERENTIEL 2P 25A 30MA TYPE AC 230-240V 400-415V', 1.03), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 0.618), ('PRISE DE COURANT MODULAIRE 16A 2P+T, STANDARD FRANÇAIS, 250V', 0.654), ('ZELIO CONTROL, ORDRE ET ABSENCE DE PHASE, TRIPHASE, 208-480VAC', 1.72), ('COMPACT NSXM - DISJONCTEUR VIGI - 70KA - MICROLOGIC 4.1 - 50A - 4P - EVERLINK', 18.9), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV', 0.0899), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV', 0.0899), ('COMPACT NSXM - DISJONCTEUR VIGI - 70KA - MICROLOGIC 4.1 - 50A - 4P - EVERLINK', 18.9), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV', 0.0899), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV', 0.0899), ('4 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12', 0.0401*4), ('ALIMENTATION A DECOUPAGE PRIMAIRE, ENTREE: MONOPHASEE, SORTIE: 24VDC 20A',37.3), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV',0.0899), ('INTERRUPTEUR iSW 415VAC 2P 32A',0.464), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22',0.618), ('AUXILIAIRE IACTS NO+NF', 0.679), ('CONTACTEUR iCT BI 2NO 16A 230-240VAC', 0.679), ('ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC',0.364), ('ACTI9, IC60N DISJONCTEUR 2P 10A COURBE C', 0.835), ('CONTACT AUXILIAIRE INVERSEUR OF iSW 250VAC/6A 415VAC/3A', 0.464), ('INTERRUPTEUR iSW 415VAC 2P 32A', 0.464), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22',0.618), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 0.364), ('ACTI9, IC60N DISJONCTEUR 2P 6A COURBE C', 0.835), ('ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC', 0.364), ('ACTI9, IC60N DISJONCTEUR 2P 6A COURBE C', 0.835), ('2 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12', 0.0401), ('AUXILIAIRE IACTS NO+NF', 0.679), ('CONTACTEUR iCT BI 2NO 16A 230-240VAC', 0.679), ('ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC',0.364), ('ACTI9, IC60N DISJONCTEUR 2P 10A COURBE C', 0.835), ('RELAIS TEMPO TRAVAIL - 1s..100h - 24..240V AC/DC - SORTIE STATIQUE', 1.43), ('AUXILIAIRE IACTS NO+NF', 0.679), ('CONTACTEUR iCT BI 2NO 16A 230-240VAC',0.679), ('ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC',0.364), ('ACTI9, IC60N DISJONCTEUR 2P 10A COURBE C', 0.835), ('RELAIS TEMPO TRAVAIL - 1s..100h - 24..240V AC/DC - SORTIE STATIQUE', 1.43), ("TETE ARRET D'URGENCE", 1.69), ('CORPS CONTACT', 0.598), ("6 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.0401*6), ('SWITCH ETHERNET, 5 PORTS RJ45 24VDC', 11.27), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, ROUGE, D22", 0.618), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, VERT, D22",0.618), ("RELAIS TEMPORISE, 1INV, 1s-100h, 24VDC/24-240VAC", 1.43), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, VERT, D22", 0.618), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, JAUNE/ORANGE, D22", 0.618), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, BLEU, D22", 0.618), ("BOUTON POUSSOIR AFFLEURANT, ROND, 1NO, NOIR, D22", 0.598), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, ROUGE, D22", 0.618), ("BOUTON TOURNANT A MANETTE NOIRE, ROND, 2POS. FIXES, 1NO, D22", 0.664),
    ("BOUTON POUSSOIR LUMINEUX DEL INTEGREE 24VAC/DC, AFFLEURANT , RONDE, 1NO+1NF, BLEU, D22", 0.773), ('VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, JAUNE/ORANGE, D22', 0.618), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, JAUNE/ORANGE, D22", 0.618), ("TETE BOUTON TOURNANT", 0.664), ("EMBASE DE FIXATION XB4B", 0.598), ("2 x CONTACT VIS ETRIER O", 0.121*2), ("2 x CONTACT DOUBLE F+O", 0.121*2), ("4 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.0401*4), ("2 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.0401*2), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, ROUGE, D22", 0.618), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, VERT, D22", 0.618), ("BOUTON POUSSOIR AFFLEURANT, ROND, 1NO, VERT, D22", 0.598), ("BOUTON POUSSOIR", 0.598), ("CONTACT VIS ETRIER F", 0.112), ("3 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.0401), ("3 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.0401), ("3 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.0401), ("3 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.0401)]
        Distribution1= [('interrupteur MTZ2 HA 2000A 3P débrochable', 11.6), ('6 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,2mm2 - 6mm2, AWG: 24 - 10', 0.000996*6), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 0.0108), ('ZELIO CONTROL, ORDRE ET ABSENCE DE PHASE, TRIPHASE, 208-480VAC', 0.225), ('interrupteur MTZ2 HA 2000A 3P débrochable', 11.6), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 0.0108), ('ZELIO CONTROL, ORDRE ET ABSENCE DE PHASE, TRIPHASE, 208-480VAC', 0.225), ('6 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,2mm2 - 6mm2, AWG: 24 - 10', 0.000996*6), ('CENTRALE DE MESURE POWER METER PM5561', 0.26), ('ACTI9, IC60L DISJONCTEUR 2P 4A COURBE C', 0.0156), ('ACTI9, VIGI IC60, BLOC DIFFERENTIEL 2P 25A 30MA TYPE AC 230-240V 400-415V', 0.032), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 0.0108), ('PRISE DE COURANT MODULAIRE 16A 2P+T, STANDARD FRANÇAIS, 250V', 0.0129), ('ZELIO CONTROL, ORDRE ET ABSENCE DE PHASE, TRIPHASE, 208-480VAC', 0.225), ('COMPACT NSXM - DISJONCTEUR VIGI - 70KA - MICROLOGIC 4.1 - 50A - 4P - EVERLINK', 0.287), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV',0.00486), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV',0.00486), ('COMPACT NSXM - DISJONCTEUR VIGI - 70KA - MICROLOGIC 4.1 - 50A - 4P - EVERLINK', 0.287), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV',0.00486), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV',0.00486), ('4 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12', 0.000476*4), ('ALIMENTATION A DECOUPAGE PRIMAIRE, ENTREE: MONOPHASEE, SORTIE: 24VDC 20A', 0.0855), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV',0.00486), ('INTERRUPTEUR iSW 415VAC 2P 32A',0.00955), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22',0.0108), ('AUXILIAIRE IACTS NO+NF', 0.0161), ('CONTACTEUR iCT BI 2NO 16A 230-240VAC',0.0161), ('ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC', 0.00594), ('ACTI9, IC60N DISJONCTEUR 2P 10A COURBE C',0.0156), ('CONTACT AUXILIAIRE INVERSEUR OF iSW 250VAC/6A 415VAC/3A',0.00955), ('INTERRUPTEUR iSW 415VAC 2P 32A',0.00955),('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 0.0108), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 0.00594), ('ACTI9, IC60N DISJONCTEUR 2P 6A COURBE C', 0.0156), ('ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC', 0.00594), ('ACTI9, IC60N DISJONCTEUR 2P 6A COURBE C', 0.0156), ('2 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12', 0.000476), ('AUXILIAIRE IACTS NO+NF', 0.0161), ('CONTACTEUR iCT BI 2NO 16A 230-240VAC', 0.0161), ('ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC',0.00594), ('ACTI9, IC60N DISJONCTEUR 2P 10A COURBE C', 0.00156), ('RELAIS TEMPO TRAVAIL - 1s..100h - 24..240V AC/DC - SORTIE STATIQUE', 0.0106), ('AUXILIAIRE IACTS NO+NF', 0.0161), ('CONTACTEUR iCT BI 2NO 16A 230-240VAC', 0.0161), ('ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC', 0.00594), ('ACTI9, IC60N DISJONCTEUR 2P 10A COURBE C', 0.0156), ('RELAIS TEMPO TRAVAIL - 1s..100h - 24..240V AC/DC - SORTIE STATIQUE', 0.0106), ("TETE ARRET D'URGENCE", 0.0206), ('CORPS CONTACT', 0.011), ("6 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.000476*6), ('SWITCH ETHERNET, 5 PORTS RJ45 24VDC', 0.3841), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, ROUGE, D22", 0.0108), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, VERT, D22", 0.0108), ("RELAIS TEMPORISE, 1INV, 1s-100h, 24VDC/24-240VAC", 0.0106), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, VERT, D22", 0.0108), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, JAUNE/ORANGE, D22", 0.0108), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, BLEU, D22", 0.0108), ("BOUTON POUSSOIR AFFLEURANT, ROND, 1NO, NOIR, D22", 0.011), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, ROUGE, D22", 0.0108), ("BOUTON TOURNANT A MANETTE NOIRE, ROND, 2POS. FIXES, 1NO, D22", 0.013),
    ('BOUTON POUSSOIR LUMINEUX DEL INTEGREE 24VAC/DC, AFFLEURANT , RONDE, 1NO+1NF, BLEU, D22', 0.0164), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, JAUNE/ORANGE, D22", 0.0108), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, JAUNE/ORANGE, D22", 0.0108), ("TETE BOUTON TOURNANT", 0.013), ("EMBASE DE FIXATION XB4B", 0.011), ("2 x CONTACT VIS ETRIER O", 0.00235*2), ("2 x CONTACT DOUBLE F+O", 0.00235*2), ("4 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.000476*4), ("2 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.000476*2), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, ROUGE, D22", 0.0108), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, VERT, D22", 0.0108), ("BOUTON POUSSOIR AFFLEURANT, ROND, 1NO, VERT, D22", 0.011), ("BOUTON POUSSOIR", 0.011), ("CONTACT VIS ETRIER F", 0.00235), ("3 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.000476), ("3 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.000476), ("3 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.000476), ("3 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.000476)]
        Installation1= [('interrupteur MTZ2 HA 2000A 3P débrochable', 13.5), ('6 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,2mm2 - 6mm2, AWG: 24 - 10', 0), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 0.0153), ('ZELIO CONTROL, ORDRE ET ABSENCE DE PHASE, TRIPHASE, 208-480VAC', 0.00034), ('interrupteur MTZ2 HA 2000A 3P débrochable', 13.5), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 0.0153), ('ZELIO CONTROL, ORDRE ET ABSENCE DE PHASE, TRIPHASE, 208-480VAC', 0.00034), ('6 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,2mm2 - 6mm2, AWG: 24 - 10', 0), ('CENTRALE DE MESURE POWER METER PM5561', 0.0479), ('ACTI9, IC60L DISJONCTEUR 2P 4A COURBE C', 0.0104), ('ACTI9, VIGI IC60, BLOC DIFFERENTIEL 2P 25A 30MA TYPE AC 230-240V 400-415V', 0.0327), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 0.0153), ('PRISE DE COURANT MODULAIRE 16A 2P+T, STANDARD FRANÇAIS, 250V', 0), ('ZELIO CONTROL, ORDRE ET ABSENCE DE PHASE, TRIPHASE, 208-480VAC', 0.00034), ('COMPACT NSXM - DISJONCTEUR VIGI - 70KA - MICROLOGIC 4.1 - 50A - 4P - EVERLINK', 0.318), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV', 0.0227), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV', 0.0227), ('COMPACT NSXM - DISJONCTEUR VIGI - 70KA - MICROLOGIC 4.1 - 50A - 4P - EVERLINK', 0.318), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV', 0.0227), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV', 0.0227), ('4 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12',0), ('ALIMENTATION A DECOUPAGE PRIMAIRE, ENTREE: MONOPHASEE, SORTIE: 24VDC 20A',0), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV',0.0227), ('INTERRUPTEUR iSW 415VAC 2P 32A',0.00612), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22',0.0153), ('AUXILIAIRE IACTS NO+NF',0), ('CONTACTEUR iCT BI 2NO 16A 230-240VAC',0), ('ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC', 0.000788), ('ACTI9, IC60N DISJONCTEUR 2P 10A COURBE C', 0.00104), ('CONTACT AUXILIAIRE INVERSEUR OF iSW 250VAC/6A 415VAC/3A',0.00612), ('INTERRUPTEUR iSW 415VAC 2P 32A', 0.00612), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22',0.0153), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 0.000788), ('ACTI9, IC60N DISJONCTEUR 2P 6A COURBE C', 0.0104), ('ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC', 0.000788), ('ACTI9, IC60N DISJONCTEUR 2P 6A COURBE C', 0.0104), ('2 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12',0), ('AUXILIAIRE IACTS NO+NF', 0), ('CONTACTEUR iCT BI 2NO 16A 230-240VAC',0), ('ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC',0.000788), ('ACTI9, IC60N DISJONCTEUR 2P 10A COURBE C', 0.0104), ('RELAIS TEMPO TRAVAIL - 1s..100h - 24..240V AC/DC - SORTIE STATIQUE',0), ('AUXILIAIRE IACTS NO+NF',0), ('CONTACTEUR iCT BI 2NO 16A 230-240VAC',0), ('ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC', 0.000788), ('ACTI9, IC60N DISJONCTEUR 2P 10A COURBE C', 0.0104), ('RELAIS TEMPO TRAVAIL - 1s..100h - 24..240V AC/DC - SORTIE STATIQUE',0), ("TETE ARRET D'URGENCE", 0.000691), ('CORPS CONTACT', 0.0169), ("6 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0), ('SWITCH ETHERNET, 5 PORTS RJ45 24VDC', 0), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, ROUGE, D22", 0.0153), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, VERT, D22", 0.0153), ("RELAIS TEMPORISE, 1INV, 1s-100h, 24VDC/24-240VAC", 0), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, VERT, D22", 0.0153), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, JAUNE/ORANGE, D22", 0.0153), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, BLEU, D22", 0.0153), ("BOUTON POUSSOIR AFFLEURANT, ROND, 1NO, NOIR, D22", 0.0169), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, ROUGE, D22", 0.0153), ("BOUTON TOURNANT A MANETTE NOIRE, ROND, 2POS. FIXES, 1NO, D22", 0.0161), 
    ('BOUTON POUSSOIR LUMINEUX DEL INTEGREE 24VAC/DC, AFFLEURANT , RONDE, 1NO+1NF, BLEU, D22', 0.0151), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, JAUNE/ORANGE, D22", 0.0153), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, JAUNE/ORANGE, D22", 0.0153), ("TETE BOUTON TOURNANT", 0.0161), ("EMBASE DE FIXATION XB4B", 0.0169), ("2 x CONTACT VIS ETRIER O", 0.0127*2), ("2 x CONTACT DOUBLE F+O", 0.0127*2), ("4 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12",0), ("2 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12",0), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, ROUGE, D22", 0.0153), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, VERT, D22", 0.0153), ("BOUTON POUSSOIR AFFLEURANT, ROND, 1NO, VERT, D22", 0.0169), ("BOUTON POUSSOIR", 0.0169), ("CONTACT VIS ETRIER F", 0.0127), ("3 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0), ("3 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12",0), ("3 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0), ("3 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12",0)] 
        Utilisation1= [('interrupteur MTZ2 HA 2000A 3P débrochable', 3280), ('6 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,2mm2 - 6mm2, AWG: 24 - 10', 0), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 12.5), ('ZELIO CONTROL, ORDRE ET ABSENCE DE PHASE, TRIPHASE, 208-480VAC', 95.4), ('interrupteur MTZ2 HA 2000A 3P débrochable', 3280), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 12.5), ('ZELIO CONTROL, ORDRE ET ABSENCE DE PHASE, TRIPHASE, 208-480VAC', 95.4), ('6 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,2mm2 - 6mm2, AWG: 24 - 10', 0), ('CENTRALE DE MESURE POWER METER PM5561', 290), ('ACTI9, IC60L DISJONCTEUR 2P 4A COURBE C', 12.9), ('ACTI9, VIGI IC60, BLOC DIFFERENTIEL 2P 25A 30MA TYPE AC 230-240V 400-415V',2.41), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 12.5), ('PRISE DE COURANT MODULAIRE 16A 2P+T, STANDARD FRANÇAIS, 250V', 25.8),('ZELIO CONTROL, ORDRE ET ABSENCE DE PHASE, TRIPHASE, 208-480VAC', 95.4), ('COMPACT NSXM - DISJONCTEUR VIGI - 70KA - MICROLOGIC 4.1 - 50A - 4P - EVERLINK', 197), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV', 1.39), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV', 1.39), ('COMPACT NSXM - DISJONCTEUR VIGI - 70KA - MICROLOGIC 4.1 - 50A - 4P - EVERLINK', 197), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV', 1.39), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV', 1.39), ('4 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12',0), ('ALIMENTATION A DECOUPAGE PRIMAIRE, ENTREE: MONOPHASEE, SORTIE: 24VDC 20A',0), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV',1.39), ('INTERRUPTEUR iSW 415VAC 2P 32A', 0.808), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22',12.5), ('AUXILIAIRE IACTS NO+NF',146), ('CONTACTEUR iCT BI 2NO 16A 230-240VAC', 146), ('ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC', 0.27), ('ACTI9, IC60N DISJONCTEUR 2P 10A COURBE C', 12.9), ('CONTACT AUXILIAIRE INVERSEUR OF iSW 250VAC/6A 415VAC/3A',0.808), ('INTERRUPTEUR iSW 415VAC 2P 32A',0.808), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22',12.5), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 0.27), ('ACTI9, IC60N DISJONCTEUR 2P 6A COURBE C', 12.9), ('ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC',0.27), ('ACTI9, IC60N DISJONCTEUR 2P 6A COURBE C', 12.9), ('2 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12', 0), ('AUXILIAIRE IACTS NO+NF', 146), ('CONTACTEUR iCT BI 2NO 16A 230-240VAC',146), ('ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC',0.27), ('ACTI9, IC60N DISJONCTEUR 2P 10A COURBE C', 12.9), ('RELAIS TEMPO TRAVAIL - 1s..100h - 24..240V AC/DC - SORTIE STATIQUE', 39.6), ('AUXILIAIRE IACTS NO+NF', 146), ('CONTACTEUR iCT BI 2NO 16A 230-240VAC',146), ('ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC', 0.27), ('ACTI9, IC60N DISJONCTEUR 2P 10A COURBE C', 12.9), ('RELAIS TEMPO TRAVAIL - 1s..100h - 24..240V AC/DC - SORTIE STATIQUE', 39.6), ("TETE ARRET D'URGENCE", 0), ('CORPS CONTACT', 0.0618), ("6 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12",0), ('SWITCH ETHERNET, 5 PORTS RJ45 24VDC', 0), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, ROUGE, D22", 12.5), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, VERT, D22", 12.5), ("RELAIS TEMPORISE, 1INV, 1s-100h, 24VDC/24-240VAC", 39.6), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, VERT, D22", 12.5), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, JAUNE/ORANGE, D22", 12.5), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, BLEU, D22", 12.5), ("BOUTON POUSSOIR AFFLEURANT, ROND, 1NO, NOIR, D22", 0.0618), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, ROUGE, D22", 12.5), ("BOUTON TOURNANT A MANETTE NOIRE, ROND, 2POS. FIXES, 1NO, D22", 0.0619), 
    ("BOUTON POUSSOIR LUMINEUX DEL INTEGREE 24VAC/DC, AFFLEURANT , RONDE, 1NO+1NF, BLEU, D22", 12.9),("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, JAUNE/ORANGE, D22", 12.5), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, JAUNE/ORANGE, D22", 12.5), ("TETE BOUTON TOURNANT", 0.0619), ("EMBASE DE FIXATION XB4B", 0.0618), ("2 x CONTACT VIS ETRIER O", 0.0279*2), ("2 x CONTACT DOUBLE F+O", 0.0279*2), ("4 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0), ("2 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12",0), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, ROUGE, D22", 12.5), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, VERT, D22", 12.5), ("BOUTON POUSSOIR AFFLEURANT, ROND, 1NO, VERT, D22", 0.0618), ("BOUTON POUSSOIR", 0.0168), ("CONTACT VIS ETRIER F", 0.0279), ("3 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12",0), ("3 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12",0), ("3 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0), ("3 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12",0)] 
        Fin1= [('interrupteur MTZ2 HA 2000A 3P débrochable', 176), ('6 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,2mm2 - 6mm2, AWG: 24 - 10', 0.000149*6), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 0.205), ('ZELIO CONTROL, ORDRE ET ABSENCE DE PHASE, TRIPHASE, 208-480VAC', 0.205), ('interrupteur MTZ2 HA 2000A 3P débrochable', 176), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 0.205), ('ZELIO CONTROL, ORDRE ET ABSENCE DE PHASE, TRIPHASE, 208-480VAC', 0.205), ('6 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,2mm2 - 6mm2, AWG: 24 - 10', 0.000149*6), ('CENTRALE DE MESURE POWER METER PM5561', 1.3), ('ACTI9, IC60L DISJONCTEUR 2P 4A COURBE C', 0.328), ('ACTI9, VIGI IC60, BLOC DIFFERENTIEL 2P 25A 30MA TYPE AC 230-240V 400-415V', 0.3), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 0.205), ('PRISE DE COURANT MODULAIRE 16A 2P+T, STANDARD FRANÇAIS, 250V', 0.0213), ('ZELIO CONTROL, ORDRE ET ABSENCE DE PHASE, TRIPHASE, 208-480VAC', 0.205), ('COMPACT NSXM - DISJONCTEUR VIGI - 70KA - MICROLOGIC 4.1 - 50A - 4P - EVERLINK', 4.48), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV', 0.0191), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV', 0.0191),  ('COMPACT NSXM - DISJONCTEUR VIGI - 70KA - MICROLOGIC 4.1 - 50A - 4P - EVERLINK', 4.48), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV', 0.0191), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV', 0.0191), ('4 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12', 0.000071*4), ('ALIMENTATION A DECOUPAGE PRIMAIRE, ENTREE: MONOPHASEE, SORTIE: 24VDC 20A',0.0128), ('CONTACT AUXILIAIRE POUR DISJONCTEUR NSXm, 1INV',0.0191), ('INTERRUPTEUR iSW 415VAC 2P 32A', 0.192), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22',0.205), ('AUXILIAIRE IACTS NO+NF',0.0167), ('CONTACTEUR iCT BI 2NO 16A 230-240VAC', 0.0167), ('ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC', 0.0066), ('ACTI9, IC60N DISJONCTEUR 2P 10A COURBE C',0.328), ('CONTACT AUXILIAIRE INVERSEUR OF iSW 250VAC/6A 415VAC/3A', 0.192), ('INTERRUPTEUR iSW 415VAC 2P 32A',0.192), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22', 0.205), ('VOYANT LUMINEUX A DEL INTEGREE, TRANSFO 1.2A 24V, 400VAC, ROND, BLANC, D22',0.0066), ('ACTI9, IC60N DISJONCTEUR 2P 6A COURBE C', 0.328), ('ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC', 0.0066), ('ACTI9, IC60N DISJONCTEUR 2P 6A COURBE C', 0.328), ('2 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12', 0.000071), ('AUXILIAIRE IACTS NO+NF', 0.0167), ('CONTACTEUR iCT BI 2NO 16A 230-240VAC',0.0167), ('ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC', 0.0066), ('ACTI9, IC60N DISJONCTEUR 2P 10A COURBE C', 0.328), ('RELAIS TEMPO TRAVAIL - 1s..100h - 24..240V AC/DC - SORTIE STATIQUE', 0.0411), ('AUXILIAIRE IACTS NO+NF',0.0167), ('CONTACTEUR iCT BI 2NO 16A 230-240VAC',0.0167), ('ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC', 0.0066), ('ACTI9, IC60N DISJONCTEUR 2P 10A COURBE C', 0.328), ('RELAIS TEMPO TRAVAIL - 1s..100h - 24..240V AC/DC - SORTIE STATIQUE', 0.0411), ("TETE ARRET D'URGENCE", 0.0186), ("CORPS CONTACT", 0.209), ("6 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.000071*6), ('SWITCH ETHERNET, 5 PORTS RJ45 24VDC', -1.796), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, ROUGE, D22", 0.205), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, VERT, D22", 0.205), ("RELAIS TEMPORISE, 1INV, 1s-100h, 24VDC/24-240VAC", 0.0411), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, VERT, D22", 0.205), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, JAUNE/ORANGE, D22", 0.205), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, BLEU, D22", 0.205), ("BOUTON POUSSOIR AFFLEURANT, ROND, 1NO, NOIR, D22", 0.209), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, ROUGE, D22", 0.205), ("BOUTON TOURNANT A MANETTE NOIRE, ROND, 2POS. FIXES, 1NO, D22", 0.253), 
    ("BOUTON POUSSOIR LUMINEUX DEL INTEGREE 24VAC/DC, AFFLEURANT , RONDE, 1NO+1NF, BLEU, D22", 0.266), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, JAUNE/ORANGE, D22", 0.205), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, JAUNE/ORANGE, D22", 0.205), ("TETE BOUTON TOURNANT", 0.253), ("EMBASE DE FIXATION XB4B", 0.209), ("2 x CONTACT VIS ETRIER O", 0.0327*2), ("2 x CONTACT DOUBLE F+O", 0.0327*2), ("4 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.000071*4), ("2 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.000071*2), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, ROUGE, D22", 0.205), ("VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, VERT, D22", 0.205), ("BOUTON POUSSOIR AFFLEURANT, ROND, 1NO, VERT, D22", 0.209), ("BOUTON POUSSOIR", 0.209), ("CONTACT VIS ETRIER F", 0.0327), ("3 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.000071), ("3 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.000071), ("3 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.000071), ("3 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12", 0.000071)]
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

        GWP6 = round(abs(total1), 2)
        st.session_state.GWP6 = GWP6
        if st.button("Afficher le GWP du TGBT"):
            st.metric(label="Total GWP du TGBT", value=f"{GWP6} kg CO₂")
        if st.button("Ajouter à la liste"):
            st.session_state.total_liste.append({f'TGBT' : GWP6})
            d = {
                '': 'TGBT',
                'Fabrication': [fab],
                'Distribution': [dis],
                'Installation': [ins],
                'Utilisation': [use],
                'Fin de vie': [fin],
                'Global warming': [GWP6]
                }
            df1 = pd.DataFrame(d)
            st.session_state.df = pd.concat([st.session_state.df, df1], ignore_index=True)
            st.dataframe(st.session_state.df)
            st.info("Ajouté à la liste !")
        detail_button_container = st.empty()
        detail_button_container2 = st.empty()
        if detail_button_container.button("Voir le détail", key="detail_button_418"):
            st.session_state.df_co = pd.DataFrame()
            t=0
            for i, row in st.session_state.df.iterrows():
                if row[''] == 'TGBT':
                    t += 1
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
            df1 = pd.DataFrame(details)
            st.session_state.df_co = pd.concat([st.session_state.df_co, df1], ignore_index=True)
            st.dataframe(st.session_state.df_co)
            detail_button_container.empty()
            if detail_button_container.button("Voir moins", key="detail_button_419"):
                if not st.session_state.df.empty:
                    st.dataframe(st.session_state.df)
                    detail_button_container.empty()
    elif page=='Tiroirs':
        st.markdown(
            "<h1 style='color: #BE162F;'>Bilan carbone de votre TGBT</h1>",
            unsafe_allow_html=True
            )
        section1 = st.selectbox("", ('TIROIR 100A', 'TIROIR 160A', 'TIROIR 250A', 'TIROIR 400A'), key="section1")
        section1 = str(section1)
        Fabrication1=[('2 x TETE BOUTON TOURNANT', 0.664*2), ('2 x CORPS CONTACT', 0.598*2), ('2 x CONTACT VIS ETRIER F', 0.112), ('2 x CONTACT VIS ETRIER O', 0.112), ('COMPLET VOYANT BLANC RONDE', 0.295), ('COMPLET VOYANT ROUGE RONDE', 0.295), ('COMPLET VOYANT JAUNE RONDE', 0.295), ('COMPLET VOYANT BLANC RONDE', 0.295), ('COMPLET VOYANT BLANC RONDE', 0.295), ('COMPLET VOYANT JAUNE RONDE', 0.295), ('VOYANT LUMINEUX A DEL INTEGREE, 230-240VAC ROND, BLANC, D22', 0.618), ('CONTACT AUXILIAIRE INVERSEUR OF', 0.124), ('CONTACT AUXILIAIRE INVERSEUR SD', 0.124), ('CONTACT AUXILIAIRE INVERSEUR SDE', 0.124), ('NSX100H MICROLOGIC 2.2 100A 4P4D; DISJONCTEUR COMPACT', 16), ('1 PERCUTEUR DE PRE-DECLENCHEMENT 2/3/4P ', 7.28), ('TELECOMMANDE AVEC ADAPTATEUR SDE, 220-240V 50/60Hz ET 208-277V 60Hz ', 9.09)]
        Distribution1=[('2 x TETE BOUTON TOURNANT', 0.013*2), ('2 x CORPS CONTACT', 0.011*2), ('2 x CONTACT VIS ETRIER F', 0.00235), ('2 x CONTACT VIS ETRIER O', 0.00235), ('COMPLET VOYANT BLANC RONDE', 0.0013), ('COMPLET VOYANT ROUGE RONDE', 0.0013), ('COMPLET VOYANT JAUNE RONDE', 0.0013), ('COMPLET VOYANT BLANC RONDE', 0.0013), ('COMPLET VOYANT BLANC RONDE', 0.0013), ('COMPLET VOYANT JAUNE RONDE', 0.0013), ('VOYANT LUMINEUX A DEL INTEGREE, 230-240VAC ROND, BLANC, D22', 0.0108), ('CONTACT AUXILIAIRE INVERSEUR OF', 0.00408), ('CONTACT AUXILIAIRE INVERSEUR SD', 0.00408), ('CONTACT AUXILIAIRE INVERSEUR SDE', 0.00408), ('NSX100H MICROLOGIC 2.2 100A 4P4D; DISJONCTEUR COMPACT', 0.602), ('1 PERCUTEUR DE PRE-DECLENCHEMENT 2/3/4P ', 0.336), ('TELECOMMANDE AVEC ADAPTATEUR SDE, 220-240V 50/60Hz ET 208-277V 60Hz ', 0.18)]
        Installation1=[("2 x TETE BOUTON TOURNANT", 0.0161*2), ("2 x CORPS CONTACT", 0.0169*2), ('2 x CONTACT VIS ETRIER F', 0.0127), ('2 x CONTACT VIS ETRIER O', 0.0127), ('COMPLET VOYANT BLANC RONDE', 0.00134),  ('COMPLET VOYANT ROUGE RONDE', 0.00134),  ('COMPLET VOYANT JAUNE RONDE', 0.00134),  ('COMPLET VOYANT BLANC RONDE', 0.00134),  ('COMPLET VOYANT BLANC RONDE', 0.00134),  ('COMPLET VOYANT JAUNE RONDE', 0.00134), ('VOYANT LUMINEUX A DEL INTEGREE, 230-240VAC ROND, BLANC, D22', 0.0153), ('CONTACT AUXILIAIRE INVERSEUR OF', 0.0197), ('CONTACT AUXILIAIRE INVERSEUR SD', 0.0197), ('CONTACT AUXILIAIRE INVERSEUR SDE', 0.0197), ('NSX100H MICROLOGIC 2.2 100A 4P4D; DISJONCTEUR COMPACT', 0.174), ('1 PERCUTEUR DE PRE-DECLENCHEMENT 2/3/4P ', 0.211), ('TELECOMMANDE AVEC ADAPTATEUR SDE, 220-240V 50/60Hz ET 208-277V 60Hz ', 0.256)]
        Utilisation1=[('2 x TETE BOUTON TOURNANT', 0.0619*2), ('2 x CORPS CONTACT', 0.0618*2), ('2 x CONTACT VIS ETRIER F', 0.0279), ('2 x CONTACT VIS ETRIER O', 0.0279), ('COMPLET VOYANT BLANC RONDE', 0.32), ('COMPLET VOYANT ROUGE RONDE', 0.32), ('COMPLET VOYANT JAUNE RONDE', 0.32), ('COMPLET VOYANT BLANC RONDE', 0.32), ('COMPLET VOYANT BLANC RONDE', 0.32), ('COMPLET VOYANT JAUNE RONDE', 0.32), ('VOYANT LUMINEUX A DEL INTEGREE, 230-240VAC ROND, BLANC, D22', 12.5), ('CONTACT AUXILIAIRE INVERSEUR OF', 16.2), ('CONTACT AUXILIAIRE INVERSEUR SD', 16.2), ('CONTACT AUXILIAIRE INVERSEUR SDE', 16.2), ('NSX100H MICROLOGIC 2.2 100A 4P4D; DISJONCTEUR COMPACT', 284), ('1 PERCUTEUR DE PRE-DECLENCHEMENT 2/3/4P ', 102), ('TELECOMMANDE AVEC ADAPTATEUR SDE, 220-240V 50/60Hz ET 208-277V 60Hz ', 0.888)]
        Fin1=[("2 x TETE BOUTON TOURNANT", 0.253*2), ('2 x CORPS CONTACT', 0.209*2), ('2 x CONTACT VIS ETRIER F', 0.0327), ('2 x CONTACT VIS ETRIER O', 0.0327), ('COMPLET VOYANT BLANC RONDE', 0.0157), ('COMPLET VOYANT ROUGE RONDE', 0.0157), ('COMPLET VOYANT JAUNE RONDE', 0.0157), ('COMPLET VOYANT BLANC RONDE', 0.0157), ('COMPLET VOYANT BLANC RONDE', 0.0157), ('COMPLET VOYANT JAUNE RONDE', 0.0157), ('VOYANT LUMINEUX A DEL INTEGREE, 230-240VAC ROND, BLANC, D22', 0.205), ('CONTACT AUXILIAIRE INVERSEUR OF', 0.0387), ('CONTACT AUXILIAIRE INVERSEUR SD', 0.0387), ('CONTACT AUXILIAIRE INVERSEUR SDE', 0.0387), ('NSX100H MICROLOGIC 2.2 100A 4P4D; DISJONCTEUR COMPACT', 3.52), ('1 PERCUTEUR DE PRE-DECLENCHEMENT 2/3/4P ', 3.39), ('TELECOMMANDE AVEC ADAPTATEUR SDE, 220-240V 50/60Hz ET 208-277V 60Hz ', 3.3)]
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
        GWP6 = round(abs(total1), 2)
        st.session_state.GWP6 = GWP6
        if st.button("Afficher le GWP du Tiroir"):
            st.metric(label=f"Total GWP du {section1}", value=f"{GWP6} kg CO₂")
        if st.button("Ajouter à la liste"):
            st.session_state.total_liste.append({section1 : GWP6})
            d = {
                '': section1,
                'Fabrication': [fab],
                'Distribution': [dis],
                'Installation': [ins],
                'Utilisation': [use],
                'Fin de vie': [fin],
                'Global warming': [GWP6]
                }
            df1 = pd.DataFrame(d)
            st.session_state.df = pd.concat([st.session_state.df, df1], ignore_index=True)
            st.dataframe(st.session_state.df)
            st.info("Ajouté à la liste !")
        detail_button_container = st.empty()
        detail_button_container2 = st.empty()
        if detail_button_container.button("Voir le détail", key="detail_button_418"):
            st.session_state.df_co = pd.DataFrame()
            t=0
            for i, row in st.session_state.df.iterrows():
                if row[''] == section1:
                    t += 1
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
            df1 = pd.DataFrame(details)
            st.session_state.df_co = pd.concat([st.session_state.df_co, df1], ignore_index=True)
            st.dataframe(st.session_state.df_co)
            detail_button_container.empty()
            if detail_button_container.button("Voir moins", key="detail_button_419"):
                if not st.session_state.df.empty:
                    st.dataframe(st.session_state.df)
                    detail_button_container.empty()
    elif page=='Armoire':
        st.markdown(
            "<h1 style='color: #BE162F;'>Bilan carbone de votre Armoire API 725-7 </h1>",
            unsafe_allow_html=True
            )
        Fabrication1= [('2 x PC CONFORT BI + TERRE A OBTURATEUR 10/16A 250VAC', 1.31), ('2 x ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC', 0.728), ('4 x DISJONCTEUR iC60N 2P 2A, 440VAC/25kA 133VDC/6kA, COURBE C', 3.34), ('DISJONCTEUR iC60N 2P 4A, 440VAC/25kA 133VDC/6kA, COURBE C', 0.835), ('DISJONCTEUR iC60N 2P 6A, 440VAC/6kA 133VDC/6kA, COURBE D', 0.835), ('4 x ACTI9, IC60N DISJONCTEUR 2P 6A COURBE C', 3.34), ('ACTI9, VIGI IC60, BLOC DIFFERENTIEL 2P 40A 30MA TYPE AC 230-240V 400-415V', 1.03), ('4 x EMBASE DE RACCORDEMENT PASSIVE (POUR CAPTEURS) 16 VOIES', 10.8), ('ETHERNET COMMUNICATION MODULE, 3 PORTS', 17.4), ('PROCESSEUR M580 - 2048 E/S TOR - 512 E/S ANA - 2 PORTS ETHERNET TEMPS REEL', 62.4), ('RACK 12 POSITIONS ETHERNET + BUS X POUR M580', 10.3), ("MODULE D'ALIMENTATION 120/240VAC, 3.3VDC 4.5A, 24VDC 1.3A", 6.33), ("MODULE D'ENTREES 64E 24VDC", 21.1), ('MODULE DE SORTIES TOR 16S RELAIS 2A', 21.1), ('2 x MODULE DE RESEAU AS-INTERFACE', 34.8), ("CORDON-MODICON X80- 1m -CONNECTEUR 40CTS- CONNECTEUR 2xHE10", 0.618), ('CORDON-MODICON X80- 2m -CONNECTEUR 40CTS- CONNECTEUR 2xHE10', 0.618), ('MODULE CONVERTISSEUR FIBRE MULTIMODE / CUIVRE RJ45 2 VOIES 100Mo/s', 17.4), ('VENTILATEUR A FILTRE 92x92 38m3/h, 230VAC', 6.05),('CELLULE AVEC CHASSIS 1P. 2000x1000x600', 362), ('SOCLE EN KIT 1000x600x100', 942), ('INTERRUPTEUR SECTIONNEUR PRINC.AU 25A', 9.04), ('VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, BLANC, D22', 0.618), ('VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, ROUGE, D22', 0.618), ('VOYANT LUMINEUX A DEL INTEGREE, 230-240VAC ROND, BLANC, D22', 0.618)]
        Distribution1= [('2 x PC CONFORT BI + TERRE A OBTURATEUR 10/16A 250VAC', 0.0258), ('2 x ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC', 0.0119), ('4 x DISJONCTEUR iC60N 2P 2A, 440VAC/25kA 133VDC/6kA, COURBE C', 0.0624), ('DISJONCTEUR iC60N 2P 4A, 440VAC/25kA 133VDC/6kA, COURBE C', 0.0156), ('DISJONCTEUR iC60N 2P 6A, 440VAC/6kA 133VDC/6kA, COURBE D', 0.0156), ('4 x ACTI9, IC60N DISJONCTEUR 2P 6A COURBE C', 0.0624), ('ACTI9, VIGI IC60, BLOC DIFFERENTIEL 2P 40A 30MA TYPE AC 230-240V 400-415V', 0.032), ('4 x EMBASE DE RACCORDEMENT PASSIVE (POUR CAPTEURS) 16 VOIES', 0), ('ETHERNET COMMUNICATION MODULE, 3 PORTS', 0.0335), ('PROCESSEUR M580 - 2048 E/S TOR - 512 E/S ANA - 2 PORTS ETHERNET TEMPS REEL', 0.11), ('RACK 12 POSITIONS ETHERNET + BUS X POUR M580', 0.139), ("MODULE D'ALIMENTATION 120/240VAC, 3.3VDC 4.5A, 24VDC 1.3A", 0.0641), ("MODULE D'ENTREES 64E 24VDC", 0.0216), ('MODULE DE SORTIES TOR 16S RELAIS 2A', 0.0216), ('2 x MODULE DE RESEAU AS-INTERFACE', 0.067), ('CORDON-MODICON X80- 1m -CONNECTEUR 40CTS- CONNECTEUR 2xHE10', 0.0149), ('CORDON-MODICON X80- 2m -CONNECTEUR 40CTS- CONNECTEUR 2xHE10', 0.0149), ('MODULE CONVERTISSEUR FIBRE MULTIMODE / CUIVRE RJ45 2 VOIES 100Mo/s', 0.0335), ('VENTILATEUR A FILTRE 92x92 38m3/h, 230VAC', 0), ('CELLULE AVEC CHASSIS 1P. 2000x1000x600', 26.7), ('SOCLE EN KIT 1000x600x100', 430), ('INTERRUPTEUR SECTIONNEUR PRINC.AU 25A', 0.279), ('VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, BLANC, D22', 0.0108), ('VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, ROUGE, D22', 0.0108), ('VOYANT LUMINEUX A DEL INTEGREE, 230-240VAC ROND, BLANC, D22', 0.0108)]
        Installation1= [('2 x PC CONFORT BI + TERRE A OBTURATEUR 10/16A 250VAC', 0), ('2 x ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC', 0.00158), ('4 x DISJONCTEUR iC60N 2P 2A, 440VAC/25kA 133VDC/6kA, COURBE C', 0.0416), ('DISJONCTEUR iC60N 2P 4A, 440VAC/25kA 133VDC/6kA, COURBE C', 0.0104), ('DISJONCTEUR iC60N 2P 6A, 440VAC/6kA 133VDC/6kA, COURBE D', 0.0104), ('4 x ACTI9, IC60N DISJONCTEUR 2P 6A COURBE C', 0.0416), ('ACTI9, VIGI IC60, BLOC DIFFERENTIEL 2P 40A 30MA TYPE AC 230-240V 400-415V', 0.0327), ('4 x EMBASE DE RACCORDEMENT PASSIVE (POUR CAPTEURS) 16 VOIES', 0), ('ETHERNET COMMUNICATION MODULE, 3 PORTS', 0.102), ('PROCESSEUR M580 - 2048 E/S TOR - 512 E/S ANA - 2 PORTS ETHERNET TEMPS REEL', 0), ('RACK 12 POSITIONS ETHERNET + BUS X POUR M580', 0), ("MODULE D'ALIMENTATION 120/240VAC, 3.3VDC 4.5A, 24VDC 1.3A", 0.238), ("MODULE D'ENTREES 64E 24VDC", 0.0439), ('MODULE DE SORTIES TOR 16S RELAIS 2A', 0.0439), ("2 x MODULE DE RESEAU AS-INTERFACE", 0.204), ('CORDON-MODICON X80- 1m -CONNECTEUR 40CTS- CONNECTEUR 2xHE10',0), ('CORDON-MODICON X80- 2m -CONNECTEUR 40CTS- CONNECTEUR 2xHE10', 0), ('MODULE CONVERTISSEUR FIBRE MULTIMODE / CUIVRE RJ45 2 VOIES 100Mo/s', 0.102), ('VENTILATEUR A FILTRE 92x92 38m3/h, 230VAC', 0), ('CELLULE AVEC CHASSIS 1P. 2000x1000x600', 37.7), ('SOCLE EN KIT 1000x600x100', 30.8), ('INTERRUPTEUR SECTIONNEUR PRINC.AU 25A', 0.125), ('VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, BLANC, D22', 0.0153), ('VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, ROUGE, D22', 0.0153), ('VOYANT LUMINEUX A DEL INTEGREE, 230-240VAC ROND, BLANC, D22', 0.0153)]
        Utilisation1= [('2 x PC CONFORT BI + TERRE A OBTURATEUR 10/16A 250VAC', 51.6), ('2 x ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC', 0.54), ('4 x DISJONCTEUR iC60N 2P 2A, 440VAC/25kA 133VDC/6kA, COURBE C', 51.6), ('DISJONCTEUR iC60N 2P 4A, 440VAC/25kA 133VDC/6kA, COURBE C', 12.9), ('DISJONCTEUR iC60N 2P 6A, 440VAC/6kA 133VDC/6kA, COURBE D', 12.9), ('4 x ACTI9, IC60N DISJONCTEUR 2P 6A COURBE C', 51.6), ('ACTI9, VIGI IC60, BLOC DIFFERENTIEL 2P 40A 30MA TYPE AC 230-240V 400-415V', 2.41), ('4 x EMBASE DE RACCORDEMENT PASSIVE (POUR CAPTEURS) 16 VOIES', 4120), ('ETHERNET COMMUNICATION MODULE, 3 PORTS', 184), ('PROCESSEUR M580 - 2048 E/S TOR - 512 E/S ANA - 2 PORTS ETHERNET TEMPS REEL', 301), ('RACK 12 POSITIONS ETHERNET + BUS X POUR M580', 333), ("MODULE D'ALIMENTATION 120/240VAC, 3.3VDC 4.5A, 24VDC 1.3A", 451), ("MODULE D'ENTREES 64E 24VDC", 92), ('MODULE DE SORTIES TOR 16S RELAIS 2A', 92), ("2 x MODULE DE RESEAU AS-INTERFACE", 368), ('CORDON-MODICON X80- 1m -CONNECTEUR 40CTS- CONNECTEUR 2xHE10', 0.0342), ('CORDON-MODICON X80- 2m -CONNECTEUR 40CTS- CONNECTEUR 2xHE10', 0.0342), ('MODULE CONVERTISSEUR FIBRE MULTIMODE / CUIVRE RJ45 2 VOIES 100Mo/s', 184), ('VENTILATEUR A FILTRE 92x92 38m3/h, 230VAC', 1480), ('CELLULE AVEC CHASSIS 1P. 2000x1000x600', 0), ('SOCLE EN KIT 1000x600x100', 0), ('INTERRUPTEUR SECTIONNEUR PRINC.AU 25A', 29), ('VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, BLANC, D22', 12.5), ('VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, ROUGE, D22', 12.5), ('VOYANT LUMINEUX A DEL INTEGREE, 230-240VAC ROND, BLANC, D22', 12.5)]
        Fin1= [('2 x PC CONFORT BI + TERRE A OBTURATEUR 10/16A 250VAC', 0.0426), ('2 x ACTI9, IOF CONTACT AUXILIAIRE OF 240...415VCA 24...130VCC', 0.0132), ('4 x DISJONCTEUR iC60N 2P 2A, 440VAC/25kA 133VDC/6kA, COURBE C', 1.31), ('DISJONCTEUR iC60N 2P 4A, 440VAC/25kA 133VDC/6kA, COURBE C', 0.328), ('DISJONCTEUR iC60N 2P 6A, 440VAC/6kA 133VDC/6kA, COURBE D', 0.328), ('4 x ACTI9, IC60N DISJONCTEUR 2P 6A COURBE C', 1.31), ('ACTI9, VIGI IC60, BLOC DIFFERENTIEL 2P 40A 30MA TYPE AC 230-240V 400-415V', 0.3), ('4 x EMBASE DE RACCORDEMENT PASSIVE (POUR CAPTEURS) 16 VOIES', 0), ('ETHERNET COMMUNICATION MODULE, 3 PORTS', 0.412), ('PROCESSEUR M580 - 2048 E/S TOR - 512 E/S ANA - 2 PORTS ETHERNET TEMPS REEL', 0.36), ('RACK 12 POSITIONS ETHERNET + BUS X POUR M580', 0.393), ("MODULE D'ALIMENTATION 120/240VAC, 3.3VDC 4.5A, 24VDC 1.3A", 0.684), ("MODULE D'ENTREES 64E 24VDC", 0.293), ('MODULE DE SORTIES TOR 16S RELAIS 2A', 0.293), ('2 x MODULE DE RESEAU AS-INTERFACE', 0.824), ('CORDON-MODICON X80- 1m -CONNECTEUR 40CTS- CONNECTEUR 2xHE10', 0.0114), ('CORDON-MODICON X80- 2m -CONNECTEUR 40CTS- CONNECTEUR 2xHE10', 0.0114), ('MODULE CONVERTISSEUR FIBRE MULTIMODE / CUIVRE RJ45 2 VOIES 100Mo/s', 0.412), ('VENTILATEUR A FILTRE 92x92 38m3/h, 230VAC', 0.193), ('CELLULE AVEC CHASSIS 1P. 2000x1000x600', 319), ('SOCLE EN KIT 1000x600x100', 534), ('INTERRUPTEUR SECTIONNEUR PRINC.AU 25A', 3.8), ('VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, BLANC, D22', 0.205), ('VOYANT LUMINEUX A DEL INTEGREE, 24VAC/DC, ROND, ROUGE, D22', 0.205), ('VOYANT LUMINEUX A DEL INTEGREE, 230-240VAC ROND, BLANC, D22', 0.205)]
        
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
        GWP6 = round(abs(total1), 2)
        st.session_state.GWP6 = GWP6
        if st.button("Afficher le GWP de l'armoire"):
            st.metric(label=f"Total GWP de l'armoire API 725-7", value=f"{GWP6} kg CO₂")
        if st.button("Ajouter à la liste"):
            st.session_state.total_liste.append({'ARMOIRE API 725-7' : GWP6})
            d = {
                '': 'ARMOIRE API 725-7',
                'Fabrication': [fab],
                'Distribution': [dis],
                'Installation': [ins],
                'Utilisation': [use],
                'Fin de vie': [fin],
                'Global warming': [GWP6]
                }
            df1 = pd.DataFrame(d)
            st.session_state.df = pd.concat([st.session_state.df, df1], ignore_index=True)
            st.dataframe(st.session_state.df)
            st.info("Ajouté à la liste !")
        detail_button_container = st.empty()
        detail_button_container2 = st.empty()
        if detail_button_container.button("Voir le détail", key="detail_button_418"):
            st.session_state.df_co = pd.DataFrame()
            t=0
            for i, row in st.session_state.df.iterrows():
                if row[''] == 'ARMOIRE API 725-7':
                    t += 1
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
            df1 = pd.DataFrame(details)
            st.session_state.df_co = pd.concat([st.session_state.df_co, df1], ignore_index=True)
            st.dataframe(st.session_state.df_co)
            detail_button_container.empty()
            if detail_button_container.button("Voir moins", key="detail_button_419"):
                if not st.session_state.df.empty:
                    st.dataframe(st.session_state.df)
                    detail_button_container.empty()
                
    elif page=='TB1':
        st.markdown(
            "<h1 style='color: #BE162F;'>Bilan carbone de votre Armoire API 725-7 </h1>",
            unsafe_allow_html=True
            )
        Fabrication1= [('6 x BLOC DE JONCTION A RESSORT 1.5mm2, GRIS', 0.208), ('27 x BLOC DE JONCTION A RESSORT 2.5mm2, GRIS', 0.936), ('17 x BLOC DE JONCTION A RESSORT 2.5mm2, GRIS, 3 CONDUCTEURS', 0.589), ('4 x BLOC DE JONCTION A RESSORT 4mm2, GRIS', 0.139), ('4 x BLOC DE JONCTION A RESSORT 4mm2, GRIS, 3 CONDUCTEURS', 0.139), ('3 x BLOC DE JONCTION A RESSORT AVEC DIODE 2.5mm2, GRIS', 0.104), ('3 x BLOC DE JONCTION A RESSORT SECTIONNABLE 2.5mm2, GRIS', 0.22), ('8 x BLOC DE JONCTION A RESSORT SECTIONNABLE 2.5mm2, GRIS, 3 CONDUCTEURS', 0.586), ('4 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,2mm2 - 6mm2, AWG: 24 - 10', 0.283), ('12 x BJ A COUTEAU DE SECTIONNEMENT, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12', 0.662), ('6 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION: 0.5mm2 - 25mm2, AWG: 20 - 4, GRIS', 0.424), ('2 x REPARTITEUR Arrivée 6mm²-Distribution 2.5mm² BLU', 0.556), ('2 x REPARTITEUR Arrivée 6mm²-Distribution 2.5mm² RED', 0.556), ('DISJONCTEUR MTZ2 2000A H1 3P DEBROCHABLE M5.0X', 537), ('2 X DISJONCTEUR iC60H 2P 4A, 440VAC/50kA, 133VDC/10kA, COURBE C', 1.67), ('DISJONCTEUR C60H-DC 500VDC 4A 2P C', 0.85), ('2 x INTERRUPTEUR iSW 415VAC 2P 20A', 0.938), ('2 x COMPACT NSXM - DISJONCTEUR - 70KA - TM63D - 3P - EVERLINK', 14.5), ('CENTRALE DE MESURE POWER METER PM5561', 36), ('8 x RELAIS DE PUISSANCE MINIATURE - ZELIO RXM - 4 CO - 48 V CC', 2.58), ('2 x RELAIS DE PUISSANCE MINIATURE - ZELIO RXM- 4 CO - 230 V CA', 0.644), ('10 x EMBASE RELAIS, 2/4INV, CONTACTS SEPARES, 12A/6A, 250V, TERMINAUX PUSH-IN', 5.5), ('TETE BOUTON POUSSOIR Ø22 AFFLEURANT VERT', 0.598), ('TETE BOUTON POUSSOIR Ø22 AFFLEURANT ROUGE', 0.598), ('TETE BOUTON POUSSOIR BLEU', 0.598), ('2 x TETE VOYANT LUMINEUX Ø22 LISSE BLANC', 1.24), ('TETE VOYANT LUMINEUX Ø22 LISSE VERT', 0.618), ('TETE VOYANT LUMINEUX Ø22 LISSE ROUGE', 0.618), ('TETE VOYANT LUMINEUX Ø22 LISSE ORANGE', 0.618), ('5 x CORPS VOYANT DEL 24-120V CA-CC', 3.09), ('2  x CORPS CONTACT', 1.2), ('CORPS CONTACT', 0.598)]
        Distribution1= [('6 x BLOC DE JONCTION A RESSORT 1.5mm2, GRIS', 0.00352), ('27 x BLOC DE JONCTION A RESSORT 2.5mm2, GRIS', 0.0158), ('17 x BLOC DE JONCTION A RESSORT 2.5mm2, GRIS, 3 CONDUCTEURS', 0.00998), ('4 x BLOC DE JONCTION A RESSORT 4mm2, GRIS', 0.00235), ('4 x BLOC DE JONCTION A RESSORT 4mm2, GRIS, 3 CONDUCTEURS', 0.00235), ('3 x BLOC DE JONCTION A RESSORT AVEC DIODE 2.5mm2, GRIS', 0.00176), ('3 x BLOC DE JONCTION A RESSORT SECTIONNABLE 2.5mm2, GRIS', 0.00212), ('8 x BLOC DE JONCTION A RESSORT SECTIONNABLE 2.5mm2, GRIS, 3 CONDUCTEURS', 0.00564), ('4 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,2mm2 - 6mm2, AWG: 24 - 10', 0.00398), ('12 x BJ A COUTEAU DE SECTIONNEMENT, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12', 0.00674), ('6 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION: 0.5mm2 - 25mm2, AWG: 20 - 4, GRIS', 0.00597), ('2 x REPARTITEUR Arrivée 6mm²-Distribution 2.5mm² BLU', 0.0544), ('2 x REPARTITEUR Arrivée 6mm²-Distribution 2.5mm² RED', 0.0544), ('DISJONCTEUR MTZ2 2000A H1 3P DEBROCHABLE M5.0X', 11.6), ('2 X DISJONCTEUR iC60H 2P 4A, 440VAC/50kA, 133VDC/10kA, COURBE C', 0.0312), ('DISJONCTEUR C60H-DC 500VDC 4A 2P C', 0.012), ('2 x INTERRUPTEUR iSW 415VAC 2P 20A', 0.0191), ('2 x COMPACT NSXM - DISJONCTEUR - 70KA - TM63D - 3P - EVERLINK', 0.386), ('CENTRALE DE MESURE POWER METER PM5561', 0.26), ('8 x RELAIS DE PUISSANCE MINIATURE - ZELIO RXM - 4 CO - 48 V CC', 0.042), ('2 x RELAIS DE PUISSANCE MINIATURE - ZELIO RXM- 4 CO - 230 V CA', 0.0105), ('10 x EMBASE RELAIS, 2/4INV, CONTACTS SEPARES, 12A/6A, 250V, TERMINAUX PUSH-IN', 0.273), ('TETE BOUTON POUSSOIR Ø22 AFFLEURANT VERT', 0.011), ('TETE BOUTON POUSSOIR Ø22 AFFLEURANT ROUGE', 0.011), ('TETE BOUTON POUSSOIR BLEU', 0.011), ('2 x TETE VOYANT LUMINEUX Ø22 LISSE BLANC', 0.0216), ('TETE VOYANT LUMINEUX Ø22 LISSE VERT', 0.0108), ('TETE VOYANT LUMINEUX Ø22 LISSE ROUGE', 0.0108), ('TETE VOYANT LUMINEUX Ø22 LISSE ORANGE', 0.0108), ('5 x CORPS VOYANT DEL 24-120V CA-CC', 0.054), ('2  x CORPS CONTACT', 0.022), ('CORPS CONTACT', 0.011)]
        Installation1= [('6 x BLOC DE JONCTION A RESSORT 1.5mm2, GRIS', 0), ('27 x BLOC DE JONCTION A RESSORT 2.5mm2, GRIS', 0), ('17 x BLOC DE JONCTION A RESSORT 2.5mm2, GRIS, 3 CONDUCTEURS', 0), ('4 x BLOC DE JONCTION A RESSORT 4mm2, GRIS', 0), ('4 x BLOC DE JONCTION A RESSORT 4mm2, GRIS, 3 CONDUCTEURS', 0), ('3 x BLOC DE JONCTION A RESSORT AVEC DIODE 2.5mm2, GRIS', 0), ('3 x BLOC DE JONCTION A RESSORT SECTIONNABLE 2.5mm2, GRIS', 0), ('8 x BLOC DE JONCTION A RESSORT SECTIONNABLE 2.5mm2, GRIS, 3 CONDUCTEURS', 0), ('4 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,2mm2 - 6mm2, AWG: 24 - 10', 0), ('12 x BJ A COUTEAU DE SECTIONNEMENT, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12', 0), ('6 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION: 0.5mm2 - 25mm2, AWG: 20 - 4, GRIS', 0), ('2 x REPARTITEUR Arrivée 6mm²-Distribution 2.5mm² BLU', 0), ('2 x REPARTITEUR Arrivée 6mm²-Distribution 2.5mm² RED', 0), ('DISJONCTEUR MTZ2 2000A H1 3P DEBROCHABLE M5.0X', 13.5), ('2 X DISJONCTEUR iC60H 2P 4A, 440VAC/50kA, 133VDC/10kA, COURBE C', 0.0208), ('DISJONCTEUR C60H-DC 500VDC 4A 2P C', 0.00837), ('2 x INTERRUPTEUR iSW 415VAC 2P 20A', 0.0122), ('2 x COMPACT NSXM - DISJONCTEUR - 70KA - TM63D - 3P - EVERLINK', 0.29), ('CENTRALE DE MESURE POWER METER PM5561', 0.0479), ('8 x RELAIS DE PUISSANCE MINIATURE - ZELIO RXM - 4 CO - 48 V CC', 0), ('2 x RELAIS DE PUISSANCE MINIATURE - ZELIO RXM- 4 CO - 230 V CA', 0), ('10 x EMBASE RELAIS, 2/4INV, CONTACTS SEPARES, 12A/6A, 250V, TERMINAUX PUSH-IN', 0.0671), ('TETE BOUTON POUSSOIR Ø22 AFFLEURANT VERT', 0.0169), ('TETE BOUTON POUSSOIR Ø22 AFFLEURANT ROUGE', 0.0169), ('TETE BOUTON POUSSOIR BLEU', 0.0169), ('2 x TETE VOYANT LUMINEUX Ø22 LISSE BLANC', 0.0306), ('TETE VOYANT LUMINEUX Ø22 LISSE VERT', 0.0153), ('TETE VOYANT LUMINEUX Ø22 LISSE ROUGE', 0.0153), ('TETE VOYANT LUMINEUX Ø22 LISSE ORANGE', 0.0153), ('5 x CORPS VOYANT DEL 24-120V CA-CC', 0.0765), ('2  x CORPS CONTACT', 0.0338), ('CORPS CONTACT', 0.0169)]
        Utilisation1= [('6 x BLOC DE JONCTION A RESSORT 1.5mm2, GRIS', 0), ('27 x BLOC DE JONCTION A RESSORT 2.5mm2, GRIS', 0), ('17 x BLOC DE JONCTION A RESSORT 2.5mm2, GRIS, 3 CONDUCTEURS', 0), ('4 x BLOC DE JONCTION A RESSORT 4mm2, GRIS', 0), ('4 x BLOC DE JONCTION A RESSORT 4mm2, GRIS, 3 CONDUCTEURS', 0), ('3 x BLOC DE JONCTION A RESSORT AVEC DIODE 2.5mm2, GRIS', 0), ('3 x BLOC DE JONCTION A RESSORT SECTIONNABLE 2.5mm2, GRIS', 0), ('8 x BLOC DE JONCTION A RESSORT SECTIONNABLE 2.5mm2, GRIS, 3 CONDUCTEURS', 0), ('4 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,2mm2 - 6mm2, AWG: 24 - 10', 0), ('12 x BJ A COUTEAU DE SECTIONNEMENT, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12', 0), ('6 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION: 0.5mm2 - 25mm2, AWG: 20 - 4, GRIS', 0), ('2 x REPARTITEUR Arrivée 6mm²-Distribution 2.5mm² BLU', 0), ('2 x REPARTITEUR Arrivée 6mm²-Distribution 2.5mm² RED', 0), ('DISJONCTEUR MTZ2 2000A H1 3P DEBROCHABLE M5.0X', 3280), ('2 X DISJONCTEUR iC60H 2P 4A, 440VAC/50kA, 133VDC/10kA, COURBE C', 25.8), ('DISJONCTEUR C60H-DC 500VDC 4A 2P C', 9.69), ('2 x INTERRUPTEUR iSW 415VAC 2P 20A', 1.62), ('2 x COMPACT NSXM - DISJONCTEUR - 70KA - TM63D - 3P - EVERLINK', 394), ('CENTRALE DE MESURE POWER METER PM5561', 290), ('8 x RELAIS DE PUISSANCE MINIATURE - ZELIO RXM - 4 CO - 48 V CC', 136), ('2 x RELAIS DE PUISSANCE MINIATURE - ZELIO RXM- 4 CO - 230 V CA', 34), ('10 x EMBASE RELAIS, 2/4INV, CONTACTS SEPARES, 12A/6A, 250V, TERMINAUX PUSH-IN', 0), ('TETE BOUTON POUSSOIR Ø22 AFFLEURANT VERT', 0.0618), ('TETE BOUTON POUSSOIR Ø22 AFFLEURANT ROUGE', 0.0618), ('TETE BOUTON POUSSOIR BLEU', 0.0618), ('2 x TETE VOYANT LUMINEUX Ø22 LISSE BLANC', 25), ('TETE VOYANT LUMINEUX Ø22 LISSE VERT', 12.5), ('TETE VOYANT LUMINEUX Ø22 LISSE ROUGE', 12.5), ('TETE VOYANT LUMINEUX Ø22 LISSE ORANGE', 12.5), ('5 x CORPS VOYANT DEL 24-120V CA-CC', 62.5), ('2  x CORPS CONTACT', 0.124), ('CORPS CONTACT', 0.0618)]
        Fin1= [('6 x BLOC DE JONCTION A RESSORT 1.5mm2, GRIS', 0.000525), ('27 x BLOC DE JONCTION A RESSORT 2.5mm2, GRIS', 0.00236), ('17 x BLOC DE JONCTION A RESSORT 2.5mm2, GRIS, 3 CONDUCTEURS', 0.00149), ('4 x BLOC DE JONCTION A RESSORT 4mm2, GRIS', 0.00035), ('4 x BLOC DE JONCTION A RESSORT 4mm2, GRIS, 3 CONDUCTEURS', 0.00035), ('3 x BLOC DE JONCTION A RESSORT AVEC DIODE 2.5mm2, GRIS', 0.000263), ('3 x BLOC DE JONCTION A RESSORT SECTIONNABLE 2.5mm2, GRIS', 0.000316), ('8 x BLOC DE JONCTION A RESSORT SECTIONNABLE 2.5mm2, GRIS, 3 CONDUCTEURS', 0.000842), ('4 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION :0,2mm2 - 6mm2, AWG: 24 - 10', 0.000595), ('12 x BJ A COUTEAU DE SECTIONNEMENT, RACCORDEMENT PUSH-IN, SECTION :0,14mm2 - 4mm2, AWG: 26 - 12', 0.00101), ('6 x BJ SIMPLE, RACCORDEMENT PUSH-IN, SECTION: 0.5mm2 - 25mm2, AWG: 20 - 4, GRIS', 0.000891), ('2 x REPARTITEUR Arrivée 6mm²-Distribution 2.5mm² BLU', 0.000814), ('2 x REPARTITEUR Arrivée 6mm²-Distribution 2.5mm² RED', 0.000814), ('DISJONCTEUR MTZ2 2000A H1 3P DEBROCHABLE M5.0X', 176), ('2 X DISJONCTEUR iC60H 2P 4A, 440VAC/50kA, 133VDC/10kA, COURBE C', 0.656), ('DISJONCTEUR C60H-DC 500VDC 4A 2P C', 0.302), ('2 x INTERRUPTEUR iSW 415VAC 2P 20A', 0.384), ('2 x COMPACT NSXM - DISJONCTEUR - 70KA - TM63D - 3P - EVERLINK', 6.04), ('CENTRALE DE MESURE POWER METER PM5561', 1.3), ('8 x RELAIS DE PUISSANCE MINIATURE - ZELIO RXM - 4 CO - 48 V CC', 0.0426), ('2 x RELAIS DE PUISSANCE MINIATURE - ZELIO RXM- 4 CO - 230 V CA', 0.0106), ('10 x EMBASE RELAIS, 2/4INV, CONTACTS SEPARES, 12A/6A, 250V, TERMINAUX PUSH-IN', 1.53),('TETE BOUTON POUSSOIR Ø22 AFFLEURANT VERT', 0.209), ('TETE BOUTON POUSSOIR Ø22 AFFLEURANT ROUGE', 0.209), ('TETE BOUTON POUSSOIR BLEU', 0.209), ('2 x TETE VOYANT LUMINEUX Ø22 LISSE BLANC', 0.41), ('TETE VOYANT LUMINEUX Ø22 LISSE VERT', 0.205), ('TETE VOYANT LUMINEUX Ø22 LISSE ROUGE', 0.205), ('TETE VOYANT LUMINEUX Ø22 LISSE ORANGE', 0.205), ('5 x CORPS VOYANT DEL 24-120V CA-CC', 1.03), ('2  x CORPS CONTACT', 0.418), ('CORPS CONTACT', 0.209)]
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
        GWP6 = round(abs(total1), 2)
        st.session_state.GWP6 = GWP6
        if st.button("Afficher le GWP du TB1"):
            st.metric(label=f"Total GWP de l'armoire API 725-7", value=f"{GWP6} kg CO₂")
        if st.button("Ajouter à la liste"):
            st.session_state.total_liste.append({'ARMOIRE TB1' : GWP6})
            d = {
                '': 'ARMOIRE TB1',
                'Fabrication': [fab],
                'Distribution': [dis],
                'Installation': [ins],
                'Utilisation': [use],
                'Fin de vie': [fin],
                'Global warming': [GWP6]
                }
            df1 = pd.DataFrame(d)
            st.session_state.df = pd.concat([st.session_state.df, df1], ignore_index=True)
            st.dataframe(st.session_state.df)
            st.info("Ajouté à la liste !")
        detail_button_container = st.empty()
        detail_button_container2 = st.empty()
        if detail_button_container.button("Voir le détail", key="detail_button_418"):
            st.session_state.df_co = pd.DataFrame()
            t=0
            for i, row in st.session_state.df.iterrows():
                if row[''] == 'ARMOIRE TB1':
                    t += 1
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
            df1 = pd.DataFrame(details)
            st.session_state.df_co = pd.concat([st.session_state.df_co, df1], ignore_index=True)
            st.dataframe(st.session_state.df_co)
            detail_button_container.empty()
            if detail_button_container.button("Voir moins", key="detail_button_419"):
                if not st.session_state.df.empty:
                    st.dataframe(st.session_state.df)
                    detail_button_container.empty()

    elif page=='Armoire Maitre':
        st.markdown(
            "<h1 style='color: #BE162F;'>Bilan carbone de votre ARMOIRE TYPE CDGR - API MAITRE - DALI LED </h1>",
            unsafe_allow_html=True
            )
        Fabrication1= [('ARMOIRE MONOBLOC SPATIAL', 471), ('POIGNÉE SM POUR INSERT + ADAPTATEUR POIGNÉE POUR SERRURE DIN', 833), ('2 x JOINT BALAI', 942), ('ANNEAUX DE LEVAGE', 471), ('SOCLE HAUTEUR 200mm', 471), ('2 x ARRET DE PORTE MECANIQUE', 942), ('AUVENT', 471), ('TABLETTE', 471), ('PORTE PLAN', 471), ('KIT DE VENTILATION GRILLE', 0.916), ('CONTACT DE PORTE', .0000511), ('ECLAIRAGE LAMPE LED COMPACTE 11W - AIMANTEE', 13.3), ('RESISTANCE CHAUFFANTE 147W - 230V', 105), ('THERMOSTAT O - REGLABLE 0..60C - POUR COMMANDER UNE RESISTANCE CHAUFFANTE', 101), ('THERMOSTAT F - REGLABLE 0..60C - POUR COMMANDER UN VENTILATEUR', 101), ('INTERRUPTEUR DIFFERENTIEL ilD - 4x25A 300mA', 3.19), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('BOUTON COUP DE POING ROUGE - TOURNER POUR DEVEROUILLER + GARDE POUR COUP DE POING', 1.69), ('2 x CONTACT NO', 0.224), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A 30mA', 0.835), ('BLOC VIGI 30mA', 1.03), ('CONTACT AUXILIAIRE iOF', 0.364), ('PRISE DE COURANT PC 10-16A - 220V - 2P+T', 0.654), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x02A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x02A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('INTERRUPTEUR DIFFERENTIEL ilD - 4x25A 300mA', 3.19),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x4A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('BOUTON POUSSOIR CAPUCHONNES BLEU', 0.598), ('3 x RELAIS INSTANTANE + EMBASE', 2.25), ('2 x COFFRET PLS - IP65 - IK09 - 360x270x180', 27), ('COUVERCLE HAUT CAPOT TRANSPARENT - IP65 - IK09 - 360x270x95', 13.5), ('JEU DE QUATRE VIS A AILETTE POUR BOITE PLS', 13.5), ('PLATINE - 360x270', 13.5), ('ALIMENTATION AUTOMATE 240VAC/24VDC', 6.3), ('RACK 4 POSITIONS - STANDARD', 10.3), ('ALIMENTATION AUTOMATE 100...240VAC/24VDC', 6.3), ('PROCESSEUR M340', 17.4), ('2 x CARTE ETHERNET', 34.8), ('Cassete Rail DIN 12 connecteurs SC APC', 6.24), ('DISJONCTEUR Differentiel 30 Ma COURBE C 2P 10A réseau SEMAN', 1.6), 
        ('DISJONCTEUR Differentiel 30 Ma COURBE C 2P 10A réseau SETRA',1.6), ('2 x Cassete Rail DIN 12 connecteurs SC APC', 12.5)]
        Distribution1= [('ARMOIRE MONOBLOC SPATIAL', 215), ('POIGNÉE SM POUR INSERT + ADAPTATEUR POIGNÉE POUR SERRURE DIN', 242), ('2 x JOINT BALAI', 430), ('ANNEAUX DE LEVAGE', 215), ('SOCLE HAUTEUR 200mm', 215), ('2 x ARRET DE PORTE MECANIQUE', 430), ('AUVENT', 215), ('TABLETTE', 215), ('PORTE PLAN', 215), ('KIT DE VENTILATION GRILLE', 0.0244), ('CONTACT DE PORTE', 0.00000000661), ('ECLAIRAGE LAMPE LED COMPACTE 11W - AIMANTEE', 0.208), ('RESISTANCE CHAUFFANTE 147W - 230V', 1.19), ('THERMOSTAT O - REGLABLE 0..60C - POUR COMMANDER UNE RESISTANCE CHAUFFANTE', 0.143), ('THERMOSTAT O - REGLABLE 0..60C - POUR COMMANDER UN VENTILATEUR', 0.143), ('INTERRUPTEUR DIFFERENTIEL ilD - 4x25A 300mA', 0.0811), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('BOUTON COUP DE POING ROUGE - TOURNER POUR DEVEROUILLER + GARDE POUR COUP DE POING', 0.0206), ('2 x CONTACT NO', 0.0047), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A 30mA', 0.0156), ('BLOC VIGI 30mA', 0.032), ('CONTACT AUXILIAIRE iOF', 0.00594), ('PRISE DE COURANT PC 10-16A - 220V - 2P+T', 0.0129), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x02A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x02A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('INTERRUPTEUR DIFFERENTIEL ilD - 4x25A 300mA', 0.0811), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x4A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('BOUTON POUSSOIR CAPUCHONNES BLEU', 0.011), ('3 x RELAIS INSTANTANE + EMBASE', 0.135), ('2 x COFFRET PLS - IP65 - IK09 - 360x270x180', 9.14), ('COUVERCLE HAUT CAPOT TRANSPARENT - IP65 - IK09 - 360x270x95', 4.57), ('JEU DE QUATRE VIS A AILETTE POUR BOITE PLS', 4.57), ('PLATINE - 360x270', 4.57), ('ALIMENTATION AUTOMATE 240VAC/24VDC', 0.0641), ('RACK 4 POSITIONS - STANDARD', 0.139), ('ALIMENTATION AUTOMATE 100...240VAC/24VDC', 0.0641), ('PROCESSEUR M340', 0.0335), ('2 x CARTE ETHERNET', 0.067), ('Cassete Rail DIN 12 connecteurs SC APC', 0), 
        ('DISJONCTEUR Differentiel 30 Ma COURBE C 2P 10A réseau SEMAN', 0.0322), ('DISJONCTEUR Differentiel 30 Ma COURBE C 2P 10A réseau SETRA',0.0322), ('2 x Cassete Rail DIN 12 connecteurs SC APC', 0)]
        Installation1 = [('ARMOIRE MONOBLOC SPATIAL', 15.4), ('POIGNÉE SM POUR INSERT + ADAPTATEUR POIGNÉE POUR SERRURE DIN', 53.1), ('2 x JOINT BALAI', 30.8), ('ANNEAUX DE LEVAGE', 15.4), ('SOCLE HAUTEUR 200mm', 15.4), ('2 x ARRET DE PORTE MECANIQUE', 30.8), ('AUVENT', 15.4), ('TABLETTE', 15.4), ('PORTE PLAN', 15.4), ('KIT DE VENTILATION GRILLE', 0.00283), ('CONTACT DE PORTE', 0), ('ECLAIRAGE LAMPE LED COMPACTE 11W - AIMANTEE', 0), ('RESISTANCE CHAUFFANTE 147W - 230V', 0), ('THERMOSTAT O - REGLABLE 0..60C - POUR COMMANDER UNE RESISTANCE CHAUFFANTE', 0), ('THERMOSTAT O - REGLABLE 0..60C - POUR COMMANDER UN VENTILATEUR', 0), ('INTERRUPTEUR DIFFERENTIEL ilD - 4x25A 300mA', 0.036), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('BOUTON COUP DE POING ROUGE - TOURNER POUR DEVEROUILLER + GARDE POUR COUP DE POING', 0.000691), ('2 x CONTACT NO', 0.0254), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A 30mA', 0.0104), ('BLOC VIGI 30mA', 0.0327), ('CONTACT AUXILIAIRE iOF', 0.000788), ('PRISE DE COURANT PC 10-16A - 220V - 2P+T', 0), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x02A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x02A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('INTERRUPTEUR DIFFERENTIEL ilD - 4x25A 300mA', 0.036), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x4A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('BOUTON POUSSOIR CAPUCHONNES BLEU', 0.0169), ('3 x RELAIS INSTANTANE + EMBASE', 0.000969), ('2 x COFFRET PLS - IP65 - IK09 - 360x270x180', 0.6), ('COUVERCLE HAUT CAPOT TRANSPARENT - IP65 - IK09 - 360x270x95', 0.3), ('JEU DE QUATRE VIS A AILETTE POUR BOITE PLS', 0.3), ('PLATINE - 360x270', 0.3), ('ALIMENTATION AUTOMATE 240VAC/24VDC', 0.238), ('RACK 4 POSITIONS - STANDARD', 0), ('ALIMENTATION AUTOMATE 100...240VAC/24VDC', 0.238), ('PROCESSEUR M340', 0.102), ('2 x CARTE ETHERNET', 0.204), ("Cassete Rail DIN 12 connecteurs SC APC", 0),
        ('DISJONCTEUR Differentiel 30 Ma COURBE C 2P 10A réseau SEMAN', 0.0654), ('DISJONCTEUR Differentiel 30 Ma COURBE C 2P 10A réseau SETRA',0.0654), ('2 x Cassete Rail DIN 12 connecteurs SC APC', 0)]
        Utilisation1=[('ARMOIRE MONOBLOC SPATIAL', 0), ('POIGNÉE SM POUR INSERT + ADAPTATEUR POIGNÉE POUR SERRURE DIN', 0), ('2 x JOINT BALAI', 0), ('ANNEAUX DE LEVAGE', 0), ('SOCLE HAUTEUR 200mm', 0), ('2 x ARRET DE PORTE MECANIQUE', 0), ('AUVENT', 0), ('TABLETTE', 0), ('PORTE PLAN', 0), ('KIT DE VENTILATION GRILLE', 0), ('CONTACT DE PORTE', 0), ('ECLAIRAGE LAMPE LED COMPACTE 11W - AIMANTEE', 207), ('RESISTANCE CHAUFFANTE 147W - 230V', 262), ('THERMOSTAT O - REGLABLE 0..60C - POUR COMMANDER UNE RESISTANCE CHAUFFANTE', 259), ('THERMOSTAT O - REGLABLE 0..60C - POUR COMMANDER UN VENTILATEUR', 259), ('INTERRUPTEUR DIFFERENTIEL ilD - 4x25A 300mA', 56.5), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('BOUTON COUP DE POING ROUGE - TOURNER POUR DEVEROUILLER + GARDE POUR COUP DE POING', 0), ('2 x CONTACT NO', 0.0558), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A 30mA', 12.9), ('BLOC VIGI 30mA', 2.41), ('CONTACT AUXILIAIRE iOF', 0.27), ('PRISE DE COURANT PC 10-16A - 220V - 2P+T', 25.8), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x02A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x02A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('INTERRUPTEUR DIFFERENTIEL ilD - 4x25A 300mA', 56.5), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x4A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('BOUTON POUSSOIR CAPUCHONNES BLEU', 0.0618), ('3 x RELAIS INSTANTANE + EMBASE', 0), ('2 x COFFRET PLS - IP65 - IK09 - 360x270x180', 0), ('COUVERCLE HAUT CAPOT TRANSPARENT - IP65 - IK09 - 360x270x95', 0), ('JEU DE QUATRE VIS A AILETTE POUR BOITE PLS', 0), ('PLATINE - 360x270', 0), ('ALIMENTATION AUTOMATE 240VAC/24VDC', 451), ('RACK 4 POSITIONS - STANDARD', 333), ('ALIMENTATION AUTOMATE 100...240VAC/24VDC', 451), ('PROCESSEUR M340', 184), ('2 x CARTE ETHERNET', 368), ('Cassete Rail DIN 12 connecteurs SC APC', 0), ('DISJONCTEUR Differentiel 30 Ma COURBE C 2P 10A réseau SEMAN', 23.2), ('DISJONCTEUR Differentiel 30 Ma COURBE C 2P 10A réseau SETRA', 23.2), ('2 x Cassete Rail DIN 12 connecteurs SC APC', 0)]
        Fin1=[('ARMOIRE MONOBLOC SPATIAL', 267), ('POIGNÉE SM POUR INSERT + ADAPTATEUR POIGNÉE POUR SERRURE DIN', 586), ('2 x JOINT BALAI', 534), ('ANNEAUX DE LEVAGE', 267), ('SOCLE HAUTEUR 200mm', 267), ('2 x ARRET DE PORTE MECANIQUE', 534), ('AUVENT', 267), ('TABLETTE', 267), ('PORTE PLAN', 267),('KIT DE VENTILATION GRILLE', 0.0316), ('CONTACT DE PORTE', 0), ('ECLAIRAGE LAMPE LED COMPACTE 11W - AIMANTEE', 1.02), ('RESISTANCE CHAUFFANTE 147W - 230V', 0.0501), ('THERMOSTAT O - REGLABLE 0..60C - POUR COMMANDER UNE RESISTANCE CHAUFFANTE', 0), ('THERMOSTAT O - REGLABLE 0..60C - POUR COMMANDER UN VENTILATEUR', 0), ('INTERRUPTEUR DIFFERENTIEL ilD - 4x25A 300mA', 0.936), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('BOUTON COUP DE POING ROUGE - TOURNER POUR DEVEROUILLER + GARDE POUR COUP DE POING', 0.0186), ('2 x CONTACT NO', 0.0654), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A 30mA', 0.328), ('BLOC VIGI 30mA', 0.3), ('CONTACT AUXILIAIRE iOF', 0.0066), ('PRISE DE COURANT PC 10-16A - 220V - 2P+T', 0.0213), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x02A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x02A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('INTERRUPTEUR DIFFERENTIEL ilD - 4x25A 300mA', 0.936),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x4A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('BOUTON POUSSOIR CAPUCHONNES BLEU', 0.209), ('3 x RELAIS INSTANTANE + EMBASE', 0.447), ('2 x COFFRET PLS - IP65 - IK09 - 360x270x180', 9.88), ('COUVERCLE HAUT CAPOT TRANSPARENT - IP65 - IK09 - 360x270x95', 4.94), ('JEU DE QUATRE VIS A AILETTE POUR BOITE PLS', 4.94), ('PLATINE - 360x270', 4.94), ('ALIMENTATION AUTOMATE 240VAC/24VDC', 0.684), ('RACK 4 POSITIONS - STANDARD', 0.393), ('ALIMENTATION AUTOMATE 100...240VAC/24VDC', 0.684), ('PROCESSEUR M340', 0.412), ('2 x CARTE ETHERNET', 0.824), ('Cassete Rail DIN 12 connecteurs SC APC', 0), ('DISJONCTEUR Differentiel 30 Ma COURBE C 2P 10A réseau SEMAN', 0.544), 
        ('DISJONCTEUR Differentiel 30 Ma COURBE C 2P 10A réseau SETRA', 0.544), ('2 x Cassete Rail DIN 12 connecteurs SC APC', 0)]
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
        GWP6 = round(abs(total1), 2)
        st.session_state.GWP6 = GWP6
        if st.button("Afficher le GWP de l'Armoire Maitre"):
            st.metric(label=f"Total GWP de l'armoire API 725-7", value=f"{GWP6} kg CO₂")
        if st.button("Ajouter à la liste"):
            st.session_state.total_liste.append({'Armoire Maitre' : GWP6})
            d = {
                '': 'Armoire Maitre',
                'Fabrication': [fab],
                'Distribution': [dis],
                'Installation': [ins],
                'Utilisation': [use],
                'Fin de vie': [fin],
                'Global warming': [GWP6]
                }
            df1 = pd.DataFrame(d)
            st.session_state.df = pd.concat([st.session_state.df, df1], ignore_index=True)
            st.dataframe(st.session_state.df)
            st.info("Ajouté à la liste !")
        detail_button_container = st.empty()
        detail_button_container2 = st.empty()
        if detail_button_container.button("Voir le détail", key="detail_button_418"):
            st.session_state.df_co = pd.DataFrame()
            t=0
            for i, row in st.session_state.df.iterrows():
                if row[''] == 'Armoire Maitre':
                    t += 1
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
            df1 = pd.DataFrame(details)
            st.session_state.df_co = pd.concat([st.session_state.df_co, df1], ignore_index=True)
            st.dataframe(st.session_state.df_co)
            detail_button_container.empty()
            if detail_button_container.button("Voir moins", key="detail_button_419"):
                if not st.session_state.df.empty:
                    st.dataframe(st.session_state.df)
                    detail_button_container.empty()

    elif page=='Armoire Esclave':
        st.markdown(
            "<h1 style='color: #BE162F;'>Bilan carbone de votre ARMOIRE TYPE CDGR - API ESCLAVE - DALI LED </h1>",
            unsafe_allow_html=True
            )
        Fabrication1= [('ARMOIRE MONOBLOC SPATIAL', 471), ('POIGNÉE SM POUR INSERT + ADAPTATEUR POIGNÉE POUR SERRURE DIN', 833), ('2 x JOINT BALAI', 942), ('ANNEAUX DE LEVAGE', 471), ('SOCLE HAUTEUR 200mm', 471), ('2 x ARRET DE PORTE MECANIQUE', 942), ('AUVENT', 471), ('TABLETTE', 471), ('PORTE PLAN', 471), ('KIT DE VENTILATION GRILLE', 0.916), ('CONTACT DE PORTE', .0000511), ('ECLAIRAGE LAMPE LED COMPACTE 11W - AIMANTEE', 13.3), ('RESISTANCE CHAUFFANTE 147W - 230V', 105), ('THERMOSTAT O - REGLABLE 0..60C - POUR COMMANDER UNE RESISTANCE CHAUFFANTE', 101), ('THERMOSTAT O - REGLABLE 0..60C - POUR COMMANDER UN VENTILATEUR', 101), ('INTERRUPTEUR DIFFERENTIEL ilD - 4x25A 300mA', 3.19), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('BOUTON COUP DE POING ROUGE - TOURNER POUR DEVEROUILLER + GARDE POUR COUP DE POING', 1.69), ('2 x CONTACT NO', 0.224), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A 30mA', 0.835), ('BLOC VIGI 30mA', 1.03), ('CONTACT AUXILIAIRE iOF', 0.364), ('PRISE DE COURANT PC 10-16A - 220V - 2P+T', 0.654), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x02A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x02A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('INTERRUPTEUR DIFFERENTIEL ilD - 4x25A 300mA', 3.19), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x4A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.835), ('CONTACT AUXILIAIRE iOF', 0.364), ('BOUTON POUSSOIR CAPUCHONNES BLEU', 0.598), ('3 x RELAIS INSTANTANE + EMBASE', 2.25), ('2 x COFFRET PLS - IP65 - IK09 - 360x270x180', 27), ('COUVERCLE HAUT CAPOT TRANSPARENT - IP65 - IK09 - 360x270x95', 13.5), ('JEU DE QUATRE VIS A AILETTE POUR BOITE PLS', 13.5), ('PLATINE - 360x270', 13.5), ('ALIMENTATION AUTOMATE 240VAC/24VDC', 6.3),('DISJONCTEUR Differentiel 30 Ma COURBE C 2P 10A réseau SEMAN', 1.6), 
        ('DISJONCTEUR Differentiel 30 Ma COURBE C 2P 10A réseau SETRA',1.6), ('2 x Cassete Rail DIN 12 connecteurs SC APC', 12.5)]
        Distribution1= [('ARMOIRE MONOBLOC SPATIAL', 215), ('POIGNÉE SM POUR INSERT + ADAPTATEUR POIGNÉE POUR SERRURE DIN', 242), ('2 x JOINT BALAI', 430), ('ANNEAUX DE LEVAGE', 215), ('SOCLE HAUTEUR 200mm', 215), ('2 x ARRET DE PORTE MECANIQUE', 430), ('AUVENT', 215), ('TABLETTE', 215), ('PORTE PLAN', 215), ('KIT DE VENTILATION GRILLE', 0.0244), ('CONTACT DE PORTE', 0.00000000661), ('ECLAIRAGE LAMPE LED COMPACTE 11W - AIMANTEE', 0.208), ('RESISTANCE CHAUFFANTE 147W - 230V', 1.19), ('THERMOSTAT O - REGLABLE 0..60C - POUR COMMANDER UNE RESISTANCE CHAUFFANTE', 0.143), ('THERMOSTAT O - REGLABLE 0..60C - POUR COMMANDER UN VENTILATEUR', 0.143), ('INTERRUPTEUR DIFFERENTIEL ilD - 4x25A 300mA', 0.0811), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('BOUTON COUP DE POING ROUGE - TOURNER POUR DEVEROUILLER + GARDE POUR COUP DE POING', 0.0206), ('2 x CONTACT NO', 0.0047), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A 30mA', 0.0156), ('BLOC VIGI 30mA', 0.032), ('CONTACT AUXILIAIRE iOF', 0.00594), ('PRISE DE COURANT PC 10-16A - 220V - 2P+T', 0.0129), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x02A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x02A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('INTERRUPTEUR DIFFERENTIEL ilD - 4x25A 300mA', 0.0811), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x4A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.0156), ('CONTACT AUXILIAIRE iOF', 0.00594), ('BOUTON POUSSOIR CAPUCHONNES BLEU', 0.011), ('3 x RELAIS INSTANTANE + EMBASE', 0.135), ('2 x COFFRET PLS - IP65 - IK09 - 360x270x180', 9.14), ('COUVERCLE HAUT CAPOT TRANSPARENT - IP65 - IK09 - 360x270x95', 4.57), ('JEU DE QUATRE VIS A AILETTE POUR BOITE PLS', 4.57), ('PLATINE - 360x270', 4.57), ('ALIMENTATION AUTOMATE 240VAC/24VDC', 0.0641), 
        ('DISJONCTEUR Differentiel 30 Ma COURBE C 2P 10A réseau SEMAN', 0.0322), ('DISJONCTEUR Differentiel 30 Ma COURBE C 2P 10A réseau SETRA',0.0322), ('2 x Cassete Rail DIN 12 connecteurs SC APC', 0)]
        Installation1 = [('ARMOIRE MONOBLOC SPATIAL', 15.4), ('POIGNÉE SM POUR INSERT + ADAPTATEUR POIGNÉE POUR SERRURE DIN', 53.1), ('2 x JOINT BALAI', 30.8), ('ANNEAUX DE LEVAGE', 15.4), ('SOCLE HAUTEUR 200mm', 15.4), ('2 x ARRET DE PORTE MECANIQUE', 30.8), ('AUVENT', 15.4), ('TABLETTE', 15.4), ('PORTE PLAN', 15.4), ('KIT DE VENTILATION GRILLE', 0.00283), ('CONTACT DE PORTE', 0), ('ECLAIRAGE LAMPE LED COMPACTE 11W - AIMANTEE', 0), ('RESISTANCE CHAUFFANTE 147W - 230V', 0), ('THERMOSTAT O - REGLABLE 0..60C - POUR COMMANDER UNE RESISTANCE CHAUFFANTE', 0), ('THERMOSTAT O - REGLABLE 0..60C - POUR COMMANDER UN VENTILATEUR', 0), ('INTERRUPTEUR DIFFERENTIEL ilD - 4x25A 300mA', 0.036), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('BOUTON COUP DE POING ROUGE - TOURNER POUR DEVEROUILLER + GARDE POUR COUP DE POING', 0.000691), ('2 x CONTACT NO', 0.0254), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A 30mA', 0.0104), ('BLOC VIGI 30mA', 0.0327), ('CONTACT AUXILIAIRE iOF', 0.000788), ('PRISE DE COURANT PC 10-16A - 220V - 2P+T', 0), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x02A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x02A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('INTERRUPTEUR DIFFERENTIEL ilD - 4x25A 300mA', 0.036),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x4A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.0104), ('CONTACT AUXILIAIRE iOF', 0.000788), ('BOUTON POUSSOIR CAPUCHONNES BLEU', 0.0169), ('3 x RELAIS INSTANTANE + EMBASE', 0.000969), ('2 x COFFRET PLS - IP65 - IK09 - 360x270x180', 0.6), ('COUVERCLE HAUT CAPOT TRANSPARENT - IP65 - IK09 - 360x270x95', 0.3), ('JEU DE QUATRE VIS A AILETTE POUR BOITE PLS', 0.3), ('PLATINE - 360x270', 0.3), ('ALIMENTATION AUTOMATE 240VAC/24VDC', 0.238),
        ('DISJONCTEUR Differentiel 30 Ma COURBE C 2P 10A réseau SEMAN', 0.0654), ('DISJONCTEUR Differentiel 30 Ma COURBE C 2P 10A réseau SETRA',0.0654), ('2 x Cassete Rail DIN 12 connecteurs SC APC', 0)]
        Utilisation1=[('ARMOIRE MONOBLOC SPATIAL', 0), ('POIGNÉE SM POUR INSERT + ADAPTATEUR POIGNÉE POUR SERRURE DIN', 0), ('2 x JOINT BALAI', 0), ('ANNEAUX DE LEVAGE', 0), ('SOCLE HAUTEUR 200mm', 0), ('2 x ARRET DE PORTE MECANIQUE', 0), ('AUVENT', 0), ('TABLETTE', 0), ('PORTE PLAN', 0), ('KIT DE VENTILATION GRILLE', 0), ('CONTACT DE PORTE', 0), ('ECLAIRAGE LAMPE LED COMPACTE 11W - AIMANTEE', 207), ('RESISTANCE CHAUFFANTE 147W - 230V', 262), ('THERMOSTAT O - REGLABLE 0..60C - POUR COMMANDER UNE RESISTANCE CHAUFFANTE', 259), ('THERMOSTAT O - REGLABLE 0..60C - POUR COMMANDER UN VENTILATEUR', 259), ('INTERRUPTEUR DIFFERENTIEL ilD - 4x25A 300mA', 56.5), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('BOUTON COUP DE POING ROUGE - TOURNER POUR DEVEROUILLER + GARDE POUR COUP DE POING', 0), ('2 x CONTACT NO', 0.0558), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A 30mA', 12.9), ('BLOC VIGI 30mA', 2.41), ('CONTACT AUXILIAIRE iOF', 0.27), ('PRISE DE COURANT PC 10-16A - 220V - 2P+T', 25.8), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x02A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x02A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('INTERRUPTEUR DIFFERENTIEL ilD - 4x25A 300mA', 56.5), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x4A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27),('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 12.9), ('CONTACT AUXILIAIRE iOF', 0.27), ('BOUTON POUSSOIR CAPUCHONNES BLEU', 0.0618), ('3 x RELAIS INSTANTANE + EMBASE', 0), ('2 x COFFRET PLS - IP65 - IK09 - 360x270x180', 0), ('COUVERCLE HAUT CAPOT TRANSPARENT - IP65 - IK09 - 360x270x95', 0), ('JEU DE QUATRE VIS A AILETTE POUR BOITE PLS', 0), ('PLATINE - 360x270', 0), ('ALIMENTATION AUTOMATE 240VAC/24VDC', 451),('DISJONCTEUR Differentiel 30 Ma COURBE C 2P 10A réseau SEMAN', 23.2), ('DISJONCTEUR Differentiel 30 Ma COURBE C 2P 10A réseau SETRA', 23.2), ('2 x Cassete Rail DIN 12 connecteurs SC APC', 0)]
        Fin1=[('ARMOIRE MONOBLOC SPATIAL', 267), ('POIGNÉE SM POUR INSERT + ADAPTATEUR POIGNÉE POUR SERRURE DIN', 586), ('2 x JOINT BALAI', 534), ('ANNEAUX DE LEVAGE', 267), ('SOCLE HAUTEUR 200mm', 267), ('2 x ARRET DE PORTE MECANIQUE', 534), ('AUVENT', 267), ('TABLETTE', 267), ('PORTE PLAN', 267),('KIT DE VENTILATION GRILLE', 0.0316), ('CONTACT DE PORTE', 0), ('ECLAIRAGE LAMPE LED COMPACTE 11W - AIMANTEE', 1.02), ('RESISTANCE CHAUFFANTE 147W - 230V', 0.0501), ('THERMOSTAT O - REGLABLE 0..60C - POUR COMMANDER UNE RESISTANCE CHAUFFANTE', 0), ('THERMOSTAT O - REGLABLE 0..60C - POUR COMMANDER UN VENTILATEUR', 0), ('INTERRUPTEUR DIFFERENTIEL ilD - 4x25A 300mA', 0.936), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('BOUTON COUP DE POING ROUGE - TOURNER POUR DEVEROUILLER + GARDE POUR COUP DE POING', 0.0186), ('2 x CONTACT NO', 0.0654), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A 30mA', 0.328), ('BLOC VIGI 30mA', 0.3), ('CONTACT AUXILIAIRE iOF', 0.0066), ('PRISE DE COURANT PC 10-16A - 220V - 2P+T', 0.0213), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x02A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x02A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('INTERRUPTEUR DIFFERENTIEL ilD - 4x25A 300mA', 0.936), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x4A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x10A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x2A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('DISJONCTEUR IC60N - Courbe C - 2p 2d -  2x16A ', 0.328), ('CONTACT AUXILIAIRE iOF', 0.0066), ('BOUTON POUSSOIR CAPUCHONNES BLEU', 0.209), ('3 x RELAIS INSTANTANE + EMBASE', 0.447), ('2 x COFFRET PLS - IP65 - IK09 - 360x270x180', 9.88), ('COUVERCLE HAUT CAPOT TRANSPARENT - IP65 - IK09 - 360x270x95', 4.94), ('JEU DE QUATRE VIS A AILETTE POUR BOITE PLS', 4.94), ('PLATINE - 360x270', 4.94), ('ALIMENTATION AUTOMATE 240VAC/24VDC', 0.684),('DISJONCTEUR Differentiel 30 Ma COURBE C 2P 10A réseau SEMAN', 0.544), 
        ('DISJONCTEUR Differentiel 30 Ma COURBE C 2P 10A réseau SETRA', 0.544), ('2 x Cassete Rail DIN 12 connecteurs SC APC', 0)]
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
        GWP6 = round(abs(total1), 2)
        st.session_state.GWP6 = GWP6
        if st.button("Afficher le GWP de l'Armoire Esclave"):
            st.metric(label=f"Total GWP de l'armoire API 725-7", value=f"{GWP6} kg CO₂")
        if st.button("Ajouter à la liste"):
            st.session_state.total_liste.append({'Armoire Esclave' : GWP6})
            d = {
                '': 'Armoire Esclave',
                'Fabrication': [fab],
                'Distribution': [dis],
                'Installation': [ins],
                'Utilisation': [use],
                'Fin de vie': [fin],
                'Global warming': [GWP6]
                }
            df1 = pd.DataFrame(d)
            st.session_state.df = pd.concat([st.session_state.df, df1], ignore_index=True)
            st.dataframe(st.session_state.df)
            st.info("Ajouté à la liste !")
        detail_button_container = st.empty()
        detail_button_container2 = st.empty()
        if detail_button_container.button("Voir le détail", key="detail_button_418"):
            st.session_state.df_co = pd.DataFrame()
            t=0
            for i, row in st.session_state.df.iterrows():
                if row[''] == 'Armoire Esclave':
                    t += 1
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
            df1 = pd.DataFrame(details)
            st.session_state.df_co = pd.concat([st.session_state.df_co, df1], ignore_index=True)
            st.dataframe(st.session_state.df_co)
            detail_button_container.empty()
            if detail_button_container.button("Voir moins", key="detail_button_419"):
                if not st.session_state.df.empty:
                    st.dataframe(st.session_state.df)
                    detail_button_container.empty()

    elif page=='Onduleur':
        st.markdown(
            "<h1 style='color: #BE162F;'>Bilan carbone de votre onduleur </h1>",
            unsafe_allow_html=True
            )
        Fabrication1= [('2 x TRIMOD HAUTE EFFICAICTÉ', 2280)]
        Distribution1= [('2 x TRIMOD HAUTE EFFICAICTÉ', 16.6)]
        Installation1=[('2 x TRIMOD HAUTE EFFICAICTÉ', 6.14)]
        Utilisation1=[('2 x TRIMOD HAUTE EFFICAICTÉ', 27200)]
        Fin1=[('2 x TRIMOD HAUTE EFFICAICTÉ', 446)]
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
        GWP6 = round(abs(total1), 2)
        st.session_state.GWP6 = GWP6
        if st.button("Afficher le GWP de l'onduleur"):
            st.metric(label=f"Total GWP de l'armoire API 725-7", value=f"{GWP6} kg CO₂")
        if st.button("Ajouter à la liste"):
            st.session_state.total_liste.append({'Onduleur' : GWP6})
            d = {
                '': 'Onduleur',
                'Fabrication': [fab],
                'Distribution': [dis],
                'Installation': [ins],
                'Utilisation': [use],
                'Fin de vie': [fin],
                'Global warming': [GWP6]
                }
            df1 = pd.DataFrame(d)
            st.session_state.df = pd.concat([st.session_state.df, df1], ignore_index=True)
            st.dataframe(st.session_state.df)
            st.info("Ajouté à la liste !")
        detail_button_container = st.empty()
        detail_button_container2 = st.empty()
        if detail_button_container.button("Voir le détail", key="detail_button_418"):
            st.session_state.df_co = pd.DataFrame()
            t=0
            for i, row in st.session_state.df.iterrows():
                if row[''] == 'Onduleur':
                    t += 1
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
            df1 = pd.DataFrame(details)
            st.session_state.df_co = pd.concat([st.session_state.df_co, df1], ignore_index=True)
            st.dataframe(st.session_state.df_co)
            detail_button_container.empty()
            if detail_button_container.button("Voir moins", key="detail_button_419"):
                if not st.session_state.df.empty:
                    st.dataframe(st.session_state.df)
                    detail_button_container.empty()
                    
    elif page == 'Gaine à barre':

        st.markdown(
            "<h1 style='color: #BE162F;'>Bilan carbone de votre gaine à barre</h1>",
            unsafe_allow_html=True
            )


        st.markdown(
            "<span style='color: #084288; font-size: 18px;'>Choisissez la section de la gaine à barre :</span>",
            unsafe_allow_html=True
            )  
        
        section1 = st.selectbox("", (800, 1000, 1250, 1600, 2000, 2500, 3200, 4000, 5000), key="section1")

        section1 = int(section1)
        Fabrication = {800: 4740, 1000: 5920, 1250: 7400, 1600: 9470, 2000: 11800, 2500: 14800, 3200: 18900, 4000: 23700, 5000: 29600}.get(section1, 0)
        Distribution = {800: 177, 1000: 222, 1250: 277, 1600: 355, 2000: 443, 2500: 554, 3200: 709, 4000: 886, 5000: 1110}.get(section1, 0)
        Installation = {800: 36.2, 1000: 45.2, 1250: 56.5, 1600: 72.3, 2000: 90.4, 2500: 113, 3200: 145, 4000: 181, 5000: 226}.get(section1, 0)
        Utilisation = {800: 66900, 1000: 83600, 1250: 105000, 1600: 134000, 2000: 167000, 2500: 209000, 3200: 268000, 4000: 334000, 5000: 418000}.get(section1, 0)
        Fin = {800: 91.2, 1000: 114, 1250: 143, 1600: 182, 2000: 228, 2500: 285, 3200: 365, 4000: 456, 5000: 570}.get(section1, 0)


        total = Fabrication + Distribution + Installation + Utilisation + Fin
        GWP3 = round(abs(total), 2)
        st.session_state.GWP3 = GWP3


        if st.button("Valider"):
            st.metric(label="Total GWP de la gaine à barre sélectionnée", value=f"{GWP3} kg CO₂")

        if st.button("Ajouter à la liste"):
            st.session_state.total_liste.append({f'Gaine à barre {section1}' : GWP3})
            d = {
                '': [f'Gaine à barre {section1}'],
                'Fabrication': [Fabrication],
                'Distribution': [Distribution],
                'Installation': [Installation],
                'Utilisation': [Utilisation],
                'Fin de vie': [Fin],
                'Global warming': [GWP3]
            }
            df1 = pd.DataFrame(d)
            st.session_state.df = pd.concat([st.session_state.df, df1], ignore_index=True)
            st.info("Ajouté à la liste !")


        if not st.session_state.df.empty:
            st.dataframe(st.session_state.df)
                    
elif selected_menu == 'Total GWP':
    total_liste = st.session_state.total_liste
    total=0
    if total_liste: 
        for x in total_liste:
            for s in x.keys():
                total += x[s]
                total= round(total,2)
        
        st.markdown(f"""
            <div style="text-align: center;">
                <div class="georgia-text">
                <h2 style="color: #084288;">Total GWP</h2>
                <p style="font-size: 28px; color : #BE162F;">{total} kg CO₂</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("Voir les éléments détaillés"):
                    for x in total_liste:
                        for s in x.keys():
                            st.write(f"• {s} : {x[s]} kg CO₂")
        with st.expander("Voir le tableau détaillé"):
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
