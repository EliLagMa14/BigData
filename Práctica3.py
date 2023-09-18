import folium
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image as PILImage
import io


df = pd.read_csv('new-york-city-art-galleries-1.csv')

# Eliminación de filas duplicadas
df.drop_duplicates(inplace=True)

# Eliminación de la columna 'ADDRESS2'
df.drop("ADDRESS2", axis=1, inplace=True)

# Filtrado de registros para galerías de arte en Brooklyn
brooklyn_art_galleries = df[(df['CITY'] == 'Brooklyn') & ((df['NAME'].str.contains('Museum')) | (df['NAME'].str.contains('Gallery')))]

# Ordenación del DataFrame basado en las calificaciones en orden descendente
df_ordenado = df.sort_values(by='GRADING', ascending=False)
tres_calificados = df_ordenado.head(3)

# Mostrar los 3 registros mejor calificados
print(tres_calificados)

# Creación del mapa centrado en una ubicación específica
m = folium.Map(location=[40.7037979,-74.0202391], zoom_start=10)

# Añadir marcadores para los tres registros mejor calificados al mapa
for index, row in tres_calificados.iterrows():
    name = row['NAME']
    address = row['ADDRESS1']
    lat, lon = map(float, row['the_geom'].replace('POINT (', '').replace(')', '').split())
    rating = row['GRADING']
    popup_text = f"Name: {name}<br>Address: {address} <br>Grade: {rating}"
    folium.Marker(location=[lat, lon], popup=popup_text).add_to(m)

# Guardar el mapa en un archivo HTML temporal
temp_html_file = 'temp_map.html'
m.save(temp_html_file)

# Convertir el mapa en una imagen PNG
img_data = m._to_png()
img = PILImage.open(io.BytesIO(img_data))
img.save('temp_map.png')

# Inicio de la creación del informe PDF
doc = SimpleDocTemplate("informe_final.pdf", pagesize=letter)
styles = getSampleStyleSheet()
contenido = []

# Añadir la imagen del mapa al contenido del PDF
imagen_mapa = Image("temp_map.png", width=500, height=400)
contenido.append(imagen_mapa)

# Añadir un título después de la imagen al contenido del PDF
titulo = "The best Galleries and Museums"
contenido.append(Paragraph(titulo, styles["Title"]))

# Añadir detalles de las tres galerías/museos principales al contenido del PDF
for index, row in tres_calificados.iterrows():
    name = row['NAME']
    address = row['ADDRESS1']
    rating = row['GRADING']
    texto_datos = f"Name: {name} Address: {address} Grade: {rating}"
    contenido.append(Paragraph(texto_datos, styles["Normal"]))

# Finalizar y guardar el informe PDF
doc.build(contenido)
