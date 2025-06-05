import streamlit as st
from openpyxl import load_workbook

st.header('Estimez le matériau le plus éco-responsable pour votre projet')

section1 = st.selectbox("Choisissez la section pour l'aluminium :", (50, 120, 150, 185))
distance1 = st.text_input("Distance pour l'aluminium :", value="1")
section2 = st.selectbox("Choisissez la section pour le cuivre :", (50, 120, 150, 185))
distance2 = st.text_input("Distance pour le cuivre :", value="1")

if st.button("Valider"):
    # Conversion
    section1 = int(section1)
    distance1 = int(distance1)
    section2 = int(section2)
    distance2 = int(distance2)

    # Poids
    poids1 = {50: 225, 120: 470, 150: 590, 185: 713}.get(section1, 0)
    poids2 = {50: 493, 120: 1178, 150: 1428, 185: 1786}.get(section2, 0)

    # Masse
    masse_totale1 = poids1 * distance1
    masse_totale2 = poids2 * distance2

    # Coefficients B et C
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
    total2 = fab2 + distrib2 + installation2 + fdv2

    if total1 > total2:
        materiau = 'le cuivre'
    else:
        materiau = "l'aluminium"

    GWP1 = round(total1, 2)
    GWP2 = round(total2, 2)

    st.success(f"Le matériau à utiliser est **{materiau}**")
    st.metric(label="Total GWP de l'aluminium", value=f"{GWP1} kg CO₂")
    st.metric(label="Total GWP du cuivre", value=f"{GWP2} kg CO₂")
