import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st
import plotly.express as px

engine = create_engine("postgresql://postgres:suivant@localhost:5432/my_db_")

query_1 = 'select*from annonce;'
query_2 = 'select* from cities;'
query_3 = 'select*from equipement;'

# Charger les villes disponibles pour le filtre
with engine.connect() as conn:
    st.header('Annonces datafram')
    res_1=conn.execute(text(query_1))
    df1=pd.DataFrame(res_1.fetchall() , columns=res_1.keys())
    st.dataframe(df1)
    
    st.header('dataframe city')
    res_2=conn.execute(text(query_2))
    df2=pd.DataFrame(res_2.fetchall() , columns=res_2.keys())
    st.dataframe(df2)
    
    st.header('dataframe Equipement')
    res_3=conn.execute(text(query_3))
    df3=pd.DataFrame(res_3.fetchall() , columns=res_3.keys())
    st.dataframe(df3)

# *******************************************************************************

st.subheader('la repartition de prix par villle ')

st.subheader('dataframe la repartition de prix par ville')
dynamic_query = 'select c.name_ville as name_ville , sum(a.price) as price_total from annonce a join cities c on c.city_id=a.city_id group by c.name_ville'
with engine.connect() as conn : 
    res = conn.execute(text(dynamic_query))
    df_prix = pd.DataFrame(res.fetchall() , columns=res.keys())
    st.dataframe(df_prix)

# *******************************************************************************

st.subheader('Graphe de repartition de prix  par ville ')
fig=px.bar(df_prix , 
x='name_ville' , 
y='price_total' , 
height=500 , 
title='repartition de prix par ville' , 
color_discrete_sequence= px.colors.qualitative.Set3)
st.plotly_chart(fig , use_container_width=True)

# *******************************************************************************

st.subheader('Les donnees du nombre d annonce par localisation')
dynamic_query='select DISTINCT c.name_ville , count(a.annonce_id) as annonce_total from annonce a join cities c on c.city_id=a.city_id group by c.name_ville;'
with engine.connect() as conn: 
    res=conn.execute(text(dynamic_query))
    df_ann_ville= pd.DataFrame(res.fetchall() , columns=res.keys())
    st.dataframe(df_ann_ville)

# *******************************************************************************

query = 'select c.name_ville , c.latitude  , c.longitude  , count(a.annonce_id) from annonce a join cities c on c.city_id=a.city_id group by  c.name_ville, c.latitude, c.longitude;'
with engine.connect() as conn : 
    res=conn.execute(text(query))
    coor=pd.DataFrame(res.fetchall() , columns=res.keys())

st.header('carte graphique : localisatio par map         boooobbbbbbbb marley')
fig = px.scatter_mapbox(coor, lat="latitude", lon="longitude", hover_name="name_ville", size_max=15, zoom=5, title="Villes en France",color="name_ville",  
color_discrete_sequence=px.colors.qualitative.Set1)
fig.update_layout(mapbox_style="open-street-map")


st.plotly_chart(fig , use_container_width=True)

# *******************************************************************************

st.subheader('Creation de boxplot pour les villes ')
selected_ville=st.multiselect('selectionne les villes : ' ,df2['name_ville'] )
ville_list = "','".join(selected_ville)
dynamic_query=f"""select a.price  , c.name_ville from annonce a join cities c ON a.city_id =c.city_id where c.name_ville in ('{ville_list}');"""

with engine.connect() as conn :
    result= conn.execute(text(dynamic_query))
    ville_data=pd.DataFrame(result.fetchall() , columns=result.keys())

if not ville_data.empty : 
    # Calculer les statistiques descriptives pour chaque ville
    grouped_descriptions = []
    for ville in selected_ville:
        ville_stats = (
            ville_data[ville_data["name_ville"] == ville]["price"]
            .describe()
            .reset_index()
            .rename(columns={"index": "Statistique", "price": ville})
        )
        grouped_descriptions.append(ville_stats.set_index('Statistique'))
    # Concaténer toutes les descriptions dans un seul DataFrame
    descriptions_combined = pd.concat(grouped_descriptions, axis=1)
    # Afficher les descriptions
    st.subheader("Descriptions des données par ville")
    st.dataframe(descriptions_combined)
    
# *******************************************************************************
    
if selected_ville and not ville_data.empty : 
    st.subheader('Graphique boxplot des raprtitions des prix par ville')
    fig = px.box(
        ville_data , 
        x='name_ville' , 
        y='price' ,
        title="Box Plot de la distribution des prix des biens" , 
        color='name_ville' ,  
        color_discrete_sequence= px.colors.qualitative.Set3)
    st.plotly_chart(fig , use_container_width=True)    
    
# *******************************************************************************

st.subheader("Filtre des villes")
selected_ville = st.multiselect("Sélectionnez des villes :", df2['name_ville'])
# Afficher le DataFrame des prix totaux (au-dessous de la barre de sélection)

    # Générer une requête SQL dynamique
ville_list = "','".join(selected_ville)  # Convertir les villes en liste SQL

dynamic_query = f"""SELECT c.name_ville, count(a.annonce_id) as Nombre_ann FROM annonce a JOIN cities c ON a.city_id = c.city_id WHERE c.name_ville IN ('{ville_list}') GROUP BY c.name_ville ;"""

