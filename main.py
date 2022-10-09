import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.title('Analysis and visualisation of French value demand in metropolitan France by Jonah JAUBERT BIA1')



#Code to sample the full dataset, replace "x" by the year

def sample():
    df_full = pd.read_csv('full_20xx.csv')
    df_reduc = df_full.sample(frac = 0.04)
    val_suppr = ['adresse_numero', 'adresse_suffixe', 'ancien_code_commune', 'ancien_nom_commune', 'ancien_id_parcelle','numero_volume','lot1_numero','lot1_surface_carrez','lot2_numero','lot2_surface_carrez','lot3_numero','lot3_surface_carrez','lot4_numero','lot4_surface_carrez','lot5_numero','lot5_surface_carrez','surface_reelle_bati','nombre_pieces_principales','code_nature_culture','nature_culture','code_nature_culture_speciale','nature_culture_speciale']
    df_reduc = df_reduc.drop(val_suppr, axis=1)
    df_reduc.to_csv('sample20xx.csv')

# Definition of usefull fonctions#

def selectyear():
    year = st.slider("Which year do you want to visualize ?", 2016, 2020)
    return year


@st.cache(allow_output_mutation=True)
def load_data(year):
    if year == 2016:
        df = pd.read_csv('sample2016.csv', low_memory=False, decimal=".")
        return df
    elif year == 2017:
        df = pd.read_csv('sample2017.csv', low_memory=False, decimal=".")
        return df
    elif year == 2018:
        df = pd.read_csv('sample2018.csv', low_memory=False, decimal=".")
        return df
    elif year == 2019:
        df = pd.read_csv('sample2019.csv', low_memory=False, decimal=".")
        return df
    elif year == 2020:
        df = pd.read_csv('sample2020.csv', low_memory=False, decimal=".")
        return df


def get_month(dt):
    return dt.month

def map():
    st.title("Map to visualize the repartition of the dataset in France")
    df.dropna(subset=['longitude', 'latitude'], axis=0, inplace=True)
    dfmap = pd.DataFrame()
    dfmap['lat'] = df['latitude']
    dfmap['lon'] = df['longitude']
    st.map(dfmap)

def bar():
    st.title("Bar chart to visualize the presence of departements in the dataset")
    dfbar = df['code_postal'].value_counts()
    st.bar_chart(dfbar)


def plotly_pie():
    st.title("Pie chart to visualize proportion of local type in France")
    donnees_manquantes = (df["type_local"].isna().sum()) / (df.shape[0]) * 100
    df_dummies = df["type_local"]
    df_dummies = pd.get_dummies(df_dummies, columns=["type_local"])
    nb_Maison = df_dummies[df_dummies["Maison"] == 1].shape[0]
    nb_Maison = nb_Maison / (df.shape[0]) * 100
    nb_Appartement = df_dummies[df_dummies["Appartement"] == 1].shape[0]
    nb_Appartement = nb_Appartement / (df.shape[0]) * 100
    nb_dependance = df_dummies[df_dummies["Dépendance"] == 1].shape[0]
    nb_dependance = nb_dependance / (df.shape[0]) * 100
    nb_Local = df_dummies[df_dummies["Local industriel. commercial ou assimilé"] == 1].shape[0]
    nb_Local = nb_Local / (df.shape[0]) * 100

    labels = ['Données Manquantes', 'Maison', 'Appartement', 'Dépendance', 'Local industriel. commercial ou assimilé']
    colors = ['rgb(255,252,82)', 'rgb(255,153,153)', 'rgb(153,255,153)', 'rgb(102,179,255)', 'rgb(255,204,153)']
    area = [donnees_manquantes, nb_Maison, nb_Appartement, nb_dependance, nb_Local]

    fig = go.Figure(
        data=[go.Pie(labels=labels, values=area, marker=dict(colors=colors, line=dict(color='#000000', width=2)))])
    st.plotly_chart(fig)


def plotly_bar():
    st.title("Bar chart to visualize nature of mutation")
    labelnature = ["Vente", "Vente en l'état futur d'achèvement", "Echange", "Vente terrain à bâtir", "Adjudication",
                   "Expropriation"]
    fig2 = go.Figure([go.Bar(x=labelnature, y=df['nature_mutation'].value_counts())])
    st.plotly_chart(fig2)


def plotly_line():
    st.title("Line chart to visualize mutation through the year")
    df["date_mutation"] = pd.to_datetime(df["date_mutation"])
    df['month_mutation'] = df['date_mutation'].map(get_month)
    df_mois = pd.DataFrame(df, columns=['month_mutation', 'type_local'])
    df_mois.sort_values(by=['month_mutation'], inplace=True)
    df_mois['count'] = df_mois.groupby('month_mutation').transform('count')
    df_mois['count'] = df_mois.groupby(['type_local', 'month_mutation']).transform('count')
    df_mois.dropna(subset=['type_local'], axis=0, inplace=True)

    fig3 = px.line(df_mois, x="month_mutation", y="count", title='Nombre de mutation dans une année',
                   color='type_local')
    st.plotly_chart(fig3)

def plotly_histo():
    st.title("Histogramme of price by m^2 in Île-de-France compared to the rest of France")
    df_m2 = df[['surface_terrain', 'valeur_fonciere', 'code_departement']]
    df_m2.dropna(subset=['surface_terrain', 'valeur_fonciere'], axis=0, inplace=True)
    df_m2["code_departement"] = df_m2["code_departement"].apply(
        lambda x: 'Ile de France' if (x == "75" or x == "78" or x == "91"
                                      or x == "92" or x == "93" or x == "94" or x == "95") else 'Autres')
    df_m2['prix_m2'] = df_m2['valeur_fonciere'] / df_m2['surface_terrain']
    fig4 = px.histogram(df_m2, x="code_departement", y="prix_m2", histfunc='avg')
    st.plotly_chart(fig4)
# END definition


year = selectyear()
df = load_data(year)

sample = st.checkbox("Working on a sample ? (4%)")

if sample:
    st.write('Go sample !')
    df = df.sample(frac=0.04)

st.write('Shape of your dataset :')
st.write(df.shape)

see_nan = st.checkbox("Want to see how many NAN are in my dataset")
if see_nan:
    st.write(df.isna().sum())


plotly_pie()
map()
bar()
plotly_bar()
plotly_line()
plotly_histo()
