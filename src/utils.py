# Carga de bibliotecas necesarias
import re
from bs4 import BeautifulSoup
import requests


# Función que permite acceder al html de las páginas web mediante BeautiflSoup
def get_soups(url):
    html_text = requests.get(url).content
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup


# Función que permite navegar por los elementos del html y construir las urls de las secciones del catálogo
def get_dptos(soup):
    nav_sub_cont = soup.find_all("ul", {"id": "nav-submenu-container"})
    nav_submenu = nav_sub_cont[0]
    urls = []
    for item in nav_submenu:
        if item.name and "iconoCat" in item.contents[1].attrs['class']:
            href = item.find('a', href=True)
            urls.append(href.get('href'))
    return urls


# Función que permite construir las urls para acceder a cada producto
def get_products(dpto, root_url):
    products = []                                  # Array de arrays con la descripición y el precio de cada producto
    show_dpto = root_url + dpto
    soup = get_soups(show_dpto)
    products.append(soup.h1.text)                  # La primera entrada en el array es el nombre del departamento

# Bucle para recopilar los elementos de las páginas de los productos que interesan
    while soup is not None:
        forms = soup.find_all('form')
        for f in forms:
            if len(f.contents) == 15:
                name = f.attrs['data-productdescription']
                name = re.sub("\\n", "", name)     # Eliminar el salto de línea al final de la descripción
                price = f.find('input', class_="price").attrs['value']
                products.append([name, price])
        nx = soup.find('a', rel="next")            # Buscar el botón 'Siguiente Página'
        soup = None
        if nx is not None:                         # Si el botón existe, obtener el 'soup' de la siguiente página
            nx_url = nx.get("href")
            soup = get_soups(root_url + nx_url)

    return products
