# Triz2DAAD

English instructions below!

Triz2DAAD versión 1.0.4b22 251118 (c) 2019-25 Pedro Fernández

Triz2DAAD es la fusión de los anteriores scripts de Python Triz2sce y Trizio2sce, que cargaban, en cada caso, ficheros procedentes de las utilidades Trizbort y Trizbort.io respectivamente. Este nuevo script carga indistintamente de una o de otra y realiza internamente la conversión necesaria para que un sólo script se puedan manejar ambos formatos.

Triz2DAAD.py es un script de Python 3.x que transforma un fichero generado con la utilidad de escritorio Trizbort (a partir de la versión 1.7.0) o su variante on-line Trizbort.io para mapear aventuras en un código fuente compatible con el compilador del DAAD. No es un diseñador visual de aventuras ni una aplicación para su desarrollo completo. Está concebido como herramienta para hacer prototipos iniciales de aventuras con rapidez y facilidad y, a su vez, como herramienta de apoyo a autores nóveles, ideal para su uso en talleres de aprendizaje.

## Uso:

Usar "Python triz2DAAD.py -h" en una línea de comandos o powershell para ver las opciones.

El script requiere como argumentos un fichero de entrada (que debe ser un mapa generado por la utilidad Trizbort en formato XML, aunque con la extensión .trizbort,  o por Trizbort.io en formato json) y, opcionalmente, el nombre de un fichero de salida, que será un código fuente en formato .SCE compatible con la versión 2.40-2.42 del compilador del DAAD. Si no se especifica se creará un fichero con el mismo nombre y la extensión .SCE

- La opción -p1 generará un listado SCE con los mensajes del sistema en primera persona. Por defecto éstos se crearán en segunda persona.
- La opción -e generará un listado SCE con los textos y el vocabulario en inglés. Por defecto se crearán en español.
- La opción -md añadirá código (de compilación condicional) para el modo "dibujo invisible" en los Amstrad CPC.
- La opción -dsf generará un fichero DSF compatible con el nuevo compilador DAAD Reborn Compiler.
- La opción -sl añadirá una barra de estado al código fuente resultante (gastando mensajes adicionales).
- La opción -idobj creará automáticamente identificadores para los objetos mediante directivas #define.
- La opción -idloc creará automáticamente identificadores para las localidades mediante directivas #define.
- La opción -lobj hará que en vez de únicamente el objeto 0, todos los objetos marcados en su nombre con [l] sean fuentes de luz.
- La opción -blockall bloqueará las acciones "TODO" en la plantilla resultante.
- La opción -dr activa los modos -dsf, -idobj e -idloc y creará una plantilla compatible con DAAD Ready A
- La opción -ink establecerá el color de tinta en 16 bits (por defecto 1).

## Enlaces:

- Trizbort:

 - http://trizbort.com

- Trizbort.io:

 - http://trizbort.io/

- DAAD

 - https://web.archive.org/web/20230303170645/http://wiki.caad.es/DAAD
 - http://www.rockersuke.com/if/ebbp/
 - https://github.com/daad-adventure-writer/daad

Hasta el momento parece convertir correctamente:

- Habitaciones, incluyendo sus descripciones y estableciendo la localidad de comienzo.
- Conexiones comunes por puntos cardinales (N,S,E,O,NE,NO,SE,SO).
- Conexiones up/down o in/out.
- Conexiones de una sola dirección.
- Objetos incluidos en las habitaciones.
- Localidades marcadas como "oscuras".

Triz2DAAD añade (con la opción -sl) una barra de estado con el nombre de la localidad actual y el número de turnos transcurridos en la aventura.
También añade un listado automático de salidas y soporte para respuestas por defecto a los comandos "SALIDAS", "MIRAR","EXAMINAR", "AYUDA", "METER", "SACAR" Y "VACIAR". Esto gastará un número variable de mensajes en la sección /MTX y las banderas 100 y 101.

Triz2DAAD usa los textos del cuadro de diálogo "map settings" como pantalla de presentación y créditos (añadiendo frases por defecto en caso de que estuviesen vacíos). Creará un texto por defecto de introducción a la aventura editable en el mensaje nº 14 que en el caso del Trizbort original se corresponderá con el campo "History" (inexistente en Trizbort.io).

