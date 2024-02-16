import streamlit as st
from db_functions import (load_empresas, load_segmentos, load_produtos, 
                          filter_by_segmento, filter_by_produto, load_segment_translation, 
                          load_estados, filter_by_estado, load_componentes_por_produto)
from rendering_functions import display_table, display_map

# Carregar os mapeamentos ao iniciar o aplicativo
pt_to_en, en_to_pt = load_segment_translation()

# Layout of the Streamlit application
st.title('Brazilian Electronic Companies')

# Sidebar for main page selection
view_option = st.sidebar.selectbox('View:', ['Table', 'Map'])

# Sidebar for filter options
with st.sidebar:
    option = st.selectbox('Filter by:', ['None', 'Segment', 'Product', 'State'])

    if option == 'Segment':
        segments = ['Choose a segment...'] + sorted(load_segmentos(pt_to_en))
        chosen_segment = st.selectbox('Choose the segment:', segments)

    elif option == 'Product':
        products = ['Choose a product...'] + sorted(load_produtos())
        chosen_product = st.selectbox('Choose the product:', products)
        
        # Carregar e exibir componentes se um produto for selecionado
        if chosen_product != 'Choose a product...':
            components = load_componentes_por_produto(chosen_product)
            st.write('Components:')  # Título para a lista de componentes
            if components:  # Se a lista de componentes não estiver vazia
                for component in components:
                    st.markdown(f"*{component}*")  # Exibe cada componente em itálico
            else:
                st.markdown("*Not Found*")  # Mensagem exibida em itálico se não houver componentes

    elif option == 'State':
        estados = ['Choose a state...'] + sorted(load_estados())
        chosen_state = st.selectbox('Choose the state:', estados)

# Determine the DataFrame to be displayed
if option == 'Segment' and chosen_segment != 'Choose a segment...':
    displayed_df = filter_by_segmento(en_to_pt[chosen_segment])
elif option == 'Product' and chosen_product != 'Choose a product...':
    displayed_df = filter_by_produto(chosen_product)
elif option == 'State' and chosen_state != 'Choose a state...':
    displayed_df = filter_by_estado(chosen_state)
else:
    displayed_df = load_empresas()

# Show selected view
if view_option == 'Table':
    display_table(displayed_df)
elif view_option == 'Map':
    display_map(displayed_df)
