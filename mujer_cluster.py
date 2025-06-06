# python -m streamlit run mujer_cluster.py

import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages


st.set_page_config(
    
    page_title='Conversación con Cristina (Perfil de cluster)',
    page_icon="logos/favicon-MERKLE.png",
    initial_sidebar_state="expanded"    
)


show_pages([
    Page("mujer_cluster.py","Powered by Vertex AI, Google."),
    Page("Cristina_Cluster_Original.py","Cristina")
])


hide_pages(['Cristina'])


##################################################################################

from streamlit_extras.app_logo import add_logo
add_logo("logos/2022-05_Merkle-logo-color.png", height = 25)

html = """
<div style="color:gray; font-size:10px;">
<i>
Texto e imagenes generadas por GenAI
</div>
"""


#add_logo("logos/2022-05_Merkle-logo-white_1000.png", height = 5)
with st.sidebar:
    st.markdown(html, unsafe_allow_html=True)
    st.subheader(":gray[Chatea con tu Buyer Persona]")
    st.markdown(":gray[Se ha generado con IA un Buyer Persona Sintético de ECI (Cristina, clúster3).]")
    st.title(
        ":gray[Chatea con un cliente :face_with_monocle:]"
    )
    
    
cliente_sidebar = st.sidebar.radio(':gray[Escoge al cliente:]', [':gray[Cristina]'])

cliente = cliente_sidebar.split("[")[1].split("]")[0]

### Main page:
st.write("# "+cliente_sidebar+"")

image_dict = {
  "Cristina": "./imagenes/cristina_cluster.png"
  }

text_dict = {
  "Cristina": '''Cristina es una mujer que, como Lucía, compra tanto online como en tienda, pero podríamos decir que no siempre combina estos canales. Para ECI presenta un valor Medio. Además de la moda, categoría de compra que comparten todos los perfiles, Cristina también compra productos de moda infantil y juguetes. También realiza compras relacionadas con el deporte. Tiene el perfil principalmente de cesta media, pero está pensando en vincularse.
'''
 }

direccion = image_dict[cliente]
text_explicativo = text_dict[cliente]

col1, col2 = st.columns(2, gap="small")

with col1:
    st.image(direccion)

with col2:
    intro_text = text_explicativo
    st.write(intro_text, unsafe_allow_html=True)
    boton_conversar = st.button("Conversar" )
    

if boton_conversar:
    switch_page(cliente)