A su vez usará el campo "subtitle" de cada localidad como texto para su descripción corta en la barra de estado (máximo 26 caracteres). Si no lo hubiera usará el campo "name" y si éste fuera el elegido por defecto ("Room" o "Cave") lo cambiará por "Localidad xx". A su vez usará el campo "description" para la descripción larga de la localidad en la ventana de texto de la aventura (usando de nuevo un texto por defecto "Descripción localidad xx" si no encontrase ninguno).

Igualmente, triz2DAAD usará el campo "Name" de los objetos como su palabra en el vocabulario. El campo "Description" se usará en los listados de objetos.

- Para Trizbort.io se recomienda usar el mismo nombre con el artículo indeterminado apropiado según género y número para su óptimo procesamiento por el motor del DAAD. Ej: "Libro" -> "Un libro", "Gafas" -> "Unas gafas".
- En el caso de partir del Trizbrt de escritorio se reconocerán los atributos [f] y [2] en el campo "name" como indicadores de "femenino" y "plural" respectivamente (entendiéndose por defecto que el objeto tiene un nombre masculino y singular si no se indica nada) y se añadirá el artículo indeterminado (un, unos, una, unas) correspondiente al texto de los listados.

Siguiendo las convenciones del Trizbort original, Triz2DAAD buscará las cadenas [w] y [c] en el nombre de los objetos para añadirles los atributos ropa y contenedor (tanto en la aplicación de escritorio como en la de web).

Triz2DAAD creará sentencias #define en la sección de definiciones para facilitar determinar los colores de tinta, papel y la posición de la ventana de texto según la plataforma de destino (desactivado en modo DAAD Ready).

**NUEVO**: Si se usa la opción -idobj, Triz2DAAD creará automáticamente sentencias #define en la sección de definiciones para usar como identificadores de los objetos del juego. Se crearán siguiendo el convencionalismo arbitrario de usar la palabra de vocabulario que el objeto tenga como nombre (1ª letra en mayúsculas) antepuesta con el prefijo "o". Si hay 2 o más objetos con el mismo nombre se le unirá como sufijo un número distintivo (el orden de numeración es imposible de determinar).

Ej:

- "llave" -> oLlave, "gafas" -> oGafas
- "llave" -> oLlave1, oLlave2, etc...

**NUEVO**: Si se usa la opción -idloc, Triz2DAAD creará automáticamente sentencias #define en la sección de definiciones para usar como identificadores de las localidades del juego. Se crearán siguiendo el convencionalismo arbitrario de usar el campo "name" de la localidad (1ª letra en mayúsculas) antepuesto con el prefijo "l". Si hay 2 o más localidades con el mismo nombre se le unirá como sufijo un número distintivo (el orden de numeración es imposible de determinar). Su el campo "name" incluyese espacios en blanco se sustituirían por "_". Es necesario tener en cuenta que en modo SCE los identificadores tienen un máximo de 20 caracteres.

**NUEVO**: Si se usa la opción -lobj en lugar de usar como fuente de luz únicamente el objeto 0, se usará cualquier objeto marcado en su nombre con [l].

**NUEVO**: La opción -blockall bloquea las acciones "TODO" con una entrada al principio de PRO5 que las descarta automáticamente.

**NUEVO**: la opción -dr creará una plantilla compatible con DAAD Ready A. En este modo la barra de estado y la opción -md quedan desactivadas. Quedan activados por defecto los modos -dsf, -idobj e -idloc.

Y por el momento triz2DAAD no puede manejarse con:

- Textos personalizados en los extremos de las conexiones.
- Conexiones con puntos intermedios en los espacios del mapa. Cualquier cosa que no sea una conexión directa entre una habitación y otra la ignorará.

## Bugs conocidos:

- Debido al comportamiento ligeramente distinto del intérprete inglés, intentar meter un objeto contenedor dentro de sí mismo (o de un objeto inexistente) en una obra inglesa, en lugar de un mensaje de error hace que el jugador deje el objeto en la localidad actual.

- Debido a que los condactos para meter y/o sacar objetos de contenedores usan un único mensaje del sistema, es probable que haya disonancias con el número (singular/plural) del objeto.

## HISTORIA

-**1.0.4b22** 251118

  - Impide la acción EXAMINAR en la oscuridad.

