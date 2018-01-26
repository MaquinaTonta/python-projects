import re,random,time

###########DECLARACION DE FUNCIONES#############

#Obtiene las frecuencias de las palabras de un archivo dada su ruta
def freqLetINtxt(texto):
    palabras=texto.split()
    conteo={}
    cont=0
    for pal in palabras:
        for letra in pal:
            conteo[letra]=conteo.get(letra,0)+1
            cont+=1
    for elem in conteo:
        conteo[elem]=conteo[elem]/cont
    return conteo

#Carga un texto dada una ruta y regresa un string con el mismo texto
def loadTxt(fail):
    archivo=open(fail,'r')
    texto=archivo.read()
    archivo.close()
    return texto

#Recibe un texto del cual extraera se removera lo que este en el parametro "eliminar"
def elimIgual(cadena,eliminar):
    newCad=''
    for letra in cadena:
        if letra not in eliminar:
            newCad+=letra
    return newCad

#Reciba una cadena y regresa una nueva cadena sin elementos duplicados
def elimDup(cadena):
    newCad=''
    for letra in cadena:
        if letra not in newCad:
            newCad+=letra
    return newCad

#Determina si es posible agregar un elemento al diccionario en el metodo contarVecinos
def posibleAdd(let,dic):
    if let in 'abcdefghijklmnñopqrstuvwxyz':
        dic[let]=dic.setdefault(let,0)+1

#Regresa un diccionario de diccionarios con los "vecinos" de cada letra del texto de referencia
###Analisis para determinar la correspondencia de las letras mas frecuentes
###en el texto de referencia con las del texto cifrado
def contarVecinos(texto):
    vecDict={}
    cadenas=texto.split()
    for palabra in cadenas:
        for i in range(len(palabra)-1):
            vecLista=vecDict.setdefault(palabra[i],{})
            posibleAdd(palabra[i+1],vecLista)
            vecLista=vecDict.setdefault(palabra[i+1],{})
            posibleAdd(palabra[i],vecLista)
    return vecDict

#Recibe un diccionario y regresa el id ordenado de forma descendente como un string
def getAlphaFreq(dic):
    dic=sorted(dic.items(),key=lambda x: x[1],reverse=True)
    frecCifrado=''
    for key,value in dic:
        frecCifrado+=key
    return frecCifrado

#Regresa una lista con las 4 primeras letras de la cadena dada
def CuatroFrec(alfaFrec):
    CuatromasFE=[]
    for i in alfaFrec[0:4]:
        CuatromasFE.append(i)
    return CuatromasFE

#Regresa las dos letras mas frecuentes que tienen vecinos en orden descendente
def determinarDosMayores(lista,dic):
    posiblesMayores=[]
    dicListas={}
    for elem in lista:
        dicListas[elem]=dic[elem].items()
    mayores={}
    for elem in lista:
        suma=0
        for key,value in dicListas[elem]:
            suma=suma+value
        mayores[elem]=suma
    mayores1=sorted(mayores.items(),key=lambda x: x[1],reverse=True)
    letrasPosibles=''
    for key,value in mayores1:
        letrasPosibles+=key
    uno=letrasPosibles[0]
    dos=letrasPosibles[1]
    return uno,dos

#Obtiene las palabras de 1 letras mas frecuentes y regresa un diccionario en forma descendente
def freq1LetINtxt(texto):
    palabras=texto.split()
    conteo={}
    for pal in palabras:
        if(len(pal)==1):
            conteo[pal]=conteo.get(pal,0)+1
    return conteo
    #return sorted(conteo.items(),key=lambda x: x[1],reverse=True)



#Obtiene las palabras de 2 letras mas frecuentes y regresa un diccionario en forma descendente
def freq2LetINtxt(texto):
    palabras=texto.split()
    conteo={}
    for pal in palabras:
        if(len(pal)==2):
            conteo[pal]=conteo.get(pal,0)+1
    return sorted(conteo.items(),key=lambda x: x[1],reverse=True)

#Obtiene las palabras de 3 letras mas frecuentes y regresa un diccionario en forma descendente
def freq3LetINtxt(texto):
    palabras=texto.split()
    conteo={}
    for pal in palabras:
        if(len(pal)==3):
            conteo[pal]=conteo.get(pal,0)+1
    return sorted(conteo.items(),key=lambda x: x[1],reverse=True)

