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
    fichier = load_workbook("Calcul_GWP.xlsx")
    fichier = fichier.active  

    fichier.range("A33").value = section1
    fichier.range("A35").value = distance1
    fichier.range("G33").value = section2
    fichier.range("G35").value = distance2
    
    fichier.save("Calcul_GWP.xlsx")

    materiau = fichier.range("E47").value
    GWP1 = round(fichier.range("D43").value, 2)
    GWP2 = round(fichier.range("J43").value, 2)

    st.success(f"Le matériau à utiliser est **{materiau}**")
    st.metric(label="Total GWP de l'aluminium", value=f"{GWP1} kg CO₂")
    st.metric(label="Total GWP du cuivre", value=f"{GWP2} kg CO₂")