- **1.0.4b21** 251114

  - Añadida forma imperativa al verbo MIRAR en el VOC español.
  - Se impide la línea en blanco en el listado de objetos cuando no hay objetos mediante HASNAT 55 y BACKAT en el proceso 3.
  - Nueva forma de diferenciar MIRAR OBJETO de REDESCRIBIR en el proceso 1 en lugar del 5.

- **1.0.4b20** 251020 

  - Adaptado a DAAD Ready A      

- **1.0.4b19** 250825

  - Arreglado bug al exportar a DAADReady en inglés: errata en imprimeMTX_ENG_DSF(), daadRaedy en vez de daadReady.

- **1.0.4b18** 240619

  - Avisa cuando un conector de trizbort.io no es válido.

- **1.0.4b17** 240402

  - Adapatado a Daad Ready 0.9.3

- **1.0.4b16** 240103

  - Adapatado a Daad Ready 0.9.2

- **1.0.4b15** 231031

  - Cambios menores para mantenerse al día con DAAD Ready 0.9.1

- **1.0.4b14** 230804

  - El comentario en la sección MTX sobre los mensajes de salidas menciona al proceso adecuado (que puede ser 7 o 10).
  - Corrije fallo de la plantilla de DAAD-Ready 0.8.1 que hace que el mensaje de ANYKEY del proceso 6 salga por la ventana 0.

- **1.0.4b13** 230723

  - Adaptado a DAAD Ready 0.8.

- **1.0.4b12** 230406
 
  - Ignora líneas de conexión no válidas (que no tengan inicio y final en localidades).

- **1.0.4b11** 230224

  - La descripción por defecto de las localidades incluye su nº y, si estuviera definido, su nombre.
  - Retiradas las restricciones para el intérprete de MSX2.

- **1.0.4b10** 230212
 
  - La opción -dr activa automáticamente -idobj e -idloc
  - Usa idloc en PRO 5 y 6.
  - Actualiza la numeración de localidades en la descripción por defecto si se usan contenedores.
  - La oscuridad impide la acción "salidas".

- **1.0.4b9** 230109

  - Adaptado a DAAD-Ready 0.7
  - Corregido: la sección /CTL se muestra correctamente en modos -dsf y -dr

- **1.0.4b7** 220608

  - Adaptado a DAAD-Ready 0.6.1

- **1.0.4b6** 220514

  - Adaptado a DAAD-Ready 0.6

- **1.0.4b5** 220114

  - Nueva opción -ink para establecer el valor por defecto de la tinta en 16 bits.

- **1.0.4b4** 211102

  - No procesa los atributos [m] y [1] de los objetos, pero los retira del nombre si estuvieran presentes (por si alguien los usase por inercia de triz2sce)

- **1.0.4b3** 210512

  - Resuelto problema con los contenedores recursivos en el nuevo formato json de Trizbort.io.

- **1.0.4b2** 210422

  - Adaptado a DAAD Ready 0.4

- **1.0.4b1** 210420

  - Arreglados varios bugs referentes a los identificadores de banderas en modo -DSF.

- **1.0.3** 210416

  - Adaptado al nuevo formato de json de Trizbort.io. En toería el antiguo debería seguir funcionando también. 

- **1.0.3b9** 210415

  - Adaptado a DAAD Ready 0.3

- **1.0.3b8** 201218

  - Mejor organización del PRO 0 en modo DAAD Ready.

- **1.0.3b7** 201209

  - Arreglado: elimina retornos de línea de textos de LTX en modo DSF y los sustituye por #n.
  - Opción para crear plantillas compatibles con DAAD Ready 0.2

- **1.0.3b6** 200327

  - Eliminado el bloqueo de DOALL en MSX2 para probar nueva versión de MSX2DAAD.
  - Añadida opción -blockall para bloquear acciones "TODO".

- **1.0.3b3** 200322

  - Añadida opción para crear automáticamente identificadores de las localidades con directivas #define.

- **1.0.3b2** 200314

  - Arreglado: el script se colgaba si quitabas todos los objetos en un mapa de Trizbort de escritorio.
  - Añadida opción para crear automáticamente identificadores de los objetos con directivas #define.
  - Añadida opción para usar cualquier objeto marcado con [l] como fuente de luz.

