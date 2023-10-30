import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

# URL de la página web que deseas analizar
url = 'https://visuales.uclv.cu/Series/Ingles/The.Walking.Dead.Daryl.Dixon'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = soup.find_all('a')
    
    carpeta_destino = 'Descargas'
    os.makedirs(carpeta_destino, exist_ok=True)

    extensiones_permitidas = ['.mkv', '.mp4', '.avi', '.srt', '.sub', '.vtt', '.ass']

    total_size_general = 0  # Tamaño total de todos los archivos
    total_descargado_general = 0  # Tamaño descargado hasta el momento de todos los archivos

    for link in links:
        href = link.get('href')
        for extension in extensiones_permitidas:
            if href.endswith(extension):
                archivo_url = f'{url}/{href}'
                
                nombre_archivo = href.split('/')[-1]
                
                ruta_archivo_destino = os.path.join(carpeta_destino, nombre_archivo)

                # Verificar si el archivo ya existe en la carpeta de destino
                if not os.path.exists(ruta_archivo_destino):
                    with requests.get(archivo_url, stream=True) as r:
                        r.raise_for_status()
                        total_size = int(r.headers.get('content-length', 0))

                        # Barra de progreso individual para cada archivo
                        with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                            pbar.set_description(f'Descargando: {nombre_archivo}')  # Establecer el nombre del archivo
                            for chunk in r.iter_content(chunk_size=8192):
                                if chunk:
                                    with open(ruta_archivo_destino, 'ab') as f:
                                        f.write(chunk)
                                    total_descargado_general += len(chunk)
                                    pbar.update(len(chunk))
                    print(f'Descargado: {nombre_archivo}')

                    # Actualizar la barra de progreso general
                    with tqdm(total=total_size_general, unit='B', unit_scale=True, unit_divisor=1024) as pbar_general:
                        pbar_general.update(total_descargado_general - pbar_general.n)
                else:
                    print(f'El archivo {nombre_archivo} ya existe, se omitirá la descarga.')

    print('Descarga completa.')
else:
    print('No se pudo acceder a la página.')
