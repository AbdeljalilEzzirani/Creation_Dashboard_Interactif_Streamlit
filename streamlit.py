import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import os
from datetime import date


# Database connection
datab = os.getenv("DATABASE_URL", "postgresql://postgres:suivant@localhost:5432/real_estate")
engine = create_engine(datab, echo=True)

st.title("Dashboard Interactif avec Streamlit")

query_annonce = 'SELECT * FROM "Annonce";'
query_city = 'SELECT * FROM "City";'
query_equipement = 'SELECT * FROM "Equipement";'
query_Table_associative = 'SELECT * FROM "Table_associative";'

# === Sidebar Creation ===
with st.sidebar:
    st.header("Filtres Interactifs")
    # 1.  Gamme de prix (slider)
    st.subheader("Gamme de prix (€)")
    min_price, max_price = st.slider("Sélectionnez une plage de prix", min_value=0, max_value=10000000, value=(5000, 500000), step=10000)
    st.write("prix selectionnes :", min_price, max_price)
    # Nombre de pièces (slider) # 2. Number of Rooms Filter
    st.subheader("Number of Rooms Filter / Nombre de pièces (slider) ")
    min_pieces, max_pieces = st.slider("Sélectionnez le Number of Rooms Filter", min_value=1, max_value=10, value=(1, 5))
    st.write("Number of Rooms Filter  selectionnes :", min_pieces, max_pieces)
    # 3. Number of Bathrooms Filter / Nombre de salles de bain
    st.subheader("Nombre de salles de bain")
    min_bathrooms, max_bathrooms = st.slider("Sélectionnez le nombre de salles de bain", min_value=1, max_value=5, value=(1, 3))
    st.write("Number of Rooms Filter  selectionnes :", min_bathrooms, max_bathrooms)
    # # 4. City Selection Filter
    st.subheader("Sélection de ville")
    with engine.connect() as con:
        cities_query = 'SELECT DISTINCT name FROM "City"'
        cities = pd.read_sql(cities_query, con)["name"].tolist()
    selected_city = st.selectbox("Choisissez une ville", options=["Toutes"] + cities)
    # # 5. Equipment Selection Filter
    st.subheader("Équipements")
    with engine.connect() as con:
        equipments_query = 'SELECT DISTINCT name FROM "Equipement"'
        equipments = pd.read_sql(equipments_query, con)["name"].tolist()
    selected_equipments = st.multiselect("Sélectionnez des équipements", options=equipments)
    # # 6. Date Range Filter
    st.subheader("Plage de dates")
    default_start = date.today()
    default_end = date.today()
    start_date, end_date = st.date_input("Sélectionnez une plage de dates (facultatif)", value=(default_start, default_end), key="date_range")
    if start_date is not None and end_date is not None:
        st.write("Dates sélectionnées :", start_date, end_date)
    else:
        st.warning("Veuillez sélectionner une plage de dates valide.")
    # st.write("Number of Rooms Filter  selectionnes :", start_date, end_date)


# this for join deux tables annonce and city
query_ville_annonce ="""SELECT * FROM "Annonce" a JOIN "City" c ON c.id_city = a.id_annonces;"""
with engine.connect() as conn :
    res=conn.execute(text(query_ville_annonce))
    df=pd.DataFrame(res.fetchall() , columns=res.keys())

st.write('Gamme de prix --> join  table annonce & table city')
st.dataframe(df)






query_annonce = f"""SELECT * From "Annonce" a WHERE price BETWEEN ('{min_price}') AND ('{max_price}');"""
with engine.connect() as con:
    res_annonce = con.execute(text(query_annonce))
    # res_annonce = con.execute(text(query_annonce), {"min_price": min_price, "max_price": max_price})
    df = pd.DataFrame(res_annonce.fetchall(), columns=res_annonce.keys())
    st.write("Data from 'annonce' Table:")
    st.dataframe(df)
    
    res_city = con.execute(text(query_city))
    df = pd.DataFrame(res_city.fetchall(), columns=res_city.keys())
    st.write("Data from 'City' Table:")
    st.dataframe(df)
    
    res_equipement = con.execute(text(query_equipement))
    df = pd.DataFrame(res_equipement.fetchall(), columns=res_equipement.keys())
    st.write("Data from 'Equipement' Table:")
    st.dataframe(df)
    
    res_assosiative = con.execute(text(query_Table_associative))
    df = pd.DataFrame(res_assosiative.fetchall(), columns=res_assosiative.keys())
    st.write("Data from 'Table_associative' Table:")
    st.dataframe(df)




















                    # # 1. Price Range Slider
                    # price_range = st.sidebar.slider(
                    #     "Gamme de prix (€)",
                    #     min_value=0,
                    #     max_value=10000,
                    #     value=(1000, 5000),  # Default range
                    #     step=100
                    # )





    # # === Main Page ===
    # st.subheader("Tableau des annonces filtrées")