- **1.0.3b1** 200305

  - En modo DSF la sección de definiciones ofrece opciónes para los colores de los modos 10 y 12 de MSX2.

- **1.0.2** 200222

  - Arreglado: especificar un fichero de salida colgaba el programa.
  - Bloqueados el reposicionamiento de la ventana de texto y las acciones "TODO" en MSX2 para una mejor compatibilidad con msx2daad.
  - Ahora la barra de estado es enteramente opcional.
  - Añadidas clausulas #define en la sección SYMBOLS para establecer los colores de texto y papel en cada plataforma, así como la fila de la ventana de texto y de la barra de estado.
  - Arreglado: Los condactos WHATO en las entradas de EXAMINAR y VACIAR podían enviar el valor 255 al condacto PRESENT [51] con resultados que parecían consistentes pero resultaron ser impredecibles.
  - Reinicia todas las banderas (menos GFlags) a 0, incluida la 255 (que se quedaba a 255 en la plantilla original).
  - Soporte para objetos contenidos dentro de otros según mapas de trizbort.io
  - Arreglado: dejaba el título en blanco si no se especificaba en map-settings de Trizbort de escritorio.
  - Arreglado: al importar ficheros XML del trizbort de escritorio ignoraba el campo 'history' de map-settings.
  - Permite objetos con el mismo nombre (avisando y evitando repetirlo en el vocabulario)

- **1.0.1** 190603

  - Actualizado a la nueva marca de inicio de entrada en formato DSF.
  - Arreglado: los mensajes de 1ª y 2ª persona estaban cambiados en modo DSF en inglés.
  - Arreglado: varios mensajes mal formateados en modo DSF en inglés.

- **1.0** 190501

  - Carga ficheros tanto de Trizbort (aplicación de escritorio) como de Trizbort.io (aplicación web).
  - Opción para exportar a formato DSF del DAAD Reborn Compiler.
 

# Triz2DAAD english doc

Triz2DAAD version 1.0.4b22 251118 (c) 2019-25 Pedro Fernández

Triz2DAAD is a Python 3.x script that transforms a file generated with either the on-line text-adventure mapping tool Trizbort.io or the Trizbort desktop application into a source code compatible with the DAAD compiler. It's the fussion of former scripts Triz2SCE and Trizio2SCE, admitting both formats.
It's not meant to be either an adventure visual designer or a complete development tool. It's conceived as a fast and easy text-adventure prototyping tool, and also as a supporting tool for novel authors, specially suitable for learning workshops.

## Usage:

Type "Python triz2DAAD.py -h" in a command line or powershell window to see the options.

The script requires as an argument a file (wwhich must be a map generated with either the Trizbort.io utility in json format or a XML trizbort file generated with the Trizbort desktop application) and, optionally, the name of an output file which will be a SCE formatted source code compatible with version 2.40-2.42 of the DAAD compiler. If it's not specified, a file with the same name and a .SCE extension will be created. 

- Option -p1 will create a SCE listing with first-person system messages. Default is second-person.
- Option -e will create a SCE listing with english texts and vocabulary. Default is spanish.
- Option -md will add some conditional code to support "Invisible string" mode in Amstrad CPC.
- Option -dsf will create a DSF file compatible with the new DAAD Reborn Compiler.
- Option -sl will add a status line to the resulting source code (at the expense of aditional messages).
- Option -idobj will automatically create object identifiers with #define directives.
- Option -idloc will automatically create location identifiers with #define directives.
- Option -lobj will make any object with its name marked with [l] a light source, instead of just object 0.
- Option -blockall will block "ALL" actions in the resulting template.
- Option -dr sets -dsf, -idobj and -idloc modes and will create a DAAD Ready A compatible template.
- Option -ink will set ink colour in 16 bits (default 1).

## Links:

-Trizbort:

 - http://trizbort.com

- Trizbort.io:

 - http://trizbort.io/

- DAAD

 - https://web.archive.org/web/20230303170645/http://wiki.caad.es/DAAD
 - http://www.rockersuke.com/if/ebbp/
 - https://github.com/daad-adventure-writer/daad

So far it seems to convert correctly:

- Rooms, including descriptions and setting the initial location.
- Common cardinal points connections (N,S,E,W,NE,NW,SE,SW).
- Up/down and in/out connections.
- One way connections
- Objects included in locations.
- Locations labelled as "dark".

