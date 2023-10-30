import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

# URL de la página web que deseas analizar
url = 'https://visuales.uclv.cu/Series/Ingles/The.Walking.Dead.Daryl.Dixon'

# Realizar la solicitud GET a la página web
response = requests.get(url)

# Comprobar si la solicitud fue exitosa
if response.status_code == 200:
    # Crear un objeto BeautifulSoup para analizar el contenido HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscar todos los enlaces (links) en la página
    links = soup.find_all('a')
    
    # Carpeta de destino para guardar los archivos
    carpeta_destino = 'Descargas'
    os.makedirs(carpeta_destino, exist_ok=True)

    # Lista de extensiones de archivos de video y subtítulos
    extensiones_permitidas = ['.mkv', '.mp4', '.avi', '.srt', '.sub', '.vtt', '.ass']

    # Iterar a través de los enlaces y descargar los archivos de video y subtítulos
    for link in links:
        href = link.get('href')
        for extension in extensiones_permitidas:
            if href.endswith(extension):
                # Construir la URL completa del archivo
                archivo_url = f'{url}/{href}'
                
                # Nombre del archivo local (separando el nombre del archivo del enlace)
                nombre_archivo = href.split('/')[-1]
                
                # Ruta completa del archivo de destino
                ruta_archivo_destino = os.path.join(carpeta_destino, nombre_archivo)

                # Descargar el archivo con barra de progreso
                with requests.get(archivo_url, stream=True) as r:
                    r.raise_for_status()
                    with open(ruta_archivo_destino, 'wb') as f:
                        total_size = int(r.headers.get('content-length', 0))
                        with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                            for chunk in r.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                                    pbar.update(len(chunk))

                print(f'Descargado: {nombre_archivo}')

    print('Descarga completa.')
else:
    print('No se pudo acceder a la página.')
