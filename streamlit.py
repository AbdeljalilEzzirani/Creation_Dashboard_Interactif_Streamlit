import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import os
from datetime import date
import plotly.express as px
from geopy.geocoders import Nominatim




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
    # *  Gamme de prix (slider)
    st.subheader("(slider)-> Gamme de prix (€)")
    min_price, max_price = st.slider("Sélectionnez une plage de prix", min_value=0, max_value=10000000, value=(5000, 5000000), step=10000)
    st.write("prix selectionnes :", min_price, max_price)
    #    Nombre de pièces (slider) # 2. Number of Rooms Filter
    st.subheader("(slider) -> Number of Rooms Filter / Nombre de pièces (slider) ")
    min_pieces, max_pieces = st.slider("Sélectionnez le Number of Rooms Filter", min_value=1, max_value=10, value=(1, 5))
    st.write("Number of Rooms Filter  selectionnes :", min_pieces, max_pieces)
    #    Number of Bathrooms Filter / Nombre de salles de bain
    st.subheader("(slider) -> Nombre de salles de bain")
    min_bathrooms, max_bathrooms = st.slider("Sélectionnez le nombre de salles de bain", min_value=1, max_value=5, value=(1, 3))
    st.write("nombre de salles de bain selectionnes :", min_bathrooms, max_bathrooms)
    # *  City Selection Filter
    st.subheader("(slider) -> Sélection de ville")
    with engine.connect() as con:
        cities_query = 'SELECT DISTINCT name FROM "City"'
        cities = pd.read_sql(cities_query, con)["name"].tolist()
    selected_city = st.selectbox("Choisissez une ville", options=["Toutes"] + cities)
    
    # st.subheader("Sélection de ville")
    # with engine.connect() as con:
    #     cities_query = 'SELECT DISTINCT name FROM "City"'
    #     cities = pd.read_sql(cities_query, con)["name"].tolist()
    # selected_city = st.selectbox("Choisissez une ville", options=["Toutes"] + cities)
    
    #    Equipment Selection Filter
    st.subheader("(slider) -> Équipements")
    with engine.connect() as con:
        equipments_query = 'SELECT DISTINCT name FROM "Equipement"'
        equipments = pd.read_sql(equipments_query, con)["name"].tolist()
    selected_equipments = st.multiselect("Sélectionnez des équipements", options=equipments)
    #    Date Range Filter
    st.subheader("(slider) -> Plage de dates")
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

# st.write('Gamme de prix --> join  table annonce & table city')
# st.dataframe(df)

# # Initialize Geolocator
# geolocator = Nominatim(user_agent="myGeocoder")

# def get_coordinates(city_name):
#     location = geolocator.geocode(city_name)
#     if location:
#         return location.latitude, location.longitude
#     else:
#         return None, None


# query_ville_annonce_with_coords = """SELECT a.*, c.name AS city_name, c.latitude, c.longitude FROM "Annonce" a JOIN "City" c ON c.id_city = a.city_id WHERE (:selected_city = 'Toutes' OR c.name = :selected_city)"""

# Execute the filtered query with the parameters
# with engine.connect() as con:
#     params = {
#         "selected_city": selected_city,
#     }
#     res = con.execute(text(query_ville_annonce_with_coords), params)
#     df_filtered_with_coords = pd.DataFrame(res.fetchall(), columns=res.keys())

# # Display the filtered results
# st.title("Table des annonces avec coordonnées")
# st.write("Résultats filtrés par ville avec coordonnées (latitude et longitude) :")
# st.dataframe(df_filtered_with_coords)



# Fetch data
# query_ville_annonce_with_coords = """SELECT a.*, c.name AS city_name, c.latitude, c.longitude FROM "Annonce" a JOIN "City" c ON c.id_city = a.city_id"""

# Query for the joined table with city filter
query_ville_annonce_filtered = """SELECT * FROM "Annonce" a JOIN "City" c ON c.id_city = a.city_id WHERE (:selected_city = 'Toutes' OR c.name = :selected_city)"""

query_annonce = f"""SELECT * From "Annonce" a JOIN "City" c ON c.id_city = a.id_annonces WHERE price BETWEEN ('{min_price}') AND ('{max_price}');"""
with engine.connect() as con:
    res_annonce = con.execute(text(query_annonce))
    # res_annonce = con.execute(text(query_annonce), {"min_price": min_price, "max_price": max_price})
    df = pd.DataFrame(res_annonce.fetchall(), columns=res_annonce.keys())
    st.write("Data from 'annonce' Table:")
    st.dataframe(df)
    
    params = {"selected_city": selected_city}
    res = con.execute(text(query_ville_annonce_filtered), params)
    df_filtered = pd.DataFrame(res.fetchall(), columns=res.keys())
    # Display the filtered results
    st.title("Table des annonces et des villes filtrées")
    st.write("Résultats filtrés par ville (jointure entre 'Annonce' et 'City'):")
    st.dataframe(df_filtered)
    
    # res = con.execute(text(query_ville_annonce_with_coords))
    # df = pd.DataFrame(res.fetchall(), columns=res.keys())
    
    
    # res_equipement = con.execute(text(query_equipement))
    # df = pd.DataFrame(res_equipement.fetchall(), columns=res_equipement.keys())
    # st.write("Data from 'Equipement' Table:")
    # st.dataframe(df)
    
    # res_assosiative = con.execute(text(query_Table_associative))
    # df = pd.DataFrame(res_assosiative.fetchall(), columns=res_assosiative.keys())
    # st.write("Data from 'Table_associative' Table:")
    # st.dataframe(df)