Triz2DAAD adds (with -sl option) a status line with the current location name and the number of used turns.
It also adds an automatic exits listing and support for default answers to the "EXITS", "LOOK", "EXAMINE", "HELP" AND "EMPTY" commands. This will use a variable amount of messages in the /MTX section and flags 100 and 101.

Triz2DAAD uses the fields in the "map settings" dialogue as an introduction screen and credits (adding default sentences if they were empty). It will create a default adventure introduction text the user can edit at message number 14 (in desktop trizbort it will use the "history" field).

It will also use each location "subtitle" field as a text for its short description at the status line (max. 26 characters). If it wasn't provided it will use the "name" field and if this was the default text ("Room" or "Cave") it will be changed to "Loaction xx". In turn, the "description" field will form the long room description in the adventure text window (again using a default "Location xx description" if there wasn't any).

Equally, Triz2DAAD will use the objects field "name" as its word in the vocabulary. "Description" will be used in the objects listing.

- When importing from Trizbort.io it's highly recommended tu use the same name with an appropriate indefinite article in order to secure an optimized processing by the DAAD engine. Examples: "Book" -> "a book", "trousers" - "some trousers".
- When working from desktop Trizbort [f] (female) and [2] (plural) atributes will be recognized in the name filed (default is male and singular) adding the relevant indefinite articles in the listing texts.

Following original Trizbort standards, Triz2DAAD will search for the [w] and [c] strings inside objects name, giving them wearable and container atributes.

Triz2DAAD will create #define directives in the definitions section to set paper and ink colours as well as the text window position according to different target machines (disabled in DAAD Ready compatible mode).

**NEW**: When using -idobj option, Triz2DAAD will automatically create #define directives in the definitions section to use as game objects identifiers. They'll be cretaed following the arbitary convention of using the vocabulary word the object uses for name capitalized and prefixed with an "o". When 2 or more objects share the same name they will be suffixed with a distinctive number (numbering order is unpredictable).

Examples:

- "key" -> "oKey", "glasses" -> oGlasses
- "key" -> oKey1, oKey2, etc...

**NEW**: When using -idloc option, Triz2DAAD will automatically create #define directives in the definitions section to use as game location identifiers. They'll be cretaed following the arbitary convention of using the location "name" field capitalized and prefixed with an "l". When 2 or more objects share the same name they will be suffixed with a distinctive number (numbering order is unpredictable). If "name" had white spaces they'll be replaced with "_". Be aware that in SCE mode identifiers are limited to 20 characters.

**NEW**: When using -lobj option, any object with its name marked with [l] will be used as lightsource, instead of just object 0.

**NEW**: -blckall option will automaticvally discard "ALL" actions with an antry at the start of PRO5.

**NEW**: -dr option will create a DAAD Ready A compatible template. In this mode status line and -md options are disabled. Modes -dsf, -idobj and -idloc are automatically enabled.

And for the moment Triz2DAAD cannot handle:

- Personalized texts at the connections extremes.
- Connections with intermediate points along the map. Anything other than a direct connection between a room and another will be ignored.

## Known bugs:

- Due to the slighty different behavior of the english interpreter, trying to put a container object inside itself (or into a non-existent object) in an english work, instead of displaying an error message will make player drop the object at current location.

- Number (singular/plural) discordances are to be expected due to the fact that putting in and out condacts use just one system message for both cases.

## HISTORY

-**1.0.4b22** 251118

  - EXAMINE action is not allowed in the dark.

- **1.0.4b21** 251114

  - Added imperative form of LOOK in spanish VOC.
  - Avoided blank line in object listing when there's no object using HASNAT 55 and BACKAT in process 3.
  - New way of discriminating LOOK OBJECT from REDESCRIBE in process 1 instead of 5.

- **1.0.4b20** 261020

  - DAAD Ready A compatible.

- **1.0.4b19** 260825

  - Fixed crash when exporting to DAADReady in english: mispelled daadRaedy instead of daadReady in imprimeMTX_ENG_DSF().

- **1.0.4b18** 240619

  - Warns when an invalid trizbort.io connector is found.

- **1.0.4b17** 240402

  - Daad Ready 0.9.3 compatible.

