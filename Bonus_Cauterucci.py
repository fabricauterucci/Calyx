import numpy as np
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys


firefoxOptions = Options()

# para que funcione en otro escritorio hay que cambiar el directorio actual, por
s = Service('/home/fcaute/Escritorio/Challenge/Bot Cotizacion_Cauterucci/drivers/geckodriver')
# el directorio que contiene geckodriver en la pc donde se ejecuta el bot

browser = webdriver.Firefox(service=s, options=firefoxOptions)
firefoxOptions.add_argument("-headless")

browser.get('https://www.bna.com.ar/Personas')
billetes = browser.find_element_by_id('billetes')
#print(billetes.text)

lista_billetes = list(billetes.text)
contenedor_cad = []

limite = len(lista_billetes)
lista_temp = []

for i in range(0,limite-1):
    if (lista_billetes[i] != ' ' and lista_billetes[i] != '\n'):
        if(lista_billetes[i] == ','):
            lista_temp += ['.']
        else:
            lista_temp += [lista_billetes[i]]
    
    if(lista_billetes[i+1] == ' ' or lista_billetes[i+1] == '\n' ):
        lista_temp = "".join(lista_temp)
        if(lista_temp != 'U.S.A' and lista_temp != '*' and lista_temp != 'Ver'):
            contenedor_cad += [lista_temp]
        if(lista_temp == 'Ver'):
            break
        lista_temp = list(lista_temp)
        lista_temp = []


def quitar_ceros(cadena):
#La funcion quitar ceros, quita los ceros que le siguen a los numeros no nulos luego de la coma
# y si es un numero entero, tambien quita la coma
    flag = 0
    cadenab = ''
    contador = 0
    for i in cadena:
        if(i == '.'):
            flag = 1
        if (flag == 1):
            if ( i != '0'):
                cadenab += i
                contador += 1
            elif(flag == 1 and i == '0' and contador == 1):
                return cadenab[:-1]
        else:
            cadenab += i
    return cadenab

#aplicamos quitar cero a las posiciones que nos interesan
# me hubiera gustado hacer un for, pero los pasos de salto eran raros
# entonces los hice manualmente (primero avanza de a uno, y luego de a dos
contenedor_cad[4] = quitar_ceros(contenedor_cad[4])
contenedor_cad[5] = quitar_ceros(contenedor_cad[5])
contenedor_cad[7] = quitar_ceros(contenedor_cad[7])
contenedor_cad[8] = quitar_ceros(contenedor_cad[8])
contenedor_cad[10] = quitar_ceros(contenedor_cad[10])
contenedor_cad[11] = quitar_ceros(contenedor_cad[11])

#mostramos como nos queda la lista pasada en limpio, aunque nos queda agregar
# el promedio
print(contenedor_cad)

#Creamos un archivo de excel
workbook = xlsxwriter.Workbook('Cotizacion_Cauterucci.xlsx')
#Agregamos una hoja de calculo
worksheet = workbook.add_worksheet()

#Escribimos en la primer fila, Dia y la variable contenedor cad que va a mostrar
# el dia que se consulte la cotizacion en la primera y segunda columna
worksheet.write_string  (0, 0,"Día")
worksheet.write_string  (0, 1,contenedor_cad[0])

#Pisamos en la lista el dia ya que ya no lo necesitamos, e insertamos la
# cadena 'Moneda' y agregamos otro elemento a la lista (Promedio)
contenedor_cad[0] = 'Moneda'
contenedor_cad.insert(3,'Promedio')

#Agregamos los promedios entre la compra y venta del dolar, euro y real
#primero convertimos la cadena a float, para sumar y dividir por 2, y luego
# la volvemos a transformar a string, luego le quitamos los ceros si es que tiene
contenedor_cad.insert(7,quitar_ceros(
    str((float(contenedor_cad[5])+float(contenedor_cad[6]))/2)))
                  
contenedor_cad.insert(11,quitar_ceros(
    str((float(contenedor_cad[9])+float(contenedor_cad[10]))/2)))
                         
contenedor_cad.insert(15,quitar_ceros(
    str((float(contenedor_cad[13])+float(contenedor_cad[14]))/2)))


matriz_cotizacion = np.array(contenedor_cad).reshape(4,4)
# Hacemos la traspuesta de la matriz, ya que la matriz
# resultante muestra las filas en lugar de las columnas, y deseamos verla
# al reves
matriz_cotizacion = np.transpose(matriz_cotizacion)

#Insertamos la matriz en la fila 1, es decir la segunda fila
# ya que en la primera va a situarse el Dia
row = 1
for col, data in enumerate(matriz_cotizacion):
    worksheet.write_column(row, col, data)


workbook.close()

browser.quit()
