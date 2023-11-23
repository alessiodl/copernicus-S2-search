import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import folium
from streamlit_folium import folium_static

st.set_page_config(
    page_title="Ricerca S2",
    page_icon=":satellite:",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'df' not in st.session_state:
    st.session_state['df'] = pd.DataFrame()
    
if 'from_date' not in st.session_state:
    st.session_state['from_date'] = ''

if 'to_date' not in st.session_state:
    st.session_state['to_date'] = ''

if 'day_delta' not in st.session_state:
    st.session_state['day_delta'] = ''

st.header(':satellite: Ricerca immagini Sentinel 2', divider='blue')
st.write('*Copernicus Data Space Ecosystem OData API*')

# Launch request
df_list = []
def call_ecosystem_api():
    
    # Check dates
    print(type(st.session_state['from_date']))
    delta = st.session_state['to_date'] - st.session_state['from_date']
    # print(delta.days)
    if delta.days >= 0:
        st.session_state['day_delta'] = 'Valid'
        for req in request_list:
            # print(req)
            json = requests.get(req).json()
            # print(json)
            # DataFrame drlla risposta
            if (len(json['value'])>0):
                df = pd.DataFrame.from_dict(json['value']).dropna()
                df = df[['Id', 'Name','OriginDate','GeoFootprint','Online']]
                # print('Immagini trovate per la singola richiesta: {}'.format(str(len(df))))
                df_list.append(df)
            else:
                pass
    
        df_tot = pd.concat(df_list, ignore_index=True)
        df_tot.sort_values(by='OriginDate', ascending = False, inplace = True)
        st.session_state.df = df_tot
    else:
        st.session_state['day_delta'] = 'Invalid'
        
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 25% !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.subheader("Parametri di ricerca")
    
    regioni_italiane = [
    'Abruzzo','Sardegna','Puglia','Bolzano','Calabria','Campania','Emilia_Romagna',
    'Friuli', 'Lazio','Lombardia','Umbria_Marche','Piemonte','Sicilia','Toscana','Veneto']

    regioni_italiane_ordinate = sorted(regioni_italiane)
    
    regione = st.selectbox('Regione', regioni_italiane_ordinate)
    
    # Tiles da scaricare in base alla regione selezionata
    if regione == 'Abruzzo':
        region_tiles = ['R122_T33TUG', 'R122_T33TUH', 'R079_T33TVG', 'R122_T33TVH']
    elif regione == 'Sardegna':
        region_tiles = ['R022_T32SMJ', 'R022_T32SNJ', 'R022_T32TMK', 'R065_T32TML',	'R022_T32TNK', 'R022_T32TNL']
    elif regione == 'Puglia':
        region_tiles = ['R079_T33TWF', 'R079_T33TWG', 'R036_T33TXE', 'R036_T33TXF', 'R036_T33TYE', 'R036_T33TYF']
    elif regione == 'Bolzano':
        region_tiles = ['R022_T32TPS', 'R065_T32TPT', 'R022_T32TQT']
    elif regione == 'Calabria':
        region_tiles = ['R036_T33SWC', 'R079_T33SWD', 'R036_T33SXC', 'R036_T33SXD']
    elif regione == 'Campania':
        region_tiles = ['R079_T33TVE', 'R079_T33TVF', 'R079_T33TWE']
    elif regione == 'Emilia_Romagna':
        region_tiles = ['R065_T32TNQ', 'R022_T32TPQ', 'R022_T32TQP', 'R022_T32TQQ']
    elif regione == 'Friuli':
        region_tiles =  ['R022_T33TUM', 'R122_T33TVL']
    elif regione == 'Lazio':
        region_tiles = ['R022_T32TPM', 'R122_T33TTF', 'R122_T33TTG', 'R122_T33TUF']
    elif regione == 'Lombardia':
        region_tiles = ['R065_T32TMR', 'R065_T32TMS', 'R065_T32TNR', 'R065_T32TNS']
    elif regione == 'Umbria_Marche':
        region_tiles = ['R122_T33TUJ', 'R122_T32TQN']
    elif regione == 'Piemonte':
        region_tiles = ['R108_T32TLP', 'R108_T32TLQ', 'R108_T32TLR', 'R108_T32TLS', 'R065_T32TMP', 'R065_T32TMQ']
    elif regione == 'Sicilia':
        region_tiles = ['R122_T33STV',	'R122_T33STA', 'R122_T33STB', 'R122_T33STC', 'R079_T33SUB', 'R079_T33SUC', 'R079_T33SUV', 'R079_T33SVA', 'R079_T33SVB',	'R079_T33SVC', 'R036_T33SWA', 'R036_T33SWB']
    elif regione == 'Toscana':
        region_tiles = ['R022_T32TNM',	'R022_T32TNN', 'R065_T32TNP', 'R022_T32TPN', 'R022_T32TPP']
    elif regione == 'Veneto':
        region_tiles = ['R022_T32TPR', 'R022_T32TQR', 'R022_T32TQS', 'R122_T33TUK', 'R122_T33TUL']
    
    tiles_to_search = st.multiselect("Tiles", region_tiles, default=region_tiles, placeholder="Scegli una Regione per popolare...")
    
    sideCol1, sideCol2 = st.columns(2)
    with sideCol1:
        st.session_state['from_date'] = st.date_input('Da', datetime(2023,1,1), format='DD-MM-YYYY')
    with sideCol2:
        st.session_state['to_date'] = st.date_input('a', "today", format='DD-MM-YYYY')
        
    st.button("Invia le richieste al CDSE :arrow_forward:", type="primary", on_click=call_ecosystem_api, use_container_width=True)
    
    st.success(':information_source: Immagini trovate: **{}**'.format(str(len(st.session_state['df']))))
    
    if st.session_state['day_delta'] == 'Invalid':
        st.error(':no_entry: Intervallo data non valido!!!')
  
    # query parameters
    base_url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
    filter_collection = "Collection/Name eq 'SENTINEL-2'"
    filter_level = "contains(Name,'S2A_MSIL2A')"
    filter_sensing_dt = "ContentDate/Start gt {}T00:00:00.000Z and ContentDate/Start lt {}T23:59:59.000Z".format(st.session_state['from_date'], st.session_state['to_date'])
    filter_online = "(Online eq true or Online eq false)"
    limit = '1000' #max = 1000

    request_list = []
    
    if len(tiles_to_search) == 0:
        tiles_to_search = region_tiles
    
    for tile in tiles_to_search:
        filter_tile = "contains(Name, '_{}_')".format(tile)
        req = base_url +'?$filter={} and {} and {} and {} and {}&$orderby=ContentDate/Start desc&$top={}'.format(filter_collection, filter_level, filter_tile, filter_sensing_dt, filter_online, limit)
        request_list.append(req)

platform = 'Sentinel-2'
product = 'S2MSI2A'
st.write('Platform: **'+platform+'**, Product: **'+product+'**')   
        
tab1, tab2, tab3 = st.tabs(["Elenco", "Footprint", "Richieste"])

with tab1:
    st.dataframe(st.session_state['df'], use_container_width=True, hide_index=True, 
                 column_config={"GeoFootprint": None, 
                                'OriginDate':st.column_config.DateColumn(format="DD/MM/YYYY")
                })
    try:
        online_count = len(st.session_state['df'][st.session_state['df']["Online"]])
        offline_count = len(st.session_state['df'][~st.session_state['df']["Online"]])
        st.write('Online: '+str(online_count) + ', Offline: '+str(offline_count))
    except:
        pass
    
with tab2:
    st.markdown("""
        <style>
        iframe {
            width: 100%;
            min-height: 400px;
            height: 100%:
        }
        </style>
        """, unsafe_allow_html=True)
    # Mappa
    m = folium.Map(location=[43.5236, 13.6750], zoom_start=5, tiles="cartodb positron")
    try:
        df = st.session_state['df']
        geojson_obj = {
            "type": "FeatureCollection",
            "features": []
        }
    
        for (polygon, id, name) in zip(df['GeoFootprint'].values, df['Id'].values, df['Name'].values):
            feature_obj = {"type":"Feature", "geometry": polygon, "properties":{"id":id, "name": name}}
            geojson_obj['features'].append(feature_obj)
            
        # footprints s2 images
        s2tooltip = folium.GeoJsonTooltip(
            fields=["id","name"],
            localize=True,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid #6495ED;
                border-radius: 3px;
                box-shadow: 3px;
            """,
            max_width=800,
        )
        
        s2footprints = folium.GeoJson(
            geojson_obj,
            tooltip=s2tooltip,
            name="S2 Footprints",
            style_function=lambda feature: {"fillColor":"#005577","fillOpacity":0.0, "color":"#005577", "weight":2, "dashArray": "5,5"}
        ).add_to(m)
    except:
        pass
    
    # m.fit_bounds(s2footprints.get_bounds(), padding=(120,120))
    
    folium_static(m, height=450)
    
with tab3:
    st.info(':information_source: Selezionare i parametri nella colonna a sinistra per comporre le richieste da inviare al servizio')
    with st.expander('Richieste inviate'):
        if len(st.session_state['df']) <= 0:
            st.write('Nessuna richiesta inviata')
        else: 
            for req in request_list:
                st.write(req)