# Exécuter la requête et récupérer les données
with engine.connect() as conn:
    result = conn.execute(text(dynamic_query))
    ville_data = pd.DataFrame(result.fetchall(), columns=result.keys())

st.dataframe(ville_data , hide_index=True)

# *******************************************************************************

st.subheader("Graphique de nombre total d'annonce par ville")

fig=px.bar(ville_data ,
    x='name_ville' , 
    y='nombre_ann' , 
    title='nombre total d\'annonce par ville' , 
    color='name_ville' , 
    color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(fig , use_container_width=True)

# *******************************************************************************

st.subheader('Visualisation par rapport aux equipement')
selected_equi=st.multiselect('Selectionner l\'equipement : ' ,df3['name_equi'] , default=df3['name_equi'])

equi_liste = "','".join(selected_equi)
dynamic_query = f"""select count(a.annonce_id) as total_ann , e.name_equi from annonce a join Annonce_equipement ae on a.annonce_id=ae.annonce_id join equipement e on e.equi_id=ae.equipement_id where e.name_equi in ('{equi_liste}') group by e.name_equi ;"""
with engine.connect() as conn : 
    res=conn.execute(text(dynamic_query))
    equi_data=pd.DataFrame(res.fetchall() , columns =res.keys())
equi_data=pd.DataFrame()

if selected_equi and not equi_data.empty : 
    st.subheader('Graphe de pie')
    fig=px.pie(equi_data , names = equi_data['name_equi'] , values=equi_data['total_ann'] , 
                 width=600 ,height=600,color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig , use_container_width=True)

# *******************************************************************************

st.subheader('Visualisation des chambres et salle de bain ')
selected_ville = st.multiselect('selectionner une ville  : ' , df2['name_ville'])


ville_list="','".join(selected_ville)

dynamic_query = f"""select c.name_ville , avg(a.nb_rooms) as moyen_Chambre , avg(a.nb_baths) as Moyen_bain
from annonce a 
join cities c on c.city_id=a.city_id
where c.name_ville in ('{ville_list}')
group by c.name_ville;
"""

with engine.connect() as conn: 
    res=conn.execute(text(dynamic_query))
    rooms_data = pd.DataFrame(res.fetchall() , columns=res.keys())

st.subheader('DataFrame de chambre et salle de bain')
st.dataframe(rooms_data)

# *******************************************************************************

if selected_ville and not rooms_data.empty:
    
    pivot_data = rooms_data.pivot_table(index='name_ville', values=['moyen_chambre', 'moyen_bain'], 
                                        aggfunc='mean').reset_index()
    
    melted_data = pivot_data.melt(id_vars=['name_ville'], value_vars=['moyen_chambre', 'moyen_bain'],
                                  var_name='Variable', value_name='Valeur Moyenne')
    
    st.subheader('Graphique des moyennes de chambres et salles de bain par ville')
    fig = px.bar(
        melted_data,
        x='name_ville',
        y='Valeur Moyenne',
        color='Variable',  # Color bars based on 'Variable' (moyen_chambre vs moyen_bain)
        title='Graphique des moyennes de chambres et salles de bain par ville',
        width=800,
        height=600,
        barmode='group',  # Grouped bars
        labels={'name_ville': 'Ville', 'Valeur Moyenne': 'Valeurs Moyennes'}
    )
    st.plotly_chart(fig)
else:
    st.warning('Aucune donnée disponible pour cet équipement.')

# *******************************************************************************


st.subheader('l’évolution du nombre d’annonces publiées au fil du temps.')

st.subheader("Le nombre d'annonce par date")

dynamic_query = 'SELECT DATE(date) AS date_, COUNT(*) AS nombre_annonce FROM annonce GROUP BY DATE(date) ORDER BY date_;'

with engine.connect() as con:
    res = con.execute(text(dynamic_query))
    df_date = pd.DataFrame(res.fetchall(), columns=res.keys())

if not df_date.empty:
    # Convertir la colonne 'date_' en format datetime
    df_date['date_'] = pd.to_datetime(df_date['date_'])
    
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

# *******************************************************************************

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

# *******************************************************************************

st.subheader('relation entre la surface et le prix des biens.')

st.subheader('Les donnees des surface par rapport a prix')
dynamic_query=""" select surface_area as surface , avg(price) as price_total 
from annonce 
group by surface;
"""

with engine.connect() as conn : 
    res=conn.execute(text(dynamic_query))
    df_surface = pd.DataFrame(res.fetchall()  , columns=res.keys())

if not  df_surface.empty:
    st.dataframe(df_surface)
else : 
    st.warning('Aucune donnee disponible pour cette ville ')

# *******************************************************************************

fig=px.scatter(df_surface ,
x='surface' , 
y='price_total' , 
title="Relation entre la surface et le prix des biens",
labels={'surface': 'Surface (m²)', 'prix': 'Prix (en AED)'},
template="plotly_white" )

st.plotly_chart(fig , use_container_width=True)

# *******************************************************************************







# *******************************************************************************
# *******************************************************************************
# *******************************************************************************
    