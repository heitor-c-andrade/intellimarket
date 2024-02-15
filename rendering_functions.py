import pydeck as pdk
import streamlit as st
import pandas as pd
import io

# Função para tornar URLs clicáveis
def make_clickable(url):
    if url is not None and url != "":
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        return f'<a target="_blank" href="{url}">{url}</a>'
    return ""

# Function to display the table
def display_table(displayed_df):
    if not displayed_df.empty:
        display_df = displayed_df.drop(columns=['LATITUDE', 'LONGITUDE'], errors='ignore').copy()
        display_df = display_df.rename(columns={
            "Nome Empresa": "Company Name",
            "Endereço da Empresa": "Company Address",
            "Nome Contato": "Contact Name",
            "Cargo Contato": "Contact Position",
            "Telefone": "Phone",
            "Website": "Website"
        })
        display_df = display_df[[
            "Company Name", 
            "Company Address", 
            "Contact Name", 
            "Contact Position", 
            "Phone", 
            "Website"
        ]]

        # Preparar DataFrame para download excluindo a coluna "Website"
        download_df = display_df.drop(columns=['Website'])

        # Converter DataFrame para Excel
        towrite = io.BytesIO()
        with pd.ExcelWriter(towrite, engine='xlsxwriter') as excel_writer:
            download_df.to_excel(excel_writer, index=False, sheet_name='Companies')
        
        towrite.seek(0)  # Voltar ao início do stream

        # Botão de download para o arquivo Excel
        st.download_button(label="Download Excel", data=towrite, file_name="companies.xlsx", mime="application/vnd.ms-excel")

        # Adiciona um espaço antes da tabela para separação visual
        st.write("\n")

        # Aplicar função para tornar URLs clicáveis
        display_df['Website'] = display_df['Website'].apply(make_clickable)
        
        # Converter DataFrame para HTML e renderizar a tabela
        st.markdown(display_df.to_html(index=False, escape=False), unsafe_allow_html=True)
        
    else:
        st.write('No companies found for the selected criteria.')

# Function to display the map
def display_map(displayed_df):
    if not displayed_df.empty:
        map_data = displayed_df.dropna(subset=['LATITUDE', 'LONGITUDE'])
        view_state = pdk.ViewState(
            latitude=map_data['LATITUDE'].mean(),
            longitude=map_data['LONGITUDE'].mean(),
            zoom=4,
            pitch=0)
        layer = pdk.Layer(
            'ScatterplotLayer',
            data=map_data,
            get_position='[LONGITUDE, LATITUDE]',
            get_color='[200, 30, 0, 160]',
            get_radius=50000,
        )
        map = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            map_style='mapbox://styles/mapbox/light-v9'
        )
        st.pydeck_chart(map)
    else:
        st.write('No companies found for the selected criteria.')