#Obtener el valor mas grande de un diccionario
def obtenerMasFreq3(dic):
    listaMasFreq=[]
    cont=0
    for key,value in dic:
        listaMasFreq.append(key)
        cont+=1
        if(cont==4):
            return listaMasFreq

#Obtener el valor mas grande de un diccionario
def obtenerMasFreq2(dic):
    listaMasFreq=[]
    cont=0
    for key,value in dic:
        listaMasFreq.append(key)
        cont+=1
        if(cont==8):
            return listaMasFreq
                
#Evalua el texto decifrado para ver si es una buena opcion
def evaluarTxtNuevo(txtCif,palFreqE):
    txtCif=txtCif.lower()
    MasFreqD3=freq3LetINtxt(txtCif)
    mayor3=obtenerMasFreq3(MasFreqD3)
    elementosFound=[]
    for elem in mayor3:
        if elem in palFreqE:
            elem=elem.upper()
            elementosFound.append(elem)
    return elementosFound

#Actualiza la lista de palabras de 3 letras con mayor frecuencia del texto cifrado
#esto lo hace con cada valor del posible alfabeto que arroja el metodo evaluarTxtNuevo
def actualizarMayor3C(listaMayor,valor,indice):
    cadenaTemp=''
    for elem in listaMayor:
        cadenaTemp=cadenaTemp+elem+" "
    cadenaTemp=cadenaTemp.replace(valor,indice.upper())
    mayor3C=cadenaTemp.split()
    return mayor3C

#Actualiza el alfaREGEX
def actualizarAlfaREGEX(txtCif,AlfaMayusculas,alfaREGEX):
    cadenas=txtCif.split()
    for palabras in cadenas:
        for letras in palabras:
            if letras in AlfaMayusculas:
                if(not(letras in alfaREGEX)):
                    alfaREGEX+=letras
    return alfaREGEX


#Obtiene la palabra en español que puede ser cambiada por la palabra cifrada; regresa ambos valores
def obtenerPalabra(alfaRE,lista):
    for elem in lista:
        palProbables=checarPalabra(alfaRE,elem)
        if(palProbables!=None):
            palProbable=palProbables.pop()
            return palProbable,elem

#Obtiene una lista con las palabras mas probables para sustituirse del txtCif
#Si la palabra ya esta decifrada, la descarta
def obtenerMasProbables(textoCifrado):
    cadenas=textoCifrado.split()
    c1=set()
    dicPorcentajes={}
    masProbables=[]
    for pal in cadenas:
        if(len(pal)>=6):
            c1.add(pal)
    for elem in c1:
        conteo=0
        for letra in elem:
            if letra in alfabetoUpper:
                conteo+=1
        if conteo!=len(elem):
            porcentaje=conteo/len(elem)
            dicPorcentajes[elem]=porcentaje
    percent=sorted(dicPorcentajes.items(),key=lambda x: x[1], reverse=True)
    for key,value in percent:
        masProbables.append(key)
    return masProbables

#Obtiene una lista con las palabras mas probables para sustituirse del txtCif
#Si la palabra ya esta decifrada, la descarta. Longitud menor a 6
def obtenerMasProbablesFinal(textoCifrado):
    cadenas=textoCifrado.split()
    c1=set()
    dicPorcentajes={}
    masProbables=[]
    for pal in cadenas:
        if(len(pal)<6):
            c1.add(pal)
    for elem in c1:
        conteo=0
        for letra in elem:
            if letra in alfabetoUpper:
                conteo+=1
        if conteo!=len(elem):
            porcentaje=conteo/len(elem)
            dicPorcentajes[elem]=porcentaje
    percent=sorted(dicPorcentajes.items(),key=lambda x: x[1], reverse=True)
    for key,value in percent:
        masProbables.append(key)
    return masProbables

#Checa las palabras que pueden corresponder conforme a un patron y un alfabeto de letras que no se han usado    
def checarPalabra(sinUsar,patron):    
    resList=[]
    c1=set()
    archivo=open('ElPrincipitoModificado.txt','r')
    texto=archivo.read()
    cadenas=texto.split()
    rePat='['+sinUsar+']'
    regex=re.sub('[a-zñ]',rePat,patron)+'$'
    regex=regex.lower()
    print('\n\nBuscando',regex)
    for pal in cadenas:
        if re.match(regex,pal):
            c1.add(pal)
    resList=list(c1)
    if len(resList)>1:
        return None
    if not resList:
        return None
    return resList

