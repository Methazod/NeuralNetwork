"""
Clase que crea un csv al recibir comentarios

Jorge Manzano Anchelergues y Jaime Usero Aranda.
"""
class SentimentDataset:
    """
    Inicializa la clase con el nombre del archivo CSV donde se guardarán los datos.
    Si no se introduce un nombre se guardara con el nombre noname.csv
    """
    def __init__(self, path: str, cabecera, filename = 'noname.csv'):        
        self.filename = path + "/" + filename
        # Escribe la cabecera solo si el archivo no existe
        try:
            file = open(self.filename, mode='x', encoding='utf-8')
        except FileExistsError:
            pass
        else:
            texto = ""
            for palabras in cabecera:
                texto += str(palabras) + ","
            file.writelines(texto.removesuffix(","))

    """
    Convierte un texto en su forma limpia: sin signos, acentos ni caracteres especiales.
    Conserva los espacios y transforma a minúsculas, añade una comilla simple
    al principio y al final del texto.
    """
    def normalToPlano(self, palabra: str):        
        palabra = palabra.upper()
        borrarSignos = "!¡?¿,.'`;/\\|[]}{()€%&$·#@¬=*+-_:<>~^"
        vocalesAcentos = "ÁÉÍÓÚÄËÏÖÜÂÊÎÔÛ"
        vocales = "AEIOU"
        palabra = palabra.replace('"', "")
        
        # Eliminar signos de puntuación, conservando espacios
        for signo in borrarSignos:
            palabra = palabra.replace(signo, "")
        
        # Reemplazar vocales acentuadas por vocales sin acento
        iterador = 0
        for letra in vocalesAcentos:
            palabra = palabra.replace(letra, vocales[iterador])
            iterador = (iterador + 1) % len(vocales)
        
        # Retorna el texto normalizado en minúsculas y entre comillas
        return f'"{palabra.lower()}"'

    """
    Agrega una entrada al csv.
    """
    def add_entry(self, linea: list):                
        with open(self.filename, mode='a', encoding='utf-8') as file:
            texto = ""
            for palabras in linea:
                texto += str(palabras) + ","
            texto = " ".join(texto.split())
            file.writelines("\n" + texto.removesuffix(","))
            
    
    """
    Carga los datos del archivo CSV y devuelve una lista.
    """
    def load_data(self):        
        data = []
        with open(self.filename, mode='r', encoding='utf-8') as file:            
            lineas = file.readlines()
            lineas.pop(0)
            for row in lineas:                
                data.append(row.strip(","))
        return data