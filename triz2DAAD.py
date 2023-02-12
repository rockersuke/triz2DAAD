#! python

import argparse
import json
import sys
import xml.etree.ElementTree as etree

def listAll():
        print()
        print('LOCALIDADES')    
        print() 

        for y in listRooms:
                print ('id:',y['id'])
                print ('loc:',y['loc'])
                print ('name:',y['name'])
                print ('subtitle:',y['subtitle'])
                print ('description:',y['description'])
                print ('con:',y['con'])
                for x in y['con']:
                        print(x)
                print ()
                

        print()
        print('OBJETOS')      
        print()

        for y in listObjects:
                print ('name:','*'+y['name']+'*')
                print ('description:',y['description'])
                print ('type', y['type'])                             
                print ('kind', y['kind'])             
                print ('content', y['content'])
                print ('loc:',y['loc'])
                print ('ropa', y['wearable'])
                print ('contenedor', y['container'])
                print('fuente de luz', y['lightsource'])
                print ()
                
        print()
        print('CONTENEDORES')
        print()

        for y in listContainers:
                print ('name:','*'+y['name']+'*')
                print ('description:',y['description'])
                print ('type', y['type'])                             
                print ('kind', y['kind'])             
                print ('content', y['content'])
                print ('loc:',y['loc'])
                print ('ropa', y['wearable'])
                print ('contenedor', y['container'])
                print('fuente de luz', y['lightsource'])
                print ()
         
        if idobj:
                print()
                print('IDENTIFICADORES DE OBJETOS')
                print()
                
                for y in listObjectIdentifiers:
                        print(y)
                        
        if idloc:
                print()
                print('IDENTIFICADORES DE LOCALIDAD')
                print()
                
                for y in listLocationIdentifiers:
                        print(y)

def acentos(x):
        b=x
        if 'á' in x:
                b=x.replace('á','a')
        if 'é' in x:
                b=x.replace('é','e')
        if 'í' in x:
                b=x.replace('í','i')
        if 'ó' in x:
                b=x.replace('ó','o')
        if 'ú' in x:
                b=x.replace('ú','u')
        return(b)       

def dirTransform(x):
        if english:
                a={0:'N',1:'N',2:'NE',3:'E',4:'E',5:'E',6:'SE',7:'S',8:'S',9:'S',10:'SW',11:'W',12:'W',13:'W',14:'NW',15:'N'}
        else:
                a={0:'N',1:'N',2:'NE',3:'E',4:'E',5:'E',6:'SE',7:'S',8:'S',9:'S',10:'SO',11:'O',12:'O',13:'O',14:'NO',15:'N'}
        if x in a:
                return a[x]
                
def dirTransform2(x):
        if english:
                a={1:'IN',2:'OUT',3:'UP',4:'DOWN'}
        else:
                a={1:'DENTRO',2:'FUERA',3:'ARRIBA',4:'ABAJO'}
        if x in a:
                return a[x]
                
def id2loc(x):
        for y in listRooms:
                if y['id']==x:
                        return str(y['loc'])
                        
def xml2json():
        tree=etree.parse(in_file)
        root=tree.getroot()
        info=root[0]
        map=root[1]

        data={
                'title':'',
                'author':'',
                'description':'',
                'history':'',
                'elements':[],
                'startRoom':0
        }

        dirType={
                'in':1,
                'out':2,
                'up':3,
                'down':4
        }

        dirCardinal={
                'n':0,
                'nne':1,
                'ne':2,
                'ene':3,
                'e':4,
                'ese':5,
                'se':6,
                'sse':7,
                's':8,
                'ssw':9,
                'sw':10,
                'wsw':11,
                'w':12,
                'wnw':13,
                'nw':14,
                'nnw':15
        }

        for y in info:
                if y.tag=='title':
                        data['title']=y.text
                if y.tag=='author':
                        data['author']=y.text
                if y.tag=='description':
                        data['description']=y.text
                if y.tag=='history':
                        data['history']=y.text

        aux=1
        for y in map:
                if y.tag=='room':
                        id=int(y.get('id'))
                        if y.get('isStartRoom')=='yes':
                                data['startRoom']=aux
                        aux = aux + 1
                        if y.get('isDark')=='yes':
                                dark=True
                        else:
                                dark=False
                        name=y.get('name')
                        subtitle=y.get('subtitle')
                        description=y.get('description')
                        objects=[]
                        x=y.find('objects')
                        if x!=None:
                                if x.text!=None:
                                        objText=x.text
                                        l=objText.split('|')
                                        for p in l:
                                        
                                                # 1.0.4b4 Busca [m] y [1] (innecesarios) y los retira
                                                # por si acaso alguien los usaba por inercia de triz2sce
                                                
                                                if '[m]' in p:
                                                        p=p.replace('[m]','')
                                                if '[1]' in p:
                                                        p=p.replace('[1]','')    
                                                        
                                                female=False
                                                plural=False
                                                if '[f]' in p:
                                                        female=True
                                                        p=p.replace('[f]','')
                                                if '[2]' in p:
                                                        plural=True
                                                        p=p.replace('[2]','')
                                                if english:
                                                        artInd='a'
                                                        if plural:
                                                                artInd='some'
                                                else:
                                                        artInd='un'
                                                        if female:
                                                                artInd='una'
                                                                if plural:
                                                                        artInd='unas'
                                                        else:
                                                                if plural:
                                                                        artInd='unos'
                                                objDescription=artInd+' '+p
                                                if '[c]' in objDescription:
                                                        objDescription=objDescription.replace('[c]','')
                                                if '[w]' in objDescription:
                                                        objDescription=objDescription.replace('[w]','')
                                                if '[l]' in objDescription:
                                                        objDescription=objDescription.replace('[l]','')
                                                objName=p.split(' ')[0]
                                                objects.append({'name':objName, 'type':'Object', 'description':objDescription, 'kind':'5', 'content':[]})
                        data['elements'].append({'id':id, 'type':'Room', 'name':name, 'subtitle':subtitle, 'description':description, 'dark':dark, 'objects':objects})
                if y.tag=='line':
                        id=int(y.get('id'))
                        if y.get('flow')=='oneWay':
                                oneWay=True
                        else:
                                oneWay=False
                        a=y.get('startText')
                        if a in dirType:
                                startType=dirType[a]
                        else:
                                startType=0
                        a=y.get('endText')
                        if a in dirType:
                                endType=dirType[a]
                        else:
                                endType=0
                        for x in y:
                                if x.tag=='dock':
                                        if x.get('index')=='0':
                                                dockStart=int(x.get('id'))
                                                a=x.get('port')
                                                if a in dirCardinal:
                                                        startDir=dirCardinal[a]
                                        else:
                                                dockEnd=int(x.get('id'))
                                                a=x.get('port')
                                                if a in dirCardinal:
                                                        endDir=dirCardinal[a]
                        data['elements'].append({'id':id, 'type':'Connector', 'oneWay':oneWay, 'startType':startType, 'endType':endType, 'dockStart':dockStart, 'dockEnd':dockEnd, 'startDir':startDir, 'endDir':endDir})

        return data

# 1.0.3 parche de compatibilidad entre el antiguo y  el nuevo formato de json de los mapas de Trizbort.io
# (¡con la esperanza de no tener que hacer esto a menudo!)

def jsonFormatPatch():
        for y in data['elements']:          
                if y['_type'] == 'Room':
                        y['type'] =  y['_type']
                        y['name'] =  y['_name']
                        y['subtitle'] = y['_subtitle']
                        y['description'] = y['_description']
                        y['dark'] = y['_dark']
                        y['endroom'] = y['_endroom']
                        for z in y['objects']:
                                if z['_type'] == 'Object':
                                        recursionPatch(z)
                if y['_type'] == 'Connector':
                        y['type'] = y['_type']
                        y['name'] = y['_name']
                        y['dockStart'] = y['_dockStart']
                        y['dockEnd'] = y['_dockEnd']
                        y['startDir'] = y['_startDir']
                        y['endDir'] = y['_endDir']
                        y['startY'] = y['_startY']
                        y['startX'] = y['_startX']
                        y['endY'] = y['_endY']
                        y['endX'] = y['_endX']
                        y['oneWay'] = y['_oneWay']
                        y['startType'] = y['_startType']
                        y['endType'] = y['_endType']
                        y['startLabel'] = y['_startLabel']
                        y['endLabel'] = y['_endLabel']
                     
# 1.0.4b3 Parche para la función jsonFormatPatch(). No cambiaba los identificadores de los objetos que estaban dentro de otros objetos.
                     
def recursionPatch(z):
        z['name'] = z['_name']
        z['type'] = z['_type']
        z['description'] = z['_description']
        z['kind'] = z['_kind']
        z['content'] = z['_content']
        if z['content'] != []:
                for y in z['content']:
                        recursionPatch(y)
        


# 1.0.2b3 Añade recursivamente los objetos de una localidad para dar soporte a los objetos "dentro de" otros objetos de trizbort.io

def recursive_objects(list, parent):
        global obj_id
        for z in list:
                if z['description']=='':
                        z['description']=z['name'].lower()
                z['name']=acentos(z['name']).upper()
                z['loc']=loc
                z['parent']=parent
                z['obj_id']=obj_id
                obj_id += 1
                listObjects.append(z)
                if z['content'] != []:
                        # A los objetos contenidos en otro les asigna el 'obj_id' del contenedor como 'parent' del objeto contenido.
                        # Como los obj_id son siempre a partir de 3000, será fácil distinguir cuando un objeto comienza el juego
                        # contenido dentro de otro.
                        recursive_objects(z['content'], z['obj_id'])

def imprimeDEF():
        if verbosity:
                if english:
                        print('Printing /DEF section', end=' -> ')
                else:     
                        print('Imprimiendo sección /DEF', end=' -> ')
        if english:
                if dsf:
                        print('; Database for DAAD (DRC syntax) generated by Triz2DAAD.', file=f)
                else:
                        print('; Database for DAAD 2.40 - 2.42 generated by Triz2DAAD.', file=f)
        else:
                if dsf:
                        print('; Base de datos para DAAD (sintáxis DRC) generada por Triz2DAAD.', file=f)
                else:
                        print('; Base de datos para DAAD V2.40 - 2.42 generada por Triz2DAAD.', file=f)
        print(';', file=f)
        if english:
                print('; Definitions section.', file=f)
        else:
                print('; Sección de definiciones.', file=f)
        print(';', file=f)
        if daadReady:
                print(';', file=f)
                if english:
                        print('; DAAD Ready 0.7 specific definitions.', file=f)
                else:
                        print('; Definiciones específicas para DAAD Ready 0.7', file=f)
                print(';', file=f)
                if english:
                        print("; --- Please don't remove the following code, it makes sure the game works fine for all supported targets", file=f)
                else:
                        print('; --- Por favor no quites este código, es importante para controlar los distintos objetivos', file=f)
                print('#ifdef "SPLIT"', file=f)
                print('#define hasSplitMode 1', file=f)
                print('#endif', file=f)
                print('', file=f)
                print('#ifndef "tape"', file=f)
                print('#ifndef "st"', file=f)
                print('#ifndef "amiga"', file=f)
                print('#ifndef "zx128"', file=f)
                print('#extern "MALUVA"', file=f)
                print('#endif', file=f)
                print('#endif', file=f)
                print('#endif', file=f)
                print('#endif', file=f)
                print('', file=f)
                print('#ifdef "html"', file=f)
                print('#define nativeraster 1', file=f)
                print('#endif', file=f)
                print('#ifdef "pcw"', file=f)
                print('#define nativeraster 1', file=f)
                print('#endif', file=f)
                print('#ifdef "amiga"', file=f)
                print('#define nativeraster 1', file=f)
                print('#endif', file=f)
                print('#ifdef "pc"', file=f)
                print('#define nativeraster 1', file=f)
                print('#endif', file=f)
                print('#ifdef "st"', file=f)
                print('#define nativeraster 1', file=f)
                print('#endif', file=f)
                print('#ifdef "nativeraster"', file=f)
                if english:
                        print('#echo  "Target supports native raster graphics"', file=f)
                else:
                        print('#echo  "La máquina de destino soporta gráficos raster de manera nativa"', file=f)
                print('#endif', file=f)
                print('', file=f)
                print('#ifdef "uno"', file=f)
                print('#int "MLV_UNO_INT.BIN"', file=f)
                print('#define canBoostSpeed 1', file=f)
                print('#endif', file=f)
                print('', file=f)
                print('#ifdef "next"', file=f)
                print('#define canBoostSpeed 1', file=f)
                print('#endif', file=f)
                print('', file=f)
                print('#ifdef "cpc"', file=f)
                print('#int "MLV_CPC_INT.BIN"', file=f)
                print('#endif', file=f)
                print('', file=f)
                print('#ifdef "hasSplitMode"', file=f)
                if english:
                        print('#echo "Target will make use of split mode"', file=f)
                else:
                        print('#echo "La máquina destino usará split mode"', file=f)
                print('#endif', file=f)
                print('', file=f)
                print('#ifdef "canBoostSpeed"', file=f)
                if english:
                        print('#echo "Target has turbo mode"', file=f)
                else:
                        print('#echo "La máquina destino tiene modo turbo"', file=f)
                print('#endif', file=f)
                print('', file=f)
                print('#ifdef "tape"', file=f)
                print('#define noretryImage 1', file=f)
                print('#endif', file=f)
                print('', file=f)
                print('#ifdef "nativeraster"', file=f)
                print('#define noretryImage 1', file=f)
                print('#endif', file=f)
                if english:
                        print("; --- Please don't remove the code above, it makes sure the game works fine for all supported targets", file=f)
                else:
                        print('; --- Por favor no quites este código de arriba, es importante para controlar los distintos objetivos', file=f)
                print('', file=f)
        if english:
                imprimeDEF_ENG()
        else:
                imprimeDEF_SPA()