#Obtiene un diccionario con el mapeo de las letras que se sustituiran en el texto cifrado
def mapeoPalabras(palProbable,palCifrada):
    mapeo=0
    dicSust={}
    for letra in palCifrada:
        if letra in alfabeto:
           dicSust[letra]=mapeo
           mapeo+=1
        else:
            mapeo+=1
    dicSustPal={}
    for key,value in dicSust.items():
        letraE=palProbable[value]
        letraC=palCifrada[value]
        dicSustPal[letraE]=letraC
    return dicSustPal


#Obtiene las palabras restantes que aun quedan por decifrar con una longitud menor a 5
def obtenerPalRestantes(txtCif):
    palabrasRestantes=[]    
    cadenasFinal=txtCif.split()
    for pal in cadenasFinal:
        contador=0
        for letra in pal:
            if letra in alfabeto:
                contador+=1
        if contador!=0:
            palabrasRestantes.append(pal)
    return palabrasRestantes

#Obtiene la llave encontrada con respecto al diccionario de letras C y E
def obtenerLlave(dicAlfa,listaLetras):
    for key,value in dicAlfa.items():
        key=key.upper()
        index=listaLetras.index(key)
        listaLetras.pop(index)
        listaLetras.insert(index,value)

    llave=''
    for let in listaAlfaFinal:
        if let=='':
            llave=llave+"-"
        else:
            llave=llave+let
    return llave


#Evaluar dos listas de palabras con 3 letras para mostrar coincidencias
def evaluarPalabras(listaE,listaC):
    alfabetoLower='abcdefghijklmnñopqrstuvwxyz'
    alfabetoUpper='ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
    for elemE in listaE:
        for elemC in listaC:
            dicEvPal={}
            mapeo=0
            for letra in elemC:
                if letra in alfabetoUpper:
                    letra=letra.lower()
                    dicEvPal[letra]=mapeo
                    mapeo+=1
                else:
                    mapeo+=1
            if bool(dicEvPal):
                coincidencias=0
                for key,value in dicEvPal.items():
                    if elemE[value] != key:
                        exito=0
                        break
                    else:
                        exito=1
                if exito==1:
                    mapeo2=0
                    dicLetrasFinales={}
                    for letra in elemC:
                        if letra in alfabetoLower:
                            dicLetrasFinales[letra]=mapeo2
                            mapeo2+=1
                        else:
                            mapeo2+=1
                    dicStore={}
                    for key,value in dicLetrasFinales.items():
                        c=elemE[value]
                        if(not(c in dicStore)):
                            dicStore[c]=key
                    return dicStore
    return 'sinCoincidencias'

#Funcion para cifrar un texto
def cifraSustituye(cadena,alfabeto,alfabetoLlave):
    cadenaCifrada=""
    for letra in cadena:
        if letra in alfabeto:
            posicion = alfabeto.find(letra)
            cadenaCifrada=cadenaCifrada+alfabetoLlave[posicion]
        else:
            cadenaCifrada = cadenaCifrada+letra
#    print("Alfabeto llave: ",alfabetoLlave)
    return cadenaCifrada

#Funcion que genera un alfabeto aleatorio
def generarAlfabeto(alfabeto):
    alfabetoCifrar=''.join(random.sample(alfabeto,len(alfabeto)))
    return alfabetoCifrar

#Funcion para limpiar un texto, cifrarlo y regresa el mismo texto ya cifrado
#####FASE DE PRUBEAS####
def cifrarTexto(texto,alfabeto,alfabetoLlave):
    texto=texto.lower()
    sinSimbolos=re.sub(r'[?|$|.|!|\'|"|¡|,|0-9|’|‘|¿|"|“|”|:|;|(|)|—|!]',r'',texto)
    cadenas=sinSimbolos.split()
    lista=[]
    for palabra in cadenas:
        contador=0
        for letra in palabra:
            contador+=1
            if(letra=='á'):
                lista.append(palabra.replace(letra,'a'))
                break
            if(letra=='é'):
                lista.append(palabra.replace(letra,'e'))
                break
            if(letra=='í'):
                lista.append(palabra.replace(letra,'i'))
                break
            if(letra=='ó'):
                lista.append(palabra.replace(letra,'o'))
                break
            if(letra=='ú'):
                lista.append(palabra.replace(letra,'u'))
                break
            if(letra=='ü'):
                lista.append(palabra.replace(letra,'u'))
                break
            if(contador==len(palabra)):
                lista.append(palabra)
                break
    txtFinal=''
    contador=0
    for palabras in lista:
        if(contador==0):
            txtFinal=palabras
        else:
            txtFinal=txtFinal+palabras+" "
        contador+=1
    txtCif=cifraSustituye(txtFinal,alfabeto,alfabetoLlave)
    return txtCif


