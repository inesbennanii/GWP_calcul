import streamlit as st
import pandas as pd
from openpyxl import load_workbook
from PIL import Image

st.header('Estimez le matériau le plus éco-responsable pour votre projet')
st.subheader('Un logiciel conçu pour faciliter ..')


section1 = st.selectbox(
    "Choisissez la section pour l'aluminium :",
    (50, 120, 150, 185),
    placeholder="Selectionnez une section"
)

distance1 = st.text_input(
        "Distance pour l'aluminium :", value="1"
)

section2 = st.selectbox(
    "Choisissez la section pour le cuivre:",
    (50, 120, 150, 185),
    placeholder="Selectionnez une section"
)

distance2 = st.text_input(
        "Distance pour le cuivre :", value="1"
)



if st.button("Valider"):
    if section1 == 50:
        poids1 = 225
    elif section1 == 120:
        poids1 = 470
    elif section1 == 150:
        poids1 = 590
    else:
        poids1 = 713

    if section2 == 50:
        poids2 = 493
    elif section2 == 120:
        poids2 = 1178
    elif section2 == 150:
        poids2 = 1428
    else:
        poids2 = 1786


    masse_totale1 = int(poids1) * int(distance1)
    masse_totale2 = int(poids2) * int(distance2)


    if masse_totale1 > 425.5:
        B39 = 4.1
        C39 = 24.3
    else:
        B39 = 4.97
        C39 = -49.4

    wb = load_workbook("Calcul_GWP.xlsx", data_only=True)
    ws = wb.active

    B40 = ws["B40"].value
    C40 = ws["C40"].value
    B41 = ws["B41"].value
    C41 = ws["C41"].value
    B42 = ws["B42"].value
    C42 = ws["C42"].value


    fab1 = float(B39) * float(masse_totale1) + float(C39)
    distrib1 = float(B40) * float(masse_totale1) + float(C40)
    installation1 = float(B41) * float(masse_totale1) + float(C41)
    fdv1 = float(B42) * float(masse_totale1) + float(C42)
    total1 = fab1 + distrib1 + installation1 + fdv1


    if masse_totale2 > 2049.5:
        H39 = 2.28
        I39 = -289
    else:
        H39 = 2.15
        I39 = 17.4

    H40 = ws["H40"].value
    I40 = ws["I40"].value
    H41 = ws["H41"].value
    I41 = ws["I41"].value
    H42 = ws["H42"].value
    I42 = ws["I42"].value


    fab2 = float(H39) * float(masse_totale2) + float(I39)
    distrib2 = float(H40) * float(masse_totale2) + float(I40)
    installation2 = float(H41) * float(masse_totale2) + float(I41)
    fdv2 = float(H42) * float(masse_totale2) + float(I42)
    total2 = fab2 + distrib2 + installation2 + fdv2

    
    if total1>total2:
        materiau= 'le cuivre'
    else:
        materiau= "l'aluminium"

    GWP1 = round(total1, 2)
    GWP2 = round(total2, 2)

    st.success(f"Le matériau à utiliser est **{materiau}**")
    st.metric(label="Total GWP de l'aluminium", value=f"{GWP1} kg CO₂")
    st.metric(label="Total GWP du cuivre", value=f"{GWP2} kg CO₂")
    st.metric(label="Total GWP de l'aluminium", value=f"{B39} kg CO₂")
    st.metric(label="Total GWP du cuivre", value=f"{C39} kg CO₂")

