from utils import *

root_url = "https://www.dia.es"                     # Establecer la URL de base de la web
soup = get_soups(root_url + "/compra-online/")      # Conseguir el 'soup' de la web de inicio de compra
departamentos = get_dptos(soup)                     # Array con las URLs de cada departamento
final = []                                          # Array que contendrá todos los productos y sus precios clasificados

# Iterar sobre todos los departamentos menos el último (tokens solidarios)
for dpto in departamentos[0:-1]:
    final.append(get_products(dpto, root_url))
    print(final[-1][0])                             # Imprimir en consola el nombre del departamento que se ha procesado

# Creación del archivo csv de salida con los datos de interés
with open('productos_supermercado_dia.csv', 'w') as f:
    f.write("Sección;Descripción;Precio_EUR\n")     # Encabezados
    for cat in final:
        dep = cat[0]
        for prod in cat[1:]:
            f.write(dep + ";" + prod[0] + ";" + prod[1] + "\n")