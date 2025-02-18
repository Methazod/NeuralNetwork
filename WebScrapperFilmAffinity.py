from bs4 import BeautifulSoup
import requests, time, random
from CrearCSV import SentimentDataset

"""
Clase que crea un objeto que web scrappea filmaffinity

Jorge Manzano Anchelergues y Jaime Usero Aranda
"""

class WebScrapper:
    # Ctor que carga los comentarios
    def __init__(self, maxComentarios):
        self.comentarios = []
        self.csv = SentimentDataset("./2º año/sistemasGestion/practicas/Neural Network",
                                    ["comentario","sentimiento", "pelicula"] ,"scrap.csv")
        comentariosPorPelicula = self.loadCSVData()
        if(len(self.comentarios) <= maxComentarios):
            try:
                currentPage = int(comentariosPorPelicula[-1]/5)
                arrLen = len(comentariosPorPelicula)-1
            except:
                self.loadComentarios(self.getURLsReviews(), maxComentarios)
            else:
                self.loadComentarios(self.getURLsReviews(), maxComentarios, currentPage, arrLen)

    # Metodo que carga la lista de comentarios con el fichero scrap.csv si no esta vacio
    def loadCSVData(self):
        comentariosPorPelicula = []
        for linea in self.csv.load_data():
            partes = linea.split(",")        
            self.comentarios.append([partes[0], int(partes[1])])
            index = int(partes[2].replace("\n", ""))
            try:
                comentariosPorPelicula[index]
            except IndexError:
                comentariosPorPelicula.append(1)
            else:
                comentariosPorPelicula[index] += 1                       
        return comentariosPorPelicula

    # Devuelve los comentarios
    def getComentarios(self):
        return self.comentarios

    # Metodo que carga una lista con la primera URL de los comentarios de cada pelicula
    def getURLsReviews(self):
        # Extraer el codigo html        
        soup = self.getRequest("https://www.filmaffinity.com/es/ranking.php?rn=ranking_fa_movies")
        # Obtenemos todas los <li> de las reviews de las peliculas
        listas = soup.find(id="top-movies").find_all("li", class_="content")
        # 
        soup = self.getRequest("https://m.filmaffinity.com/es/listtopmovies.php?list_id=101")
        trTags = soup.find("div", class_="listrank-page").find("table", class_="table mt-3 mb-0").find_all("tbody")[-1].find_all("tr")
        URLs = []
        for num in range((len(listas) + len(trTags))):            
            # Obtenemos la url de la pelicula y la separamos por las barras para formatearla
            if(num < len(listas)): 
                element = listas[num]
                url = element.find("div", class_="movie-card mc-flex movie-card-0")
            else:
                element = trTags[num - len(listas)]
                url = element.find("div", class_="row movie-card movie-card-1")
            try:
                url = url.find("a")['href'].split("/")
            except:
                continue
            else:
                # Formateamos la url para obtener la pagina de los comentarios
                url = (url[0] + "//" + url[2] + "/" + url[3] + "/reviews/1/" 
                    + url[4].replace("f", "").replace("i", "").replace("l", "").replace("m", "") + "ml")
                
                # Guardamos la url
                URLs.append(url)            
        return URLs
    
    # Metodo que carga los comentarios haciendo web scrapping
    def loadComentarios(self, URLs, maxComentarios, currentPage = 1, arrayIndex = 0):                                      
        # Recorremos las urls
        for num in range(arrayIndex, len(URLs)):                        
            url = URLs[num]
            try:
                # Sacamos la ultima pagina
                lastPage = int(self.getRequest(url).find("main").find("div", class_="pager").find_all("a")[-2].get_text())
            except:                
                try:
                    lastPage = int(self.getRequest(url).find("div", class_="center-pager").find("div",
                            class_="pager").find_all("a")[-2].get_text())
                except:
                    continue

            # Recorremos todas las paginas
            while currentPage < lastPage:   
                # Miramos si ya tenemos los comentarios que queremos
                if(len(self.comentarios) >= maxComentarios):                
                    return                 
                #Obtener el html parseado
                if(currentPage != 1):          
                    newUrl = url.split("/")
                    newUrl = (newUrl[0] + "//" + newUrl[2] + "/" + newUrl[3] + "/" + newUrl[4] + "/" + str(currentPage) + "/"
                              + newUrl[6])
                    soup = self.getRequest(newUrl)
                else:
                    soup = self.getRequest(url)
                try:
                    # Sacamos los comentarios                       
                    comentariosPelicula = soup.find_all("div", class_="fa-shadow movie-review-wrapper rw-item")          
                except:
                    continue
                # Recorremos los comentarios
                for comentario in comentariosPelicula:                    
                    # Sacamos la puntuacion
                    try:
                        rate = int(comentario.find("div", class_="user-reviews-movie-rating").get_text())
                    except:
                        continue
                    else:
                        # Decimos is un commentario es positivo o negativo
                        if(5 <= rate): # Positivo
                            self.comentarios.append(
                                    [
                                        self.csv.normalToPlano(comentario.find("div", class_="review-text1").get_text())
                                        , 1
                                    ]
                                )
                            self.csv.add_entry(
                                    [
                                        self.csv.normalToPlano(comentario.find("div", class_="review-text1").get_text())
                                        , 1
                                        , num
                                    ]
                                )
                        else: # Negativo
                            self.comentarios.append(
                                    [
                                        self.csv.normalToPlano(comentario.find("div", class_="review-text1").get_text())
                                        , 0
                                    ]
                                )
                            self.csv.add_entry(
                                    [
                                        self.csv.normalToPlano(comentario.find("div", class_="review-text1").get_text())
                                        , 0
                                        , num
                                    ]
                                )
                    print(len(self.comentarios))
                    print("")
                # Pasamos a la siguiente pagina
                currentPage += 1 
            currentPage = 1                

    # Metodo que hace un request dada una URL y devuelve el html parseado
    def getRequest(self, url):
        from fake_useragent import UserAgent
        # Duerme el programa para que no detecte que somos bots
        time.sleep(random.randint(1, 5))
        try:
            # Request de la pagina
            pagina = requests.get(url, headers={'User-Agent': UserAgent().random})
            pagina.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("Error"+ str(e) +". Vuelve a ejecutar")                                
            exit(0)
        except requests.exceptions.RequestException as e:
            time.sleep(60)
            self.getRequest(url)        
        else:
            # Parsea el requests para sacar el html
            return BeautifulSoup(pagina.content, "html.parser")        