# Bar Chart: Number of Announcements by City
city_counts = df_filtered.groupby("name").size().reset_index(name="count")
fig_bar = px.bar(city_counts, x="name", y="count", title="Nombre d'annonces par ville", labels={"name": "Ville", "count": "Nombre d'annonces"})
st.plotly_chart(fig_bar)

# Sample query for the joined table (adjust column names if needed)
query_ville_annonce_with_price = """
SELECT a.price, c.name AS city_name
FROM "Annonce" a
JOIN "City" c ON c.id_city = a.city_id
WHERE (:selected_city = 'Toutes' OR c.name = :selected_city)
"""

# Execute the query and create a DataFrame
with engine.connect() as con:
    params = {"selected_city": selected_city}
    res = con.execute(text(query_ville_annonce_with_price), params)
    df_filtered_with_price = pd.DataFrame(res.fetchall(), columns=res.keys())

# Ensure DataFrame is ready
st.write("DataFrame with 'price' and 'city_name':", df_filtered_with_price)

# **************************************************************************************

col_7, col_8 = st.columns([1/3, 2/3])

with col_7:
    st.subheader("Le nombre d'annonce par date")
    dynamic_query = """
    SELECT 
        DATE(datetime) AS date_, 
        COUNT(*) AS nombre_annonce
    FROM "Annonce"
    GROUP BY DATE(datetime)
    ORDER BY date_;
    """
    
    with engine.connect() as con:
        res = con.execute(text(dynamic_query))
        df_date = pd.DataFrame(res.fetchall(), columns=res.keys())
    
    if not df_date.empty:
        # Convertir la colonne 'date_' en format datetime
        df_date['date_'] = pd.to_datetime(df_date['date_'])
        # st.dataframe()
        
        # Définir les dates minimales et maximales dans le DataFrame
        min_date = df_date['date_'].min()
        max_date = df_date['date_'].max()

        # Sélectionner la date de début
        start_date = st.date_input(
            "Sélectionnez la date de début :",
            value=min_date,  # valeur initiale
            min_value=min_date,
            max_value=max_date
        )

        # Afficher la sélection de la date de fin uniquement après avoir choisi une date de début
        
        if start_date:
            end_date = st.date_input(
                "Sélectionnez la date de fin :",
                value=max_date,  # valeur initiale = date de début
                min_value=start_date,  # La date de fin ne peut pas être avant la date de début
                max_value=max_date
            )
            
            # Lorsque les deux dates sont sélectionnées
            if end_date:
                # Filtrer les données en fonction des dates sélectionnées
                df_filtered = df_date[(df_date['date_'] >= pd.to_datetime(start_date)) &
                                      (df_date['date_'] <= pd.to_datetime(end_date))]
                
                # Afficher le DataFrame filtré
                st.write(f"Data filtrée entre {start_date} et {end_date}:")
                st.dataframe(df_filtered)
                
with col_8:
    if not df_filtered.empty:
        st.subheader("Graphique d'évolution du nombre d'annonce au fil du temps")

        fig = px.line(
            df_filtered,
            x='date_',
            y='nombre_annonce',
            title=f'Évolution du nombre d\'annonces du {start_date} au {end_date}',
            labels={'date_': 'Date', 'nombre_annonce': 'Nombre des annonces'},
            markers=True
        )

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Nombre d'annonces",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Aucune donnée disponible pour cette plage de dates.")









# **************************************************************************************

# Histogram for Price Distribution
fig_hist = px.histogram(
    df_filtered_with_price,  # DataFrame with joined data
    x="price",
    nbins=30,
    title="Répartition des prix",
    labels={"price": "Prix (€)"},
    color_discrete_sequence=["blue"]
)

st.write("Histogramme : Répartition des prix")
st.plotly_chart(fig_hist, key="unique_price_histogram")  # Unique key

# Boxplot Comparing Price Ranges by City
fig_box = px.box(
    df_filtered_with_price,  # DataFrame with joined data
    x="city_name",
    y="price",
    title="Comparaison des gammes de prix par ville",
    labels={"city_name": "Ville", "price": "Prix (€)"},
    color="city_name"
)

st.write("Boxplot : Gammes de prix par ville")
st.plotly_chart(fig_box, key="unique_price_boxplot")  # Unique key

for index, city in enumerate(df_filtered_with_price["city_name"].unique()):
    # Subset data by city
    city_data = df_filtered_with_price[df_filtered_with_price["city_name"] == city]
    
    # Dynamic Key
    unique_key = f"price_histogram_{index}"

    # Plot Histogram for the City
    fig_city_hist = px.histogram(
        city_data,
        x="price",
        nbins=30,
        title=f"Répartition des prix : {city}",
        labels={"price": "Prix (€)"},
        color_discrete_sequence=["blue"]
    )
    st.plotly_chart(fig_city_hist, key=unique_key)  # Dynamic key
















