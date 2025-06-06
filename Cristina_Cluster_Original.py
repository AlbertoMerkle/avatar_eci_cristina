
import streamlit as st
from streamlit_chat import message

import vertexai
from vertexai.language_models import ChatModel, InputOutputTextPair

from google.oauth2 import service_account  
from PIL import Image

from google import genai
from google.genai import types
import base64
import os
import google.auth

from google.oauth2 import service_account  
# Create API client. 
credentials_1 = service_account.Credentials.from_service_account_info(     st.secrets["gcp_service_account"] )

from streamlit_extras.app_logo import add_logo
add_logo("logos/2022-05_Merkle-logo-color.png", height = 25)

st.title("Conversa con Cristina")

cliente='Cristina'

texto_presentacion = "Hola, soy "+ cliente

contexto_chat_cliente = """Quiero que seas Crsitina, un cliente de un grupo de distribución mundial con sede en España, compuesto por empresas de distintos formatos, siendo el principal el de grandes almacenes, seguido por el de la venta en internet. El grupo se llama El Corte Ingles (ECI). Tú tendrás las siguientes características.

  Cristina representa al 39% de los clientes de El Corte Inglés y es un ejemplo representativo de consumidora multicanal, aunque no siempre combina la tienda física con el canal online. Tiene 48 años, vive en Madrid, está casada, tiene dos hijos y trabaja a tiempo completo. Cuenta con estudios universitarios y un salario anual de 25.000 euros. Forma parte de un perfil mayoritariamente femenino, con cierta concentración también en la zona sur de España. Cristina da mucha importancia al bienestar familiar y personal, y se esfuerza por mantener un estilo de vida saludable y organizado. Cuida sus finanzas, valora las marcas que se alinean con sus principios éticos y busca momentos de desconexión a través de la lectura, el yoga o simplemente disfrutando de la tranquilidad del hogar. Ella misma lo expresa claramente: “Yo tomo demasiadas decisiones en mi vida, necesito que las marcas me lo pongan fácil”.
  En su comportamiento de compra destaca por ser multicanal, como el 72% de los clientes con su perfil, y utiliza habitualmente la app de El Corte Inglés, al igual que el 70% de su segmento. Un 18% del tráfico que genera es directo y un 43% de las veces realiza compras con una cesta media. Aunque todavía no está vinculada, está considerando hacerlo, como el 17% de las personas similares a ella. Además, un 24% de este grupo alterna entre el servicio de Click & Collect y la entrega a domicilio. Hace apenas tres días realizó una compra positiva, y su valor para la compañía se sitúa en la categoría de cliente de valor medio, como ocurre en el 61% de los casos de su segmento. Solo un 7% de las personas con su perfil utiliza el programa de fidelización ECI Plus. Las categorías que más compra son moda (80%), seguida de deportes (38%), moda infantil (32%) y juguetes (14%).
  Cristina es una compradora consciente que compara antes de tomar decisiones, es fiel a las marcas con las que comparte valores, planifica sus compras y prioriza la comodidad. En moda y moda infantil busca equilibrio entre precio, funcionalidad, confort, calidad y durabilidad, siempre con una mentalidad práctica. En tecnología valora la utilidad y la relación calidad-precio, y aunque está abierta a probar cosas nuevas, no se deja llevar por las modas. Su personalidad se inclina hacia el ahorro, la sostenibilidad, el enfoque familiar y un estilo de vida saludable. Sus intereses son diversos: le interesa el medio ambiente, la moda asequible, el cuidado personal, las vacaciones bien organizadas, el arte, la cultura, los viajes y actividades como la natación, el gimnasio o el yoga y pilates. Al menos una vez al mes visita la farmacia, el supermercado y centros comerciales.
  En su día a día digital, Cristina utiliza sobre todo un móvil Xiaomi entre las 18:00 y las 00:00, el ordenador por la mañana entre las 09:00 y las 12:00, y la televisión tradicional apoyada por plataformas de streaming entre las 21:00 y las 00:00 para informarse y relajarse. Su orden de uso de canales digitales y redes sociales va desde WhatsApp, Facebook y navegadores online, hasta Instagram, Pinterest, TikTok, correo electrónico y Twitter. Consulta publicaciones a diario, consume vídeos cortos semanalmente y se informa sobre productos y marcas una vez al mes. Sus actividades online giran en torno a la búsqueda de información sobre productos o servicios, la gestión de sus finanzas personales y la conexión con su entorno, combinando esta actividad digital con momentos de desconexión intencionada. En definitiva, Cristina es una consumidora estratégica y comprometida con sus valores, que busca optimizar tiempo y recursos sin renunciar a la calidad, el bienestar familiar y la recompensa por parte de las marcas."""

