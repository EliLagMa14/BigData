import pandas as pd

url  = 'https://raw.githubusercontent.com/sundeepblue/movie_rating_prediction/master/movie_metadata.csv'

df =  pd.df = pd.read_csv(url)

#1.- La columna gross posee valores en blanco o nulos, estos deben ser rellenados con el valor promedio de todos los valores de esa columna.
meno = df['gross'].mean()

df['gross'].fillna(meno, inplace=True)

#2.- El atributo o columna facenumber_in_poster posee valores nulos o en blanco y valores negativos, los cuales deber rellenados o reemplazados con el valor de cero 0.
df['facenumber_in_poster'].fillna(0, inplace=True)

df.loc[df['facenumber_in_poster']< 0, 'facenumber_in_poster'] = 0

#3.- Crear una nueva columna denominada TittleCode y los valores que serán asignados resultar de realizar una extracción o subcadena de la columna movie_imdb_link. Ejemplo: http://www.imdb.com/title/tt0499549/?ref_=fn_tt_tt_1    se extrae el dato:  tt0499549

df['TitleCode'] = df['movie_imdb_link'].str.extract('(/title/(tt\d+))').iloc[:, 1]

#4.- La columna title_year posee valores en blanco o nulos, se debe rellenar todas esas celdas con el valor de cero 0.
df['title_year'].fillna(0, inplace=True)

#5.- Realizar una selección de todas las filas (Rows) de las Movies filmadas en "USA" tomando como referencia la columna country; posteriormente eliminar las filas restantes en el dataframe.
city = df[df['country'] == 'USA']

city.to_csv("C:/Users/LAMAEL/Documents/8° semestre/Big Data/FilmTV_USAMovies.csv", index=False)
