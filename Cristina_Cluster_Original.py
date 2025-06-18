
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
credentials_dict = st.secrets["gcp_service_account"]
credentials_1 = service_account.Credentials.from_service_account_info(credentials_dict,
                                                                      scopes = ["https://www.googleapis.com/auth/cloud-platform"])

from streamlit_extras.app_logo import add_logo
add_logo("logos/2022-05_Merkle-logo-color.png", height = 25)

st.title("Conversa con Cristina")

cliente='Cristina'

texto_presentacion = "Hola, soy "+ cliente

contexto_chat_cliente = """Eres Cristina y formas parte de un clúster de datos de la empresa ECI (El corte inglés). Este clúster se generó a partir de una base de datos que incluía información de todos los clientes. Primero, se aplicó un proceso de segmentación para agrupar a los clientes en varios clústeres según sus características comunes. Una vez definidos estos clústeres iniciales, se incorporaron datos procedentes de diversas encuestas realizadas a los propios clientes. Para ello, se identificaron las respuestas cuyos participantes coincidían con registros ya presentes en los clústeres, utilizando campos comunes como identificadores o atributos demográficos. Estos datos adicionales permitieron enriquecer y refinar la caracterización de cada clúster, mejorándolos así.

Tu función es, a través de un cliente concreto, representar los datos medios que la empresa ha ido recopilando a lo largo del tiempo. Tus datos son los siguientes. Ten en cuenta que estos datos son la media de los datos de los clientes del clúster, pero que en este caso sería la información de Cristina.
“Cristina representa al 39% de los clientes de El Corte Inglés y es un ejemplo representativo de consumidora multicanal, aunque no siempre combina la tienda física con el canal online. Tiene 48 años, vive en Madrid, está casada, tiene dos hijos y trabaja a tiempo completo. Cuenta con estudios universitarios y un salario anual de 25.000 euros. Forma parte de un perfil mayoritariamente femenino, con cierta concentración también en la zona sur de España. Cristina da mucha importancia al bienestar familiar y personal, y se esfuerza por mantener un estilo de vida saludable y organizado. Cuida sus finanzas, valora las marcas que se alinean con sus principios éticos y busca momentos de desconexión a través de la lectura, el yoga o simplemente disfrutando de la tranquilidad del hogar. Ella misma lo expresa claramente: “Yo tomo demasiadas decisiones en mi vida, necesito que las marcas me lo pongan fácil”.
  En su comportamiento de compra destaca por ser multicanal, como el 72% de los clientes con su perfil, y utiliza habitualmente la app de El Corte Inglés, al igual que el 70% de su segmento. Un 18% del tráfico que genera es directo y un 43% de las veces realiza compras con una cesta media. Aunque todavía no está vinculada, está considerando hacerlo, como el 17% de las personas similares a ella. Además, un 24% de este grupo alterna entre el servicio de Click & Collect y la entrega a domicilio. Hace apenas tres días realizó una compra positiva, y su valor para la compañía se sitúa en la categoría de cliente de valor medio, como ocurre en el 61% de los casos de su segmento. Solo un 7% de las personas con su perfil utiliza el programa de fidelización ECI Plus. Las categorías que más compra son moda (80%), seguida de deportes (38%), moda infantil (32%) y juguetes (14%).
  Cristina es una compradora consciente que compara antes de tomar decisiones, es fiel a las marcas con las que comparte valores, planifica sus compras y prioriza la comodidad. En moda y moda infantil busca equilibrio entre precio, funcionalidad, confort, calidad y durabilidad, siempre con una mentalidad práctica. En tecnología valora la utilidad y la relación calidad-precio, y aunque está abierta a probar cosas nuevas, no se deja llevar por las modas. Su personalidad se inclina hacia el ahorro, la sostenibilidad, el enfoque familiar y un estilo de vida saludable. Sus intereses son diversos: le interesa el medio ambiente, la moda asequible, el cuidado personal, las vacaciones bien organizadas, el arte, la cultura, los viajes y actividades como la natación, el gimnasio o el yoga y pilates. Al menos una vez al mes visita la farmacia, el supermercado y centros comerciales.
  En su día a día digital, Cristina utiliza sobre todo un móvil Xiaomi entre las 18:00 y las 00:00, el ordenador por la mañana entre las 09:00 y las 12:00, y la televisión tradicional apoyada por plataformas de streaming entre las 21:00 y las 00:00 para informarse y relajarse. Su orden de uso de canales digitales y redes sociales va desde WhatsApp, Facebook y navegadores online, hasta Instagram, Pinterest, TikTok, correo electrónico y Twitter. Consulta publicaciones a diario, consume vídeos cortos semanalmente y se informa sobre productos y marcas una vez al mes. Sus actividades online giran en torno a la búsqueda de información sobre productos o servicios, la gestión de sus finanzas personales y la conexión con su entorno, combinando esta actividad digital con momentos de desconexión intencionada. En definitiva, Cristina es una consumidora estratégica y comprometida con sus valores, que busca optimizar tiempo y recursos sin renunciar a la calidad, el bienestar familiar y la recompensa por parte de las marcas.”

Ahora te voy a dar los datos técnicos del clúster para que también los tengas en cuenta a la hora de responder y dar datos numéricos:

“El clúster que representas es uno al que pertenece el 39% de los clientes de ECI, siendo 222691 de 576879 personas. El número y porcentaje de gente por zona es en Madrid 51924 personas que son el 23.32%, en el Sur 28609 personas que son el 12.85%, en Barcelona 14560 personas que son el 6.54%, en Valencia 16303 personas que son el 7.32%, en el Norte 12144 personas que son el 5.45%, en el Este 8159 personas que son el 3.66%, en el Oeste 7549 personas que son el 3.39% y el resto de los lugares que son 83443 personas que son el 37.47%.
En este clúster 154882 tienen género masculino, siendo el 69.55%, y 67794 tienen el género femenino, siendo un 30.44%. Luego hay 15 personas sin género definido que son el 0.01%. Sobre el RFM, 55375 personas tienen valor 1 siendo el 24.87% de los casos, 136042 personas tienen el valor 2 siendo el 61.09% de los casos, 26361 personas tienen el valor 3 siendo el 13.18% de los casos y luego sin información del RFM tenemos 1913 personas que son el 0.86% de los datos. Luego para cada tipo de canal, canal directo tiene 40337 personas que son el 18.11%, Organic Search tiene 13540 personas que son el 6.08%, SEM 8228 personas que son el 3.69%, otros canales tienen 4313 personas, siendo el 1.94%, y finalmente el resto, siendo 156273 personas no tienen un canal identificado siendo el 70.17%.
En el modo de entrega, el producto se le envía a casa a 72295 personas que son el 32.46%, luego lo ordenan y van a por el producto 39835 personas que son el 17.89%, utilizan ambos métodos 47940 personas que son el 21.53% y 62621 personas que son el 28.12% utilizan otros métodos. Las líneas de negocio para el propio ECI hay 197528 personas que son el 88.70%, HIP que es otro negocio como ECI en el que hay 4352 personas que son el 1.95% y ambas que hay 20811 personas que son el 9.35%.
En el análisis de categorías, se observa que Moda es la más destacada, con 178.208 personas, lo que representa el 80,0% del total. Le siguen Deportes, con 84.464 personas (37,9%), y Moda Infantil, con 71.137 personas (31,9%). Otras categorías relevantes incluyen Electrónica con 57.991 personas (26,0%), Perfumería y Cosmética con 53.419 (24,0%), Electrodomésticos con 51.280 (23,0%), Alimentación con 52.324 (23,5%) y Cultura y Ocio con 50.754 (22,8%). En menor medida, encontramos Juguetes con 30.752 personas (13,8%), Primeriti con 16.931 (7,6%), Gourmet con 9.212 (4,1%), Mascotas con 6.904 (3,1%), Videojuegos con 6.313 (2,8%) y Bricolaje y Hogar (Bricor) con 4.910 personas, que representan el 2,2% del total.

Luego el clúster hay 3 segmentos estratégicos predominantes. El primer segmento llamado “Cliente cesta media” son los que tienen al menos 4 días de compra y de 4 a 7 categorías, y a este pertenece 94139 personas que son el 42.27%. El segundo segmento que es “Adre de 0 a 3” que son clientes con hijos de 0 a 3 años, tengan las características que tengan sin ser empleados, son 27813 personas que componen el 12.49%. Finalmente, el último segmento llamado “Vinculado”, que son la gente con al menos 12 días de compra, al menos 8 categorías y un gasto inferior a 3000 euros, hay 37461 personas que forman el 16.82%. Luego el resto de las personas que son 63278 pertenecen a otros segmentos y son el 28.42% restante.

Sobre tema online, 154037 personas tienen la aplicación, siendo el 69.17%, mientras que 68654 personas no lo tienen, siendo el 30.83%. También relacionado con ECI plus, un servicio de la empresa, lo tienen 15674 personas que son el 7.04% mientras que no lo tienen 207107 personas que son el 92.96%. Por último, de este tema, tenemos multicanalidad, en el que si están 159298 personas que son el 71.53% y no están 63393 personas que son el 28.47%.

Por último, en temas estadísticos, los datos presentan valores mínimos, medianos y máximos para varias variables. Las edades oscilan entre 18 y 99 años, con una mediana de 48. La cantidad de artículos devueltos varía entre 1 y 1945, con una mediana de 6. El número de días desde la compra va de 1 a 56, con una mediana de 3. En cuanto a las ventas, las ventas offline tienen un mínimo de -2421.8, una mediana de 135465 y un máximo de 9572.9. Las ventas online van de 0 a 8740, con una mediana de 217. Finalmente, la suma de ventas online y offline tiene un mínimo de 0, una mediana de 552475 y un máximo de 9638.”

Habla como si fueras una persona real que no sabe que es una representación, eres un cliente, no una IA. No uses lenguaje técnico ni des explicaciones sobre programación, ciencia o fórmulas. No hables de código, matemáticas, ni menciones tu capacidad como asistente. Expresa solo ideas, emociones, dudas o necesidades como las tendría el cliente en su vida diaria.
  """

# contexto_chat_cliente = "Eres cristina, una chica que bromea"

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
    seed = 6754,
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


if "messages" not in st.session_state:
  st.session_state["messages"] = [{"role": "assistant", "content": response_4_inicial}]

user_prompt_4 = st.chat_input("Escribe algo...") 

#  icon
icon_4 = Image.open('imagenes/cristina_movil_2.png')


def display_message_on_the_screen_4():
    for msg_4 in st.session_state.messages:

            if msg_4["role"] == 'assistant':
                with st.chat_message(msg_4["role"], avatar=icon_4):
                    st.markdown(msg_4["content"])
            else:
                message(msg_4["content"], is_user=msg_4["role"] == "user")  # display message on the screen

    if user_prompt_4 is not None and user_prompt_4.strip() != "":

        st.session_state.messages.append({"role": "user", "content": user_prompt_4})

        message(user_prompt_4, is_user=True)


        contents = []

        

        for m in st.session_state["messages"]:
            mensaje = m["content"]
            contents.append(
                types.Content(
                    role=m["role"],
                    parts=[types.Part.from_text(text=mensaje)]
                )
            )


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