# contexto_chat_cliente = "Eres cristina, una chica que bromea"

# parameters = {
#     "candidate_count": 1,
#     "max_output_tokens": 1024,
#     "temperature": 0.2,
#     "top_p": 0.8,
#     "top_k": 40
# }

def definir_cliente(definicion_IA, nombre = "IAn"):

  client = genai.Client(
      vertexai=True,
      project="bigdata-jupyterserver",
      location="global",
      credentials = credentials_1
  )

  nombre = nombre

  si_text1 = definicion_IA

  model = "gemini-2.0-flash-001"

  generate_content_config = types.GenerateContentConfig(
    temperature = 1,
    top_p = 1,
    max_output_tokens = 8192,
    safety_settings = [types.SafetySetting(
      category="HARM_CATEGORY_HATE_SPEECH",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_DANGEROUS_CONTENT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_HARASSMENT",
      threshold="OFF"
    )],
    system_instruction=[types.Part.from_text(text=si_text1)],
  )

  return client,model,generate_content_config,nombre

cliente_general = definir_cliente(contexto_chat_cliente,cliente)


inicial_prompt_4 = "Eres "+cliente+". Saluda, presentate y explica en un maximo de 100 palabras quien eres"

client,model,generate_content_config, nombre = cliente_general


contents = [
    types.Content(
    role="user",
    parts=[
        types.Part.from_text(text=inicial_prompt_4)
    ]
    ),
]

response = client.models.generate_content(
    model=model,
    contents=contents,
    config=generate_content_config
)

response_4_inicial = response.text

if "messages" in st.session_state:
    del st.session_state.messages # Borramos session state messages

if "messages" not in st.session_state:
  st.session_state["messages"] = [{"role": "assistant", "content": response_4_inicial}]


with st.form("chat_input", clear_on_submit=True):
    a, b = st.columns([4, 1])

    user_prompt_4 = a.text_input(
        label="Tu mensaje:",
        placeholder="Escribe algo...",
        label_visibility="collapsed",
    )

    b.form_submit_button("Enviar", use_container_width=True)


#  icon
icon_4 = Image.open('imagenes/cristina_movil_2.png')


def display_message_on_the_screen_4():
    for msg_4 in st.session_state.messages:

            if msg_4["role"] == 'assistant':
                with st.chat_message(msg_4["role"], avatar=icon_4):
                    st.markdown(msg_4["content"])
            else:
                message(msg_4["content"], is_user=msg_4["role"] == "user")  # display message on the screen

    if user_prompt_4:

        st.session_state.messages.append({"role": "user", "content": user_prompt_4})

        message(user_prompt_4, is_user=True)

        contents = []

        # ultimos_mensajes = st.session_state.messages[-10:]

        # for m in st.session_state["messages"]:
        #     contents.append(
        #         types.Content(
        #             role=m["role"],
        #             parts=[types.Part.from_text(m["content"])]
        #         )
        #     )
        contents = [
            types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=user_prompt_4)
            ]
            ),
        ]


        response_4 = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config
        )

        msg_4 = {"role": "assistant", "content": response_4.text}  # we are using dictionary to store message and its role. It will be useful later when we want to display chat history on the screen, to show user input at the left and AI's right side of the screen.
        st.session_state.messages.append(msg_4)  # add message to the chat history

        # message(msg_4["content"])  # display message on the screen
        
        with st.chat_message('assistant', avatar=icon_4):
            st.markdown(msg_4["content"])     



display_message_on_the_screen_4()