- **1.0.4b16** 240103

  - Daad Ready 0.9.2 compatible.

- **1.0.4b15** 231031

  - Minor changes to keep up to date with DAAD Ready 0.9.1

-**1.0.4b14** 230804

  - Comment about exit messages at MTX mentions the right process (could be either 7 or 10).
  - Fixed DAAD-Ready template bug that prints the ANYKEY message at process 6 in window 0.

- **1.0.4b13** 230723

  - DAAD-Ready 0.8 compatible.

- **1.0.4b12** 230406

  -Non valid connection lines (those without a dock at locations) are ignored.

- **1.0.4b11** 230224

  - Default location description includes its number and, if defined, its name.
  - Removed MSX2 interpreter restrictions.

- **1.0.4b10** 230212

  -  -dr option automatically sets  -idobj and  -idloc.
  - idloc used in PRO 5 and 6.
  - Updates location numbers in default descriptions when using containers.
  - Darkness avoids the "exits" command.

- **1.0.4b9** 230109

  - DAAD-Ready 0.7 compatible.
  - Fixed: /CTL section shows properly in  -dsf and  -dr modes.

- **1.0.4b7** 220608

  - DAAD-Ready 0.6.1 compatible.

- **1.0.4b6** 220514

  - DAAD-Ready 0.6 compatible.

- **1.0.4b5** 220114

  - Added  -ink option to set default ink value in 16 bits.

- **1.0.4b4** 211102

  - Removes unused [m] and [1] attributes from objects (just in case someone used them from triz2sce days).

- **1.0.4b3** 210512

  - Fixed issue with recursive containers in the new trizbort.io json format.

- **1.0.4b2** 210422

  - Adapted to DAAD Ready 0.4
 
- **1.0.4b1** 210420

  - Fixed some bugs related to flag identifiers in  -DSF mode.

- **1.0.3** 210416

  - Adapted to Trizbort.io new json file format. Theorically older maps should still work.

- **1.0.3b9** 210415

  - Adapted to DAAD Ready 0.3

- **1.0.3b8** 201218

  - Better PRO 0 in DAAD Ready mode.

- **1.0.3b7** 201209

  - Fixed: line feeds are removed from LTX section in mode DSF and are replaced by #n. 
  - Added option to create DAAD Ready 0.2 compatible templates.

- **1.0.3b6** 200327

  - Removed DOALL lock in MSX2 to test latest MSX2DAAD version.
  - Added new  -blockall option to block "ALL" actions. 

- **1.0.3b3** 200322

  - Added option to automatically create identifiers for locations with #define directives.

- **1.0.3b2** 200314

  - Fixed: Script crashed if you deleted all objects in a desktop trizbort map.
  - Added option to automatically create identifiers for objects with #define directives.
  - Added option to make any object marked with [l] a lightsource.

- **1.0.3b1** 200305

  - When using DSF DEF section offers options for colours in MSX2 modes 10 and 12.

- **1.0.2** 200222

  - Fixed: adding a name for the output file crashed the program.
  - Blocked text-window repositioning and "ALL" actions in MSX2 for better compatibility with msx2daad.
  - Now the status line is entirely optional.
  - Added #define statements at SYMBOLS section to set paper and ink colours in every target platform as well as the text window and the status line row.
  - Fixed: WHATO condacts in EXAMINE and EMPTY entries could send a value of 255 to a PRESENT [51] condact with results that seemed consistent but turned out to be unpredictable.
  - All flags (save GFlags) are reset to 0, including 255 (which was kept to 255 in the original template).
  - Fixed: Containers support from 1.0.2b3 crashed in maps without objects.
  - Support for objects inside other objects as established in trizbort.io maps.
  - Fixed: title was left blank if not specified at map-settings in desktop Trizbort.
  - Fixed: Map-settings 'history' field is no longer ignored when importing XML from desktop trizbort.
  - Objects with the same name are now allowed (with a warning and without repeating the name at the VOC section).

- **1.0.1** 190602

  - Updated support for the new ">" mark for new entries in DSF format.
  - FIXED: 2nd and 1st person system messages were swapped in english DSF format.
  - FIXED: bad formatting in several english DSF messages.

- **1.0** 190501

  - Load files from both Trizbort desktop and web applications.
  - Support for DAAD Reborn Compiler DSF format.