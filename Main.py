import re
"""
Jorge Manzano Anchelergues y Jaime Usero Aranda
"""
from WebScrapperFilmAffinity import WebScrapper
from CrearCSV import SentimentDataset

comentarios = WebScrapper(10000).getComentarios()

abecedario = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
    'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q',
    'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    ' ', '1', '2', '3', '4', '5', '6', '7', '8',
    '9', '0', '"', 'Ō', 'Š', 'Ç'
]

signos = []
for comentario in comentarios:
  for letra in comentario[0].upper():
    if(letra not in abecedario):
      if(letra not in signos):
        signos.append(letra)

for comentario in comentarios:
    for signo in signos:
       comentario[0] = comentario[0].replace(signo, "")
    comentario[0] = re.sub(r'\s+', ' ', comentario[0])

# Mirar 9994, 9968

if(len(comentarios) >= 10000):
    csv = SentimentDataset("./2º año/sistemasGestion/practicas/Neural Network" ,["comentario", "sentimiento"], 
                        "sentimientos.csv")
    for coment in comentarios:
        csv.add_entry([coment[0], coment[1]])