##########AQUI EMPIEZA EL PROGRAMA#########

#Rutas de los archivos que se cargaran
inicio = time.clock()
principito='ElPrincipitoModificado.txt'
club='clubPeleaSimple.txt'
neil='NeilDegrasseSimple.txt'
steve='SteveJobsSimple.txt'

#Alfabeto en español y el mismo ordenado por frecuencia de aparicion
alfabeto='abcdefghijklmnñopqrstuvwxyz'
alfabetoUpper='ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
alfaFrecuente='eaosrnidlctumpbgvyqhfzjñxwk'
alfaREGEX=''
listaAlfaFinal=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z']
mayor3E=['que','los','del','las','por','con','una']
mayor1E=['a','y','o','e']
cont=0
alfaCifrado={}
for letra in alfabeto:
    alfaCifrado[letra]=''

txtParaCifrar=loadTxt(steve)
randomKey=generarAlfabeto(alfabeto)
txtCif=cifraSustituye(txtParaCifrar,alfabeto,randomKey)

#Carga texto de referencia en español
txtEsp=loadTxt(principito)

#Carga texto cifrado
#txtCif=loadTxt(neil)     

#Regresa un diccionario con las letras mas frecuentes en el texto de referencia
freqEsp=freqLetINtxt(principito)

#Regresa un diccionario con las letras mas frecuentes del texto cifrado
freqCif=freqLetINtxt(txtCif)

#Obtenemos las letras frecuentes del texto cifrado en forma de string
alfaPosible=getAlphaFreq(freqCif)

#Obtendra dos listas con las 4 letras mas frecuentes de los alfabetos (alfaFrecuente y alfaPosible)
masFreqEsp=CuatroFrec(alfaFrecuente)
masFreqCif=CuatroFrec(alfaPosible)

#Genera los diccionarios con todos los vecinos de cada letra del texto simple
d=contarVecinos(txtEsp)
#Genera los diccionarios con todos los vecinos de cada letra del texto cifrado
d2=contarVecinos(txtCif)

#Regresa las dos mas letras (de las 4 mas frecuentes) con vecinos que tienen mas frecuencias
Euno,Edos=determinarDosMayores(masFreqEsp,d)
Cuno,Cdos=determinarDosMayores(masFreqCif,d2)

#Imprime el texto cifrado antes del primer intento
print("Tu texto cifrado es: \n\n%s" % txtCif)

#Reemplaza en el texto los valores obtenidos por los metodos determinarDosMayores
txtCif=txtCif.replace(Cuno,Euno.upper())
txtCif=txtCif.replace(Cdos,Edos.upper())
alfaCifrado[Euno]=Cuno
alfaCifrado[Edos]=Cdos
            
cont+=1
#Imprime el texto cifrado despues del primer intento
print("\nTu texto cifrado despues del intento numero ",cont," es: \n\n%s"%txtCif)

#Obtiene las palabras de 3 letras mas frecuentes de txtEsp y txtCif
masFreq3C=freq3LetINtxt(txtCif)

#Obtiene lista de palabras con mayor frecuencia de las lista de 3 letras
mayor3C=obtenerMasFreq3(masFreq3C)

#Realiza el analisis con las letras de 3
cont+=1
palFound=[]
dicNewSust=evaluarPalabras(mayor3E,mayor3C)
for key,value in dicNewSust.items():
    txtCif=txtCif.replace(value,key.upper())
    mayor3C=actualizarMayor3C(mayor3C,value,key)
    alfaCifrado[key]=value
palFound=evaluarTxtNuevo(txtCif,mayor3E)


print("\nTu texto cifrado despues del intento numero ",cont," es: \n\n%s"%txtCif)
for elem in palFound:
    mayor3C.remove(elem)
    elem=elem.lower()
    mayor3E.remove(elem)

