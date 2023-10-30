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

    for link in links:
        href = link.get('href')
        for extension in extensiones_permitidas:
            if href.endswith(extension):
                archivo_url = f'{url}/{href}'
                
                nombre_archivo = href.split('/')[-1]
                
                ruta_archivo_destino = os.path.join(carpeta_destino, nombre_archivo)

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