def imprimeDEF_SPA():
        #No establece ROWS en modo DSF ya que en éste lo define por sí mismo.
        if dsf==False:
                print('; Establece el símbolo ROWS para representar 32 filas (de ventana de texto) en el caso del PCW', file=f)
                print('; y 25 en todos los demás.', file=f)
                print('; ', file=f)        
                print('#IF PCW', file=f)
                print(' #define ROWS 32', file=f)
                print('#ELSE', file=f)
                print(' #define ROWS 25', file=f)
                print('#ENDIF', file=f)
        else:
                if daadReady==False:
                        print('#define Turns_TAB "COLS-13"', file=f)
        print(';', file=f)
        if daadReady==False:
                print('; Define valores por defecto para la posición de la ventana de texto.', file=f)
                textRow1=14
                if statusLine:
                        textRow2=1
                else:
                        textRow2=0
                if dsf:
                        print('#ifdef "MSX2"', file=f)
                        print(' #define textrow1 ' + str(textRow1) + ' ; Posición de la ventana de texto en localidades con gráfico.', file=f)
                        print(' #define textrow2 ' + str(textRow1) + ' ; Posición de la ventana de texto en localidades sin gráfico.', file=f)
                        print('#endif', file=f)
                        print(';', file=f)
                        print('#ifndef "MSX2"', file=f)
                        print(' #define textrow1 ' + str(textRow1) + ' ; Posición de la ventana de texto en localidades con gráfico.', file=f)
                        print(' #define textrow2 ' + str(textRow2) + ' ; Posición de la ventana de texto en localidades sin gráfico.', file=f)
                        print('#endif', file=f)
                else:
                        print('#define textrow1 ' + str(textRow1) + ' ; Posición de la ventana de texto en localidades con gráfico.', file=f)
                        print('#define textrow2 ' + str(textRow2) + ' ; Posición de la ventana de texto en localidades sin gráfico.', file=f)
                print(';', file=f)
                if statusLine:
                        print('; Define posición de la barra de estado.', file=f)
                        print('#define slrow 0', file=f)
                        print(';', file=f)
                print('; Define valores por defecto para papel y tinta tanto de la ventana de texto como de la barra de estado', file=f)
                print(';', file=f)
                print('; Valores para PC.', file=f)
                print('; Para pruebas en modo sólo texto se recomienda usar 7 en vez de 1 (larga historia detrás).', file=f)
                print(';', file=f)
                if dsf:
                        print('#ifdef "PC"', file=f)
                else:
                        print('#IF PC', file=f)
                print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                print(' #define fg_colour ' + str(ink) + '      ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour ' + str(ink) + '   ; Color de fondo (papel) de la barra de estado.', file=f)
                        print(' #define sb_fg_colour 0   ; Color del texto (tinta) de la barra de estado.', file=f)
                if dsf:
                        print('#endif', file=f)
                else:
                        print('#ENDIF', file=f)
                print(';', file=f)
                print('; Valores para ZX SPECTRUM', file=f)
                print(';', file=f)
                if dsf:
                        print('#ifdef "SPE"', file=f)
                else:
                        print('#IF SPE', file=f)
                print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                print(' #define fg_colour 1      ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour 7   ; Color de fondo (papel) de la barra de estado.', file=f)
                        print(' #define sb_fg_colour 5   ; Color del texto (tinta) de la barra de estado.', file=f)
                if dsf:
                        print('#endif', file=f)
                else:
                        print('#ENDIF', file=f)
                print(';', file=f)
                print('; Valores para COMMODORE 64', file=f)
                print(';', file=f)
                if dsf:
                        print('#ifdef "CBM64"', file=f)
                else:
                        print('#IF CBM64', file=f)
                print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                print(' #define fg_colour 1      ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour 7   ; Color de fondo (papel) de la barra de estado.', file=f)
                        print(' #define sb_fg_colour 5   ; Color del texto (tinta) de la barra de estado.', file=f)
                if dsf:
                        print('#endif', file=f)
                else:
                        print('#ENDIF', file=f)
                print(';', file=f)
                print('; Valores para AMSTRAD CPC', file=f)
                print(';', file=f)
                if dsf:
                        print('#ifdef "CPC"', file=f)
                else:
                        print('#IF CPC', file=f)
                print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                print(' #define fg_colour 1      ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour 1   ; Color de fondo (papel) de la barra de estado.', file=f)
                        print(' #define sb_fg_colour 0   ; Color del texto (tinta) de la barra de estado.', file=f)
                if dsf:
                        print('#endif', file=f)
                else:
                        print('#ENDIF', file=f)
                print(';', file=f)
                print('; Valores para MSX', file=f)
                print(';', file=f)
                if dsf:
                        print('#ifdef "MSX"', file=f)
                else:
                        print('#IF MSX', file=f)
                print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                print(' #define fg_colour 1      ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour 7   ; Color de fondo (papel) de la barra de estado.', file=f)
                        print(' #define sb_fg_colour 5   ; Color del texto (tinta) de la barra de estado.', file=f)
                if dsf:
                        print('#endif', file=f)
                else:
                        print('#ENDIF', file=f)
                print(';', file=f)
                print('; Valores para ATARI ST', file=f)
                print(';', file=f)
                if dsf:
                        print('#ifdef "ST"', file=f)
                else:
                        print('#IF ST', file=f)
                print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                print(' #define fg_colour ' + str(ink) + '      ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour ' + str(ink) + '   ; Color de fondo (papel) de la barra de estado.', file=f)
                        print(' #define sb_fg_colour 0   ; Color del texto (tinta) de la barra de estado.', file=f)
                if dsf:
                        print('#endif', file=f)
                else:
                        print('#ENDIF', file=f)
                print(';', file=f)
                print('; Valores para AMIGA', file=f)
                print(';', file=f)
                if dsf:
                        print('#ifdef "AMIGA"', file=f)
                else:
                        print('#IF AMIGA', file=f)
                print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                print(' #define fg_colour ' + str(ink) + '      ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour ' + str(ink) + '   ; Color de fondo (papel) de la barra de estado.', file=f)
                        print(' #define sb_fg_colour 0   ; Color del texto (tinta) de la barra de estado.', file=f)
                if dsf:
                        print('#endif', file=f)
                else:
                        print('#ENDIF', file=f)
                print(';', file=f)
                print('; Valores para PCW', file=f)
                print(';', file=f)
                if dsf:
                        print('#ifdef "PCW"', file=f)
                else:
                        print('#IF PCW', file=f)
                print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                print(' #define fg_colour 1      ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour 1   ; Color de fondo (papel) de la barra de estado.', file=f)
                        print(' #define sb_fg_colour 0   ; Color del texto (tinta) de la barra de estado.', file=f)
                if dsf:
                        print('#endif', file=f)
                else:
                        print('#ENDIF', file=f)
                print(';', file=f)
                if dsf:
                        print('; Valores para Commodore Plus 4', file=f)
                        print(';', file=f)
                        print('#ifdef "CP4"', file=f)
                        print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                        print(' #define fg_colour 1      ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                        if statusLine:
                                print(' #define sb_bg_colour 1   ; Color de fondo (papel) de la barra de estado.', file=f)
                                print(' #define sb_fg_colour 0   ; Color del texto (tinta) de la barra de estado.', file=f)
                        print('#endif', file=f)
                        print(';', file=f)
                        print('; Valores para MSX2', file=f)
                        print(';', file=f)
                        print('#ifdef "MODE_5_6"', file=f)
                        print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                        print(' #define fg_colour 15     ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                        if statusLine:
                                print(' #define sb_bg_colour 15  ; Color de fondo (papel) de la barra de estado.', file=f)
                                print(' #define sb_fg_colour 0   ; Color del texto (tinta) de la barra de estado.', file=f)
                        print('#endif', file=f)
                        print(';', file=f)
                        print('#ifdef "MODE_5_8"', file=f)
                        print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                        print(' #define fg_colour 15     ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                        if statusLine:
                                print(' #define sb_bg_colour 15  ; Color de fondo (papel) de la barra de estado.', file=f)
                                print(' #define sb_fg_colour 0   ; Color del texto (tinta) de la barra de estado.', file=f)
                        print('#endif', file=f)
                        print(';', file=f)
                        print('#ifdef "MODE_6_6"', file=f)
                        print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                        print(' #define fg_colour 3      ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                        if statusLine:
                                print(' #define sb_bg_colour 3   ; Color de fondo (papel) de la barra de estado.', file=f)
                                print(' #define sb_fg_colour 0   ; Color del texto (tinta) de la barra de estado.', file=f)
                        print('#endif', file=f)
                        print(';', file=f)
                        print('#ifdef "MODE_6_8"', file=f)
                        print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                        print(' #define fg_colour 3      ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                        if statusLine:
                                print(' #define sb_bg_colour 3   ; Color de fondo (papel) de la barra de estado.', file=f)
                                print(' #define sb_fg_colour 0   ; Color del texto (tinta) de la barra de estado.', file=f)
                        print('#endif', file=f)
                        print(';', file=f)
                        print('#ifdef "MODE_7_6"', file=f)
                        print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                        print(' #define fg_colour 15     ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                        if statusLine:
                                print(' #define sb_bg_colour 15  ; Color de fondo (papel) de la barra de estado.', file=f)
                                print(' #define sb_fg_colour 0   ; Color del texto (tinta) de la barra de estado.', file=f)
                        print('#endif', file=f)
                        print(';', file=f)
                        print('#ifdef "MODE_7_8"', file=f)
                        print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                        print(' #define fg_colour 15     ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                        if statusLine:
                                print(' #define sb_bg_colour 15  ; Color de fondo (papel) de la barra de estado.', file=f)
                                print(' #define sb_fg_colour 0   ; Color del texto (tinta) de la barra de estado.', file=f)
                        print('#endif', file=f)
                        print(';', file=f)
                        print('#ifdef "MODE_8_6"', file=f)
                        print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                        print(' #define fg_colour 15     ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                        if statusLine:
                                print(' #define sb_bg_colour 15  ; Color de fondo (papel) de la barra de estado.', file=f)
                                print(' #define sb_fg_colour 0   ; Color del texto (tinta) de la barra de estado.', file=f)
                        print('#endif', file=f)
                        print(';', file=f)
                        print('#ifdef "MODE_8_8"', file=f)
                        print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                        print(' #define fg_colour 15     ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                        if statusLine:
                                print(' #define sb_bg_colour 15  ; Color de fondo (papel) de la barra de estado.', file=f)
                                print(' #define sb_fg_colour 0   ; Color del texto (tinta) de la barra de estado.', file=f)
                        print('#endif', file=f)
                        print(';', file=f)
                        print('#ifdef "MODE_10_6"', file=f)
                        print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                        print(' #define fg_colour 15     ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                        if statusLine:
                                print(' #define sb_bg_colour 15  ; Color de fondo (papel) de la barra de estado.', file=f)
                                print(' #define sb_fg_colour 0   ; Color del texto (tinta) de la barra de estado.', file=f)
                        print('#endif', file=f)
                        print(';', file=f)
                        print('#ifdef "MODE_10_8"', file=f)
                        print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                        print(' #define fg_colour 15     ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                        if statusLine:
                                print(' #define sb_bg_colour 15  ; Color de fondo (papel) de la barra de estado.', file=f)
                                print(' #define sb_fg_colour 0   ; Color del texto (tinta) de la barra de estado.', file=f)
                        print('#endif', file=f)
                        print(';', file=f)
                        print('#ifdef "MODE_12_6"', file=f)
                        print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                        print(' #define fg_colour 15     ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                        if statusLine:
                                print(' #define sb_bg_colour 15  ; Color de fondo (papel) de la barra de estado.', file=f)
                                print(' #define sb_fg_colour 0   ; Color del texto (tinta) de la barra de estado.', file=f)
                        print('#endif', file=f)
                        print(';', file=f)
                        print('#ifdef "MODE_12_8"', file=f)
                        print(' #define bg_colour 0      ; Color de fondo (papel) de la ventana principal de texto.', file=f)
                        print(' #define fg_colour 15     ; Color del texto (tinta) de la ventana principal de texto.', file=f)
                        if statusLine:
                                print(' #define sb_bg_colour 15  ; Color de fondo (papel) de la barra de estado.', file=f)
                                print(' #define sb_fg_colour 0   ; Color del texto (tinta) de la barra de estado.', file=f)
                        print('#endif', file=f)
                        print(';', file=f)
                if dsf == False:        
                        print('#define NOTCREATED 252', file=f)
                        print('#define TRUE 1', file=f)
                        print('#define FALSE 0', file=f)
                print(';', file=f)
        print('; Atributos para el sistema.', file=f)
        print(';', file=f)
        print('#define WEARABLE  23            ; Objeto actual es ropa.', file=f)
        print('#define CONTAINER 31            ; Objeto actual es contenedor.', file=f)
        print('#define LISTED    55            ; Objetos - listados por LISTOBJ etc', file=f)
        print('#define OA_CLIST  54            ; - Listado continuo', file=f)
        print('#define OO_CLIST  64', file=f)
        print('#define TIMEOUT   87            ; If Timeout last frame', file=f)
        print('#define IA_RBUF   85            ; Input - recall buffer', file=f)
        print('#define IO_RBUF   32', file=f)
        print('#define IA_PINP   84            ; - reprint in stream', file=f)
        print('#define IO_PINP   16', file=f)
        print('#define IA_CSTR   83            ; - clear stream', file=f)
        print('#define IO_CSTR   8', file=f)
        print('#define IA_TAKEY  82            ; - timeout on any key', file=f)
        print('#define IO_TAKEY  4', file=f)
        print('#define IA_TMORE  81            ; - timeout on More...', file=f)
        print('#define IO_TMORE  2', file=f)
        print('#define IA_TSTAR  80            ; - timeout at start of input', file=f)
        print('#define IO_TSTAR  1', file=f)
        print('#define GMODE     247           ; - Gráficos - disponibles', file=f)
        print('#define GA_MDRW   246           ; - Dibujo invisible (drawstring)', file=f)
        print('#define GO_MDRW   64', file=f)
        print('#define GA_POFF   245           ; - Imágenes OFF (drawstring)', file=f)
        print('#define GO_POFF   32', file=f)
        print('#define GA_WKEY   244           ; - Espera después de dibujar (drawstring)', file=f)
        print('#define GO_WKEY   16', file=f)
        print('#define GA_CBOR   243           ; - Cambia BORDER (drawstring)', file=f)
        print('#define GO_CBOR   8', file=f)
        print('#define MOUSE     240           ; ratón disponible (sólamente !DRAW)', file=f)
        print(';', file=f)
        print('#define O2      152     ; Offset de los atributos del segundo objeto', file=f)
        print(';', file=f)
        print('; Banderas del sistema 0 - 63', file=f)
        print(';', file=f)
        if dsf:
                print('#define fDark              0', file=f)
                print('#define fObjectsCarried    1', file=f)
                print('', file=f)
                print('#define fDarkF             28', file=f)
                print('#define fGFlags            29     ; This is best tested using HASAT GMODE', file=f)
                print('#define fScore             30', file=f)
                print('#define fTurns             31     ; 2 bytes', file=f)
                print('#define fTurnsHi           32', file=f)
                print('', file=f)
                print('#define fVerb              33', file=f)
                print('#define fNoun              34', file=f)
                print('#define fAdject1           35', file=f)
                print('#define fAdverb            36', file=f)
                print('#define fMaxCarr           37', file=f)
                print('#define fPlayer            38', file=f)
                print('#define fPrep              43', file=f)
                print('#define fNoun2             44', file=f)
                print('#define fAdject2           45', file=f)
                print('#define fCPronounNoun      46', file=f)
                print('#define fCPronounAdject    47', file=f)
                print('#define fTimeout           48', file=f)
                print('#define fTimeoutFlags      49', file=f)
                print('#define fDoallObjNo        50', file=f)
                print('#define fRefObject         51', file=f)
                print('#define fStrength          52', file=f)
                print('#define fObjFlags          53', file=f)
                print('#define fRefObjLoc         54', file=f)
                print('#define fRefObjWeight      55', file=f)
                print('#define fRefObjIsContainer 56', file=f)
                print('#define fRefObjIsWearable  57', file=f)
                print('#define fRefObjAttr1       58', file=f)
                print('#define fRefObjAttr2       59', file=f)
                print('#define fInkeyKey1         60', file=f)
                print('#define fInkeyKey2         61', file=f)
                print('#define fScreenMode        62     ; 2=Text, 4=CGA, 13=EGA, 141=VGA', file=f)
                print('#define fCurrentWindow     63     ; Which window is active at the moment', file=f)
        else:
                print('#define Dark      0', file=f)
                print('#define NOCarr    1', file=f)
                print('#define Work1     2     ; These are system as we consider the stack such', file=f)
                print('#define Work2     3', file=f)
                print('#define Stack    24     ; A small stack (always 2 bytes pushed) 10 pushes', file=f)
                print('#define EMPTY    23     ; Stack can run from here', file=f)
                print('#define FULL      3     ; to here - There will be an internal one soon', file=f)
                print('#define O2Num    25     ; 1st free in system 64', file=f)
                print('#define O2Con    26     ; Objeto 2 es contenedor.', file=f)
                print('#define O2Loc    27', file=f)
                print('#define DarkF    28', file=f)
                print('#define GFlags   29     ; Esto se prueba mejor usando HASAT GMODE', file=f)
                print('#define Score    30', file=f)
                print('#define Turns    31     ; 2 bytes', file=f)
                print('#define Verb     33', file=f)
                print('#define Noun1    34', file=f)
                print('#define Adject1  35', file=f)
                print('#define Adverb   36', file=f)
                print('#define MaxCarr  37', file=f)
                print('#define Player   38', file=f)
                print('#define O2Att    39     ; Usar banderas 39 y 40 para los atributos de otro objeto.', file=f)
                print('#define InStream 41', file=f)
                print('#define Prompt   42', file=f)
                print('#define Prep     43', file=f)
                print('#define Noun2    44', file=f)
                print('#define Adject2  45', file=f)
                print('#define CPNoun   46', file=f)
                print('#define CPAdject 47', file=f)
                print('#define Time     48', file=f)
                print('#define TIFlags  49', file=f)
                print('#define DAObjNo  50', file=f)
                print('#define CONum    51', file=f)
                print('#define Strength 52', file=f)
                print('#define OFlags   53', file=f)
                print('#define COLoc    54', file=f)
                print('#define COWei    55', file=f)
                print('#define COCon    56', file=f)
                print('#define COWR     57', file=f)
                print('#define COAtt    58', file=f)
                print('#define Key1     60', file=f)
                print('#define Key2     61', file=f)
                print('#define ScMode   62     ; 2=Text, 4=CGA, 13=EGA, 141=VGA', file=f)
                print('#define CurWin   63     ; Qué ventana está activa en este momento.', file=f)
        print(';', file=f)
        # La sección de defines de Grupos útiles no la ponemos en DRC por incompatibilidad
        if dsf == False:
                print('; Grupos útiles.', file=f)
                print('; ', file=f)
                print('#define Z80 SPE+MSX+CPC+PCW', file=f)
                print('#define M6502 CBM64', file=f)
                print('#define M68000 ST+AMIGA', file=f)
                print('#define I86 PC', file=f)
                print(';', file=f)
        if idobj:        
                print('; Identificadores de objetos.', file=f)
                print(';', file=f)
                for y, z in enumerate(listObjectIdentifiers):
                        print('#define ' + z + ' ' + str(y), file=f)
                print(';', file=f)
        if idloc:
                print('; Identificadores de localidadades.', file=f)
                print(';', file=f)
                for y, z in enumerate(listLocationIdentifiers, start=1):
                        print('#define ' + z + ' ' + str(y), file=f)
                print(';', file=f)
        if verbosity:
                print('OK.')
        
def imprimeDEF_ENG():
        # Does not set ROWS in DSF mode
        if dsf==False:
                print('; Sets the ROWS symbol to represent 32 text window height in PCW', file=f)
                print('; and 25 in any other target machine.', file=f)
                print('; ', file=f)
                print('#IF PCW', file=f)
                print(' #define ROWS 32', file=f)
                print('#ELSE', file=f)
                print(' #define ROWS 25', file=f)
                print('#ENDIF', file=f)
        else:
                print('#define Turns_TAB "COLS-13"', file=f)
        print(';', file=f)
        print('; Default values for text window position.', file=f)
        textRow1=14
        if statusLine:
                textRow2=1
        else:
                textRow2=0
        if dsf:
                print('#ifdef "MSX2"', file=f)
                print(' #define textrow1 ' + str(textRow1) + ' ; Locations with graphics.', file=f)
                print(' #define textrow2 ' + str(textRow1) + ' ; Locations without graphics.', file=f)
                print('#endif', file=f)
                print(';', file=f)
                print('#ifndef "MSX2"', file=f)
                print(' #define textrow1 ' + str(textRow1) + ' ; Locations with graphics.', file=f)
                print(' #define textrow2 ' + str(textRow2) + ' ; Locations without graphics.', file=f)
                print('#endif', file=f)
        else:
                print('#define textrow1 ' + str(textRow1) + ' ; Locations with graphics.', file=f)
                print('#define textrow2 ' + str(textRow2) + ' ; Locations without graphics.', file=f)
        print(';', file=f)
        print('; Set default paper and ink colours for both main text and status bar windows.', file=f)
        print(';', file=f)
        print('; PC Colours', file=f)
        print('; If using text-only mode 7 is recommended instead of 1 (long story behind).', file=f)
        print(';', file=f)
        if dsf:
                print('#ifdef "PC"', file=f)
        else:
                print('#IF PC', file=f)
        print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
        print(' #define fg_colour ' + str(ink) + '      ; Main window foreground (ink) colour.', file=f)
        if statusLine:
                print(' #define sb_bg_colour ' + str(ink) + '   ; Status bar background (paper) colour.', file=f)
                print(' #define sb_fg_colour 0   ; Status bar foreground (ink) colour.', file=f)
        if dsf:
                print('#endif', file=f)
        else:
                print('#ENDIF', file=f)
        print(';', file=f)
        print('; ZX SPECTRUM Colours', file=f)
        print(';', file=f)
        if dsf:
                print('#ifdef "SPE"', file=f)
        else:
                print('#IF SPE', file=f)
        print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
        print(' #define fg_colour 1      ; Main window foreground (ink) colour.', file=f)
        if statusLine:
                print(' #define sb_bg_colour 7   ; Status bar background (paper) colour.', file=f)
                print(' #define sb_fg_colour 5   ; Status bar foreground (ink) colour.', file=f)
        if dsf:
                print('#endif', file=f)
        else:
                print('#ENDIF', file=f)
        print(';', file=f)
        print('; COMMODORE 64 Colours', file=f)
        print(';', file=f)
        if dsf:
                print('#ifdef "CBM64"', file=f)
        else:
                print('#IF CBM64', file=f)
        print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
        print(' #define fg_colour 1      ; Main window foreground (ink) colour.', file=f)
        if statusLine:
                print(' #define sb_bg_colour 7   ; Status bar background (paper) colour.', file=f)
                print(' #define sb_fg_colour 5   ; Status bar foreground (ink) colour.', file=f)
        if dsf:
                print('#endif', file=f)
        else:
                print('#ENDIF', file=f)
        print(';', file=f)
        print('; AMSTRAD CPC Colours', file=f)
        print(';', file=f)
        if dsf:
                print('#ifdef "CPC"', file=f)
        else:
                print('#IF CPC', file=f)
        print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
        print(' #define fg_colour 1      ; Main window foreground (ink) colour.', file=f)
        if statusLine:
                print(' #define sb_bg_colour 1   ; Status bar background (paper) colour.', file=f)
                print(' #define sb_fg_colour 0   ; Status bar foreground (ink) colour.', file=f)
        if dsf:
                print('#endif', file=f)
        else:
                print('#ENDIF', file=f)
        print(';', file=f)
        print('; MSX Colours', file=f)
        print(';', file=f)
        if dsf:
                print('#ifdef "MSX"', file=f)
        else:
                print('#IF MSX', file=f)
        print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
        print(' #define fg_colour 1      ; Main window foreground (ink) colour.', file=f)
        if statusLine:
                print(' #define sb_bg_colour 7   ; Status bar background (paper) colour.', file=f)
                print(' #define sb_fg_colour 5   ; Status bar foreground (ink) colour.', file=f)
        if dsf:
                print('#endif', file=f)
        else:
                print('#ENDIF', file=f)
        print(';', file=f)
        print('; ATARI ST Colours', file=f)
        print(';', file=f)
        if dsf:
                print('#ifdef "ST"', file=f)
        else:
                print('#IF ST', file=f)
        print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
        print(' #define fg_colour ' + str(ink) + '      ; Main window foreground (ink) colour.', file=f)
        if statusLine:
                print(' #define sb_bg_colour ' + str(ink) + '   ; Status bar background (paper) colour.', file=f)
                print(' #define sb_fg_colour 0   ; Status bar foreground (ink) colour.', file=f)
        if dsf:
                print('#endif', file=f)
        else:
                print('#ENDIF', file=f)
        print(';', file=f)
        print('; AMIGA Colours', file=f)
        print(';', file=f)
        if dsf:
                print('#ifdef "AMIGA"', file=f)
        else:
                print('#IF AMIGA', file=f)
        print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
        print(' #define fg_colour ' + str(ink) + '      ; Main window foreground (ink) colour.', file=f)
        if statusLine:
                print(' #define sb_bg_colour ' + str(ink) + '   ; Status bar background (paper) colour.', file=f)
                print(' #define sb_fg_colour 0   ; Status bar foreground (ink) colour.', file=f)
        if dsf:
                print('#endif', file=f)
        else:
                print('#ENDIF', file=f)
        print(';', file=f)
        print('; PCW Colours', file=f)
        print(';', file=f)
        if dsf:
                print('#ifdef "PCW"', file=f)
        else:
                print('#IF PCW', file=f)
        print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
        print(' #define fg_colour 1      ; Main window foreground (ink) colour.', file=f)
        if statusLine:
                print(' #define sb_bg_colour 1   ; Status bar background (paper) colour.', file=f)
                print(' #define sb_fg_colour 0   ; Status bar foreground (ink) colour.', file=f)
        if dsf:
                print('#endif', file=f)
        else:
                print('#ENDIF', file=f)
        print(';', file=f)
        if dsf:
                print('; Valores para Commodore Plus 4', file=f)
                print(';', file=f)
                print('#ifdef "CP4"', file=f)
                print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
                print(' #define fg_colour 1      ; Main window foreground (ink) colour.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour 1   ; Status bar background (paper) colour.', file=f)
                        print(' #define sb_fg_colour 0   ; Status bar foreground (ink) colour.', file=f)
                print('#endif', file=f)
                print(';', file=f)
                print('; Valores para MSX2', file=f)
                print(';', file=f)
                print('#ifdef "MODE_5_6"', file=f)
                print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
                print(' #define fg_colour 15     ; Main window foreground (ink) colour.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour 15  ; Status bar background (paper) colour.', file=f)
                        print(' #define sb_fg_colour 0   ; Status bar foreground (ink) colour.', file=f)
                print('#endif', file=f)
                print(';', file=f)
                print('#ifdef "MODE_5_8"', file=f)
                print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
                print(' #define fg_colour 15     ; Main window foreground (ink) colour.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour 15  ; Status bar background (paper) colour.', file=f)
                        print(' #define sb_fg_colour 0   ; Status bar foreground (ink) colour.', file=f)
                print('#endif', file=f)
                print(';', file=f)
                print('#ifdef "MODE_6_6"', file=f)
                print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
                print(' #define fg_colour 3      ; Main window foreground (ink) colour.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour 3   ; Status bar background (paper) colour.', file=f)
                        print(' #define sb_fg_colour 0   ; Status bar foreground (ink) colour.', file=f)
                print('#endif', file=f)
                print(';', file=f)
                print('#ifdef "MODE_6_8"', file=f)
                print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
                print(' #define fg_colour 3      ; Main window foreground (ink) colour.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour 3   ; Status bar background (paper) colour.', file=f)
                        print(' #define sb_fg_colour 0   ; Status bar foreground (ink) colour.', file=f)
                print('#endif', file=f)
                print(';', file=f)
                print('#ifdef "MODE_7_6"', file=f)
                print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
                print(' #define fg_colour 15     ; Main window foreground (ink) colour.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour 15  ; Status bar background (paper) colour.', file=f)
                        print(' #define sb_fg_colour 0   ; Status bar foreground (ink) colour.', file=f)
                print('#endif', file=f)
                print(';', file=f)
                print('#ifdef "MODE_7_8"', file=f)
                print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
                print(' #define fg_colour 15     ; Main window foreground (ink) colour.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour 15  ; Status bar background (paper) colour.', file=f)
                        print(' #define sb_fg_colour 0   ; Status bar foreground (ink) colour.', file=f)
                print('#endif', file=f)
                print(';', file=f)
                print('#ifdef "MODE_8_6"', file=f)
                print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
                print(' #define fg_colour 15     ; Main window foreground (ink) colour.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour 15  ; Status bar background (paper) colour.', file=f)
                        print(' #define sb_fg_colour 0   ; Status bar foreground (ink) colour.', file=f)
                print('#endif', file=f)
                print(';', file=f)
                print('#ifdef "MODE_8_8"', file=f)
                print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
                print(' #define fg_colour 15     ; Main window foreground (ink) colour.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour 15  ; Status bar background (paper) colour.', file=f)
                        print(' #define sb_fg_colour 0   ; Status bar foreground (ink) colour.', file=f)
                print('#endif', file=f)
                print(';', file=f)
                print('#ifdef "MODE_10_6"', file=f)
                print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
                print(' #define fg_colour 15     ; Main window foreground (ink) colour.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour 15  ; Status bar background (paper) colour.', file=f)
                        print(' #define sb_fg_colour 0   ; Status bar foreground (ink) colour.', file=f)
                print('#endif', file=f)
                print(';', file=f)
                print('#ifdef "MODE_10_8"', file=f)
                print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
                print(' #define fg_colour 15     ; Main window foreground (ink) colour.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour 15  ; Status bar background (paper) colour.', file=f)
                        print(' #define sb_fg_colour 0   ; Status bar foreground (ink) colour.', file=f)
                print('#endif', file=f)
                print(';', file=f)
                print('#ifdef "MODE_12_6"', file=f)
                print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
                print(' #define fg_colour 15     ; Main window foreground (ink) colour.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour 15  ; Status bar background (paper) colour.', file=f)
                        print(' #define sb_fg_colour 0   ; Status bar foreground (ink) colour.', file=f)
                print('#endif', file=f)
                print(';', file=f)
                print('#ifdef "MODE_12_8"', file=f)
                print(' #define bg_colour 0      ; Main window background (paper) colour.', file=f)
                print(' #define fg_colour 15     ; Main window foreground (ink) colour.', file=f)
                if statusLine:
                        print(' #define sb_bg_colour 15  ; Status bar background (paper) colour.', file=f)
                        print(' #define sb_fg_colour 0   ; Status bar foreground (ink) colour.', file=f)
                print('#endif', file=f)
                print(';', file=f)
        if dsf == False:                
                print('#define NOTCREATED 252', file=f)
                print('#define TRUE 1', file=f)
                print('#define FALSE 0', file=f)
                print(';', file=f)
        print('; Attributes for system', file=f)
        print(';', file=f)
        print('#define WEARABLE  23            ;Current object is wearable', file=f)
        print('#define CONTAINER 31            ;Current object is a container', file=f)
        print('#define LISTED    55            ;Objects - listed by LISTOBJ etc', file=f)
        print('#define OA_CLIST  54            ; - continous list', file=f)
        print('#define OO_CLIST  64', file=f)
        print('#define TIMEOUT   87            ;If Timeout last frame', file=f)
        print('#define IA_RBUF   85            ;Input - recall buffer', file=f)
        print('#define IO_RBUF   32', file=f)
        print('#define IA_PINP   84            ; - reprint in stream', file=f)
        print('#define IO_PINP   16', file=f)
        print('#define IA_CSTR   83            ; - clear stream', file=f)
        print('#define IO_CSTR   8', file=f)
        print('#define IA_TAKEY  82            ; - timeout on any key', file=f)
        print('#define IO_TAKEY  4', file=f)
        print('#define IA_TMORE  81            ; - timeout on More...', file=f)
        print('#define IO_TMORE  2', file=f)
        print('#define IA_TSTAR  80            ; - timeout at start of input', file=f)
        print('#define IO_TSTAR  1', file=f)
        print('#define GMODE     247           ;Graphics - available', file=f)
        print('#define GA_MDRW   246           ; - Invisible draw (drawstring)', file=f)
        print('#define GO_MDRW   64', file=f)
        print('#define GA_POFF   245           ; - Pictures OFF (drawstring)', file=f)
        print('#define GO_POFF   32', file=f)
        print('#define GA_WKEY   244           ; - Wait after drawing (drawstring)', file=f)
        print('#define GO_WKEY   16', file=f)
        print('#define GA_CBOR   243           ; - Change BORDER (drawstring)', file=f)
        print('#define GO_CBOR   8', file=f)
        print('#define MOUSE     240           ;mouse available (!DRAW only)', file=f)
        print(';', file=f)
        print('#define O2      152     ; Offset of second object attributes', file=f)
        print(';', file=f)
        print('; System flags 0 - 63', file=f)
        print(';', file=f)
        if dsf:
                print('#define fDark              0', file=f)
                print('#define fObjectsCarried    1', file=f)
                print('', file=f)
                print('#define fDarkF             28', file=f)
                print('#define fGFlags            29     ; This is best tested using HASAT GMODE', file=f)
                print('#define fScore             30', file=f)
                print('#define fTurns             31     ; 2 bytes', file=f)
                print('#define fTurnsHi           32', file=f)
                print('', file=f)
                print('#define fVerb              33', file=f)
                print('#define fNoun              34', file=f)
                print('#define fAdject1           35', file=f)
                print('#define fAdverb            36', file=f)
                print('#define fMaxCarr           37', file=f)
                print('#define fPlayer            38', file=f)
                print('#define fPrep              43', file=f)
                print('#define fNoun2             44', file=f)
                print('#define fAdject2           45', file=f)
                print('#define fCPronounNoun      46', file=f)
                print('#define fCPronounAdject    47', file=f)
                print('#define fTimeout           48', file=f)
                print('#define fTimeoutFlags      49', file=f)
                print('#define fDoallObjNo        50', file=f)
                print('#define fRefObject         51', file=f)
                print('#define fStrength          52', file=f)
                print('#define fObjFlags          53', file=f)
                print('#define fRefObjLoc         54', file=f)
                print('#define fRefObjWeight      55', file=f)
                print('#define fRefObjIsContainer 56', file=f)
                print('#define fRefObjIsWearable  57', file=f)
                print('#define fRefObjAttr1       58', file=f)
                print('#define fRefObjAttr2       59', file=f)
                print('#define fInkeyKey1         60', file=f)
                print('#define fInkeyKey2         61', file=f)
                print('#define fScreenMode        62     ; 2=Text, 4=CGA, 13=EGA, 141=VGA', file=f)
                print('#define fCurrentWindow     63     ; Which window is active at the moment', file=f)
        else:
                print('#define Dark      0', file=f)
                print('#define NOCarr    1', file=f)
                print('#define Work1     2     ; These are system as we consider the stack such', file=f)
                print('#define Work2     3', file=f)
                print('#define Stack    24     ; A small stack (always 2 bytes pushed) 10 pushes', file=f)
                print('#define EMPTY    23     ; Stack can run from here', file=f)
                print('#define FULL      3     ; to here - There will be an internal one soon', file=f)
                print('#define O2Num    25     ; 1st free in system 64', file=f)
                print('#define O2Con    26     ; Object 2 is a container', file=f)
                print('#define O2Loc    27', file=f)
                print('#define DarkF    28', file=f)
                print('#define GFlags   29     ; This is best tested using HASAT GMODE', file=f)
                print('#define Score    30', file=f)
                print('#define Turns    31     ; 2 bytes', file=f)
                print('#define Verb     33', file=f)
                print('#define Noun1    34', file=f)
                print('#define Adject1  35', file=f)
                print('#define Adverb   36', file=f)
                print('#define MaxCarr  37', file=f)
                print('#define Player   38', file=f)
                print('#define O2Att    39     ; Using Flags 39 and 40 to contain attribs for other obj', file=f)
                print('#define InStream 41', file=f)
                print('#define Prompt   42', file=f)
                print('#define Prep     43', file=f)
                print('#define Noun2    44', file=f)
                print('#define Adject2  45', file=f)
                print('#define CPNoun   46', file=f)
                print('#define CPAdject 47', file=f)
                print('#define Time     48', file=f)
                print('#define TIFlags  49', file=f)
                print('#define DAObjNo  50', file=f)
                print('#define CONum    51', file=f)
                print('#define Strength 52', file=f)
                print('#define OFlags   53', file=f)
                print('#define COLoc    54', file=f)
                print('#define COWei    55', file=f)
                print('#define COCon    56', file=f)
                print('#define COWR     57', file=f)
                print('#define COAtt    58', file=f)
                print('#define Key1     60', file=f)
                print('#define Key2     61', file=f)
                print('#define ScMode   62     ; 2=Text, 4=CGA, 13=EGA, 141=VGA', file=f)
                print('#define CurWin   63     ; Which window is active at the moment', file=f)
        print(';', file=f)
        # Useful groups define section is not included in DRC
        if dsf == False:
                print(';Useful groups', file=f)
                print('#define Z80 SPE+MSX+CPC+PCW', file=f)
                print('#define M6502 CBM64', file=f)
                print('#define M68000 ST+AMIGA', file=f)
                print('#define I86 PC', file=f)
                print(';', file=f)
        if idobj:
                print('; Object identifiers.', file=f)
                print(';', file=f)
                for y, z in enumerate(listObjectIdentifiers):
                        print('#define ' + z + ' ' + str(y), file=f)
                print(';', file=f)
        if idloc:
                print('; Location identifiers.', file=f)
                print(';', file=f)
                for y, z in enumerate(listLocationIdentifiers, start=1):
                        print('#define ' + z + ' ' + str(y), file=f)
                print(';', file=f)
        if verbosity:
                print('OK.')
        
def imprimeCTL():
        if verbosity:
                if english:
                        print('Printing /CTL section',end=' -> ')   
                else:     
                        print('Imprimiendo sección /CTL',end=' -> ')
        print('/CTL', file = f)
        print(';', file = f)
        if english:
            print('; Control section', file = f)
        else:
            print('; Sección de control', file = f)
        print(';', file = f)
        print('_', file = f)
        print(';', file = f)
        if verbosity:
                print('OK.')
        
def imprimeTOK():
        if verbosity:
                print('Imprimeindo sección /TOK',end=' -> ')
        print('/TOK', file=f)
        print('_____', file=f)
        print('_que_', file=f)
        print('a_de_', file=f)
        print('o_de_', file=f)
        print('_una_', file=f)
        print('_del_', file=f)
        print('s_de_', file=f)
        print('_de_l', file=f)
        print('_con_', file=f)
        print('ente_', file=f)
        print('_por_', file=f)
        print('_está', file=f)
        print('tiene', file=f)
        print('s_un_', file=f)
        print('ante_', file=f)
        print('_para', file=f)
        print('_las_', file=f)
        print('entra', file=f)
        print('n_el_', file=f)
        print('e_de_', file=f)
        print('a_la_', file=f)
        print('erior', file=f)
        print('ción_', file=f)
        print('ando_', file=f)
        print('iente', file=f)
        print('_el_', file=f)
        print('_la_', file=f)
        print('_de_', file=f)
        print('_con', file=f)
        print('_en_', file=f)
        print('los_', file=f)
        print('ado_', file=f)
        print('_se_', file=f)
        print('esta', file=f)
        print('_un_', file=f)
        print('las_', file=f)
        print('enta', file=f)
        print('_des', file=f)
        print('_al_', file=f)
        print('ada_', file=f)
        print('as_', file=f)
        print('es_', file=f)
        print('os_', file=f)
        print('_y_', file=f)
        print('ado', file=f)
        print('te_', file=f)
        print('ada', file=f)
        print('la_', file=f)
        print('ent', file=f)
        print('res', file=f)
        print('que', file=f)
        print('an_', file=f)
        print('o_p', file=f)
        print('rec', file=f)
        print('ido', file=f)
        print('s,_', file=f)
        print('ant', file=f)
        print('ina', file=f)
        print('ida', file=f)
        print('lar', file=f)
        print('ero', file=f)
        print('mpl', file=f)
        print('a_', file=f)
        print('o_', file=f)
        print('er', file=f)
        print('es', file=f)
        print('or', file=f)
        print('ar', file=f)
        print('al', file=f)
        print('en', file=f)
        print('as', file=f)
        print('os', file=f)
        print('e_', file=f)
        print('an', file=f)
        print('el', file=f)
        print('on', file=f)
        print('in', file=f)
        print('ci', file=f)
        print('un', file=f)
        print('._', file=f)
        print('co', file=f)
        print('re', file=f)
        print('di', file=f)
        print(',_', file=f)
        print('ur', file=f)
        print('tr', file=f)
        print('de', file=f)
        print('su', file=f)
        print('ab', file=f)
        print('ol', file=f)
        print('am', file=f)
        print('st', file=f)
        print('cu', file=f)
        print('s_', file=f)
        print('ac', file=f)
        print('il', file=f)
        print('gr', file=f)
        print('ad', file=f)
        print('te', file=f)
        print('y_', file=f)
        print('im', file=f)
        print('to', file=f)
        print('ue', file=f)
        print('pi', file=f)
        print('gu', file=f)
        print('ch', file=f)
        print('ca', file=f)
        print('la', file=f)
        print('n_', file=f)
        print('ro', file=f)
        print('ri', file=f)
        print('lo', file=f)
        print('mi', file=f)
        print('l_', file=f)
        print('ti', file=f)
        print('ob', file=f)
        print('me', file=f)
        print('si', file=f)
        print('pe', file=f)
        print('_n', file=f)
        print('tu', file=f)
        print('at', file=f)
        print('fi', file=f)
        print('do', file=f)
        print('em', file=f)
        print('ay', file=f)
        print('".', file=f)
        print('ll', file=f)
        print(';------------------------------------------------------------------------------', file=f)
        if verbosity:
                print('OK.')
        
def imprimeTOK_ENG():
        if verbosity:
                print('Printing english /TOK section.',end=' -> ')
        print('/TOK    ;Tokens as supplied with PAW under CP/M', file=f)
        print('_the_', file=f)
        print('_you_', file=f)
        print('_are_', file=f)
        print('ing_', file=f)
        print('_to_', file=f)
        print('_and', file=f)
        print('_is_', file=f)
        print('You_', file=f)
        print('and_', file=f)
        print('The_', file=f)
        print("n't_", file=f)
        print('_of_', file=f)
        print('_you', file=f)
        print('ing', file=f)
        print('ed_', file=f)
        print('_a_', file=f)
        print('_op', file=f)
        print('ith', file=f)
        print('out', file=f)
        print('ent', file=f)
        print('_to', file=f)
        print('_in', file=f)
        print('all', file=f)
        print('_th', file=f)
        print('_it', file=f)
        print('ter', file=f)
        print('ave', file=f)
        print('_be', file=f)
        print('ver', file=f)
        print('her', file=f)
        print('and', file=f)
        print('ear', file=f)
        print('You', file=f)
        print('_on', file=f)
        print('en_', file=f)
        print('ose', file=f)
        print('no', file=f)
        print('ic', file=f)
        print('ap', file=f)
        print('_b', file=f)
        print('gh', file=f)
        print('__', file=f)
        print('ad', file=f)
        print('is', file=f)
        print('_c', file=f)
        print('ir', file=f)
        print('ay', file=f)
        print('ur', file=f)
        print('un', file=f)
        print('oo', file=f)
        print('_d', file=f)
        print('lo', file=f)
        print('ro', file=f)
        print('ac', file=f)
        print('se', file=f)
        print('ri', file=f)
        print('li', file=f)
        print('ti', file=f)
        print('om', file=f)
        print('bl', file=f)
        print('ck', file=f)
        print('I_', file=f)
        print('ed', file=f)
        print('ee', file=f)
        print('_f', file=f)
        print('ha', file=f)
        print('pe', file=f)
        print('e_', file=f)
        print('t_', file=f)
        print('in', file=f)
        print('s_', file=f)
        print('th', file=f)
        print(',_', file=f)
        print('er', file=f)
        print('d_', file=f)
        print('on', file=f)
        print('to', file=f)
        print('an', file=f)
        print('ar', file=f)
        print('en', file=f)
        print('ou', file=f)
        print('or', file=f)
        print('st', file=f)
        print('._', file=f)
        print('ow', file=f)
        print('le', file=f)
        print('at', file=f)
        print('al', file=f)
        print('re', file=f)
        print('y_', file=f)
        print('ch', file=f)
        print('am', file=f)
        print('el', file=f)
        print('_w', file=f)
        print('as', file=f)
        print('es', file=f)
        print('it', file=f)
        print('_s', file=f)
        print('ll', file=f)
        print('do', file=f)
        print('op', file=f)
        print('sh', file=f)
        print('me', file=f)
        print('he', file=f)
        print('bo', file=f)
        print('hi', file=f)
        print('ca', file=f)
        print('pl', file=f)
        print('il', file=f)
        print('cl', file=f)
        print('_a', file=f)
        print('of', file=f)
        print('_h', file=f)
        print('tt', file=f)
        print('mo', file=f)
        print('ke', file=f)
        print('ve', file=f)
        print('so', file=f)
        print('e.', file=f)
        print('d.', file=f)
        print('t.', file=f)
        print('vi', file=f)
        print('ly', file=f)
        print('id', file=f)
        print('sc', file=f)
        print('_p', file=f)
        print('em', file=f)
        print('r_', file=f)
        print(';------------------------------------------------------------------------------', file=f)
        if verbosity:
                print('OK.')
        
def imprimeVOC():
        if verbosity:
                print('Imprimiendo sección /VOC',end=' -> ')
        print('/VOC', file=f)
        print(';', file=f)
        print('; Sección de vocabulario del juego.', file=f)
        print(';', file=f)
        print('; Movimiento: verbos y nombres < 14 X', file=f)
        print(';', file=f)
        print('N       2       noun', file=f)
        print('NORTE   2       noun', file=f)
        print('S       3       noun', file=f)
        print('SUR     3       noun', file=f)
        print('E       4       noun', file=f)
        print('ESTE    4       noun', file=f)
        print('O       5       noun', file=f)
        print('OESTE   5       noun', file=f)
        print('NE      6       noun', file=f)
        print('NORES   6       noun', file=f)     
        print('NO      7       noun', file=f)
        print('NOROE   7       noun', file=f)     
        print('SE      8       noun', file=f)
        print('SURES   8       noun', file=f)
        print('SO      9       noun', file=f)
        print('SUROE   9       noun', file=f)     
        print('AR      10      noun', file=f)
        print('ARRIBA  10      noun', file=f)
        print('SUBIR   10      verb', file=f)
        print('SUBE    10      verb', file=f)     
        print('AB      11      noun', file=f)
        print('ABAJO   11      noun', file=f)
        print('BAJAR   11      verb', file=f)
        print('BAJA    11      verb', file=f)     
        print('ENTRA   12      verb', file=f)
        print('DENTRO  12      noun', file=f)
        print('SALIR   13      verb', file=f)
        print('SAL     13      verb', file=f)     
        print('FUERA   13      noun', file=f)
        print(';', file=f)
        print('; Nombres <20 indica que se pueden usar como verbos', file=f)
        print(';         <50 indica nombre propio (no admite lo, la...)', file=f)
        print(';', file=f)
        print('I       14      noun', file=f)
        print('INVEN   14      noun', file=f)
        print('TODO    20      noun', file=f)
        print('TODOS   20      noun', file=f)
        print('TODAS   20      noun', file=f)
        print(';', file=f)
        
def imprimeVOC_ENG():
        if verbosity:
                print('Printing english /VOC section',end=' -> ')
        print('/VOC', file=f)
        print(';', file=f)
        print('; Game vocabulary section.', file=f)
        print(';', file=f)
        print('; Movements ie verbs and nouns < 14', file=f)
        print(';', file=f)
        print('N       2       noun', file=f)
        print('NORTH   2       noun', file=f)
        print('S       3       noun', file=f)
        print('SOUTH   3       noun', file=f)
        print('E       4       noun', file=f)
        print('EAST    4       noun', file=f)
        print('W       5       noun', file=f)
        print('WEST    5       noun', file=f)
        print('NE      6       noun', file=f)
        print('NW      7       noun', file=f)
        print('SE      8       noun', file=f)
        print('SW      9       noun', file=f)
        print('U       10      noun', file=f)
        print('UP      10      noun', file=f)
        print('ASCEN   10      verb', file=f)
        print('D       11      noun', file=f)
        print('DOWN    11      noun', file=f)
        print('DESCE   11      verb', file=f)
        print('IN      12      verb', file=f)
        print('INSID   12      noun', file=f)
        print('OUT     13      verb', file=f)
        print('OUTSI   13      verb', file=f)     
        print(';', file=f)
        print('; Nouns   <20 means can be used as verbs', file=f)
        print(';         <50 means a proper noun ie not an "IT"', file=f)
        print(';', file=f)
        print('I       14      noun', file=f)
        print('INVEN   14      noun', file=f)
        print('ALL     20      noun', file=f)
        print('LOT     20      noun', file=f)
        print('EVERY   20      noun', file=f)
        print(';', file=f)
        
def imprimeVOC2():
        print(';', file=f)
        print('; Verbos', file=f)
        print(';', file=f)
        print('COGER   20      verb', file=f)
        print('COGE    20      verb', file=f)
        print('COGEL   20      verb', file=f)     
        print('DEJAR   21      verb', file=f)
        print('DEJA    21      verb', file=f)
        print('DEJAL   21      verb', file=f)     
        print('SOLTAR  21      verb', file=f)
        print('QUITAR  22      verb', file=f)
        print('PONER   23      verb', file=f)
        print('PONTE   23      verb', file=f)     
        print('MIRAR   24      verb', file=f)
        print('M       24      verb', file=f)     
        print('REDES   24      verb', file=f)
        print('R       24      verb', file=f)
        print('F       25      verb', file=f)
        print('FIN     25      verb', file=f)
        print('SAVE    26      verb', file=f)
        print('LOAD    27      verb', file=f)
        print('RAMSA   28      verb', file=f)
        print('RAMLO   29      verb', file=f)
        print('EX      30      verb', file=f)
        print('EXAMI   30      verb', file=f)
        print('DECIR   31      verb', file=f)
        print('PREGUNT 31      verb', file=f)
        print('HABLAR  31      verb', file=f)
        print('SALIDAS 32      verb', file=f)
        print('AYUDA   33      verb', file=f)
        print('METER   34      verb', file=f)
        print('METE    34      verb', file=f)
        print('METEL   34      verb', file=f)
        print('INTRO   34      verb', file=f)
        print('SACAR   35      verb', file=f)
        print('SACA    35      verb', file=f)
        print('SACAL   35      verb', file=f)
        print('EXTRA   35      verb', file=f)
        print('VACIAR  36      verb', file=f)
        print(';', file=f)
        print('; Adjetivos', file=f)
        print(';', file=f)
        print('PEQUE   2       adjective', file=f)
        print('GRANDE  3       adjective', file=f)
        print('VIEJO   4       adjective', file=f)
        print('VIEJA   4       adjective', file=f)
        print('NUEVO   5       adjective', file=f)
        print('NUEVA   5       adjective', file=f)
        print('DURO    6       adjective', file=f)
        print('DURA    6       adjective', file=f)
        print('BLANDO  7       adjective', file=f)
        print('CORTO   8       adjective', file=f)
        print('CORTA   8       adjective', file=f)
        print('LARGO   9       adjective', file=f)
        print('LARGA   9       adjective', file=f)
        print(';', file=f)
        print('; Adverbios', file=f)
        print(';', file=f)
        print('RAPID   2       adverb', file=f)
        print('RáPID   2       adverb', file=f)
        print('DESPA   3       adverb', file=f)
        print('LENTA   3       adverb', file=f)
        print('CUIDA   5       adverb', file=f)
        print(';', file=f)
        print('; Preposiciones', file=f)
        print(';', file=f)
        print('A       2       preposition', file=f)
        print('DE      3       preposition', file=f)
        print('EN      4       preposition', file=f)
        print('POR     5       preposition', file=f)
        print('TRAVES  5       preposition', file=f)
        print('BAJO    7       preposition', file=f)
        print('JUNTO   8       preposition', file=f)
        print('MENOS   13      preposition', file=f)
        print(';', file=f)
        print('; Pronombres', file=f)
        print(';', file=f)
        print(';', file=f)
        print('; Conjunciones (mal llamadas "conjugation" en el DAAD). :-)', file=f)
        print(';', file=f)
        print('Y       2       conjugation', file=f)
        print('ENTONCE 2       conjugation', file=f)
        print('LUEGO   2       conjugation', file=f)
        print(';', file=f)
        if verbosity:
                print('OK.')
        
def imprimeVOC2_ENG():
        print(';', file=f)
        print('; Verbs', file=f)
        print(';', file=f)
        print('GET     20      verb', file=f)
        print('TAKE    20      verb', file=f)
        print('DROP    21      verb', file=f)
        print('PUT     21      verb', file=f)
        print('REMOV   22      verb', file=f)
        print('WEAR    23      verb', file=f)
        print('R       24      verb', file=f)
        print('REDES   24      verb', file=f)
        print('LOOK    24      verb', file=f)
        print('L       24      verb', file=f)     
        print('QUIT    25      verb', file=f)
        print('STOP    25      verb', file=f)
        print('SAVE    26      verb', file=f)
        print('LOAD    27      verb', file=f)
        print('RAMSA   28      verb', file=f)
        print('RAMLO   29      verb', file=f)
        print('X       30      verb', file=f)
        print('EX      30      verb', file=f)
        print('EXAMI   30      verb', file=f)
        print('SAY     31      verb', file=f)
        print('ASK     31      verb', file=f)
        print('TALK    31      verb', file=f)
        print('SPEAK   31      verb', file=f)
        print('EXITS   32      verb', file=f)
        print('HELP    33      verb', file=f)
        print('EMPTY   34      verb', file=f)
        print('INSERT  35      verb', file=f)
        print('PLACE   35      verb', file=f)
        print('EXTRACT 36      verb', file=f)
        print(';', file=f)
        print('; Adjectives', file=f)
        print(';', file=f)
        print('SMALL   2       adjective', file=f)
        print('BIG     3       adjective', file=f)
        print('LARGE   3       adjective', file=f)
        print('OLD     4       adjective', file=f)
        print('NEW     5       adjective', file=f)
        print('HARD    6       adjective', file=f)
        print('SOFT    7       adjective', file=f)
        print('SHORT   8       adjective', file=f)
        print('LONG    9       adjective', file=f)
        print(';', file=f)
        print('; Adverbs', file=f)
        print(';', file=f)
        print('QUICK   2       adverb', file=f)
        print('SLOWL   3       adverb', file=f)
        print('QUIET   4       adverb', file=f)
        print('LOUDL   5       adverb', file=f)
        print('CAREF   6       adverb', file=f)
        print('SOFTL   6       adverb', file=f)
        print('GENTL   6       adverb', file=f)
        print(';', file=f)
        print('; Prepositions', file=f)
        print(';', file=f)
        print('TO      2       preposition', file=f)
        print('FROM    3       preposition', file=f)
        print(';IN      4       preposition', file=f)
        print(';OUT     5       preposition', file=f)
        print('THROU   6       preposition', file=f)
        print('OVER    7       preposition', file=f)
        print('UNDER   8       preposition', file=f)
        print('BY      9       preposition', file=f)
        print('ON      10      preposition', file=f)
        print('OFF     11      preposition', file=f)
        print('AT      12      preposition', file=f)
        print('EXCEP   13      preposition', file=f)
        print(';', file=f)
        print('; Pronouns', file=f)
        print(';', file=f)
        print('IT      2       pronoun', file=f)
        print('THEM    2       pronoun', file=f)
        print(';', file=f)
        print('; Conjunctions (improperly called conjugations in DAAD). :-)', file=f)
        print(';', file=f)
        print('AND     2       conjugation', file=f)
        print('THEN    2       conjugation', file=f)
        print(';', file=f)
        print(';------------------------------------------------------------------------------', file=f)
        if verbosity:
                print('OK.')      

def imprimeSTX_2p_SPA_DSF():
        if verbosity:
                print('Imprimiendo sección /STX (en 2ª persona)',end=' -> ')
        print('/STX', file=f)
        print(';', file=f)
        print('; Mensajes del sistema (en segunda persona).', file=f)
        print(';', file=f)
        print('/0 "Está demasiado oscuro para ver nada."', file=f)
        print('/1 "También puedes ver: "', file=f)
        print('/2 "#n¿Qué haces ahora?"', file=f)
        print('/3 "#n¿Qué quieres hacer?"', file=f)
        print('/4 "#n¿Qué quieres hacer ahora?"', file=f)
        print('/5 "#n¿Qué haces?"', file=f)
        print('/6 "No he entendido nada.#n"', file=f)
        print('/7 "No puedes ir en esa dirección.#n"', file=f)
        print('/8 "No puedes hacer eso.#n"', file=f)
        print('/9 "Llevas:#n"', file=f)
        print('/10 "Llevas puesto:#n"', file=f)
        print('/11 "" ;*Libre', file=f)
        print('/12 "¿Seguro?"', file=f)
        print('/13 "¿Quieres intentarlo de nuevo?"', file=f)
        print('/14 "";*Libre', file=f)
        print('/15 "Vale.#n"', file=f)
        print('/16 "Pulsa una tecla para continuar.#n"', file=f)
        print('/17 "" ;*Has jugado', file=f)
        print('/18 "" ;*\sturno', file=f)
        print('/19 "" ;*s', file=f)
        print('/20 "" ;*.[CR]', file=f)
        print('/21 "" ;*Has resuelto un', file=f)
        print('/22 "" ;*%[CR]', file=f)
        print('/23 "No llevas eso puesto.#n"', file=f)
        print('/24 "No puedes. Tienes puesto _.#n"', file=f)
        print('/25 "Ya tienes _.#n"', file=f)
        print('/26 "Aquí no hay nada de eso.#n"', file=f)
        print('/27 "No puedes llevar nada más.#n"', file=f)
        print('/28 "No tienes eso.#n"', file=f)
        print('/29 "Ya llevas puesto _.#n"', file=f)
        print('/30 "S" ;Un sólo caracter en mayúsculas. Inicial de Sí', file=f)
        print('/31 "N" ;Un sólo caracter en mayúsculas. Inicial de No', file=f)
        print('/32 "Hay más..."', file=f)
        print('/33 "#n>"', file=f)
        print('/34 "";*Libre', file=f)
        print('/35 "#nEl tiempo pasa...#n"', file=f)
        print('/36 "Has cogido _.#n"', file=f)
        print('/37 "Te has puesto _.#n"', file=f)
        print('/38 "Te has quitado _.#n"', file=f)
        print('/39 "Has dejado _.#n"', file=f)
        print('/40 "No puedes ponerte _.#n"', file=f)
        print('/41 "No puedes quitarte _.#n"', file=f)
        print('/42 "No puedes quitarte _.  No puedes llevar nada más en las manos.#n"', file=f)
        print('/43 "@ pesa demasiado para tí.#n"', file=f)
        print('/44 "@ está en "', file=f)
        print('/45 "@ no está en "', file=f)
        print('/46 ", "', file=f)
        print('/47 " y "', file=f)
        print('/48 ".#n"', file=f)
        print('/49 "No tienes _.#n"', file=f)
        print('/50 "No llevas puesto _.#n"', file=f)
        print('/51 ".#n"', file=f)
        print('/52 "No hay nada de eso en "', file=f)
        print('/53 "Nada.#n"', file=f)
        print('/54 "C" ;Inicial de Cinta', file=f)
        print('/55 "D" ;Disco', file=f)
        print('/56 "Unidad no preparada. Pulsa una tecla para volver a intentarlo.#n"', file=f)
        print('/57 "Error de entrada/salida.#n"', file=f)
        print('/58 "El disco o el directorio puede estar lleno.#n"', file=f)
        print('/59 "Nombre de fichero no válido.#n"', file=f)
        print('/60 "Nombre del fichero:"', file=f)
        print('/61 "Pon en marcha la cinta.#n"', file=f)
        print('/62 "¿Cinta o disco?"', file=f)
        print('/63 "No ves nada extraño en _.#n"', file=f)
        print('/64 "En _ ves:#n"', file=f)
        print(';', file=f)
        if verbosity:
                print('OK.')

def imprimeSTX1p_SPA_DSF():
        if verbosity:
                print('Imprimiendo sección /STX (en 1ª persona)',end=' -> ')
        print('/STX', file=f)
        print(';', file=f)
        print('; Mensajes del sistema (en primera persona).', file=f)
        print(';', file=f)
        print('/0 "Está demasiado oscuro para ver nada."', file=f)
        print('/1 "También puedo ver: "', file=f)
        print('/2 "#n¿Qué hago ahora?"', file=f)
        print('/3 "#n¿Qué quieres que haga?"', file=f)
        print('/4 "#n¿Qué quieres que haga ahora?"', file=f)
        print('/5 "#n¿Qué hago?"', file=f)
        print('/6 "No he entendido nada.#n"', file=f)
        print('/7 "No puedo ir en esa dirección.#n"', file=f)
        print('/8 "No puedo hacer eso.#n"', file=f)
        print('/9 "Llevo:#n"', file=f)
        print('/10 "Llevo puesto:#n"', file=f)
        print('/11 "" ;*Libre', file=f)
        print('/12 "¿Seguro?"', file=f)
        print('/13 "¿Quieres intentarlo de nuevo?"', file=f)
        print('/14 "" ;*Libre', file=f)
        print('/15 "Vale.#n"', file=f)
        print('/16 "Pulsa una tecla para continuar.#n"', file=f)
        print('/17 "" ;*Has jugado', file=f)
        print('/18 "" ;*\sturno', file=f)
        print('/19 "" ;*s', file=f)
        print('/20 "" ;*.[CR]', file=f)
        print('/21 "" *Ha resuelto un', file=f)
        print('/22 "" ;*%[CR]', file=f)
        print('/23 "No llevo eso puesto.#n"', file=f)
        print('/24 "No puedo. Tengo puesto _.#n"', file=f)
        print('/25 "Ya tengo _.#n"', file=f)
        print('/26 "Aquí no hay nada de eso.#n"', file=f)
        print('/27 "No puedo llevar nada más.#n"', file=f)
        print('/28 "No tengo eso.#n"', file=f)
        print('/29 "Ya llevo puesto _.#n"', file=f)
        print('/30 "S" ; Un solo caracter en mayúsculas. Inicial de Sí', file=f)
        print('/31 "N" ; Un solo caracter en mayúsculas. Inicial de No', file=f)
        print('/32 "Hay más..."', file=f)
        print('/33 "#n>"', file=f)
        print('/34 "" ;*Libre', file=f)
        print('/35 "#nEl timpo pasa...#n"', file=f)
        print('/36 "He cogido _.#n"', file=f)
        print('/37 "Me he puesto _.#n"', file=f)
        print('/38 "Me he quitado _.#n"', file=f)
        print('/39 "He dejado _.#n"', file=f)
        print('/40 "No puedo ponerme _.#n"', file=f)
        print('/41 "No puedo quitarme _.#n"', file=f)
        print('/42 "No puedo quitarme _.  No puedo llevar nada más en las manos.#n"', file=f)
        print('/43 "@ pesa demasiado para mí.#n"', file=f)
        print('/44 "@ está en "', file=f)
        print('/45 "@ no está en "', file=f)
        print('/46 ", "', file=f)
        print('/47 " y "', file=f)
        print('/48 ".#n"', file=f)
        print('/49 "No tengo _.#n', file=f)
        print('/50 "No llevo puesto _.#n"', file=f)
        print('/51 ".#n"', file=f)
        print('/52 "No hay nada de eso en "', file=f)
        print('/53 "Nada.#n"', file=f)
        print('/54 "C" ; Inicial de Cinta', file=f)
        print('/55 "D" ; Disco', file=f)
        print('/56 "Unidad no preparada. Pulsa una tecla para volver a intentarlo.#n"', file=f)
        print('/57 "Error de entrada/salida.#n"', file=f)
        print('/58 "El disco o el directorio puede estar lleno.#n', file=f)
        print('/59 "Nombre de fichero no válido.#n"', file=f)
        print('/60 "Nombre del fichero:"', file=f)
        print('/61 "Pon en marcha la cinta.#n"', file=f)
        print('/62 "¿Cinta o disco?"', file=f)
        print('/63 "No veo nada extraño en _.#n"', file=f)
        print('/64 "En _ veo:#n"', file=f)
        print(';', file=f)
        if verbosity:
                print('OK.')        

def imprimeSTX_1p_ENG_DSF():
        if verbosity:
                print('Printing english 2º person /STX section',end=' -> ')
        print('/STX', file=f)
        print(';', file=f)
        print('; System Message Texts (2nd person).', file=f)
        print(';', file=f)
        print('/0 "It\'s too dark to see anything."', file=f)
        print('/1 "I can also see: "', file=f)
        print('/2 "#nWhat now?"', file=f)
        print('/3 "#nWhat next?"', file=f)
        print('/4 "#nWhat should I do now?"', file=f)
        print('/5 "#nWhat should I do next?"', file=f)
        print('/6 "I was not able to understand any of that.  Please try again.#n"', file=f)
        print('/7 "I can\'t go in that direction.#n"', file=f)
        print('/8 "I can\'t do that.#n"', file=f)
        print('/9 "I have with me:#n"', file=f)
        print('/10 "I am wearing:#n"', file=f)
        print('/11 "" ;*Spare', file=f)
        print('/12 "Are you sure?"', file=f)
        print('/13 "Would you like another go?"', file=f)
        print('/14 "" ; *Spare', file=f)
        print('/15 "OK.#n"', file=f)
        print('/16 "Press any key to continue.#n"', file=f)
        print('/17 "" ; *You have taken', file=f)
        print('/18 "" ; *\sturn', file=f)
        print('/19 "" ; *s', file=f)
        print('/20 "" ; *.[CR]', file=f)
        print('/21 "" ; *You have scored', file=f)
        print('/22 "" ; *%[CR]', file=f)
        print('/23 "I\'m not wearing one of those.#n"', file=f)
        print('/24 "I can\'t. I\'m wearing the _.#n"', file=f)
        print('/25 "I already have the _.#n"', file=f)
        print('/26 "There isn\'t one of those here..#n"', file=f)
        print('/27 "I can\'t carry any more things.#n"', file=f)
        print('/28 "I don\'t have one of those.#n"', file=f)
        print('/29 "I\'m already wearing the _.#n"', file=f)
        print('/30 "Y" ; One upper case character only. Initial of Yes', file=f)
        print('/31 "N" ; One upper case character only. Inicial de No', file=f)
        print('/32 "More..."', file=f)
        print('/33 "#n>"', file=f)
        print('/34 "" ; *Spare', file=f)
        print('/35 "#nTime passes...#n"', file=f)
        print('/36 "I now have the _.#n"', file=f)
        print('/37 "I\'m now wearing the _.#n"', file=f)
        print('/38 "I\'ve removed the _.#n"', file=f)
        print('/39 "I\'ve dropped the _.#n"', file=f)
        print('/40 "I can\'t wear the _.#n"', file=f)
        print('/41 "I can\'t remove the _.#n"', file=f)
        print('/42 "I can\'t remove the _. My hands are full.#n"', file=f)
        print('/43 "The _ weighs too much for me.#n"', file=f)
        print('/44 "The _ is in the "', file=f)
        print('/45 "The _ isn\'t in the "', file=f)
        print('/46 ", "', file=f)
        print('/47 " and "', file=f)
        print('/48 ".#n"', file=f)
        print('/49 "I don\'t have the _.#n"', file=f)
        print('/50 "I\'m not wearing the _.#n"', file=f)
        print('/51 ".#n"', file=f)
        print('/52 "There isn\'t one of those in the "', file=f)
        print('/53 "Nothing.#n"', file=f)
        print('/54 "T" ; Letter for Tape', file=f)
        print('/55 "D" ; Disk', file=f)
        print('/56 "Drive not ready. Press any key to retry.#n"', file=f)
        print('/57 "I/O error.#n"', file=f)
        print('/58 "Disk or directory may be full.#n"', file=f)
        print('/59 "Invalid filename.#n"', file=f)
        print('/60 "Type in name of file:"', file=f)
        print('/61 "Start tape.#n"', file=f)
        print('/62 "Tape or disk?"', file=f)
        print('/63 "I see nothing unusual in the _.#n"', file=f)
        print('/64 "Inside the _ I see:#n"', file=f)
        print(";", file=f)
        if verbosity:
                print('OK.')

def imprimeSTX_2p_ENG_DSF():
        if verbosity:
                print('Printing english 2º person /STX section',end=' -> ')
        print('/STX', file=f)
        print(';', file=f)
        print('; System Message Texts (2nd person).', file=f)
        print(';', file=f)
        print('/0 "It\'s too dark to see anything."', file=f)
        print('/1 "You can also see: "', file=f)
        print('/2 "#nWhat now?"', file=f)
        print('/3 "#nWhat next?"', file=f)
        print('/4 "#nWhat do you want to do now?"', file=f)
        print('/5 "#nAny idea?"', file=f)
        print('/6 "I couldn\'t understand that.#n"', file=f)
        print('/7 "You can\'t go that way.#n"', file=f)
        print('/8 "You can\'t do that.#n"', file=f)
        print('/9 "You\'re carrying:#n"', file=f)
        print('/10 "You\'re wearing:#n"', file=f)
        print('/11 "" ;*Spare', file=f)
        print('/12 "Are you sure?"', file=f)
        print('/13 "Would you like to try again?"', file=f)
        print('/14 "" ; *Spare', file=f)
        print('/15 "OK.#n"', file=f)
        print('/16 "Press any key to continue.#n"', file=f)
        print('/17 "" ; *You have taken', file=f)
        print('/18 "" ; *\sturn', file=f)
        print('/19 "" ; *s', file=f)
        print('/20 "" ; *.[CR]', file=f)
        print('/21 "" ; *You have scored', file=f)
        print('/22 "" ; *%[CR]', file=f)
        print('/23 "You\'re not wearing that.#n"', file=f)
        print('/24 "You can\'t. You\'re wearing the _.#n"', file=f)
        print('/25 "You already have the _.#n"', file=f)
        print('/26 "You can\'t see that here.#n"', file=f)
        print('/27 "You can\'t carry any more things.#n"', file=f)
        print('/28 "You don\'t have that.#n"', file=f)
        print('/29 "You\'re already wearing the _.#n"', file=f)
        print('/30 "Y" ; One upper case character only. Initial of Yes', file=f)
        print('/31 "N" ; One upper case character only. Inicial de No', file=f)
        print('/32 "More..."', file=f)
        print('/33 "#n>"', file=f)
        print('/34 "" ; *Spare', file=f)
        print('/35 "#nTime passes...#n"', file=f)
        print('/36 "You now have the _.#n"', file=f)
        print('/37 "You\'re now wearing the _.#n"', file=f)
        print('/38 "You have removed the _.#n"', file=f)
        print('/39 "You have dropped the _.#n"', file=f)
        print('/40 "You can\'t wear the _.#n"', file=f)
        print('/41 "You can\'t remove the _.#n"', file=f)
        print('/42 "You can\'t remove the _. Your hands are full.#n"', file=f)
        print('/43 "The _ weighs too much for you.#n"', file=f)
        print('/44 "The _ is in the "', file=f)
        print('/45 "The _ isn\'t in the "', file=f)
        print('/46 ", "', file=f)
        print('/47 " and "', file=f)
        print('/48 ".#n"', file=f)
        print('/49 "You don\'t have the _.#n"', file=f)
        print('/50 "You\'re not wearing the _.#n"', file=f)
        print('/51 ".#n"', file=f)
        print('/52 "There isn\'t one of those in the "', file=f)
        print('/53 "Nothing.#n"', file=f)
        print('/54 "T" ; Letter for Tape', file=f)
        print('/55 "D" ; Disk', file=f)
        print('/56 "Unit not ready. Press a key to try again.#n"', file=f)
        print('/57 "Input/output error.#n"', file=f)
        print('/58 "Disk or directory might be full.#n"', file=f)
        print('/59 "Invalid filename.#n"', file=f)
        print('/60 "Filename:"', file=f)
        print('/61 "Start the tape.#n"', file=f)
        print('/62 "Tape or disk?"', file=f)
        print('/63 "You see nothing unusual in the _.#n"', file=f)
        print('/64 "Inside the _ you see:#n"', file=f)
        print(";", file=f)
        if verbosity:
                print('OK.')

def imprimeSTX_2p_SPA():
        if verbosity:
                print('Imprimiendo sección /STX (en 2ª persona)',end=' -> ')
        print('/STX',file=f)
        print(';', file=f)
        print('; Mensajes del sistema (en segunda persona).', file=f)
        print(';', file=f)
        print('/0',file=f)
        print('Está demasiado oscuro para ver nada.',file=f)
        print('/1',file=f)
        print('También puedes ver: ',file=f)
        print('/2',file=f)
        print('',file=f)
        print('¿Qué haces ahora?',file=f)
        print('/3',file=f)
        print('',file=f)
        print('¿Qué quieres hacer?',file=f)
        print('/4',file=f)
        print('',file=f)
        print('¿Qué quieres hacer ahora?',file=f)
        print('/5',file=f)
        print('',file=f)
        print('¿Qué haces?',file=f)
        print('/6',file=f)
        print('No he entendido nada.',file=f)
        print('',file=f)
        print('/7',file=f)
        print('No puedes ir en esa dirección.',file=f)
        print('',file=f)
        print('/8',file=f)
        print('No puedes hacer eso.',file=f)
        print('',file=f)
        print('/9',file=f)
        print('Llevas:',file=f)
        print('',file=f)
        print('/10',file=f)
        print('Llevas puesto:',file=f)
        print('',file=f)
        print('/11 ;*Libre',file=f)
        print('/12',file=f)
        print('¿Seguro?',file=f)
        print('/13',file=f)
        print('¿Quieres intentarlo de nuevo?',file=f)
        print('/14 ;*Libre',file=f)
        print('/15',file=f)
        print('Vale.',file=f)
        print('',file=f)
        print('/16',file=f)
        print('Pulsa una tecla para continuar.',file=f)
        print('',file=f)
        print('/17 ;*Has jugado',file=f)
        print('/18 ;*\sturno',file=f)
        print('/19 ;*s',file=f)
        print('/20 ;*.[CR]',file=f)
        print('/21 ;*Has resuelto un',file=f)
        print('/22 ;*%[CR]',file=f)
        print('/23',file=f)
        print('No llevas eso puesto.',file=f)
        print('',file=f)
        print('/24',file=f)
        print('No puedes. Tienes puesto _.',file=f)
        print('',file=f)
        print('/25',file=f)
        print('Ya tienes _.',file=f)
        print('',file=f)
        print('/26',file=f)
        print('Aquí no hay nada de eso.',file=f)
        print('',file=f)
        print('/27',file=f)
        print('No puedes llevar nada más.',file=f)
        print('',file=f)
        print('/28',file=f)
        print('No tienes eso.',file=f)
        print('',file=f)
        print('/29',file=f)
        print('Ya llevas puesto _.',file=f)
        print('',file=f)
        print('/30     ;Un solo caracter en mayúsculas. Inicial de Sí',file=f)
        print('S',file=f)
        print('/31     ;Un solo caracter en mayúsculas. Inicial de No',file=f)
        print('N',file=f)
        print('/32',file=f)
        print('Hay más...',file=f)
        print('/33',file=f)
        print('',file=f)
        print('>',file=f)
        print('/34 ;*Libre',file=f)
        print('/35',file=f)
        print('',file=f)
        print('El tiempo pasa...',file=f)
        print('',file=f)
        print('/36',file=f)
        print('Has cogido _.',file=f)
        print('',file=f)
        print('/37',file=f)
        print('Te has puesto _.',file=f)
        print('',file=f)
        print('/38',file=f)
        print('Te has quitado _.',file=f)
        print('',file=f)
        print('/39',file=f)
        print('Has dejado _.',file=f)
        print('',file=f)
        print('/40',file=f)
        print('No puedes ponerte _.',file=f)
        print('',file=f)
        print('/41',file=f)
        print('No puedes quitarte _.',file=f)
        print('',file=f)
        print('/42',file=f)
        print('No puedes quitarte _.  No puedes llevar nada más en las manos.',file=f)
        print('',file=f)
        print('/43',file=f)
        print('@ pesa demasiado para tí.',file=f)
        print('',file=f)
        print('/44',file=f)
        print('@ está en ',file=f)
        print('/45',file=f)
        print('@ no está en ',file=f)
        print('/46',file=f)
        print(', ',file=f)
        print('/47',file=f)
        print(' y ',file=f)
        print('/48',file=f)
        print('.',file=f)
        print('',file=f)
        print('/49',file=f)
        print('No tienes _.',file=f)
        print('',file=f)
        print('/50',file=f)
        print('No llevas puesto _.',file=f)
        print('',file=f)
        print('/51',file=f)
        print('.',file=f)
        print('',file=f)
        print('/52',file=f)
        print('No hay nada de eso en',file=f)
        print('/53',file=f)
        print('Nada.',file=f)
        print('',file=f)
        print('/54 ;Inicial de Cinta',file=f)
        print('C',file=f)
        print('/55 ;Disco',file=f)
        print('D',file=f)
        print('/56',file=f)
        print('Unidad no preparada. Pulsa una tecla para volver a intentarlo.',file=f)
        print('',file=f)
        print('/57',file=f)
        print('Error de entrada/salida.',file=f)
        print('',file=f)
        print('/58',file=f)
        print('El disco o el directorio puede estar lleno.',file=f)
        print('',file=f)
        print('/59',file=f)
        print('Nombre de fichero no válido.',file=f)
        print('',file=f)
        print('/60',file=f)
        print('Nombre del fichero:',file=f)
        print('/61',file=f)
        print('Pon en marcha la cinta.',file=f)
        print('',file=f)
        print('/62',file=f)
        print('¿Cinta o disco?',file=f)
        print('/63', file=f)      
        print('No ves nada extraño en _.', file=f)
        print('', file=f)
        print('/64', file=f)
        print('En _ ves:', file=f)
        print('', file=f)
        print(';', file=f)
        if verbosity:
                print('OK.')
        
def imprimeSTX_2p_ENG():
        if verbosity:
                print('Printing english 2º person /STX section',end=' -> ')
        print('/STX', file=f)
        print(';', file=f)
        print('; System Message Texts (2nd person).', file=f)
        print(';', file=f)
        print('/0', file=f)
        print("It's too dark to see anything.", file=f)
        print('/1', file=f)
        print('You can also see: ', file=f)
        print('/2', file=f)
        print('', file=f)
        print('What now?', file=f)
        print('/3', file=f)
        print('', file=f)
        print('What next?', file=f)
        print('/4', file=f)
        print('', file=f)
        print('What do you want to do now?', file=f)
        print('/5', file=f)
        print('', file=f)
        print('Any idea?', file=f)
        print('/6', file=f)
        print("I couldn't understand that.", file=f)
        print('', file=f)
        print('/7', file=f)
        print("You can't go that way.", file=f)
        print('', file=f)
        print('/8', file=f)
        print("You can't do that.", file=f)
        print('', file=f)
        print('/9', file=f)
        print("You're carrying:", file=f)
        print('', file=f)
        print('/10', file=f)
        print("You're wearing:", file=f)
        print('', file=f)
        print('/11 ;*Spare', file=f)
        print('/12', file=f)
        print('Are you sure?', file=f)
        print('/13', file=f)
        print('Would you like to try again?', file=f)
        print('/14 ;*Spare', file=f)
        print('/15', file=f)
        print('OK.', file=f)
        print('', file=f)
        print('/16', file=f)
        print('Press any key to continue.', file=f)
        print('', file=f)
        print('/17 ;*You have taken', file=f)
        print('/18 ;*\sturn', file=f)
        print('/19 ;*s', file=f)
        print('/20 ;*.[CR]', file=f)
        print('/21 ;*You have scored', file=f)
        print('/22 ;*%[CR]', file=f)
        print('/23', file=f)
        print("You're not wearing that.", file=f)
        print('', file=f)
        print('/24', file=f)
        print("You can't. You're wearing the _.", file=f)
        print('', file=f)
        print('/25', file=f)
        print('You already have the _.', file=f)
        print('', file=f)
        print('/26', file=f)
        print("You can't see that here.", file=f)
        print('', file=f)
        print('/27', file=f)
        print("You can't carry any more things.", file=f)
        print('', file=f)
        print('/28', file=f)
        print("You don't have that.", file=f)
        print('', file=f)
        print('/29', file=f)
        print("You're already wearing the _.", file=f)
        print("", file=f)
        print("/30     ;One upper case character only. Inicial de S¡", file=f)
        print("Y", file=f)
        print("/31     ;One upper case character only. Inicial de No", file=f)
        print("N", file=f)
        print("/32", file=f)
        print("More...", file=f)
        print("/33", file=f)
        print("", file=f)
        print(">", file=f)
        print("/34 ;*Spare", file=f)
        print("/35", file=f)
        print("", file=f)
        print("Time passes...", file=f)
        print("", file=f)
        print("/36", file=f)
        print("You now have the _.", file=f)
        print("", file=f)
        print("/37", file=f)
        print("You're now wearing the _.", file=f)
        print("", file=f)
        print("/38", file=f)
        print("You have removed the _.", file=f)
        print("", file=f)
        print("/39", file=f)
        print("You have dropped the _.", file=f)
        print("", file=f)
        print("/40", file=f)
        print("You can't wear the _.", file=f)
        print("", file=f)
        print("/41", file=f)
        print("You can't remove the _.", file=f)
        print("", file=f)
        print("/42", file=f)
        print("You can't remove the _. Your hands are full.", file=f)
        print("", file=f)
        print("/43", file=f)
        print("The _ weighs too much for you.", file=f)
        print("", file=f)
        print("/44", file=f)
        print("The _ is in the ", file=f)
        print("/45", file=f)
        print("The _ isn't in the ", file=f)
        print("/46", file=f)
        print(", ", file=f)
        print("/47", file=f)
        print(" and ", file=f)
        print("/48", file=f)
        print(".", file=f)
        print("", file=f)
        print("/49", file=f)
        print("You don't have the _.", file=f)
        print("", file=f)
        print("/50", file=f)
        print("You're not wearing the _.", file=f)
        print("", file=f)
        print("/51", file=f)
        print(".", file=f)
        print("", file=f)
        print("/52", file=f)
        print("There isn't one of those in the ", file=f)
        print("/53", file=f)
        print("Nothing.", file=f)
        print("", file=f)
        print("/54 ;Letter for Tape", file=f)
        print("T", file=f)
        print("/55 ;Disk", file=f)
        print("D", file=f)
        print("/56", file=f)
        print("Unit not ready. Press a key to try again.", file=f)
        print("", file=f)
        print("/57", file=f)
        print("Input/output error.", file=f)
        print("", file=f)
        print("/58", file=f)
        print("Disk or directory might be full.", file=f)
        print("", file=f)
        print("/59", file=f)
        print("Invalid filename.", file=f)
        print("", file=f)
        print("/60", file=f)
        print("Filename:", file=f)
        print("/61", file=f)
        print("Start the tape.", file=f)
        print("", file=f)
        print("/62", file=f)
        print("Tape or disk?", file=f)
        print("/63", file=f)      
        print("You see nothing unusual in the _.", file=f)
        print("", file=f)
        print("/64", file=f)
        print('Inside the _ you see:', file=f)
        print('', file=f)
        print(";", file=f)
        if verbosity:
                print('OK.')      
        
def imprimeSTX_1p_SPA():
        if verbosity:
                print('Imprimiendo sección /STX (en 1ª persona)',end=' -> ')
        print('/STX', file=f)
        print(';', file=f)
        print('; Mensajes del sistema (en primera persona).', file=f)
        print(';', file=f)
        print('/0', file=f)
        print('Está demasiado oscuro para ver nada.', file=f)
        print('/1', file=f)
        print('Tambien puedo ver:', file=f)
        print('/2', file=f)
        print('', file=f)
        print('¿Qué hago ahora?', file=f)
        print('/3', file=f)
        print('', file=f)
        print('¿Qué quieres que haga?', file=f)
        print('/4', file=f)
        print('', file=f)
        print('¿Qué quieres que haga ahora?', file=f)
        print('/5', file=f)
        print('', file=f)
        print('¿Qué hago?', file=f)
        print('/6', file=f)
        print('No he entendido nada.', file=f)
        print('', file=f)
        print('/7', file=f)
        print('No puedo ir en esa dirección.', file=f)
        print('', file=f)
        print('/8', file=f)
        print('No puedo hacer eso.', file=f)
        print('', file=f)
        print('/9', file=f)
        print('Llevo:', file=f)
        print('', file=f)
        print('/10', file=f)
        print('Llevo puesto:', file=f)
        print('', file=f)
        print('/11 ;*Libre', file=f)
        print('/12', file=f)
        print('¿Seguro?', file=f)
        print('/13', file=f)
        print('¿Quieres intentarlo de nuevo?', file=f)
        print('/14 ;*Libre', file=f)
        print('/15', file=f)
        print('Vale.', file=f)
        print('', file=f)
        print('/16', file=f)
        print('Pulsa una tecla para continuar.', file=f)
        print('', file=f)
        print('/17 ;*Has jugado', file=f)
        print('/18 ;*\sturno', file=f)
        print('/19 ;*s', file=f)
        print('/20 ;*.[CR]', file=f)
        print('/21 ;*Ha resuelto un', file=f)
        print('/22 ;*%[CR]', file=f)
        print('/23', file=f)
        print('No llevo eso puesto.', file=f)
        print('', file=f)
        print('/24', file=f)
        print('No puedo. Tengo puesto _.', file=f)
        print('', file=f)
        print('/25', file=f)
        print('Ya tengo _.', file=f)
        print('', file=f)
        print('/26', file=f)
        print('Aquí no hay nada de eso.', file=f)
        print('', file=f)
        print('/27', file=f)
        print('No puedo llevar nada más.', file=f)
        print('', file=f)
        print('/28', file=f)
        print('No tengo eso.', file=f)
        print('', file=f)
        print('/29', file=f)
        print('Ya llevo puesto _.', file=f)
        print('', file=f)
        print('/30     ;Un solo caracter en mayúsculas. Inicial de Sí', file=f)
        print('S', file=f)
        print('/31     ;Un solo caracter en mayúsculas. Inicial de No', file=f)
        print('N', file=f)
        print('/32', file=f)
        print('Hay más...', file=f)
        print('/33', file=f)
        print('', file=f)
        print('>', file=f)
        print('/34 ;*Libre', file=f)
        print('/35', file=f)
        print('', file=f)
        print('El timpo pasa...', file=f)
        print('', file=f)
        print('/36', file=f)
        print('He cogido _.', file=f)
        print('', file=f)
        print('/37', file=f)
        print('Me he puesto _.', file=f)
        print('', file=f)
        print('/38', file=f)
        print('Me he quitado _.', file=f)
        print('', file=f)
        print('/39', file=f)
        print('He dejado _.', file=f)
        print('', file=f)
        print('/40', file=f)
        print('No puedo ponerme _.', file=f)
        print('', file=f)
        print('/41', file=f)
        print('No puedo quitarme _.', file=f)
        print('', file=f)
        print('/42', file=f)
        print('No puedo quitarme _.  No puedo llevar nada más en las manos.', file=f)
        print('', file=f)
        print('/43', file=f)
        print('@ pesa demasiado para mí.', file=f)
        print('', file=f)
        print('/44', file=f)
        print('@ está en ', file=f)
        print('/45', file=f)
        print('@ no está en ', file=f)
        print('/46', file=f)
        print(', ', file=f)
        print('/47', file=f)
        print(' y ', file=f)
        print('/48', file=f)
        print('.', file=f)
        print('', file=f)
        print('/49', file=f)
        print('No tengo _.', file=f)
        print('', file=f)
        print('/50', file=f)
        print('No llevo puesto _.', file=f)
        print('', file=f)
        print('/51', file=f)
        print('.', file=f)
        print('', file=f)
        print('/52', file=f)
        print('No hay nada de eso en', file=f)
        print('/53', file=f)
        print('Nada.', file=f)
        print('', file=f)
        print('/54 ;Inicial de Cinta', file=f)
        print('C', file=f)
        print('/55 ;Disco', file=f)
        print('D', file=f)
        print('/56', file=f)
        print('Unidad no preparada. Pulsa una tecla para volver a intentarlo.', file=f)
        print('', file=f)
        print('/57', file=f)
        print('Error de entrada/salida.', file=f)
        print('', file=f)
        print('/58', file=f)
        print('El disco o el directorio puede estar lleno.', file=f)
        print('', file=f)
        print('/59', file=f)
        print('Nombre de fichero no válido.', file=f)
        print('', file=f)
        print('/60', file=f)
        print('Nombre del fichero:', file=f)
        print('/61', file=f)
        print('Pon en marcha la cinta.', file=f)
        print('', file=f)
        print('/62', file=f)
        print('¿Cinta o disco?', file=f)
        print('/63', file=f)
        print('No veo nada extraño en _.', file=f)
        print('', file=f)
        print('/64', file=f)
        print('En _ veo:', file=f)
        print('', file=f)
        print(';', file=f)
        if verbosity:
                print('OK.')
        
def imprimeSTX_1p_ENG():
        if verbosity:
                print('Printing english /STX section 1st person)',end=' -> ')
        print("/STX    ;System Message Texts", file=f)
        print(';', file=f)
        print('; System Message Texts (1st person).', file=f)
        print(';', file=f)
        print("/0", file=f)
        print("It's too dark to see anything.", file=f)
        print("/1", file=f)
        print("I can also see: ", file=f)
        print("/2", file=f)
        print("", file=f)
        print("What now?", file=f)
        print("/3", file=f)
        print("", file=f)
        print("What next?", file=f)
        print("/4", file=f)
        print("", file=f)
        print("What should I do now?", file=f)
        print("/5", file=f)
        print("", file=f)
        print("What should I do next?", file=f)
        print("/6", file=f)
        print("I was not able to understand any of that.  Please try again.", file=f)
        print("", file=f)
        print("/7", file=f)
        print("I can't go in that direction.", file=f)
        print("", file=f)
        print("/8", file=f)
        print("I can't do that.", file=f)
        print("", file=f)
        print("/9", file=f)
        print("I have with me: ", file=f)
        print("", file=f)
        print("/10", file=f)
        print("I am wearing:", file=f)
        print("", file=f)
        print("/11 ;*Spare", file=f)
        print("/12", file=f)
        print("Are you sure? ", file=f)
        print("/13", file=f)
        print("Would you like another go? ", file=f)
        print("/14 ;*Spare", file=f)
        print("/15", file=f)
        print("OK.", file=f)
        print("", file=f)
        print("/16", file=f)
        print("Press any key to continue.", file=f)
        print("", file=f)
        print("/17 ;*You have taken", file=f)
        print("/18 ;*\sturn", file=f)
        print("/19 ;*s", file=f)
        print("/20 ;*.[CR]", file=f)
        print("/21 ;*You have scored", file=f)
        print("/22 ;*%[CR]", file=f)
        print("/23", file=f)
        print("I'm not wearing one of those.", file=f)
        print("", file=f)
        print("/24", file=f)
        print("I can't.  I'm wearing the _.", file=f)
        print("", file=f)
        print("/25", file=f)
        print("I already have the _.", file=f)
        print("", file=f)
        print("/26", file=f)
        print("There isn't one of those here.", file=f)
        print("", file=f)
        print("/27", file=f)
        print("I can't carry any more things.", file=f)
        print("", file=f)
        print("/28", file=f)
        print("I don't have one of those.", file=f)
        print("", file=f)
        print("/29", file=f)
        print("I'm already wearing the _.", file=f)
        print("", file=f)
        print("/30     ;One upper case character only", file=f)
        print("Y", file=f)
        print("/31     ;One upper case character only", file=f)
        print("N", file=f)
        print("/32", file=f)
        print("More...", file=f)
        print("/33", file=f)
        print("", file=f)
        print(">", file=f)
        print("/34 ;*Spare", file=f)
        print("/35", file=f)
        print("", file=f)
        print("Time passes...", file=f)
        print("", file=f)
        print("/36", file=f)
        print("I now have the _.", file=f)
        print("", file=f)
        print("/37", file=f)
        print("I'm now wearing the _.", file=f)
        print("", file=f)
        print("/38", file=f)
        print("I've removed the _.", file=f)
        print("", file=f)
        print("/39", file=f)
        print("I've dropped the _.", file=f)
        print("", file=f)
        print("/40", file=f)
        print("I can't wear the _.", file=f)
        print("", file=f)
        print("/41", file=f)
        print("I can't remove the _.", file=f)
        print("", file=f)
        print("/42", file=f)
        print("I can't remove the _.  My hands are full.", file=f)
        print("", file=f)
        print("/43", file=f)
        print("The _ weighs too much for me.", file=f)
        print("", file=f)
        print("/44", file=f)
        print("The _ is in the ", file=f)
        print("/45", file=f)
        print("The _ isn't in the ", file=f)
        print("/46", file=f)
        print(", ", file=f)
        print("/47", file=f)
        print(" and ", file=f)
        print("/48", file=f)
        print(".", file=f)
        print("", file=f)
        print("/49", file=f)
        print("I don't have the _.", file=f)
        print("", file=f)
        print("/50", file=f)
        print("I'm not wearing the _.", file=f)
        print("", file=f)
        print("/51", file=f)
        print(".", file=f)
        print("", file=f)
        print("/52", file=f)
        print("There isn't one of those in the ", file=f)
        print("/53", file=f)
        print("Nothing.", file=f)
        print("", file=f)
        print("/54 ;Letter for Tape", file=f)
        print("T", file=f)
        print("/55 ;Disc", file=f)
        print("D", file=f)
        print("/56", file=f)
        print("Drive not ready - press any key to retry.", file=f)
        print("", file=f)
        print("/57", file=f)
        print("I/O Error.", file=f)
        print("", file=f)
        print("/58", file=f)
        print("Disc or Directory may be full.", file=f)
        print("", file=f)
        print("/59", file=f)
        print("Invalid filename.", file=f)
        print("", file=f)
        print("/60", file=f)
        print("Type in name of file:", file=f)
        print("/61", file=f)
        print("Start tape.", file=f)
        print("", file=f)
        print("/62", file=f)
        print("Tape or Disc?", file=f)
        print("/63", file=f)      
        print("I see nothing unusual in the _.", file=f)
        print("", file=f)
        print('/64', file=f)
        print('Inside the _ I see:', file=f)
        print('', file=f)
        print(";------------------------------------------------------------------------------", file=f)
        if verbosity:
                print('OK.')      

def imprimeMTX_SPA_DSF():
        if verbosity:
                print('Imprimiendo sección /MTX',end=' -> ')      
        print('/MTX',file=f)
        print(';', file=f)
        print('; Mensajes del juego.', file=f)
        print(';', file=f)
        print('; Los mensajes 0 a 13 se usan por Triz2DAAD para su rutina de listado de salidas (process 10).', file=f)
        print(';', file=f)
        print('/0 "Salidas visibles: "', file=f)       
        print('/1 "ninguna"', file=f)  
        print('/2 "norte "', file=f)
        print('/3 "sur "', file=f)
        print('/4 "este "', file=f)
        print('/5 "oeste "', file=f)
        print('/6 "noreste "', file=f)
        print('/7 "noroeste "', file=f)
        print('/8 "sureste "', file=f)
        print('/9 "suroeste "', file=f)
        print('/10 "arriba "', file=f)
        print('/11 "abajo "', file=f)
        print('/12 "entrar "', file=f)
        print('/13 "salir "', file=f)
        print(';', file=f)
        print('; El mensaje 14 se usa por Triz2DAAD como texto de introducción del juego.', file=f)
        print(';', file=f)
        print('/14' + ' "' + history + '"', file=f)
        print(';', file=f)
        if statusLine:
                print('; El mensaje 15 se usa por Triz2DAAD para imprimir los turnos en la barra de estado.', file=f)
                print(';', file=f)
                print('/15 "Turnos: "', file=f)
                print(';', file=f)
                print('; Tras el mensaje 15, Triz2DAAD usará un nº variable de mensajes para los nombres de localidad en la barra de estado.', file=f)
                print(';', file=f)
        
def imprimeMTX_SPA():
        if verbosity:
                print('Imprimiendo sección /MTX',end=' -> ')      
        print('/MTX',file=f)
        print(';', file=f)
        print('; Mensajes del juego.', file=f)
        print(';', file=f)
        print('; Los mensajes 0 a 13 se usan por Triz2DAAD para su rutina de listado de salidas (process 10).', file=f)
        print(';', file=f)
        print('/0',file=f)
        print('Salidas visibles: ', file=f)       
        print('/1',file=f)
        print('ninguna', file=f)  
        print('/2',file=f)
        print('norte ',file=f)
        print('/3',file=f)
        print('sur ',file=f)
        print('/4',file=f)
        print('este ',file=f)
        print('/5',file=f)
        print('oeste ',file=f)
        print('/6',file=f)
        print('noreste ',file=f)
        print('/7',file=f)
        print('noroeste ',file=f)
        print('/8',file=f)
        print('sureste ',file=f)
        print('/9',file=f)
        print('suroeste ',file=f)
        print('/10',file=f)
        print('arriba ',file=f)
        print('/11',file=f)
        print('abajo ',file=f)
        print('/12',file=f)
        print('entrar ',file=f)
        print('/13',file=f)
        print('salir ',file=f)
        print(';', file=f)
        print('; El mensaje 14 se usa por Triz2DAAD como texto de introducción del juego.', file=f)
        print(';', file=f)
        print('/14', file=f)
        print(history, file=f)
        print(';', file=f)
        if statusLine:
                print('; El mensaje 15 se usa por Triz2DAAD para imprimir los turnos en la barra de estado.', file=f)
                print(';', file=f)
                print('/15', file=f)
                print('Turnos: ', file=f)
                print(';', file=f)
                print('; Tras el mensaje 15, Triz2DAAD usará un nº variable de mensajes para los nombres de localidad en la barra de estado.', file=f)
                print(';', file=f)
        
def imprimeMTX_ENG():
        if verbosity:
                print('Printing english /MTX sectión',end=' -> ') 
        print('/MTX',file=f)
        print(';', file=f)
        print('; Game messages.', file=f)
        print(';', file=f)
        print('; Messages 0 to 13 are used by Triz2DAAD in its exits listing routine (process 10).', file=f)
        print(';', file=f)
        print('/0',file=f)
        print('Visible exits: ', file=f)  
        print('/1',file=f)
        print('none', file=f)     
        print('/2',file=f)
        print('north ',file=f)
        print('/3',file=f)
        print('south ',file=f)
        print('/4',file=f)
        print('east ',file=f)
        print('/5',file=f)
        print('west ',file=f)
        print('/6',file=f)
        print('northeast ',file=f)
        print('/7',file=f)
        print('northwest ',file=f)
        print('/8',file=f)
        print('southeast ',file=f)
        print('/9',file=f)
        print('southwest ',file=f)
        print('/10',file=f)
        print('up ',file=f)
        print('/11',file=f)
        print('down ',file=f)
        print('/12',file=f)
        print('in ',file=f)
        print('/13',file=f)
        print('out ',file=f)
        print(';', file=f)
        print('; Message 14 is used by Triz2DAAD as an introduction text.', file=f)
        print(';', file=f)
        print('/14', file=f)
        print(history, file=f)
        print(';', file=f)
        if statusLine:
                print('; Message 15 is used by Triz2DAAD while printing the numbre of turns at the status line.', file=f)
                print(';', file=f)
                print('/15', file=f)
                print('Turns: ', file=f)
                print(';', file=f)
                print('; After message 15, Triz2DAAD will use a variable amount of messages as location names at the status line.', file=f)
                print(';', file=f)
        
def imprimeMTX_ENG_DSF():
        if verbosity:
                print('Printing english /MTX sectión',end=' -> ') 
        print('/MTX',file=f)
        print(';', file=f)
        print('; Game messages.', file=f)
        print(';', file=f)
        print('; Messages 0 to 13 are used by Triz2DAAD in its exits listing routine (process 10).', file=f)
        print(';', file=f)
        print('/0 "Visible exits: "', file=f)  
        print('/1 "none"', file=f)     
        print('/2 "north "', file=f)
        print('/3 "south "', file=f)
        print('/4 "east "', file=f)
        print('/5 "west "', file=f)
        print('/6 "northeast "', file=f)
        print('/7 "northwest "', file=f)
        print('/8 "southeast "', file=f)
        print('/9 "southwest "', file=f)
        print('/10 "up "', file=f)
        print('/11 "down "', file=f)
        print('/12 "in "', file=f)
        print('/13 "out "', file=f)
        print(';', file=f)
        print('; Message 14 is used by Triz2DAAD as an introduction text.', file=f)
        print(';', file=f)
        print('/14', file=f)
        print('"' + history + '"', file=f)
        print(';', file=f)
        if statusLine:
                print('; Message 15 is used by Triz2DAAD while printing the numbre of turns at the status line.', file=f)
                print(';', file=f)
                print('/15', file=f)
                print('"Turns: "', file=f)
                print(';', file=f)
                print('; After message 15, Triz2DAAD will use a variable amount of messages as location names at the status line.', file=f)
                print(';', file=f)
        
def imprimePRO0():
        if verbosity:
                if english:
                        print('Printing english /PRO 0',end=' -> ') 
                else:     
                        print('Imprimiendo /PRO 0',end=' -> ')
        print('/PRO 0', file=f)
        print('', file=f)
        if english:
                print('; PRO 0 is the first process to be executed in DAAD.', file=f)
        else:
                print('; PRO 0 es el primer proceso en ejecutarse en DAAD.', file=f)
        print('', file=f)
        if english:
                print('; If location is 0 (start of game)', file=f)
                print('; calls initialization process (PRO 6).', file=f)
        else:
                print('; Si estamos en la localidad 0 (inicio del juego)', file=f)
                print('; llama al proceso de inicialización (PRO 6).', file=f)
        print('', file=f)
        if daadReady:
                imprimePRO0_DR()
                return
        if dsf:
                print('>', file=f)
        print('_       _       AT 0', file=f)
        print('                PROCESS 6', file=f)
        print('', file=f)
        if english:
                print('; Sets text window position.', file=f)
        else:
                print('; Establece la posición de la ventana de texto.', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       PROCESS 9', file=f)       
        print('', file=f)
        if english:
                print('; Sets flag DarkF acording to flag Dark and', file=f)
                print('; the presence (or not) of light sources (default is object 0, but Triz2DAAD can change that).', file=f)
                print('; ', file=f)
        else:
                print('; Establece el flag DarkF en función del flag Dark y de la', file=f)
                print('; presencia o no de fuentes de luz (en principio el objeto 0, aunque Triz2DAAD puede cambiar eso).', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
                print('_       _       CLEAR fDarkF', file=f)
                print('                NOTZERO fDark', file=f)
        else:
                print('_       _       CLEAR DarkF', file=f)
                print('                NOTZERO Dark', file=f)
        if not lobj:
                if idobj:
                        print('                ABSENT ' + listObjectIdentifiers[0], file=f)
                else:
                        print('                ABSENT 0', file=f)
        else:                
                for z, y in enumerate(listObjects):
                        if y['lightsource']:
                                if idobj:
                                        print('                ABSENT ' + listObjectIdentifiers[z], file=f)
                                else:
                                        print('                ABSENT ' + str(z), file=f)
        if dsf:
                print('                SET fDarkF', file=f)
        else:
                print('                SET DarkF', file=f)
        print('', file=f)
        if statusLine:
                if english:
                        print('; Updates status line.', file=f)
                else:
                        print('; Actualiza la barra de estado.', file=f)
                print('', file=f)
                if dsf:
                        print('>', file=f)
                print('_       _       PROCESS 11', file=f)
                print('', file=f)
        if english:
                print('; If there is a graphic at player\'s location', file=f)
                print('; it loads it and, if it\'s not dark, draws it.', file=f)
        else:
                print('; Si hay un gráfico en la posición correspondiente a la localidad del jugador', file=f)
                print('; lo carga y, si no está oscuro, lo dibuja.', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       WINDOW  0', file=f)
        if dsf:
                print('                PICTURE @fPlayer', file=f)
        else:
                print('                PICTURE [Player]', file=f)
        if dsf:
                print('                DISPLAY @fDarkF', file=f)
        else:
                print('                DISPLAY [DarkF]', file=f)
        print('', file=f)
        if english:
                print('; It goes to the text window. If there is no light, prints system message 0', file=f)
                print('; "It\'s too dark to see".', file=f)
        else:
                print('; Pasa a la ventana de texto. Si no hay luz, imprime el mensaje de sistema 0', file=f)
                print('; "No se ve nada".', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       WINDOW 1', file=f)
        if dsf:
                print('                NOTZERO fDarkF', file=f)
        else:
                print('                NOTZERO DarkF', file=f)
        print('                SYSMESS 0', file=f)
        print('', file=f)
        if english:
                print('; Otherwise, If there is light, prints current location description.', file=f)
        else:
                print('; En caso contario (sí hay luz) imprime la descripción correspondiente', file=f)
                print('; a la localidad actual.', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
                print('_       _       ZERO fDarkF', file=f)
        else:
                print('_       _       ZERO DarkF', file=f)
        if dsf:
                print('                DESC @fPlayer', file=f)
        else:
                print('                DESC [Player]', file=f)
        print('', file=f)
        if english:
                print('; Calls process 3.', file=f)
        else:
                print('; Llama al proceso 3.', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       PROCESS 3', file=f)
        print('', file=f)
        if english:
                print('; Calls process 1.', file=f)
        else:
                print('; Llama al proceso 1.', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       PROCESS 1', file=f)
        print('', file=f)
        print(';------------------------------------------------------------------------------', file=f)
        if verbosity:
                print('OK.')

def imprimePRO0_DR():
        print('', file=f)
        print('>', file=f)
        print('_       _       AT 0', file=f)
        print('                #ifdef "canBoostSpeed"', file=f)
        print('                XSPEED  1', file=f)
        print('                #endif', file=f)
        print('                #ifdef "hasSplitMode"', file=f)
        print('                XSPLITSCR 1', file=f)
        print('                #endif', file=f)
        print('                PROCESS 6', file=f)
        print('', file=f)
        if english:
                print('; Sets flag DarkF acording to flag Dark and', file=f)
                print('; the presence (or not) of light sources (default is object 0, but Triz2DAAD can change that).', file=f)
                print('; ', file=f)
        else:
                print('; Establece el flag DarkF en función del flag Dark y de la', file=f)
                print('; presencia o no de fuentes de luz (en principio el objeto 0, aunque Triz2DAAD puede cambiar eso).', file=f)
        print('', file=f)
        print('>', file=f)
        print('_       _       WINDOW 0', file=f)
        print('                CLEAR fDarkF', file=f)
        print('                NOTZERO fDark', file=f)
        # Añadimos a DAAD Ready la funcionalidad de poder tener varias fuentes de luz
        if not lobj:
                if idobj:
                        print('                ABSENT ' + listObjectIdentifiers[0], file=f)
                else:
                        print('                ABSENT 0', file=f)
        else:                
                for z, y in enumerate(listObjects):
                        if y['lightsource']:
                                if idobj:
                                        print('                ABSENT ' + listObjectIdentifiers[z], file=f)
                                else:
                                        print('                ABSENT ' + str(z), file=f)
        print('                SET fDarkF', file=f)
        print('', file=f)
        # 1.0.4b6 Lo que sigue es un copia-pega del PRO 0 de DAAD-Ready 0.7 ya que no hay tiempo de hacer una versión específica para Triz2DAAD. Si todo va bien, funcionará.
        if english:
            print('; What follows is essentially a copy-paste from DAAD Ready 0.7 PRO 0 template.', file = f)
            print('; Hopefully, it will work!', file = f)
        else:
            print('; Lo que sigue es básicamente un copia-pega de la plantilla del PRO 0 de DAAD Ready 0.7', file = f)
            print('; ¡Con suerte, funcionará!', file = f)
        print('', file = f)    
        print('#ifndef "zx128"', file = f)
        print('> _       _     CLEAR 20', file = f)
        print('#ifndef "tape"', file = f)
        print('                ZERO fDarkF', file=f)
        print('                XPICTURE @fPlayer        ; If there is a picture, Load it', file = f)
        print('                #ifndef "nativeraster"', file = f)
        print('                GT 20 127', file = f)
        print('                #endif', file = f)
        print('#endif', file = f)
        print('#ifdef "nativeraster"', file = f)
        print('                DISPLAY @fDarkF         ; & Display it if not dark, else CLS', file = f)
        print('#endif', file = f)
        print('#ifdef "next"', file = f)
        print('                GT 20 127               ; Muestralo si no oscuro; si oscuro', file = f)
        print('                XNEXTCLS                 ; Disable adn clear Layer2', file = f)
        print('#endif', file = f)
        print('', file = f)
        print('> _      _      NOTZERO fDarkF', file = f)
        print('                CLS', file = f)
        print('', file = f)
        print('#ifndef "noretryImage"', file = f)
        print('> _        _    GT 20 127', file = f)
        print('                XPICTURE 255            ; If XPICTURE failed, then try to paint filler picture 255', file = f)
        print('#endif', file = f)
        print('', file = f)
        print('', file = f)
        print('#ifndef "hasSplitMode"', file = f)
        print('> _        _    GT 20 127                ; XPICTURE failed to load', file = f)
        print('                CLS', file = f)
        print('                WINDOW 1', file = f)
        print('                WINAT 0 0', file = f)
        print('                WINSIZE 25 127           ; Maximum window', file = f)
        print('                CLS', file = f)
        print('                SKIP 1', file = f)
        print('#endif', file = f)
        print('', file = f)
        print('> _        _    WINDOW 1', file = f)
        print('                WINAT 0 0', file = f)
        print('                #ifndef "tape"', file = f)
        print('                WINAT 14 0', file = f)
        print('                #endif', file = f)
        print('#else', file = f)
        print(';ZX 128', file = f)
        print('> _       _     PICTURE @fPlayer        ; Si hay gráfico, cárgalo', file = f)
        print('                DISPLAY @fDarkF         ; Muestralo si no oscuro; si oscuro hace un CLS', file = f)
        print('                SKIP 2                  ; Saltamos', file = f)
        print('', file = f)
        print('> _        _    PICTURE 255             ; Si hemos fallado, cargamos la localidad 255 (pantalla de paso)', file = f)
        print('                DISPLAY @fDarkF', file = f)
        print('                SKIP 1                  ; Saltamos', file = f)
        print('', file = f)
        print('> _        _    CLS                     ; Fallback si no encontramos imagen', file = f)
        print('                WINDOW 1', file = f)
        print('                WINAT 0 0', file = f)
        print('                WINSIZE 24 42           ; Ventana máxima para texto', file = f)
        print('                CLS', file = f)
        print('                SKIP 1                  ; Saltar parte inferior.', file = f)
        print('', file = f)
        print('> _        _    WINDOW 1                ; Ventana en la parte inferior', file = f)
        print('                WINAT 14 0', file = f)
        print('#endif', file = f)
        print('', file = f)
        print('> _       _     NOTZERO fDarkF           ; Oscuro', file = f)
        print('                SYSMESS 0', file = f)
        print('', file = f)
        print('> _       _     ZERO fDarkF', file = f)
        print('                DESC @fPlayer            ; DESC No sale del bucle ahora', file = f)
        print('', file = f)
        print('> _       _     PROCESS 3', file = f)
        print('', file = f)
        print('; Ahora usamos el proceso 1 como el bucle principal del juego. Un retorno desde', file = f)
        print('; aquí significa el fin del juego', file = f)
        print('', file = f)
        print('> _       _     PROCESS 1', file = f)
        
def imprimePRO1():
        if verbosity:
                if english:
                        print('Printing english /PRO 1',end=' -> ')
                else:
                        print('Imprimiendo /PRO 1',end=' -> ')      
        print('/PRO 1', file=f)
        print('', file=f)
        if english:
                print('; Called from PRO 0.', file=f)
        else:
                print('; Llamado desde PRO 0.', file=f)
        print('', file=f)
        if english:
                print('; Calls PRO 4, former process 2 in PAWS.', file=f)
        else:
                print('; Llama a PRO 4, antiguo proceso 2 del PAWS.', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       PROCESS 4', file=f)
        print('', file=f)
        if english:
                print('; Gets and analyzes plyer input.', file=f)
        else:
                print('; Recibe y analiza el input del jugador.', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       PARSE 0', file=f)
        print('                PROCESS 2', file=f)
        print('                REDO', file=f)
        print('', file=f)
        if english:
                print('; Turns counter entries.', file=f)      
        else:     
                print('; Entradas para el contador de turnos.', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
                print('_       _       EQ fTurns 255', file=f)
                print('                EQ fTurnsHi 255', file=f)
                print('                CLEAR fTurns', file=f)      
                print('                CLEAR fTurnsHi', file=f)
                print('                SKIP 2', file=f)   
                print('', file=f)
                print('>', file=f)
                print('_       _       EQ fTurns 255', file=f)
                print('                PLUS fTurnsHi 1', file=f)
                print('                CLEAR fTurns', file=f)
                print('                SKIP 1', file=f)
                print('', file=f)
                print('>', file=f)
                print('_       _       PLUS fTurns 1', file=f)
        else:
                print('_       _       EQ Turns 255', file=f)
                print('                EQ Turns+1 255', file=f)
                print('                CLEAR Turns', file=f)      
                print('                CLEAR Turns+1', file=f)
                print('                SKIP 2', file=f)   
                print('', file=f) 
                print('_       _       EQ Turns 255', file=f)
                print('                PLUS Turns+1 1', file=f)
                print('                CLEAR Turns', file=f)
                print('                SKIP 1', file=f)
                print('', file=f)
                print('_       _       PLUS Turns 1', file=f)
        print('', file=f)
        if statusLine:
                if english:
                        print('; Updates (again) the status line.', file=f)
                else:
                        print('; Actualiza (de nuevo) la barra de estado.', file=f)
                print('', file=f)
                if dsf:
                        print('>', file=f)
                print('_       _       PROCESS 11', file=f)
                print('', file=f)
        if english:
                print('; Calls PRO 5. If it returns having executed an action', file=f)
                print('; it continues the game loop re-starting PRO 1.', file=f)
        else:
                print('; Llama a PRO 5. Si al volver se ha ejecutado una acción', file=f)
                print('; continua el bucle del juego recomenzando el PRO 1.', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       PROCESS 5', file=f)
        print('                ISDONE', file=f)
        print('                REDO', file=f)
        print('', file=f)
        if english:
                print('; If not, it tries to move the player. If successful', file=f)
                print('; it continues the game loop re-starting PRO 0.', file=f)
        else:
                print('; Si no, trata de mover al jugador. Si lo consigue', file=f)
                print('; continua el bucle del juego recomenzando el PRO 0.', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
                print('_       _       MOVE fPlayer', file=f)
        else:
                print('_       _       MOVE Player', file=f)
        if daadReady:
                print('                CLS', file=f)
        print('                RESTART', file=f)
        print('', file=f)
        if english:
                print('; If not, checks the verb in the LS (logic sentence). If it\'s a movement action', file=f)
                print('; system message 7 ("you can\'t go that way") is printed and', file=f)
                print('; game loop continues re-starting PRO 1.', file=f)
        else:
                print('; Si no, mira si el verbo de la SL (sentencia lógica) era de movimiento,', file=f)
                print('; en cuyo caso imprime el mensaje de sistema 7 "no puedes ir en esa dirección" y', file=f)
                print('; el bucle del juego continua recomenzando PRO 1.', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       NEWTEXT', file=f)
        if dsf:
                print('                LT fVerb 14', file=f)
        else:
                print('                LT Verb 14', file=f)
        print('                SYSMESS 7', file=f)
        print('                REDO', file=f)
        print('', file=f)
        if english:
                print('; If it reaches here, system message 8 ("you can\'t do that") is displayed and', file=f)
                print('; game loop continues re-starting PRO 1.', file=f)
        else:
                print('; Y si llega hasta aquí, imprime el mesaje de sistema 8 ("no puedes hacer eso") y', file=f)
                print('; el bucle del juego continua recomenzando PRO 1.', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       SYSMESS 8', file=f)
        print('                REDO', file=f)
        print('', file=f)
        print(';------------------------------------------------------------------------------', file=f)
        if verbosity:
                print('OK.')      
        
def imprimePRO2():
        if verbosity:
                if english:
                        print('Printing english /PRO 2',end=' -> ') 
                else:     
                        print('Imprimiendo /PRO 2',end=' -> ')
        print('/PRO 2', file=f)
        print('', file=f)
        if english:
                print('; Called from PRO 1.', file=f)
        else:
                print('; Llamado desde PRO 1.', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       HASAT TIMEOUT', file=f)
        print('                SYSMESS 35', file=f)
        print('                DONE', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       SYSMESS 6', file=f)
        print('', file=f)
        print(';------------------------------------------------------------------------------', file=f)
        if verbosity:
                print('OK.')      
        
def imprimePRO3():
        if verbosity:
                if english:
                        print('Printing english /PRO 3',end=' -> ') 
                else:     
                        print('Imprimiendo /PRO 3',end=' -> ')
        print('/PRO 3', file=f)
        print('', file=f)
        if english:
                print('; PRO 3 is former "process 1" from PAWS.', file=f)
                print('; It\'s called from PRO 0.', file=f)
                print('; It executes right after location description.', file=f)
        else:
                print('; PRO 3 es el antiguo "process 1" de PAWS.', file=f)
                print('; Se le llama desde PRO 0.', file=f)
                print('; Se ejecuta justo después de la descripción de la localidad.', file=f)
        print('', file=f)
        if english:
                print('; Exits listing (if not dark).', file=f)
        else:
                print('; Listado de salidas (si no está oscuro).', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       NEWLINE', file=f)
        if dsf:
                print('                ZERO fDarkF', file=f)
        else:
                print('                ZERO DarkF', file=f)
        # En modo daadReady el listado de salidas estará en el PROCESS 7
        # en lugar de el 10
        if daadReady:        
                print('                PROCESS 7', file=f)
        else:
                print('                PROCESS 10', file=f)
        print('', file=f)
        if english:
                print('; Objects listing (if not dark).', file=f)
        else:
                print('; Listado de objetos (si no está oscuro).', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       NEWLINE', file=f)
        if dsf:
                print('                ZERO fDarkF', file=f)
        else:
                print('                ZERO DarkF', file=f)
        print('                LISTOBJ', file=f)
        print('', file=f)
        print(';------------------------------------------------------------------------------', file=f)
        if verbosity:
                print('OK.')      
          
def imprimePRO4(): # 4 es el antiguo proceso 2 en PAW
        if verbosity:
                if english:
                        print('Printing english /PRO 4',end=' -> ')         
                else:     
                        print('Imprimiendo /PRO 4',end=' -> ')
        print('/PRO 4', file=f)
        print('', file=f)
        if english:
                print('; PRO 4 is the former "status table" from Quill or "process 2" from PAWS.', file=f)
                print('; It\'s called from PRO 1.', file=f)
                print('; It executes right before the parser asks for a new order o logical sentence.', file=f)
        else:
                print('; PRO 4 equivale a la antigua "status table" de Quill o al antiguo "process 2" en PAWS.', file=f)
                print('; Se le llama desde PRO 1.', file=f)
                print('; Se ejecuta justo antes de que el parser pida una nueva órden o sentencia lógica', file=f)
        print('', file=f)
        if verbosity:
                print('OK.')
        
def imprimePRO5(helpMessage1, helpMessage2, listRooms2):
        if verbosity:
                print('Imprimiendo /PRO 5',end=' -> ')
        print('/PRO 5', file=f)
        print('', file=f)
        print('; PRO 5 equivale a la antigua "events table" de Quill o a la "tabla de respeuestas" de PAWS.', file=f)
        print('; Se le llama desde PRO 1.', file=f)
        print('', file=f)
        if blockall:
                print('; Bloquea acciones "TODO".', file=f)
                print('', file=f)
                if dsf:
                        print('>', file=f)
                print('_       TODO    NOTDONE', file=f)
                print('', file=f)
        x=False
        for y in listRooms2:
                if y['dark']==True:
                        x=True
        if x:
                print('; Entradas añadidas por Triz2DAAD para tratar las localidades sin luz.', file=f) 
                print('', file=f)
        for y in listRooms2:
                for x in y['con']:
                        a=x.split()
                        b=a[0]
                        c=int(a[1])
                        d=listRooms2[c-len(listContainers)-1]
                        e=y['dark']
                        e2=d['dark']
                        if e==False and e2==True:
                                if dsf:
                                        print('>', file=f)
                                if idloc:
                                    print(b + '       _       AT ' + listLocationIdentifiers[y['loc'] - 1], file=f)
                                else:
                                    print(b + '       _       AT ' + str(y['loc']), file=f)
                                if dsf:
                                        print('                SET fDark', file=f)
                                else:
                                        print('                SET Dark', file=f)
                                print('                NOTDONE', file=f)
                                print('', file=f)
                        if e==True and e2==False:
                                if dsf:
                                        print('>', file=f)
                                if idloc:
                                    print(b + '       _       AT ' + listLocationIdentifiers[y['loc'] - 1], file=f)
                                else:
                                    print(b + '       _       AT ' + str(y['loc']), file=f)
                                if dsf:
                                        print('                CLEAR fDark', file=f)
                                else:
                                        print('                CLEAR Dark', file=f)
                                print('                NOTDONE', file=f)
                                print('', file=f)
        print('; Entrada añadida por Triz2DAAD para pantallas de ayuda.', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        if daadReady:
                print('AYUDA   _       CLS', file=f)
                print('                MESSAGE ' + str(helpMessage1), file=f)
        else:
                print('AYUDA   _       PROCESS 7', file=f)
                if statusLine:
                        print('                WINDOW 2', file=f)
                print('                CLS', file=f)
                if statusLine:
                        print('                MES '+str(helpMessage1), file=f)
                        print('                WINDOW 1', file=f)
                else:
                        print('                MESSAGE '+str(helpMessage1), file=f)
        print('                MESSAGE '+str(helpMessage2), file=f)
        print('                ANYKEY', file=f)
        print('                RESTART', file=f)  
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('EXAMI   _       WHATO', file=f)
        print('                NOTEQ 51 255', file=f)
        if dsf:
                print('                PRESENT @51', file=f)
        else:
                print('                PRESENT [51]', file=f)
        print('                HASAT CONTAINER', file=f)  
        print('                SYSMESS 64', file=f)
        if dsf:
                print('                LISTAT @51', file=f)
        else:
                print('                LISTAT [51]', file=f)
        print('                DONE', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('EXAMI   _       WHATO', file=f)
        print('                NOTEQ 51 255', file=f)
        if dsf:
                print('                PRESENT @51', file=f)
        else:
                print('                PRESENT [51]', file=f)
        print('                SYSMESS 63', file=f)
        print('                DONE', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('EXAMI   _       NOTDONE', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        # En DAAD Ready el proceso para SALIDAS es el 7
        if daadReady:
                print('SALID   _       PROCESS 7', file=f)
        else:
                print('SALID   _       PROCESS 10', file=f)
        print('                DONE', file=f)
        print('', file=f)
        if dsf:
                print('; "VACIAR" y "SACAR TODO" bloqueados en MSX2.', file=f)
                print('', file=f)
                print('#ifndef "MSX2"', file=f)
                print('>', file=f)
        print('VACIA   _       WHATO', file=f)
        print('                NOTEQ 51 255', file=f)
        if dsf:
                print('                PRESENT @51', file=f)
        else:
                print('                PRESENT [51]', file=f)
        print('                HASAT CONTAINER', file=f)
        if dsf:
                print('                COPYFF fNoun fNoun2', file=f)
        else:
                print('                COPYFF Noun1 Noun2', file=f)
        print('                SYNONYM SACAR TODO', file=f)
        if dsf:
                print('#endif', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('VACIA   _       NOTDONE', file=f)
        print('', file=f)
        if listContainers!=[]:
                listContainers.reverse()
                for x,y in enumerate(listContainers, start=1):
                        if dsf:
                                print('>', file=f)
                        print('METER   TODO    NOUN2 '+y['name'], file=f)
                        if idobj:
                                print('                PRESENT ' + listObjectIdentifiers[x], file=f)
                        else:
                                print('                PRESENT ' + str(x), file=f)
                        print('                DOALL CARRIED', file=f)
                        if idobj:
                                print('                AUTOP ' + listObjectIdentifiers[x], file=f)
                        else:
                                print('                AUTOP ' + str(x), file=f)
                        print('                DONE', file=f)
                        print('', file=f)
                        if dsf:
                                print('>', file=f)
                        print('METER   _       NOUN2 '+y['name'], file=f)
                        print('                NOTSAME 34 44', file=f)
                        if idobj:
                                print('                PRESENT ' + listObjectIdentifiers[x], file=f)
                        else:
                                print('                PRESENT ' + str(x), file=f)
                        if idobj:
                                print('                AUTOP ' + listObjectIdentifiers[x], file=f)
                        else:
                                print('                AUTOP ' + str(x), file=f)
                        if dsf:
                                print('#ifdef "MSX2"', file=f)
                                print('                DONE     ; Parche exclusivo para MSX2', file=f)
                                print('#endif', file=f)
                        print('', file=f)
                for x,y in enumerate(listContainers, start=1):
                        if dsf:
                                print('>', file=f)
                        print('SACAR   TODO    NOUN2 '+y['name'], file=f)
                        if idobj:
                                print('                PRESENT ' + listObjectIdentifiers[x], file=f)
                        else:
                                print('                PRESENT ' + str(x), file=f)
                        if idobj:
                                print('                DOALL ' + listObjectIdentifiers[x], file=f)
                        else:
                                print('                DOALL '+str(x), file=f)
                        if idobj:
                                print('                AUTOT ' + listObjectIdentifiers[x], file=f)
                        else:
                                print('                AUTOT ' + str(x), file=f)
                        print('                DONE', file=f)
                        print('', file=f)
                        if dsf:
                               print('>', file=f)
                        print('SACAR   _       NOUN2 '+y['name'], file=f)
                        if idobj:
                                print('                PRESENT ' + listObjectIdentifiers[x], file=f)
                        else:
                                print('                PRESENT ' + str(x), file=f)
                        if idobj:
                                print('                AUTOT ' + listObjectIdentifiers[x], file=f)
                        else:
                                print('                AUTOT ' + str(x), file=f)
                        if dsf:
                                print('#ifdef "MSX2"', file=f)
                                print('                DONE     ; Parche exclusivo para MSX2', file=f)
                                print('#endif', file=f)
                        print('', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('I       _       SYSMESS 9', file=f)
        print('                LISTAT CARRIED', file=f)
        print('                SYSMESS 10', file=f)
        print('                LISTAT WORN', file=f)
        print('                DONE', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('COGER   TODO    DOALL HERE', file=f)
        if dsf:
                print('>', file=f)
        print('COGER   _       AUTOG', file=f)
        print('                DONE', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('DEJAR   TODO    DOALL CARRIED', file=f)
        if dsf:
                print('>', file=f)
        print('DEJAR   _       AUTOD', file=f)
        print('                DONE', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('QUITAR  TODO    DOALL WORN', file=f)
        if dsf:
                print('>', file=f)
        print('QUITAR  _       AUTOR', file=f)
        print('                DONE', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('PONER   TODO    DOALL CARRIED', file=f)
        if dsf:
                print('>', file=f)
        print('PONER   _       AUTOW', file=f)
        print('                DONE', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('R       _       EQ 34 255', file=f)
        if daadReady:
                print('                CLS', file = f)
        print('                RESTART' , file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('R       _       LET 33 30', file=f)
        print('                REDO', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('FIN     _       QUIT', file=f)
        print('                END', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('FIN     _       DONE', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        if daadReady:
                print('SAVE    _       #ifndef "tape"', file=f)
                print('                XSAVE 0', file=f)
                print('                #endif', file=f)
                print('                #ifdef "tape"', file=f)
                print('                SAVE 0', file=f)
                print('                #endif', file=f)
                print('                CLS', file = f)
        else:
                print('SAVE    _       SAVE 0', file=f)
        print('                RESTART', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        if daadReady:
                print('LOAD    _       #ifndef "tape"', file=f)
                print('                XLOAD 0', file=f)
                print('                #endif', file=f)
                print('                #ifdef "tape"', file=f)
                print('                LOAD 0', file=f)
                print('                #endif', file=f)
                print('                CLS', file = f)
        else:
                print('LOAD    _       LOAD 0', file=f)
        print('                RESTART', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('RAMSA   _       RAMSAVE', file=f)
        if daadReady:
                print('                CLS', file = f)
        print('                RESTART', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('RAMLO   _       RAMLOAD 255', file=f)
        if daadReady:
                print('                CLS', file = f)
        print('                RESTART', file=f)
        print('', file=f)
        if verbosity:
                print('OK.')
        
def imprimePRO5_ENG(helpMessage1, helpMessage2, listRooms2):
        if verbosity:
                print('Printing english /PRO 5',end=' -> ')
        print('/PRO 5', file=f)
        print('', file=f)
        print('; PRO 5 is the former "events table" from Quill or "Response table" from PAWS.', file=f)
        print('; It\s called from PRO 1.', file=f)
        print('', file=f)
        if blockall:
                print('; Block "ALL" actions..', file=f)
                print('', file=f)
                if dsf:
                        print('>', file=f)
                print('_       TODO    NOTDONE', file=f)
                print('', file=f)
        x=False
        for y in listRooms2:
                if y['dark']==True:
                        x=True
        if x:
               print('; Entries added by Triz2DAAD for dealing with dark locations.', file=f) 
               print('', file=f)
        for y in listRooms2:
                for x in y['con']:
                        a=x.split()
                        b=a[0]
                        c=int(a[1])
                        d=listRooms2[c-len(listContainers)-1]
                        e=y['dark']
                        e2=d['dark']
                        if e==False and e2==True:
                                if dsf:
                                        print('>', file=f)
                                if idloc:
                                    print(b + '       _       AT ' + listLocationIdentifiers[y['loc'] - 1], file=f)
                                else:
                                    print(b + '       _       AT ' + str(y['loc']), file=f)
                                if dsf:
                                        print('                SET fDark', file=f)
                                else:
                                        print('                SET Dark', file=f)
                                print('                NOTDONE', file=f)
                                print('', file=f)
                        if e==True and e2==False:
                                if dsf:
                                        print('>', file=f)
                                if idloc:
                                    print(b + '       _       AT ' + listLocationIdentifiers[y['loc'] - 1], file=f)
                                else:
                                    print(b + '       _       AT ' + str(y['loc']), file=f)
                                if dsf:
                                        print('                CLEAR fDark', file=f)
                                else:
                                        print('                CLEAR Dark', file=f)
                                print('                NOTDONE', file=f)
                                print('', file=f)
        print('; Entry added by Triz2DAAD to display help screens.', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        if daadReady:
                print('HELP    _       CLS', file=f)
                print('                MESSAGE ' + str(helpMessage1), file=f)
        else:        
                print('HELP    _       PROCESS 7', file=f)
                if statusLine:
                        print('                WINDOW 2', file=f)
                print('                CLS', file=f)
                if statusLine:
                        print('                MES '+str(helpMessage1), file=f)
                        print('                WINDOW 1', file=f)
                else:
                        print('                MESSAGE '+str(helpMessage1), file=f)
        print('                MESSAGE '+str(helpMessage2), file=f)
        print('                ANYKEY', file=f)
        print('                RESTART', file=f)  
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('EXAMI   _       WHATO', file=f)
        print('                NOTEQ 51 255', file=f)
        if dsf:
                print('                PRESENT @51', file=f)
        else:
                print('                PRESENT [51]', file=f)
        print('                HASAT CONTAINER', file=f)  
        print('                SYSMESS 64', file=f)
        if dsf:
                print('                LISTAT @51', file=f)
        else:
                print('                LISTAT [51]', file=f)
        print('                DONE', file=f)     
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('EXAMI   _       WHATO', file=f)
        print('                NOTEQ 51 255', file=f)
        if dsf:
                print('                PRESENT @51', file=f)
        else:
                print('                PRESENT [51]', file=f)
        print('                SYSMESS 63', file=f)
        print('                DONE', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('EXAMI   _       NOTDONE', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        # Exits goes in PROCESS 7 in DAAD Ready instead of 10
        if daadReady:
                print('EXITS   _       PROCESS 7', file=f)
        else:
                print('EXITS   _       PROCESS 10', file=f)
        print('                DONE', file=f)
        print('', file=f)
        if dsf:
                print('; Block "EMPTY" and "GET ALL FROM" in MSX2.', file=f)
                print('', file=f)
                print('#ifndef "MSX2"', file=f)
                print('>', file=f)
        print('EMPTY   _       WHATO', file=f)
        print('                NOTEQ 51 255', file=f)
        if dsf:
                print('                PRESENT @51', file=f)
        else:
                print('                PRESENT [51]', file=f)
        print('                HASAT CONTAINER', file=f)
        if dsf:
                print('                COPYFF fNoun fNoun2', file=f)
        else:
                print('                COPYFF Noun1 Noun2', file=f)
        print('                SYNONYM GET ALL', file=f)
        if dsf:
                print('#endif', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('EMPTY   _       NOTDONE', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
                print('GET     _       NOTEQ fNoun2 255', file=f)
        else:        
                print('GET     _       NOTEQ Noun2 255', file=f)
        print('                SYNONYM EXTRACT _', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
                print('PUT     _       NOTEQ fNoun2 255', file=f)
        else:
                print('PUT     _       NOTEQ Noun2 255', file=f)
        print('                SYNONYM INSERT _', file=f)
        print('', file=f)
        if listContainers!=[]:
                listContainers.reverse()
                for x,y in enumerate(listContainers, start=1):
                        if dsf:
                                print('>', file=f)
                        print('INSERT  ALL     NOUN2 '+y['name'], file=f)
                        print('                PRESENT '+str(x), file=f)
                        print('                DOALL CARRIED', file=f)
                        print('                AUTOP '+str(x), file=f)
                        print('                DONE', file=f)
                        print('', file=f)
                        if dsf:
                                print('>', file=f)
                        print('INSERT  _       NOUN2 '+y['name'], file=f)
                        print('                PRESENT '+str(x), file=f)
                        print('                AUTOP '+str(x), file=f)
                        print('                DONE', file=f)
                        print('', file=f)
                if dsf:
                        print('>', file=f)
                print('INSERT  _       NOTDONE', file=f)
                print('', file=f)
                for x,y in enumerate(listContainers, start=1):
                        if dsf:
                                print('>', file=f)
                        print('EXTRACT ALL     NOUN2 '+y['name'], file=f)
                        print('                PRESENT '+str(x), file=f)
                        print('                DOALL '+str(x), file=f)
                        print('                AUTOT '+str(x), file=f)
                        print('                DONE', file=f)
                        print('', file=f)
                        if dsf:
                                print('>', file=f)
                        print('EXTRACT _       NOUN2 '+y['name'], file=f)
                        print('                PRESENT '+str(x), file=f)
                        print('                AUTOT '+str(x), file=f)
                        print('                DONE', file=f)
                        print('', file=f)
                if dsf:
                        print('>', file=f)
                print('EXTRACT _       NOTDONE', file=f)                   
                print('', file=f)
        if dsf:
                print('>', file=f)
        print('I       _       SYSMESS 9', file=f)
        print('                LISTAT CARRIED', file=f)
        print('                SYSMESS 10', file=f)
        print('                LISTAT WORN', file=f)
        print('                DONE', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('GET     ALL     DOALL HERE', file=f)
        if dsf:
                print('>', file=f)
        print('GET     _       AUTOG', file=f)
        print('                DONE', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('DROP    ALL     DOALL CARRIED', file=f)
        if dsf:
                print('>', file=f)
        print('DROP    _       AUTOD', file=f)
        print('                DONE', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('REMOVE  ALL     DOALL WORN', file=f)
        if dsf:
                print('>', file=f)
        print('REMOVE  _       AUTOR', file=f)
        print('                DONE', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('WEAR    ALL     DOALL CARRIED', file=f)
        if dsf:
                print('>', file=f)
        print('WEAR    _       AUTOW', file=f)
        print('                DONE', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('R       _       EQ 34 255', file=f)
        if daadReady:
                print('                CLS', file = f)
        print('                RESTART' , file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('R       _       LET 33 30', file=f)
        print('                REDO', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('QUIT    _       QUIT', file=f)
        print('                END', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('QUIT    _       DONE', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        if daadReady:
                print('SAVE    _       #ifndef "tape"', file=f)
                print('                XSAVE 0', file=f)
                print('                #endif', file=f)
                print('                #ifdef "tape"', file=f)
                print('                SAVE 0', file=f)
                print('                #endif', file=f)
                print('                CLS', file = f)
        else:
                print('SAVE    _       SAVE 0', file=f)
        print('                RESTART', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        if daadReady:
                print('LOAD    _       #ifndef "tape"', file=f)
                print('                XLOAD 0', file=f)
                print('                #endif', file=f)
                print('                #ifdef "tape"', file=f)
                print('                LOAD 0', file=f)
                print('                #endif', file=f)
                print('                CLS', file = f)
        else:
                print('LOAD    _       LOAD 0', file=f)
        print('                RESTART', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('RAMSA   _       RAMSAVE', file=f)
        if daadReady:
                print('                CLS', file = f)
        print('                RESTART', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('RAMLO   _       RAMLOAD 255', file=f)
        if daadReady:
                print('                CLS', file = f)
        print('                RESTART', file=f)
        print('', file=f)
        if verbosity:
                print('OK.')

def imprimePRO6():
        if verbosity:
                if english:
                        print('Printing english /PRO 6',end=' -> ')
                else:     
                        print('Imprimiendo /PRO 6',end=' -> ')
        print('/PRO 6', file=f)
        print('', file=f)
        if english:
                print('; Initialization process.', file=f)
                print('; Called from PRO 0.', file=f)
        else:
                print('; Proceso de inicialización.', file=f)
                print('; Llamado desde PRO 0.', file=f)
        print('', file=f)
        if daadReady:
                imprimePRO6_DR()
                return
        if statusLine:
                if english:
                        print('; Creates status line window.', file=f)
                else:
                        print('; Crea la ventana de la barra de estado.', file=f)
                print('', file=f)
                if dsf:
                        print('>', file=f)
                print('_       _       WINDOW 2', file=f)
                print('                WINAT slrow 0', file=f)
                print('                WINSIZE 1 COLS', file=f)
                print('', file=f)
                if dsf:
                        print('>', file=f)
                if dsf:
                        print('_       _       LT fGFlags 128', file=f)
                else:
                        print('_       _       LT GFlags 128', file=f)
                print('                WINSIZE 1 80', file=f)
                print('', file=f)
                if dsf:
                        print('>', file=f)
                print('_       _       PAPER bg_colour', file=f)
                print('                INK fg_colour', file=f)
                print('                CLS', file=f)
                print('                PAPER sb_bg_colour', file=f)
                print('                INK sb_fg_colour', file=f)
                print('', file=f)
        if english:
                print('; -Initial paper-ink colours.', file=f)
        else:
                print('; -Colores de papel-tinta iniciales.', file=f)
        if english:
                print('; -Rearrange text and graphics windows position.', file=f)
        else:
                print('; -Recoloca las ventanas de texto y gráficos.', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       WINDOW 1', file=f)
        print('                PAPER bg_colour', file=f)
        print('                INK fg_colour', file=f)
        print('                CLS', file=f)
        print('                PROCESS 9', file=f)
        if md:
                print('', file=f)
                if english:
                        print('; Triz2DAAD optionally (-md) adds conditional code to activate', file=f)
                        print('; "Invisible drawing" mode in Amstrad CPC.', file=f)
                else:
                        print('; Triz2DAAD añade opcionalmente (-md) código condicional para activas el modo', file=f)
                        print('; "dibujo invisible" en Amstrad CPC.', file=f)
                print('', file=f)
                if dsf:
                        print('#ifdef "CPC"', file=f)
                        print('>', file=f)
                        print(' _       _       HASNAT GA_MDRW', file=f)
                        print('                 PLUS fGFlags GO_MDRW', file=f)
                        print('#endif', file=f)
                else:
                        print('#IF CPC', file=f)
                        print(' _       _       HASNAT GA_MDRW', file=f)
                        print('                 PLUS GFlags GO_MDRW', file=f)
                        print('#ENDIF', file=f)
        print('', file=f)
        if english:
                print('; -Describes location 0 (usually presentation screen).', file=f)
        else:
                print('; -Describe localidad 0 (normalmente pantalla de presentación).', file=f)
        if english:
                print('; -Displays introduction text.', file=f)
        else:
                print('; -Muestra texto de introducción.', file=f)
        if english:
                print('; -Starts flags resetting loop.', file=f)
        else:
                print('; -Comienza el bucle de reseteo de banderas.', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       DESC 0', file=f)
        print('                ANYKEY', file=f)
        print('                CLS', file=f)
        print('                MESSAGE 14', file=f)
        print('                ANYKEY', file=f)
        print('                SET 255', file=f)
        print('', file=f)
        if dsf:
                cadena='(fGFlags)'
        else:
                cadena='(GFlags)'
        if english:
                print('; Clear all flags save 29 ' + cadena + '.', file=f)
        else:
                print('; Pone a 0 todas las banderas excepto la 29 '+ cadena + '.', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       MINUS 255 1', file=f)
        if dsf:
                print('                NOTEQ 255 fGFlags', file=f)
        else:
                print('                NOTEQ 255 GFlags', file=f)
        if dsf:
                print('                CLEAR @255', file=f)
        else:
                print('                CLEAR [255]', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       NOTZERO 255', file=f)
        print('                SKIP -2', file=f)
        print('', file=f)
        if english:
                print('; -Reset object locations to original values (established in /OBJ).', file=f)
        else:
                print('; -Pone las localidades de los objetos a su valor original (establecido en /OBJ).', file=f)
        if english:
                print('; -Set default values for flags 52, 37, 46, 47 and 53.', file=f)
        else:
                print('; -Valores por defecto de las banderas 52, 37, 46, 47 y 53.', file=f)
        if english:
                print('; -Set initial location..', file=f)
        else:
                print('; -Establece la localidad inicial.', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
                print('_       _       RESET', file=f)
                print('                LET fStrength 10', file=f)
                print('                LET fMaxCarr 4', file=f)
                print('                SET fCPronounNoun', file=f)
                print('                SET fCPronounAdject', file=f)
                print('                LET fObjFlags 64', file=f)
        else:
                print('_       _       RESET', file=f)
                print('                LET Strength 10', file=f)
                print('                LET MaxCarr 4', file=f)
                print('                SET CPNoun', file=f)
                print('                SET CPAdject', file=f)
                print('                LET OFlags 64', file=f)
        if idloc:
            print('                GOTO '+listLocationIdentifiers[startRoom-1], file=f)
        else:
            print('                GOTO '+str(startRoom), file=f)
        print('', file=f)
        if verbosity:
                print('OK.')
                
def imprimePRO6_DR():
        if english:
                print('; -Sets initial position of the text window (WINDOW 1).', file=f)
        else:
                print('; -Establece la posición inicial de la ventana de texto (WINDOW 1).', file=f)
        if english:
                print('; -Describes location 0 (usually presentation screen).', file=f)
        else:
                print('; -Describe localidad 0 (normalmente pantalla de presentación).', file=f)
        if english:
                print('; -Displays introduction text.', file=f)
        else:
                print('; -Muestra texto de introducción.', file=f)
        if english:
                print('; -Starts flags resetting loop.', file=f)
        else:
                print('; -Comienza el bucle de reseteo de banderas.', file=f)
        print('', file=f)
        if english:
            print('; What follows is essentially a copy-paste from DAAD-Ready 0.7 routine.', file = f)
            print('; Hopefully, it will work!', file=f)
        else:
            print('; Lo que sigue es básicamente un copia-pega de la rutina de DAAD-Ready 0.7', file = f)
            print('; ¡Con suerte, funcionará!', file=f)
        print('', file=f)    
        print('#ifndef "zx128"', file = f)
        print('>', file=f)
        print('_       _       WINDOW 1', file=f)
        print('                #ifdef "pc"', file = f)
        print('                PAPER 0', file = f)
        print('                INK 15', file = f)
        print('                #endif', file = f)
        print('                #ifndef "tape"', file=f)
        print('                WINAT 14 0', file=f)
        print('                #endif', file=f)
        print('                #ifdef "tape"', file=f)
        print('                WINAT 0 0', file = f)
        print('                #endif', file = f)
        print('                WINSIZE 25 127', file = f)
        print('                CLS', file=f)
        print('                DESC 0', file = f)                
        print('#ifndef "tape"', file = f)
        print('                XPICTURE 0', file=f)
        print('                #ifdef "nativeraster"', file=f)
        print('                DISPLAY 0', file=f)
        print('                #endif', file=f)
        print('#endif', file = f)
        print('', file = f)
        print('>', file = f)
        print('_       _       ANYKEY', file = f)
        print('                CLS', file=f)
        print('                MESSAGE 14', file = f)
        print('                ANYKEY', file = f)
        print('                CLS', file = f)
        print('                SET 255', file = f)
        print('#else', file = f)
        print('; ZX 128', file = f)
        print('>', file=f)
        print('_       _       WINDOW 1', file = f)
        print('                WINAT 14 0', file = f)
        print('                WINSIZE 25 127', file = f)
        print('                CLS', file = f)
        print('                PICTURE 0', file = f)
        print('                DISPLAY 0', file = f)
        print('                SKIP 1', file = f)
        print('', file = f)
        print('>', file = f)
        print('_       _       WINAT 0 0', file = f)
        print('                WINSIZE 25 127', file = f)
        print('                CLS', file = f)
        print('', file = f)
        print('>', file = f)
        print('_       _       DESC 0', file = f)
        print('                ANYKEY', file = f)
        print('                CLS', file = f)
        print('                MESSAGE 14', file = f)
        print('                ANYKEY', file = f)
        print('                CLS', file = f)
        print('                SET 255', file = f)
        print('#endif', file = f)
        print('', file=f)
        if english:
                print('; Clear all flags save 29 (fGflags).', file=f)
        else:
                print('; Pone a 0 todas las banderas excepto la 29 (fGFlags).', file=f)
        print('', file=f)
        print('>', file=f)
        print('_       _       MINUS 255 1', file=f)
        print('                NOTEQ 255 fGFlags', file=f)
        print('                CLEAR @255', file=f)
        print('', file=f)
        print('>', file=f)
        print('_       _       NOTZERO 255', file=f)
        print('                SKIP -2', file=f)
        print('', file=f)
        if english:
                print('; -Reset object locations to original values (established in /OBJ).', file=f)
        else:
                print('; -Pone las localidades de los objetos a su valor original (establecido en /OBJ).', file=f)
        if english:
                print('; -Set default values for flags 52, 37, 46, 47 and 53.', file=f)
        else:
                print('; -Valores por defecto de las banderas 52, 37, 46, 47 y 53.', file=f)
        if english:
                print('; -Set initial location..', file=f)
        else:
                print('; -Establece la localidad inicial.', file=f)
        print('', file=f)
        print('>', file=f)
        print('_       _       RESET', file=f)
        print('                LET fStrength 10', file=f)
        print('                LET fMaxCarr  4', file=f)
        print('                SET fCPronounNoun', file=f)
        print('                SET fCPronounAdject', file=f)
        print('                LET fObjFlags 64', file=f)
        if idloc:
            print('                GOTO '+listLocationIdentifiers[startRoom-1], file=f)
        else:
            print('                GOTO '+str(startRoom), file=f)
        print('', file=f)
        if verbosity:
                print('OK.')
        
def imprimeOtrosPros(darkStatusLine):
        if verbosity:
                if english:
                      print('Printing rest of PROs',end=' -> ')
                else:
                      print('Imprimiendo otros PROs',end=' -> ')
        if daadReady:
                imprimeOtrosPros_DR()
                return
        print('/PRO 7',file=f)
        print('', file=f)
        if english:
              print('; Text "up.', file=f)        
        else:
              print('; Texto "arriba."', file=f)   
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       WINDOW 1',file=f)
        print('                WINAT textrow2 0',file=f)
        print('                WINSIZE ROWS 127',file=f)
        print('                CLS',file=f)
        print('',file=f)
        print('/PRO 8',file=f)
        print('', file=f)
        if english:
              print('; Text "down."', file=f)      
        else:
              print('; Texto "abajo."', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       WINDOW 1',file=f)
        print('                WINAT textrow1 0',file=f)
        print('                WINSIZE ROWS 127',file=f)
        print('                CLS',file=f)
        print('',file=f)  
        print('/PRO 9',file=f)
        print('', file=f)
        if english:
              print('; Set text window position.', file=f) 
        else:
              print('; Recoloca la ventana de texto.', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
                print('_       _       PICTURE @fPlayer',file=f)
        else:
                print('_       _       PICTURE [Player]',file=f)
        print('                PROCESS 8',file=f)
        print('                DONE',file=f)
        print('',file=f)
        if dsf:
                print('>', file=f)
        print('_       _       PROCESS 7',file=f)
        print('',file=f)  
        print('/PRO 10',file=f)
        print('', file=f)
        if english:
              print('; Automatic exits listing', file=f)
              print('; WARNING! It uses flags 100 and 101', file=f)       
        else:     
              print('; Listado automático de salidas', file=f)
              print('; ¡OJO!, gasta los flags 100 y 101', file=f)         
        print('',file=f)
        if dsf:
            print('>', file=f)
        if dsf:
            print('_       _       NOTZERO fDarkF', file = f)
        else:
            print('_       _       NOTZERO DarkF', file = f)
        print('                SYSMESS 0 ', file = f)
        print('                NEWLINE', file = f)
        print('                DONE ', file = f)
        print('',file=f)
        if dsf:
                print('>', file=f)
        print('_       _       MES 0',file=f)
        print('                CLEAR 101',file=f)
        print('                LET 33 2',file=f)
        print('',file=f)
        if dsf:
                print('>', file=f)
        print('_       _       COPYFF 38 100',file=f)
        print('                MOVE 100',file=f)
        if dsf:
                print('                MES @33',file=f)
        else:
                print('                MES [33]',file=f)
        print('                PLUS 101 1',file=f)
        print('',file=f)
        if dsf:
                print('>', file=f)
        print('_       _       PLUS 33 1',file=f)
        print('                LT 33 14',file=f)
        print('                SKIP -2',file=f)
        print('',file=f)
        if dsf:
                print('>', file=f)
        print('_       _       NOTZERO 101', file=f)
        print('                NEWLINE', file = f)
        print('                DONE',file=f)      
        print('',file=f)
        if dsf:
                print('>', file=f)
        print('_       _       MESSAGE 1', file=f)
        print('',file=f)
        if statusLine:
                print('/PRO 11', file=f)
                print('', file=f)
                if english:
                      print('; Updates status line', file=f)      
                else:     
                      print('; Actualiza barra de estado', file=f)
                print('',file=f)
                if dsf:
                        print('>', file=f)
                print('_       _       WINDOW 2', file=f)
                print('                CLS', file=f)
                print('', file=f)
                if english:
                        print('; If dark, says it so at the status line and leaves the process.', file=f)
                else:        
                        print('; Si no hay luz, lo indica en la barra de estado y sale del proceso.', file=f)
                print('', file=f)
                if dsf:
                        print('>', file=f)
                if dsf:
                        print('_       _       NOTZERO fDarkF' , file=f)
                else:
                        print('_       _       NOTZERO DarkF' , file=f)
                print('                MES '+str(darkStatusLine), file=f)
                print('                PROCESS 12', file=f)
                print('                DONE', file=f)
                print('', file=f)
                if english:
                      print('; Prints location name at status line.', file=f)     
                      print('; If you add more locations after using trizbort,', file=f)
                      print('; You can add its text here with a condition as:', file=f)
                      print('; _       _       AT loc num', file=f)
                      print(';                 MES XX', file=f)
                      print('; where XX is the message with the text to write.', file=f)          
                      print('', file=f)
                else:
                      print('; Imprime el texto de la localidad en la barra.', file=f)    
                      print('; Si añades más localidades tras el uso de trizbort,', file=f)
                      print('; Puedes poner su texto aquí con una condición del tipo:', file=f)
                      print('; _  _       AT nº de loc', file=f)
                      print(';            MES XX', file=f)
                      print('; siendo XX el mensaje donde has puesto el texto a poner en la barra.', file=f)              
                      print('', file=f)
        if verbosity:
                print('OK.')
                      
def imprimeOtrosPros_DR():
        print('/PRO 7',file = f)
        print('', file = f)
        if english:
              print('; Automatic exits listing', file = f)
              print('; WARNING! It uses flags 100 and 101', file = f)       
        else:     
              print('; Listado automático de salidas', file = f)
              print('; ¡OJO!, gasta los flags 100 y 101', file = f)         
        print('', file = f)
        print('>', file = f)
        print('_       _       NOTZERO fDarkF', file = f)    
        print('                SYSMESS 0 ', file = f)
        print('                NEWLINE', file = f)
        print('                DONE ', file = f)
        print('', file = f)
        print('>', file = f)
        print('_       _       MES 0', file = f)
        print('                CLEAR 101', file = f)
        print('                LET 33 2', file = f)
        print('', file = f)
        print('>', file = f)
        print('_       _       COPYFF 38 100', file = f)
        print('                MOVE 100', file = f)
        print('                MES @33', file = f)
        print('                PLUS 101 1', file = f)
        print('', file = f)
        print('>', file=f)
        print('_       _       PLUS 33 1', file = f)
        print('                LT 33 14', file = f)
        print('                SKIP -2', file = f)
        print('', file = f)
        print('>', file = f)
        print('_       _       NOTZERO 101', file = f)
        print('                NEWLINE', file = f)
        print('                DONE',file = f)      
        print('', file = f)
        if dsf:
                print('>', file = f)
        print('_       _       MESSAGE 1', file = f)
        print('', file=  f)
        if verbosity:
                print('OK.')

def imprimeOtrosPros2():
        print('', file=f)
        print('/PRO 12', file=f)
        print('', file=f)
        if english:
                print('; Print turns at status line', file=f)
        else:     
                print('; Imprime turnos en la barra de estado', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
                print('_       _       TAB Turns_TAB', file=f)
        else:
                print('_       _       TAB COLS-13', file=f)
        print('                LT 29 128', file=f)
        if dsf:
                print('                TAB 67', file=f)
        else:
                print('                TAB 80-13', file=f)
        print('', file=f)
        if dsf:
                print('>', file=f)
        print('_       _       MES 15', file=f)
        if dsf:
                print('                DPRINT fTurns', file=f)
        else:
                print('                DPRINT Turns', file=f)
        print('                WINDOW 1', file=f)
        if verbosity:
                print('OK.')
        
def imprimeTodo():
        imprimeDEF()
                
        imprimeCTL()        

        if dsf==False:
                if english:
                        imprimeTOK_ENG()
                else:
                        imprimeTOK()

        if english:
                imprimeVOC_ENG()
        else:
                imprimeVOC()

        x=50
        if english:
                print('; User defined objects, if any.', file=f)
                print(';', file=f)
        else:
                print('; Objetos definidos por el usuario en el mapa visual, si los hubiera.', file=f)
                print(';', file=f)
                
        # Imprime el nombre del objeto en la sección vocabulario siempre que no haya otro objeto con el mismo nombre.
        # Se hizo para permitir que haya objetos con el mismo nombre sin que triz2DAAD repitiese inadvertidamente la 
        # palabra en la sección noun del VOC
        
        listNames=[]
        for y in listObjects:
                z=y['name']
                listNames.append(z)
                if listNames.count(z)==1:
                        print (y['name']+'      '+str(x)+'      noun',file=f)
                        x=x+1

        if english:
                imprimeVOC2_ENG()               
        else:
                imprimeVOC2()
        
        if dsf:
                if p1:
                        if english:
                                imprimeSTX_1p_ENG_DSF()
                        else:
                                imprimeSTX_1p_SPA_DSF()
                else:
                        if english:
                                imprimeSTX_2p_ENG_DSF()
                        else:
                                imprimeSTX_2p_SPA_DSF()
        else:
                if p1:
                        if english:
                                imprimeSTX_1p_ENG()
                        else:
                                imprimeSTX_1p_SPA()
                else:
                        if english:
                                imprimeSTX_2p_ENG()
                        else:
                                imprimeSTX_2p_SPA()
        
        if dsf:
                if english:
                        imprimeMTX_ENG_DSF()
                else:
                        imprimeMTX_SPA_DSF()
        else:
                if english:
                        imprimeMTX_ENG()
                else:
                        imprimeMTX_SPA()
        
        # Crea una lista de localidades sin las localidades "contenedor" para manejar los nombres de localidad en la barra de estado en la sección MTX
                
        listRooms2=listRooms[len(listContainers):]

        if statusLine:
                for x, y in enumerate(listRooms2, start=1):
                        if dsf:
                                print('/' + str(15+x) + ' "' + y['subtitle'] + '"', file=f)
                        else:
                                print('/'+str(15+x), file=f)
                                print(y['subtitle'], file=f)
                        
                helpMessage1=len(listRooms2) + 15 + 1
                helpMessage2=helpMessage1 + 1
        else:
                helpMessage1=15
                helpMessage2=16
        
        print(';', file=f)
        if english:
                if statusLine:
                        myString='After location names messages, '
                else:
                        myString=''
                print('; ' + myString + 'Triz2DAAD uses 2 messages for the help screen.', file=f)
        else:
                if statusLine:
                        myString='Tras los mensajes con los nombres de las localidades, '
                else:
                        myString=''
                print('; ' + myString + 'Triz2DAAD usa 2 mensajes para la pantalla de ayuda.', file=f)
        print(';', file=f)
        
        if dsf:
                if english:
                        print('/' + str(helpMessage1) + ' " HELP SCREEN"', file=f)
                        print('/' + str(helpMessage2) + ' "Text adventures are text games based on exploring locations and manipulating objects next to the player character.#n#nActions are told to the computer using simple ACTION-OBJECT like sentences.#n#nMovements are done using cardinal points: GO NORTH, SOUTH, WEST or their abreviations: N, S, E, W. Occasionally commands as UP or IN will also work.#n#nCommon actions with objects are GET object, DROP, EXAMINE (or its abbreviation EX). INVENTORY (or I) lists carried items. LOOK (or L) redescribes the location.#n"', file=f)
                else:
                        print('/' + str(helpMessage1) + ' " PANTALLA DE AYUDA"', file=f)
                        print('/'+str(helpMessage2) + ' "Las aventuras conversacionales son juegos de texto basados en la exploración de localidades y la manipulación de objetos al alcance inmediato del protagonista.#n#nLas acciones se comunican al ordenador mediante frases sencillas del tipo ACCION-OBJETO.#n#nEl movimiento se efectua mediante puntos cardinales: IR NORTE, SUR, OESTE o sus abreviaturas: N, S, E, O. Ocasionalmente órdenes como SUBIR, o ENTRAR también funcionarán.#n#nAcciones comunes con los objetos son COGER objeto, DEJAR, EXAMINAR (o su abreviatura EX). INVENTARIO (o I) lista los objetos llevados. MIRAR o M redescribe la localidad.#n"', file=f)
        else:
                if english:
                        print('/'+str(helpMessage1), file=f)
                        print(' HELP SCREEN', file=f)
                        print('/'+str(helpMessage2), file=f)
                        print('Text adventures are text games based on exploring locations and manipulating objects next to the player character.', file=f)
                        print('', file=f)
                        print('', file=f)
                        print('Actions are told to the computer using simple "action-object" like sentences.', file=f)
                        print('', file=f)
                        print('', file=f)
                        print('Movements are done using cardinal points "GO NORTH", "SOUTH", "WEST" or their abreviations: N, S, E, W. Occasionally commands as "UP" or "IN" will also work.', file=f)
                        print('', file=f)
                        print('', file=f)
                        print('Common actions with objects are "GET object", "DROP", "EXAMINE" (or its abbreviation "EX"). "INVENTORY" (or "I") lists carried items. "LOOK" (or "L") redescribes the location.', file=f)
                        print('', file=f)
                else:
                        print('/'+str(helpMessage1), file=f)
                        print(' PANTALLA DE AYUDA', file=f)
                        print('/'+str(helpMessage2), file=f)
                        print('Las aventuras conversacionales son juegos de texto basados en la exploración de localidades y la manipulación de objetos al alcance inmediato del protagonista.', file=f)
                        print('', file=f)
                        print('', file=f)
                        print('Las acciones se comunican al ordenador mediante frases sencillas del tipo "acción-objeto".', file=f)
                        print('', file=f)
                        print('', file=f)
                        print('El movimiento se efectua mediante puntos cardinales "IR NORTE", "SUR", "OESTE" o sus abreviaturas: N, S, E, O. Ocasionalmente órdenes como "SUBIR", o "ENTRAR" también funcionarán.', file=f)
                        print('', file=f)
                        print('', file=f)
                        print('Acciones comunes con los objetos son "COGER objeto", "DEJAR", "EXAMINAR" (o su abreviatura "EX"). "INVENTARIO" (o "I") lista los objetos llevados. "MIRAR" o "M" redescribe la localidad.', file=f)
                        print('', file=f)
                
        darkStatusLine=helpMessage2+1
        
        print(';', file=f)
        if statusLine:
                if english:
                        print('; After help messages, Triz2DAAD uses one more message as status line text in dark locations.', file=f)
                else:
                        print('; Tras los mensajes de ayuda, Triz2DAAD usa un mensaje más para la barra de estado en localidades sin luz.', file=f)
                print(';', file=f)
                
                if dsf:
                        if english:
                                print('/'+str(darkStatusLine) + ' "Darkness"', file=f)
                        else:
                                print('/'+str(darkStatusLine) + ' "Oscuridad"', file=f)
                else:
                        if english:
                                print('/'+str(darkStatusLine), file=f)
                                print('Darkness', file=f)
                        else:
                                print('/'+str(darkStatusLine), file=f)
                                print('Oscuridad', file=f)
                print(';', file=f)
        if verbosity:
                print('OK.')        

        if verbosity:
                if english:
                        print('Printing english /OTX section',end=' -> ')
                else:
                        print('Imprimiendo sección /OTX',end=' -> ')
        print('/OTX',file=f)
        print(';', file=f)
        if english:
                print('; Objects listing text.', file=f)
        else:
                print('; Texto para los listados de los objetos.', file=f)
        print(';', file=f)
        x=0
        for y in listObjects:
                if dsf:
                        print('/'+str(x) + ' "' + y['description'] + '"', file=f)
                else:
                        print('/'+str(x),file=f)
                        print(y['description'], file=f)
                x=x+1
        print(';', file=f)
        if verbosity:
                print('OK.')

        if verbosity:
                if english:
                        print('Printing /LTX section', end=' ->- ')
                else:
                        print('Imprimiendo sección /LTX',end=' -> ')    
        print('/LTX',file=f)
        print(';', file=f)
        if english:
                print('; Locations text.', file=f)
        else:
                print('; Texto de las localidades.', file=f)
        print(';', file=f)
        if dsf:
                if english:
                        cadena = 'by: '
                else:
                        cadena = 'por: '
                print('/0' + ' "' + title.title() + '#n#n' + cadena + author + '#n#n' + description + '#n#n' + '"', file=f)
        else:
                print('/0',file=f)
                print(title.title(), file=f)
                print('', file=f)
                print('', file=f)
                if english:
                        print('by: ', author, file=f)
                else:
                        print('por: ', author, file=f)
                print('', file=f)
                print('', file=f)
                print(description, file=f)
                print('', file=f)
                print('', file=f)
        x=1
        for y in listRooms:
                #el modo dsf no admite retornos de carro en las cadenas de LTX
                if dsf:
                        # Si estamos en Windows
                        if '\r\n' in y['description']:
                                y['description']=y['description'].replace('\r\n','#n')
                                if english:
                                        print('WARNING: Line feeds were removed from location ' + str(y['loc']) + ' description.\n')
                                else:
                                        print('ATENCIÓN: Retornos de línea eliminados en la descripción de localidad ' + str(y['loc']) + '\n')
                        # Si estamos en Linux
                        if '\n' in y['description']:
                                y['description']=y['description'].replace('\n','#n')
                                if english:
                                        print('WARNING: Line feeds were removed from location ' + str(y['loc']) + ' description.\n')
                                else:
                                        print('ATENCIÓN: Retornos de línea eliminados en la descripción de localidad ' + str(y['loc']) + '\n')
                if dsf:
                        cadena='"'
                        if listContainers !=  None:
                                if x <= len(listContainers):
                                        cadena=''
                        print('/'+str(x) + ' "' + y['description'] + cadena, file=f)
                else:
                        print('/'+str(x), file=f)
                        print(y['description'], file=f)
                x=x+1
        print(';', file=f)
        if verbosity:
                print('OK.')

        if verbosity:
                if english:
                        print('Printing /CON section',end=' -> ')
                else:
                        print('Imprimiendo sección /CON',end=' -> ')
        print('/CON',file=f)
        print(';', file=f)
        if english:
                print('; Location connections table', file=f)
        else:
                print('; Tabla de conexiones entre localidades.', file=f)
        print(';', file=f)
        print('/0',file=f)
        x=1
        for y in listRooms:
                print('/'+str(x),file=f)
                if y['con']!=[]:
                        for z in y['con']:
                                print(z, file=f)
                x=x+1
        print(';', file=f)
        if verbosity:
                print('OK.')

        if verbosity:
                if english:
                        print('Printing /OBJ section',end=' -> ')
                else:
                        print('Imprimiendo sección /OBJ',end=' -> ')
        print ('/OBJ',file=f)
        print(';', file=f)
        if english:
                print('; Objects definition table:', file=f)
                print('; -Start location.', file=f)
                print('; -Weight.', file=f)
                print('; -Container - wearable atributes.', file=f)
                print('; -16 user defined atributes.', file=f)
                print('; -Noun and adjective.', file=f)
        else:
                print('; Tabla de definición de objetos:', file=f)
                print('; -Localidad inicial.', file=f)
                print('; -Peso.', file=f)
                print('; -Atributos de contenedor y ropa.', file=f)
                print('; -16 atributos definibles por el usuario.', file=f)
                print('; -Nombre y adjetivo.', file=f)
        print(';', file=f)
        x=0
        for y in listObjects:
                cadena=''
                cadena = cadena + '/' + str(x) + ' ' + str(y['loc']) + ' ' + '1' + ' '
                if y['container']==1:
                        cadena=cadena + 'Y '
                else:
                        cadena=cadena + '_ '
                if y['wearable']==1:
                        cadena=cadena + 'Y   '  
                else:
                        cadena=cadena + '_   '
                cadena=cadena+'_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _  '+y['name']+' _'
                print(cadena, file=f)
                x=x+1
        print(';', file=f)
        if verbosity:
                print('OK.')

        imprimePRO0()
        imprimePRO1()
        imprimePRO2()
        imprimePRO3()
        imprimePRO4()
        if english:
                imprimePRO5_ENG(helpMessage1, helpMessage2, listRooms2)
        else:
                imprimePRO5(helpMessage1, helpMessage2, listRooms2)
        imprimePRO6()
        imprimeOtrosPros(darkStatusLine)
        if statusLine:
                for x, y in enumerate(listRooms2, start=1):
                        if dsf:
                                print('>', file=f)
                        print('_       _       AT '+str(x+len(listContainers)), file=f)
                        print('                MES '+str(x+15), file=f)
                        print('', file=f)
                if dsf:
                        print('>', file=f)
                print('_       _       PROCESS 12', file=f)
                imprimeOtrosPros2()
        
        if dsf:
                print('/END', file=f)

        if verbosity:
                print()
                
def createObjectIdentifiers():
        aux=[]
        for y in listObjects:
                aux.append('o' + y['name'].capitalize())
        aux2=[]
        for y in aux:
                if aux.count(y)>1:
                        aux2.append(y)
        aux2=set(aux2)
        for y in aux2:
                x=1
                for w, z in enumerate(aux.copy()):
                        if y==z:
                                aux[w] = aux[w] + str(x)
                                x+=1
        return aux

def createLocationIdentifiers():
        aux=[]
        for x, y in enumerate(listRooms):
                cadena=y['name'].capitalize().replace(' ', '_')
                if cadena=='':
                        if english:
                                cadena='Container_'
                        else:
                                cadena='Contenedor_'
                        cadena+=str(x)
                aux.append('l' + cadena)
        aux2=[]
        for y in aux:
                if aux.count(y)>1:
                        aux2.append(y)
        aux2=set(aux2)
        for y in aux2:
                x=1
                for w, z in enumerate(aux.copy()):
                        if y==z:
                                aux[w] = aux[w] + str(x)
                                x+=1
        return aux

print()
print('Triz2DAAD versión 1.0.4b10 230212 (c) 2019-23 Pedro Fernández')     
print('-h para ayuda / -h for options')
print()

parser = argparse.ArgumentParser()

parser.add_argument("in_file", help='Fichero de entrada')
parser.add_argument("out_file", help='Fichero de salida', nargs='?')
parser.add_argument('-p1', help="Mensajes de sistema en primera persona", action="store_true")
parser.add_argument('-e', '--english', help="Create an english DAAD template", action='store_true')
parser.add_argument('-md', help="Añade código condicional para activar el modo de dibujo invisible en CPC", action="store_true")
parser.add_argument('-dsf', help="Exporta a fichero con sintáxis DSF", action="store_true")
parser.add_argument('-v', '--verbosity', help="Modo 'verbose'", action="store_true")
parser.add_argument('-sl', '--statusline', help="Añade barra de estado", action="store_true")
parser.add_argument('-idobj', help="Añade directivas 'define' para identificar a los objetos", action="store_true")
parser.add_argument('-idloc', help="Añade directivas 'define' para identificar las localidades", action="store_true")
parser.add_argument('-lobj', help="En lugar del objeto 0, considera objetos marcados con [l] como fuente de luz.", action="store_true")
parser.add_argument('-blockall', help="Bloquea acciones TODO.", action="store_true")
parser.add_argument('-dr', '--daadready', help="Crea plantillas compatibles con DAADReady 0.7", action="store_true")
parser.add_argument('-ink', help='Tinta por defecto en 16 bits', type=int)

args=parser.parse_args()

in_file = args.in_file
out_file = args.out_file
p1 = args.p1
english = args.english
md = args.md
dsf = args.dsf
verbosity = args.verbosity
statusLine = args.statusline
idobj = args.idobj
idloc = args.idloc
lobj = args.lobj
blockall = args.blockall
daadReady = args.daadready
ink = args.ink

if ink:
        if ink < 0 or ink > 15:
                if english:
                        print('WARNING: unexpected ink value for DAAD classic.')
                else:
                        print('ATENCIÓN: valor de tinta no esperado para DAAD clásico.')
else:
        ink = 1
                
if daadReady:
        if english:
                print('-Exporting to a DAADReady 0.7 compatible template.')
        else:
                print('-Exportando a una plantilla comnpatible con DAADReady 0.7')
        dsf=True
        if statusLine:
                if english:
                        print(' WARNING: DAADReady mode deactivates status line.')
                else:
                        print(' ATENCIÓN: el modo DAADReady desactiva la barra de estado.')
        statusLine=False
        idobj = True
        idloc = True

if dsf:
        ext='.dsf'
else:
        ext='.sce'

trizbort=False

in_file=in_file.lower()

if in_file.endswith('.trizbort'):
        trizbort=True
        
if out_file == None:
        out_file = in_file
        if out_file.endswith('.json'):
                out_file = out_file.replace('.json', ext)
        elif out_file.endswith('.trizbort'):
                out_file = out_file.replace('.trizbort', ext)
        else:
                out_file = out_file + ext
else:
        out_file=out_file.lower()
        if not out_file.endswith(ext):
                out_file = out_file + ext

if verbosity:
        if english:
                print('-English temnplate selected.')
        else:
                print('-Usando plantilla en español.')
                
        if p1:
                if english:
                        print('-First person selected.')
                else:
                        print('-Usando primnera persona.')
        else:
                if english:
                        print('-Second person selected.')
                else:
                        print('-Usando segunda persona.')
                        
        if md:
                if english:
                        print('-CPC "MDRW" mode ON.')
                        if daadReady:
                                print(' WARNING: "MDRW" mode is ignored in DAAD Ready.')
                else:
                        print('-CPC modo "MDRW" activado.')
                        if daadReady:
                                print(' ATENCIÓN: el modo "MDRW" es ignorado en DAAD Ready.')
        else:
                if english:
                        print('-CPC "MDRW" mode OFF.')
                else:
                        print('-CPC modo "MDRW" desactivado.')

        if dsf:
                if english:
                        print('-Exporting to DSF template (DAAD Reborn Compiler).')
                else:
                        print('-Exportando a plantilla DSF (DAAD Reborn Compiler).')
        else:
                if english:
                        print('-Exporting to SCE template (Classic DAAD).')
                else:
                        print('-Exportando a plantilla SCE (DAAD clásico).')

        if verbosity:
                if english:
                        print('-Verbose mode ON.')
                else:
                        print('-Modo "verbose" activado.')
        else:
                if english:
                        print('-Verbose mode OFF.')
                else:
                        print('-Modo "verbose" desactivado.')
                        
        if statusLine:
                if english:
                        print('-Stauus line active.')
                else:
                        print('-Barra de estado activada.')
        else:
                if english:
                        print('-Status line deactivated.')
                else:
                        print('-Barra de estado desactivada.')

        if idobj:
                if english:
                        print('-Object identifiers ON.')
                else:
                        print('-Identificadores de objeto activados.')
        else:
                if english:
                        print('-Object identifiers OFF.')
                else:
                        print('-Identificadores de objeto desactivados.')

        if idloc:
                if english:
                        print('-Location identifiers ON.')
                else:
                        print('-Identificadores de localidad activados.')
        else:
                if english:
                        print('-Location identifiers OFF.')
                else:
                        print('-Identificadores de localidad desactivados.')

        if lobj:
                if english:
                        print('-Using [l] objects as light source')
                else:
                        print('-Usando objetos [l] como fuentes de luz')
        else:                
                if english:
                        print('-Using object 0 as light source')
                else:
                        print('-Usando objeto 0 como fuente de luz')
                        
        if blockall:
                if english:
                        print('-"ALL" actions blocked.')
                else:
                        print('-Acciones "TODO" bloqueadas.')
        else:                
                if english:
                        print('-"ALL" actions not blocked.')
                else:
                        print('-Acciones "TODO" sin bloquear.')

        if daadReady:
                if english:
                        print('-Using DAAD Ready 0.5 compatible template.')
                else:
                        print('-Usando plantilla compatible con DAAD Ready 0.5.')
        else:
                if english:
                        print('-Using standard template.')
                else:
                        print('-Usando plantilla standard.')

        if ink:
                if english:
                        print('-16 bits INK set to ' + str(ink) + '.')
                else:
                        print('-Tinta en 16 bits puesta en ' + str(ink) +  '.')
        else:
                if english:
                        print('-16 bits INK set to 1.')
                else:
                        print('-Tinta en 16 bits puesta a 1.')

        print()

if english:
        print('Processing, please wait.')
else:
        print('Procesando, por favor espere.')
        
print()

if trizbort:
        data=xml2json()
else:
        with open(in_file, encoding='UTF-8') as f:
                data=json.load(f)
        # 1.0.3 Detecta si tiene el formato nuevo de json de los mapas de Trizbort.io.
        # Si es el antiguo no hace nada para mantener la compatibilidad.
        if not 'type' in data['elements'][0]:
                jsonFormatPatch()

# Valores por defecto para título, autor, etc...

if trizbort:
        triz_string=''
else:
        triz_string='.io'
if dsf:
        sce_string='DSF'
else:
        sce_string='SCE'
if english:
        title='Test adventure generated with Triz2DAAD.'
        author='Anonymous'
        description='Test adventure for the conversion script Triz2DAAD (trizbort'
        description=description + triz_string
        description=description + ' maps to DAAD '
        description=description + sce_string
        description=description + ' source code.'
        history='Adventure introduction text (edit in message 14).'
else:
        title='Aventura de prueba generada con Triz2DAAD.'
        author='Anónimo'
        description='Aventura de prueba del script conversor Triz2DAAD (mapas de trizbort'
        description=description + triz_string
        description=description + ' a código fuente '
        description=description + sce_string
        description=description + ' del DAAD).'
        history='Texto introductorio de la aventura (editar en mensaje 14).' 

startRoom=data['startRoom']
if startRoom==0:
        startRoom=1
        
if data['title'] != 'Untitled map' and data['title'] != '':
        title=data['title']
if data['author']:
        author=acentos(data['author']).upper()
if data['description']:
        description=data['description']
if 'history' in data:
        if data['history']:
                history=data['history']

if verbosity:
        if english:
                print ('Creating locations and objects list.')
        else:
                print ('Creando lista de localidades y objetos.')

listRooms=[]
listObjects=[]

# 1.0.2b3 Creamos la variable objId para dar un nº de identificación exclusivo a cada objeto.
# 3000 es un valor arbitrario fácil de distinguir de los nºs de localidad.
# Todo ello para hacernos la vida más fácil al establecer la relacción de contenedores.

obj_id=3000

loc=1

for y in data['elements']:
        if y['type']=='Room':
                if y['name'] in ['', 'Cave', 'Room']:
                        if english:
                                y['name']='Location ' + str(loc)
                        else:
                                y['name']='Localidad ' + str(loc)
                if y['subtitle']=='':
                        y['subtitle']=y['name']
                y['subtitle']=y['subtitle'][:26]
                if y['description']=='':
                        if english:
                                y['description']='Location ' + str(loc) + ' description'
                        else:
                                y['description']='Descripción de localidad ' + str(loc)
                y['loc']=loc
                listRooms.append(y)
                if y['objects']!=[]:
                        recursive_objects(y['objects'],loc)                        
                loc+=1

# busca las cadenas [W] o [C] en el nombre de los objetos. Si las encuentra añade las claves 'wearable' o 'container' como 1 al diccionario (y si no, las añade como 0).

for y in listObjects:
        if '[W]' in y['name']:
                y['name']=y['name'].replace('[W]','')
                y['wearable']=1
        else:
                y['wearable']=0
        if '[C]' in y['name']:
                y['name']=y['name'].replace('[C]','')
                y['container']=1        
        else:
                y['container']=0
        if y['content'] != []:
                y['container']=1
        if '[L]' in y['name']:
                y['name']=y['name'].replace('[L]','')
                y['lightsource']=1
        else:
                y['lightsource']=0
                
# Elimina objetos con nombre no válido (cadena nula o espacios en blanco).

for y in listObjects:
        if y['name'].strip()=='':
                if english:
                        print ('WARNING: skipping object with invalid name at location', y['loc'], ':', listRooms[y['loc']-1]['name'])
                else:
                        print ('ATENCIÓN: se ignora un objeto de nombre no válido en localidad', y['loc'], ':', listRooms[y['loc']-1]['name'])                        
                print()        

listObjects=[y for y in listObjects if y['name'].strip()!='']

# Añade una advertencia si hay objetos con el mismo nombre.
# Aunque desde 1.0.2 no detiene el proceso.

listNames=[]
for y in listObjects:
        z=y['name']
        listNames.append(z)
        if listNames.count(z)>1:
                if english:
                        print ('WARNING: duplicate object name:', z)
                else:
                        print ('ATENCIÓN: nombre de objeto duplicado:', z)
                print()

# Separa los objetos contenedores en una lista aparte.

listContainers=[y for y in listObjects if y['container']==1]
listObjects=[y for y in listObjects if y['container']==0]

# Si no hay objetos (normales), crea una linterna como objeto dummy (como en la plantilla original)

if listObjects==[]:
        if english:
                listObjects.append({'name':'TORCH', 'type':'Object', 'description':'a torch (lit)', 'kind':5, 'content':[], 'loc':1, 'wearable':0, 'container':0, 'parent':1})
        else:
                listObjects.append({'name':'LINTERNA', 'type':'Object', 'description':'una linterna (encendida)', 'kind':5, 'content':[], 'loc':1, 'wearable':0, 'container':0, 'parent':1})

# Añade los objetos contenedores a partir de la posición 1 de la lista de objetos.

for y in listContainers:
        listObjects.insert(1,y)

# Añade tantas localidades "falsas" como contenedores al principio de la lista de localidades.

if english:
        cadena='; Fake location meant to support some container object.'
else:
        cadena='; Localidad falsa para dar soporte a un objeto contenedor.'
        
if dsf:
        cadena='" ' + cadena
        
for y in listContainers:
        listRooms.insert(0,{'id':0, 'loc':0, 'name':'', 'subtitle':'', 'description':cadena})

# Actualiza la clave loc (nº de localidad) de cada entrada de la lista de localidades según las localidades "contenedor" que se hubieren añadido.

for x, y in enumerate(listRooms, start=1):
        y['loc']=x
        
# 1.0.4b10 Actualiza los nombres y descripciones de localidad por defecto ("localidad XX", "descripción de localidad XX") si se hubieran añadido contenedores que hubiesen afectado la numeración.

if listContainers != []:
    for y in listRooms:
        if english:
            if y['description'].startswith('Location '):
                y['description'] = 'Location ' + str(y['loc']) + ' description'
            if y['name'].startswith('Location '):
                y['name'] = 'Location ' + str(y['loc'])
            if y['subtitle'].startswith('Location '):
                y['subtitle'] = 'Location ' + str(y['loc'])    
        else:
            if y['description'].startswith('Descripción de localidad '):
                y['description'] = 'Descripción de localidad ' + str(y['loc'])
            if y['name'].startswith('Localidad '):
                y['name'] = 'Localidad ' + str(y['loc'])
            if y['subtitle'].startswith('Localidad '):
                y['subtitle'] = 'Localidad ' + str(y['loc'])

# Actualiza las localidades de inicio de los objetos en función de las localidades "contenedor" añadidas.

for y in listObjects:
        y['loc']=y['loc']+len(listContainers)

# Actualiza la localidad de inicio de acuerdo a la cantidad de localidades "falsas" añadidas para contenedores.

startRoom=startRoom+len(listContainers)

# 1.0.2b3 Utiliza las claves 'obj_id' y 'parent' para reubicar los objetos contenidos en sus respectivos contenedores

for y in listObjects:
        if y['parent'] > 2999:
                for x, z in enumerate(listObjects):
                        if z['obj_id'] == y['parent']:
                                y['loc']=x

if verbosity:
        if english:
                print ('Creating connectors list.')
        else:
                print ('Creando lista de conexiones.')          
                
listConnectors=[]

for y in data['elements']:
        if y['type']=='Connector':
                if y['dockStart']!=0 and y['dockEnd']!=0:
                        listConnectors.append(y)
                        
if listConnectors==[]:
        if english:
                print('WARNING: No valid connectors.')
        else:
                print('ATENCIÓN: No hay conectores válidos.')

for y in listRooms:
        a=[]
        for x in listConnectors:
                if y['id']==x['dockStart']:
                        if x['startType']==0:
                                a1=dirTransform(x['startDir'])
                        else:
                                a1=dirTransform2(x['startType'])
                        b1=id2loc(x['dockEnd'])
                        a.append(a1 + ' ' + b1)
                if y['id']==x['dockEnd'] and x['oneWay']==False:
                        if x['endType']==0:
                                a1=dirTransform(x['endDir'])
                        else:
                                a1=dirTransform2(x['endType'])
                        b1=id2loc(x['dockStart'])
                        a.append(a1 + ' ' + b1)
        y['con']=a

if idobj:
        listObjectIdentifiers=createObjectIdentifiers()
        
if idloc:
        listLocationIdentifiers=createLocationIdentifiers()

if dsf:
        a='latin1'
else:
        a='850'

with open(out_file, 'w', encoding=a, newline='\r\n') as f:
        imprimeTodo()

if english:
        print('File ' + out_file + ' created.')
else:
        print('Fichero ' + out_file + ' creado.')
print()

#listAll()