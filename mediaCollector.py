import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

def descargar_archivo(url, carpeta_destino):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))

        nombre_archivo = url.split('/')[-1]
        ruta_archivo_destino = os.path.join(carpeta_destino, nombre_archivo)

        with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
            pbar.set_description(f'Descargando: {nombre_archivo}')
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    with open(ruta_archivo_destino, 'ab') as f:
                        f.write(chunk)
                    pbar.update(len(chunk))
        print(f'Descargado: {nombre_archivo}')

def descargar_carpeta(url, carpeta_destino_base):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')

        # Obtener el último segmento de la URL como nombre de carpeta
        nombre_carpeta = url.split('/')[-1]
        carpeta_destino = os.path.join(carpeta_destino_base, nombre_carpeta)
        os.makedirs(carpeta_destino, exist_ok=True)

        for link in links:
            href = link.get('href')
            if href.endswith('/'):
                carpeta_url = f'{url}/{href}'
                nombre_carpeta = href.rstrip('/')
                carpeta_destino_carpeta = os.path.join(carpeta_destino, nombre_carpeta)
                os.makedirs(carpeta_destino_carpeta, exist_ok=True)
                descargar_carpeta(carpeta_url, carpeta_destino_carpeta)
            else:
                for extension in extensiones_permitidas:
                    if href.endswith(extension):
                        archivo_url = f'{url}/{href}'
                        descargar_archivo(archivo_url, carpeta_destino)

if __name__ == '__main__':
    url = input('Inserte una URL para comenzar la descarga: ')
    carpeta_destino_base = 'Descargas'
    os.makedirs(carpeta_destino_base, exist_ok=True)
    extensiones_permitidas = ['.mkv', '.mp4', '.avi', '.srt', '.sub', '.vtt', '.ass', '.jpg', '.jpeg', '.png']

    descargar_carpeta(url, carpeta_destino_base)
    print('Descarga completa.')