#Actualiza el alfabeto de letras sin usar
alfaREGEX=actualizarAlfaREGEX(txtCif,alfabetoUpper,alfaREGEX)


#Analisis de palabras con una sola letra; sustitucion de ellas en el texto Cifrado
masFreq1C=freq1LetINtxt(txtCif)
elimDDic=[]
for key,value in masFreq1C.items():
    if key in alfabetoUpper:
        elimDDic.append(key)
        key=key.lower()
        if key in mayor1E:
            mayor1E.remove(key)
for let in elimDDic:
    del masFreq1C[let]

masFreq1C=sorted(masFreq1C.items(), key=lambda x: x[1],reverse=True)
posibles1LC=[]
for key,value in masFreq1C:
    posibles1LC.append(key)

txtCif=txtCif.replace(posibles1LC[0],mayor1E[0].upper())
alfaCifrado[mayor1E[0]]=posibles1LC[0]
            
cont+=1
print("\nTu texto cifrado despues del intento numero ",cont," es:\n\n%s"%txtCif)


alfaREGEX=actualizarAlfaREGEX(txtCif,alfabetoUpper,alfaREGEX)
alfaRE=elimIgual(alfabeto,alfaREGEX.lower())

cont+=1
try:
    #Reduce la posibilidad de el alfabeto disponible a un numero de 5 elementos
    while len(alfaRE)>5:
        #Obtiene la lista de las palabras mas probables que pueden ser decifradas
        probables=obtenerMasProbables(txtCif)
        #Obtiene la palabra cifrada como la palabra por la cual puede ser sustituida
        palProbable,palCifrada=obtenerPalabra(alfaRE,probables)
        
        dicSustPal=mapeoPalabras(palProbable,palCifrada)


        for key,value in dicSustPal.items():
                txtCif=txtCif.replace(value,key.upper())
                alfaCifrado[key]=value
        print("\nTu texto cifrado despues del intento numero ",cont," es:\n\n%s"%txtCif)
        cont+=1


        alfaREGEX=actualizarAlfaREGEX(txtCif,alfabetoUpper,alfaREGEX)
        alfaRE=elimIgual(alfabeto,alfaREGEX.lower())
except TypeError:
    print('Comenazando a analizar ultimas palabras')

try:
    while len(alfaRE)!=0:
        #Obtiene la lista de las palabras mas probables que pueden ser decifradas
        probables=obtenerMasProbablesFinal(txtCif)
        #Obtiene la palabra cifrada como la palabra por la cual puede ser sustituida
        palProbable,palCifrada=obtenerPalabra(alfaRE,probables)
        
        dicSustPal=mapeoPalabras(palProbable,palCifrada)


        or key,value in dicSustPal.items():
                txtCif=txtCif.replace(value,key.upper())
                alfaCifrado[key]=value
        print("\nTu texto cifrado despues del intento numero ",cont," es:\n\n%s"%txtCif)
        cont+=1


        alfaREGEX=actualizarAlfaREGEX(txtCif,alfabetoUpper,alfaREGEX)
        alfaRE=elimIgual(alfabeto,alfaREGEX.lower())
except TypeError:
    print('\nFin de analisis\n')

palabrasRestantes=obtenerPalRestantes(txtCif)
while bool(palabrasRestantes):
    print('Analizando letras restantes')
    palProbable,palCifrada=obtenerPalabra(alfaRE,palabrasRestantes)
    dicSustPal=mapeoPalabras(palProbable,palCifrada)
    for key,value in dicSustPal.items():
            txtCif=txtCif.replace(value,key.upper())
            alfaCifrado[key]=value
    print("\nTu texto cifrado despues del intento numero ",cont," es:\n\n%s"%txtCif)
    cont+=1
    alfaREGEX=actualizarAlfaREGEX(txtCif,alfabetoUpper,alfaREGEX)
    alfaRE=elimIgual(alfabeto,alfaREGEX.lower())
    palabrasRestantes=obtenerPalRestantes(txtCif)

print('\n\nTu texto ha sido decifrado\n\n')
alfaLlave=obtenerLlave(alfaCifrado,listaAlfaFinal)
print("La llave obtenida mediante el analisis es: \n%s"%alfaLlave)
print("\nLa llave utilizada para cifrar el texto es: \n%s"%randomKey)
print("\nEl numero de intentos fue de: ",cont-1," con un tiempo de: ",time.clock()-inicio," segundos")

