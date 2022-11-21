
import plotly.express as px
import pandas as pd
import streamlit as st
import base64
import plotly.graph_objects as go

df = pd.read_csv('programasinternacionaleslimpio.csv')
conteo = pd.read_csv('conteo.csv')
st.set_page_config(page_title='Programas Internacionales', page_icon=":peach:", layout="wide")

file_ = open("globe.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

#Header Section
t1, t2 = st.columns(2)
with t1:
    st.header('Anibal José Angulo Cardoza  -  A01654684')
    st.title('Análisis de datos de programas internacionales :airplane:')
    st.write('En esta pagína trataré de comprobar 2 hipótesis diferentes a través la visualización de datos.')

with t2:
    st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
    unsafe_allow_html=True)

#Graphs
with st.container():
    st.write('---')
    a1, a2 = st.columns(2)
    with a1:
        st.subheader('Hipótesis 1:')
        fig1 = px.pie(df, names='Primera Opcion', hole=0.4, title='Asignado en primera opcion', width=700, color_discrete_sequence=px.colors.qualitative.D3)
        a1.write(fig1)
    with a2:
        st.subheader('Hipótesis 2:')
        fig2 = px.pie(df, names='Tipo de transferencia', hole=0.4, title='Tipo de transferencia', width=800, color_discrete_sequence=px.colors.qualitative.G10)
        a2.write(fig2)

with st.container():
        st.write('---')
        st.title('World Map')
    # b1, b2 = st.columns((1,2))
    # with b1:
        selec = st.selectbox('Selección', ['Asignado', 'Rechazado'])
    # with b2:
        if selec == 'Asignado':
            fig3 = go.Figure(data=go.Choropleth(
                locations = conteo['index'],
                z = conteo['Asignado'],
                text = conteo['Country'],
                colorscale = 'Inferno',
                autocolorscale=False,
                reversescale=True,
                marker_line_color='#444',
                marker_line_width=0.5,
                colorbar_title = 'Asignaciones'
            ))

            fig3.update_layout(
                width=1600,
                height=900,
                geo=dict(
                    showframe=False,
                    showcoastlines=False,
                    projection_type='equirectangular'
                ),
                title={
                    'text': '<b>Asignaciones por país</b>',
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                },
                title_font_color='#f7f5f5',
                title_font_size=26,
                font=dict(
                    family='Heebo', 
                    size=18, 
                    color='#f7f5f5'
                )
            )
            st.write(fig3)
        else:
            fig3 = go.Figure(data=go.Choropleth(
                locations = conteo['index'],
                z = conteo['Rechazado'],
                text = conteo['Country'],
                colorscale = 'Inferno',
                autocolorscale=False,
                reversescale=True,
                marker_line_color='#444',
                marker_line_width=0.5,
                colorbar_title = 'Rechazos'
            ))

            fig3.update_layout(
                width=1600,
                height=900,
                geo=dict(
                    showframe=False,
                    showcoastlines=False,
                    projection_type='equirectangular'
                ),
                title={
                    'text': '<b>Rechazos por país</b>',
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                },
                title_font_color='#f7f5f5',
                title_font_size=26,
                font=dict(
                    family='Heebo', 
                    size=18, 
                    color='#f7f5f5'
                )
            )
            st.write(fig3)

df['PaisAsignado'] = df['PaisAsignado'].astype(str) + ' '

dftemp = df.groupby(['Región', 'PaisSeleccionado'])['Matrícula'].count().reset_index()
dftemp.columns = ['source', 'target', 'value']

dftemp1 = df.groupby(['PaisSeleccionado', 'Estatuslimpio'])['Matrícula'].count().reset_index()
dftemp1.columns = ['source', 'target', 'value']

dftemp2 = df.groupby(['Estatuslimpio', 'PaisAsignado'])['Matrícula'].count().reset_index()
dftemp2.columns = ['source', 'target', 'value']

links = pd.concat([dftemp, dftemp1, dftemp2], axis=0)

uniquecode = list(pd.unique(links[['source','target']].values.ravel('K')))

mappingdict = {k: v for v, k in enumerate(uniquecode)}

links['source'] = links['source'].map(mappingdict)
links['target'] = links['target'].map(mappingdict)

linksdict = links.to_dict(orient='list')

colors = ['blue', 'blue', 'blue', 'blue', 'blue', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'navy', 'crimson', 'green', 'green', 'green', 'green', 'green', 'green', 'green', 'green', 'green', 'green', 'green', 'green', 'green']


with st.container():
        st.write('---')
        st.title('Diagrama Alluvial/Sankey')
    # d1, d2, d3 = st.columns((4, 8, 1))
    # with d2:
        fig5 = go.Figure(data=[go.Sankey(
            node = dict(
                pad = 15,
                thickness = 20,
                line = dict(color='black', width = 0.5),
                label = uniquecode,
                color = colors
            ),
            link = dict(
                source = linksdict['source'],
                target = linksdict['target'],
                value = linksdict['value'],
            )
        )]
        )

        fig5.update_layout(title_text = "Programas Internacionales - Selección vs Asignación", font_size=10, width = 1600, height = 700)
        st.write(fig5)
