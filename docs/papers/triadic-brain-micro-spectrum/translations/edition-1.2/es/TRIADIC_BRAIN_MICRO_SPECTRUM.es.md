# Triadic Brain: de la identidad de bytes al conocimiento revisable

**Nota de traducción:** Traducción asistida por IA de la edición inglesa 1.2. No cuenta con certificación de un traductor humano ni con aprobación de un hablante nativo. Se conservan literalmente las ecuaciones, los diagramas y bloques de código técnicos, los identificadores y los títulos bibliográficos. La mención heredada «no publicado» corresponde a los metadatos del borrador fuente, no al estado actual de esta publicación.

## Un análisis técnico vinculado a las fuentes de las transformaciones de datos, los controles y la indagación distribuida

**Thomas Prislac**  
**Manuscrito de investigación, edición sucesora local 1.2, 3 de noviembre de 2026**  
**Análisis de las fuentes preservado, con una propuesta de evaluación de la reutilización y un objetivo de autonomía; no publicado**

## Resumen

Se examina Triadic Brain como una arquitectura para la indagación atribuible, acotada y revisable. La unidad de análisis no es una partícula cognitiva metafórica, sino la representación más pequeña en la que una operación especificada está bien definida: una cadena de octetos, un intervalo Unicode, un registro de aplicación, una solicitud a un proveedor, una afirmación candidata, una correspondencia relacional, un artefacto de evidencia o un evento de custodia. Una reconstrucción vinculada a las fuentes sigue estas unidades a través de la admisión autenticada, el despacho al modelo autorizado por separado, la captura de respuestas, la fundamentación determinista, la evaluación nativa, la revisión y la presentación. Un caso testigo multibyte exacto distingue los bytes originales de la fuente normalizada, la respuesta extraída y la captura semántica derivada. La reconstrucción revela un límite de importancia: el puente JOINED ordinario de modelo capturado asigna a la incertidumbre no medida el valor conservador de uno, lo que, bajo determinadas condiciones, obliga a su filtro nativo a rechazar incluso una cita exacta con cobertura léxica completa y masa softmax unitaria para un único candidato. La respuesta sigue siendo inspeccionable. Las magnitudes relacionadas con GUFT se distinguen según su productor, dominio, unidades y versión; las transformaciones históricas de evaluación comparativa, las hipótesis de campos sobre grafos y los indicadores sustitutivos estructurales actuales no se reducen a una sola puntuación. Un análisis explícito del núcleo reducido de río muestra por qué el paso de uno que utiliza realmente su invocador exige condiciones de estabilidad dependientes del grafo que el valor predeterminado menor del núcleo no establece. AHA se analiza como una comprobación vinculada a las fuentes de puentes relacionales suministrados, mientras que los mecanismos de enjambre y de gramática compartida se distinguen de la corroboración empírica. La contribución consiste en un análisis auditable de las transformaciones implementadas y de las conexiones de investigación aún sin resolver, junto con un grafo de afirmaciones legible por máquina. Este estudio no ejecuta el producto ni realiza experimentos de inferencia, y no afirma haber demostrado una cualificación en vivo de tres nodos, una utilidad semántica calibrada ni autoridad para actuar de forma autónoma.

**Palabras clave:** procedencia; arquitectura cognitiva; representación; razonamiento analógico; incertidumbre; estabilidad numérica; indagación multiagente; gobernanza de la información.

## 1 Pregunta de investigación y contribución

¿Qué ocurre con una pequeña pieza de datos cuando entra en Triadic Brain, y qué justificación adicional existe cuando el sistema presenta después un resultado útil? Para responder, hay que distinguir tres preguntas: qué representación se transformó, qué procedimiento la consumió realmente y qué inferencia respalda la evidencia resultante. Un resumen criptográfico de una fuente puede establecer una relación de identidad sin establecer la verdad factual. Una analogía válida según un esquema puede preservar una relación sin validar su transferencia a un nuevo dominio. Un candidato revisado puede seguir careciendo de permiso para un uso con consecuencias relevantes.

La proposición de investigación que organiza la arquitectura es que la recepción de entradas, la comparación estructural, la continuidad, el cuestionamiento y la revisión pueden operar sobre un registro tipado común, preservando los significados propios de cada dominio y los desacuerdos. Lo que comparten es una gramática de relaciones entre observaciones, transformaciones, hipótesis, restricciones, residuos y procedencia. No se afirma que una sola coordenada de valor real represente toda la cognición. Esta lectura preserva el vocabulario previsto de corredor, río, trenza y terraza como un programa para organizar la indagación, sin tratar ese vocabulario como evidencia de una ley física universal. [I11, I12, I15]

El artículo se organiza en torno a cuatro contribuciones. En primer lugar, un análisis al nivel de las representaciones identifica los límites reales entre bytes, texto, afirmaciones y artefactos en una ruta de aplicación mantenida. En segundo lugar, un análisis formal distingue la evidencia de identidad componible de las afirmaciones no componibles sobre verdad, independencia y permiso. En tercer lugar, las deducciones específicas de las fuentes revelan un cuello de botella de filtrado conservador, espacios de nombres de coherencia distintos y una condición de estabilidad numérica dependiente del grafo. En cuarto lugar, un programa de investigación explícito describe cómo podrían cualificarse la indagación distribuida, la gramática compartida y la reconstrucción retrospectiva sin elevar la existencia de fuentes a la categoría de capacidad demostrada.

La bibliografía pertinente aporta puntos de comparación, no una validación prestada. W3C PROV-DM proporciona un vocabulario preciso de procedencia para entidades, actividades, agentes y derivaciones. La teoría de correspondencia estructural de Gentner motiva el examen de la organización relacional en lugar de la similitud superficial. La investigación sobre calibración distingue las puntuaciones normalizadas de las probabilidades que se corresponden con la corrección empírica. Ninguno de esos trabajos establece la adecuación de esta arquitectura particular. [PROV](https://www.w3.org/TR/prov-dm/), [Gentner 1983](https://groups.psych.northwestern.edu/gentner/papers/Gentner83.2b.pdf), [Guo et al 2017](https://proceedings.mlr.press/v70/guo17a.html).

## 2 Método y clases de evidencia

### 2.1 Reconstrucción de las fuentes, no un nuevo estudio de ejecución

El análisis utiliza un conjunto cerrado de fuentes seleccionado y conservado de forma privada, identidades de bytes conservadas por separado, informes históricos de cualificación y documentos de investigación conciliados. Una comparación actualizada de las fuentes aceptadas encontró únicamente cambios en la documentación respecto de la instantánea de ejecución previamente mapeada. El inventario seleccionado contiene 163 copias de lectura; 157 coinciden exactamente con sus blobs originales de Git, conservados por separado. Seis copias de lectura obtenidas mediante conectores contienen un LF final adicional; al eliminar exactamente ese byte se obtienen copias de fuente reconstruidas independientes cuyas identidades completas de blob de Git coinciden con los originales fijados. El mapa privado de fuentes conserva las copias de lectura, los comprobantes de reconstrucción y los hashes distintos, en lugar de sustituir una identidad por otra. Estos hechos respaldan una reconstrucción acotada de las fuentes, no una auditoría íntegra y nueva del repositorio ni una atestación del despliegue. [I01]

Para este estudio no se importó ningún módulo del producto, no se ejecutó ninguna prueba del proyecto ni tarea de CI, no se llamó a ningún proveedor y no se utilizó ningún cliente instalado ni par en vivo. Los cálculos sobre el ejemplo sintético de bytes y las deducciones analíticas elementales se distinguen de la ejecución del producto. El ejemplo es deliberadamente incompleto como registro de ejecución: no tiene actor autenticado, perfil de despliegue efectivo, respuesta real de un proveedor, reloj de eventos ni revisión humana completada. Los valores que dependen de esas entradas permanecen simbólicos. [I01, I04]

El vocabulario de evidencia es deliberadamente multidimensional:

| Código | Clase de evidencia | Qué establece | Qué no establece |
|---|---|---|---|
| S | Fuente inspeccionada | Existe una definición, rama o contrato en la fuente identificada | Ejecución, instalación o utilidad |
| C | Ruta de llamadas inspeccionada | Un productor especificado está conectado con un consumidor especificado dentro del conjunto cerrado inspeccionado | Que esa ruta se haya invocado en un despliegue |
| T | Prueba escrita | Existen una comprobación y una población prevista de datos de prueba | Un resultado satisfactorio |
| R | Informe de ejecución conservado | Un informe vinculado a las fuentes registra una ejecución histórica acotada | Una repetición independiente o paridad con las fuentes actuales |
| D | Deducción analítica | Una conclusión se sigue de las ecuaciones y los supuestos declarados de las fuentes | Un resultado observado en producción |
| P | Mecanismo propuesto | Se especifica una interfaz o un experimento previsto | Implementación o adopción |
| H | Hipótesis de investigación | Se especifica una relación conjeturada o un modelo formal; la comprobación empírica aún puede requerir definiciones operativas | Validez empírica |
| U | No disponible o no observado | La evidencia pertinente no se ha establecido aquí | Cero, falsedad o permiso para inventar un valor |

Una afirmación puede tener varios códigos, por ejemplo S+C+D. Una hipótesis empírica lista para ponerse a prueba especifica además sus observables, su alcance y sus posibles criterios de refutación; una definición formal por sí sola no tiene por qué proporcionarlos todavía. La cadena S→C→R→despliegue→utilidad no es una cadena de implicaciones. Una implementación mecánicamente correcta de un estimador deficiente sigue siendo un estimador deficiente. [I01, I11]

### 2.2 Cualificación histórica y revisión independiente

Los informes conservados describen una cualificación anterior de 46 casos y un complemento independiente de tres casos que utilizaba capturas sintéticas de proveedores, incluida la inspección persistente tras la pérdida de la confirmación de recepción o una limpieza incierta. Otro informe describe 59 casos seleccionados sin modelos, distribuidos entre dos fuentes, y especifica que no se trata de una única ejecución nueva de 59 casos. No todos los archivos subyacentes estaban disponibles para su inspección independiente en este estudio. Son informes de clase R con vinculaciones privadas exactas a las fuentes, no evidencia de que se ejecutara el caso testigo actual, se validara la semántica de modelos en vivo o se cualificara un sistema instalado de tres nodos. Las pruebas escritas se registran por separado como T. [I18]

Las citas de fuentes privadas I01–I20 remiten a rutas exactas, intervalos de líneas, identidades de fuentes y alcances de informes en un mapa de revisión separado. Las referencias públicas están enlazadas directamente. Esta separación protege información operativa y de implementación no publicada, pero limita la reproducción pública independiente hasta que exista una publicación autorizada de fuentes y evidencias depuradas de información sensible. Esta limitación no puede subsanarse citando un estándar público como si probara un comportamiento privado. Para la edición predecesora congelada, release 1, cinco líneas de revisión técnica de alcance delimitado cubrieron la fidelidad a las fuentes, las matemáticas, la seguridad y privacidad, las afirmaciones científicas y la consistencia entre las representaciones para máquinas y la prosa. A la revisión inicial le siguieron correcciones y una nueva revisión independiente de las partes afectadas; se cerraron los 31 hallazgos y recomendaciones de esos ámbitos. Esta edición sucesora local preserva ese análisis de las fuentes y añade la sección 14.3, su propuesta de cualificación y dos afirmaciones explicativas legibles por máquina. Los resultados de la revisión de la edición predecesora no se extienden automáticamente a esta incorporación; la edición sucesora dispone de su propio registro de revisión de las partes afectadas. La revisión técnica no implica aceptación por una revista, ejecución del producto, cualificación de un sistema instalado ni reproducción empírica independiente.

## 3 Tipos de representación y la unidad mínima significativa

Sean \(\mathbb B^*\) las cadenas finitas de octetos, \(\mathbb U^*\) las secuencias finitas de valores escalares Unicode, \(\mathcal J_p\) los valores JSON aceptados bajo el perfil \(p\) y \(\mathcal A\) los artefactos de aplicación tipados. Una transformación se modela como una función parcial

\[
f:(x,\kappa,\pi)\rightharpoonup(y,e,z),
\tag{1}
\]

donde \(\kappa\) es el contexto de interpretación, \(\pi\) el contexto de control efectivo, \(e\) la evidencia de la operación y \(z\) un estado. El rechazo, la entrada no disponible y la finalización incierta son estados representados; no se sustituyen silenciosamente por valores de éxito. Este es un modelo expositivo, no una afirmación de que todas las funciones de la implementación tengan literalmente esta signatura.

Un octeto es la unidad direccionada más pequeña en los contratos de bytes presentados. Un punto de código Unicode es la unidad utilizada por las coordenadas de texto. Un token del proveedor es una unidad definida por el tokenizador, cuya correspondencia depende del modelo y de la plantilla. Un tipo de token léxico es una unidad distinta utilizada por el diagnóstico nativo de citas. Un intervalo de afirmación es una propuesta textual acotada; una correspondencia de relaciones es la unidad del caso AHA suministrado. Un evento de custodia es una observación registrada con orden local. Un segmento TCP o un registro TLS pertenece a una capa de transporte, no a estas unidades semánticas. UTF-8 permite que un carácter ocupe varios octetos; TCP proporciona un flujo de bytes en lugar de preservar los límites de los registros de aplicación. [RFC 3629](https://www.rfc-editor.org/rfc/rfc3629.html), [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293.html).

Por tanto, para un artefacto \(a\), el portador semántico mínimo útil depende de la pregunta. Para verificar un extracto se necesita, como mínimo, su texto, la identidad de la fuente, la convención de intervalos y los bytes de la fuente o un registro de verificación suficientemente fiable. Para evaluar una analogía se necesitan relaciones, extremos puestos en correspondencia, restricciones de dominio y una prueba en el dominio de destino. Eliminar esas dependencias puede acortar un mensaje y, al mismo tiempo, hacer que la operación prevista quede indefinida. Las fuentes no respaldan la existencia de un paquete semántico mínimo universal. [I04, I05, I09]

Definamos por separado la identidad de bytes y la identidad de perfil:

\[
H_B(b)=\operatorname{SHA256}(b),\qquad
H_p(x)=H_B(C_p(x)),
\tag{2}
\]

donde \(C_p\) es una codificación canónica con versión explícita. Para un JSON entrante no canónico \(b\), en general \(H_B(b)\ne H_p(\operatorname{parse}(b))\). SHA-256 detecta cambios de bytes respecto de una referencia fiable bajo sus supuestos criptográficos. No autentica al autor original ni valida una proposición contenida en los bytes. [FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final).

Los serializadores canónicos inspeccionados utilizan JSON UTF-8 compacto con claves ordenadas, números finitos y un LF final. Sus dominios aceptados difieren. Uno exige cadenas ya en NFC y rechaza los sustitutos Unicode; el perfil nativo rechaza además determinados controles y caracteres ignorables por defecto, y aplica restricciones a las claves. Algunos puntos de entrada del analizador aceptan los espacios en blanco habituales de JSON, y la igualdad de bytes canónicos se comprueba en límites posteriores. El entero 1 y el valor de coma flotante 1.0 pueden compararse como iguales en un lenguaje anfitrión y, sin embargo, serializarse en bytes diferentes. Estos son perfiles del proyecto, no una afirmación de conformidad con JSON Canonicalization Scheme. RFC 8785 resulta una comparación útil precisamente porque las reglas numéricas y de Unicode forman parte de un contrato de canonicalización. [I02, I05]. [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html).

## 4 La ruta mantenida y sus límites de autoridad

La figura 1 presenta la ruta JOINED ordinaria de modelo capturado que se inspeccionó. Los bloques son responsables lógicos o etapas de artefactos, no máquinas físicas fijas ni una afirmación de que cada uno sea un modelo independiente.

```text
Untrusted source + user task + explicit consent
                 |
          application intake
                 |
       authenticated gateway -------- technical rejection
                 |
       durable attempt and admission
          |              |
      AEGIS/UCC       frozen bindings
                 |
        exact dispatch authorization
                 |
        transactional claim and reservation
                 |
      provider adapter and bounded transport
                 |
      body capture + completion observations
                 |
      provider-specific text normalization
          |                    |
   CAPTURE_ONLY return     CAPTURED + JOINED
                               |
                    deterministic semantic bridge
                               |
                grounding / claims / UCM / AHA
                waveform / counterexamples / aperture
                               |
                    separately claimed Sophia audit
                               |
                   Atlas orientation and TEL closure
                               |
                     sealed inspectable artifacts
                               |
                separate human decision and permitted use
```

**Figura 1.** Reconstrucción estática de la ruta de llamadas. Los eventos sin modelo utilizan una ruta separada de admisión/finalización sin candidato de modelo. Las observaciones terminales del proveedor distintas de CAPTURED no se convierten por implicación en candidatos nativos. Ni el diagrama ni una etiqueta de artefacto otorgan autoridad para una acción posterior. [I03–I10]

La recepción combina una fuente acotada, una tarea, evidencia suministrada y consentimiento explícito, escribe los bytes exactos de la tarea antes del envío y puede vincular pares completos seleccionados de conversaciones anteriores. La ruta de reutilización contextual inspeccionada limita los mensajes anteriores a 16 y el contexto canónico a 16,000 bytes; rechaza el exceso en lugar de truncarlo silenciosamente. Se trata de una selección explícita, no de una prueba de recuperación general de memoria. La pasarela impone un límite de 32,768 bytes al cuerpo de la tarea y deriva el actor del contexto autenticado de la aplicación. El texto fuente no puede autorizarse a sí mismo alegando un rol de confianza. [I03]

La pasarela reenvía a custodia los bytes de la tarea codificados en base64. Para \(n\) bytes de entrada, la longitud de base64 con relleno es de \(4\lceil n/3\rceil\) caracteres. Es una codificación reversible, con sobrecarga, no cifrado ni compresión semántica. Custodia registra un intento antes de la admisión, incluidos los bytes enviados acotados y su identidad. La idempotencia del registro vincula el actor y la clave a la semántica exacta de la carga útil sin procesar: la reutilización con bytes modificados genera un conflicto. Los intentos rechazados e inciertos siguen formando parte de la población observada. [I03]

La admisión fija un perfil de control efectivo y un contexto de ejecución, valida la autorización de tarea/privacidad/proveedor, construye una fundamentación normalizada e invoca AEGIS. Los modos heredados que no son de observación también ejecutan el plan de admisión UCC; el perfil de observación inspeccionado conserva ese plan de compatibilidad únicamente como definición y realiza posteriormente una evaluación empresarial consultiva separada, mientras que siguen aplicándose los límites técnicos de entrada, rol, privacidad, capacidad y despacho. Por tanto, «controlado» no significa que todas las políticas nombradas sean un veto ejecutable en todos los modos. Aquí, la comprobación de privacidad de la aplicación verifica el consentimiento explícito para la tarea y la concordancia con el identificador de política configurado. La compuerta nativa de privacidad conserva esa base declarada y comprueba su contrato booleano/de base; no clasifica por su cuenta el contenido sensible ni establece la adecuación de la política para toda persona o destinatario afectado. Un análisis sintáctico satisfactorio no convierte en autoridad las instrucciones de una fuente no fiable. [I03]

El despacho requiere el registro exacto en cola, la versión y el hash de la solicitud. La toma transaccional vuelve a comprobar los límites y las vinculaciones pertinentes, construye el cuerpo de la solicitud al proveedor y reserva la contabilización antes de la invocación. Una reserva no demuestra ni la finalización remota ni un cargo. Las solicitudes en curso tras un reinicio pasan a UNKNOWN en lugar de repetirse a ciegas. La justificación de ingeniería se asemeja al mínimo privilegio y la mediación completa, pero la presencia de esos principios de diseño no constituye una certificación de seguridad. [I06]. [Saltzer and Schroeder 1975](https://web.mit.edu/Saltzer/www/publications/protection/Basic.html).

## 5 Un caso testigo multibyte exacto

### 5.1 Bytes y coordenadas

Tomemos la fuente ilustrativa ` Café.\r\n` y la tarea `Quote the source.`. La fuente contiene un U+0020 inicial, el carácter U+00E9 ya en NFC y CRLF. Estipulemos, sin llamar a ningún modelo, que el texto extraído de la respuesta es `Café.`. El normalizador del puente de la aplicación es

\[
N(s)=\operatorname{NFC}\!\left(\operatorname{CRtoLF}
 (\operatorname{CRLFtoLF}(s))\right).\operatorname{strip}()+\mathrm{LF}.
\tag{3}
\]

NFC se refiere a la equivalencia canónica de Unicode; la sustitución de saltos de línea y la eliminación de espacios en los extremos son operaciones adicionales de la aplicación. No deben atribuirse al estándar de normalización Unicode. La fundamentación nativa directa tiene otro contrato: convierte los saltos de línea y elimina espacios en los extremos, pero exige una entrada ya en NFC en lugar de aplicar NFC silenciosamente. La recepción canónica inicial también puede rechazar entradas que no estén en NFC antes del puente posterior. Este caso testigo ya está en NFC y no demuestra que se acepte cualquier grafía descompuesta. [I02, I04, I05]. [Unicode UAX 15 revision 57](https://www.unicode.org/reports/tr15/tr15-57.html).

| Representación | Hexadecimal UTF-8 | Puntos de código | Bytes | SHA-256 |
|---|---|---:|---:|---|
| Fuente original | `20436166c3a92e0d0a` | 8 | 9 | `4068c2d9de08c36023e33a7858bf0d9e36bfa39017edd2af2d1927ed413e2498` |
| Fuente normalizada | `436166c3a92e0a` | 6 | 7 | `ead8f00c3b7dd22fe4ea6e1679b51bbbe2696e72b0692a278bf100aae0928b9d` |
| Respuesta extraída | `436166c3a92e` | 5 | 6 | `7d84df6634452499da807a641b387dbcb28193ef940a6fb297ac86c652d5ca75` |

Estas son identidades calculadas de bytes sintéticos, no evidencia capturada de inferencia. U+00E9 ocupa dos bytes UTF-8. El intervalo de la respuesta es [0,5) en puntos de código y [0,6) en bytes UTF-8. Son coordenadas semiabiertas con base cero en la fuente normalizada, no coordenadas de grupos de grafemas, UTF-16, tokenizador o archivo original. [I04]

En esta ruta, el constructor nativo de fundamentación recibe los siete bytes ya normalizados. En consecuencia, sus hashes de fuente y fuente normalizada coinciden, mientras que la identidad original de nueve bytes permanece en la vinculación de admisión separada. Un invocador de nivel inferior que pasara directamente los bytes originales produciría una identidad de fuente nativa diferente. Un artículo que denomine a todas ellas «la fuente sin procesar» pierde la distinción que pretende explicar. [I04, I05]

La ecuación (3) es una función de muchos a uno. Por ejemplo, desaparecen las distinciones de espacios en blanco en los extremos. Por tanto, no existe una inversa general \(N^{-1}\). Conservar el hash original registra qué original se admitió solo cuando está disponible la vinculación de custodia fiable; el resumen criptográfico por sí solo no puede reconstruir los bytes descartados. Esto establece un límite concreto de pérdida de información sin afirmar que la operación preserve el significado en lenguajes o formatos sensibles a los espacios en blanco.

### 5.2 Expansión e identidad de artefactos

La fuente breve no constituye toda la entrada del modelo. Una envoltura ilustrativa de fuente/evidencia/tarea tiene 161 bytes UTF-8, y su arreglo JSON canónico de un solo mensaje tiene 200 bytes. Un cuerpo de respuesta fabricado con la estructura de un proveedor, utilizado únicamente para ilustrar la serialización, tiene 91 bytes y una identidad explícita NOT_EXECUTED. De estos tamaños no se infieren recuentos del tokenizador, latencia, identidad del proveedor ni captura de paquetes. La envoltura completa de la solicitud y la configuración del proveedor siguen sin especificarse. [I04]

La fundamentación nativa segmenta el texto normalizado según los límites entre párrafos, con una alternativa basada en líneas para un único párrafo multilínea. No infiere proposiciones mínimas. El caso testigo produce un segmento con el texto `Café.`, desplazamientos independientes de puntos de código y bytes, y el resumen criptográfico del extracto indicado arriba. El JSONL del segmento construido correspondiente tiene 243 bytes, su manifiesto 525 bytes y el JSON de captura semántica derivada 684 bytes. Estos artefactos de mayor tamaño contienen información de coordenadas, identidad y control. Ilustran la sobrecarga de la rendición de cuentas, no una razón de eficiencia medida de extremo a extremo. [I04, I05]

La serialización crea dominios de identidad adicionales. Los bytes de la respuesta sin envoltura tienen longitud seis; el escalar JSON nativo `"Café."` más LF tiene longitud nueve; el objeto `{"text":"Café."}` más LF tiene longitud 18; una grafía de comparación con escapes ASCII tiene longitud 22. Omitir el LF terminal del objeto da 17 bytes y un resumen criptográfico diferente. La igualdad de las cadenas decodificadas no implica igualdad de los artefactos serializados. El caso testigo legible por máquina registra los bytes y hashes exactos de cada comparación. [I04]

## 6 Procesamiento del modelo y lo que la traza no puede ver

### 6.1 Semántica del adaptador y del transporte

Los perfiles de proveedor compatibles definen contratos de texto acotados y sin transmisión incremental. Un adaptador de tipo generate puede serializar el historial etiquetado por roles en una sola cadena de instrucción, mientras que los adaptadores de tipo chat envían arreglos de mensajes y otro perfil utiliza bloques tipados de entrada/salida de texto. La existencia de una envoltura de aplicación común no hace idénticas la tokenización de los proveedores ni sus plantillas de chat. La normalización de la respuesta comprueba la forma de finalización admitida: un texto completo puede pasar a CAPTURED; un rechazo explícito permanece REFUSED; los errores HTTP pasan a FAILED; una salida incompleta, limitada por longitud o no admitida puede pasar a UNKNOWN. Las llamadas a herramientas y las modalidades no admitidas no pueden interpretarse silenciosamente como la respuesta textual compatible. [I06]

El transporte mantenido conserva observaciones del cuerpo de respuesta de la aplicación, no tramas Ethernet, paquetes IP, segmentos TCP, registros TLS ni los bytes completos de las cabeceras HTTP. El entramado HTTP y la protección de registros TLS son capas separadas. Un fragmento entregado por una biblioteca no es ni un paquete de red estable ni un token del modelo. La configuración inspeccionada desactiva HTTP/2, rechaza las redirecciones, ignora los proxies del entorno y solicita la codificación de contenido identity; estos son ajustes de las fuentes, no mediciones de una sesión. La especificación TLS 1.3 de 2018 se cita aquí como referencia de capa, no como una afirmación sobre una conexión negociada particular ni sobre la especificación más reciente. [I06]. [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.html), [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.html).

Para las rutas externas, las fuentes especifican la resolución a direcciones públicas aprobadas, un destino de conexión numérico con Host/SNI oficiales, la verificación TLS, observaciones del par conectado y del resumen criptográfico del certificado, así como límites de solicitud, respuesta, plazo y limpieza. Las rutas locales tienen restricciones de bucle local separadas. Las comprobaciones de eco de secretos conocidos pueden impedir la entrega de un cuerpo, pero no establecen una prevención integral de pérdida de datos. La protección del transporte no oculta los valores de fuente/contexto al punto de cómputo autorizado; §15 distingue esa visibilidad y el alcance de las copias conservadas. Los bytes observados del cuerpo y los bytes del prefijo conservado tienen longitudes y hashes separados, de modo que un prefijo acotado no se etiqueta erróneamente como un cuerpo completo. [I06]

### 6.2 Componentes internos condicionales del modelo

Para un entorno de ejecución basado en transformadores, una descomposición de referencia útil es

\[
u\xrightarrow{\text{format}_t}\tilde u
\xrightarrow{\tau_v}(t_1,\dots,t_n)
\xrightarrow{\text{embedding}}H_0
\xrightarrow{F_{\theta,b}}H_L
\xrightarrow{\text{head/decoding}}(\hat t_1,\dots,\hat t_m)
\xrightarrow{\operatorname{decode}_v}\hat u.
\tag{4}
\]

Aquí, \(v,t,\theta,b\) denotan el tokenizador/versión, el formato/plantilla de entrada, los parámetros y el contexto del backend, no valores observados. El decodificador nombrado no presupone una inversa biyectiva de la tokenización. Un bloque de atención estándar utiliza

\[
\operatorname{Attn}(Q,K,V)
=\operatorname{softmax}(QK^\top/\sqrt{d_k}+M)V.
\tag{5}
\]

En la ecuación (5), \(d_k\) es la dimensión de consulta/clave y M es la máscara aditiva de atención; softmax opera sobre las claves. Las ecuaciones (4)–(5) constituyen contexto arquitectónico. No identifican las capas, la cuantización, las activaciones ocultas, el estado KV ni la aleatoriedad de decodificación del entorno de ejecución real. El trabajo original de Transformer establece esta construcción de atención, no la implementación de ningún despliegue privado. [Vaswani et al 2017](https://arxiv.org/abs/1706.03762v7).

La traza de aplicación inspeccionada no expone la secuencia real de tokens, la expansión de plantilla aplicada, los tensores internos, el error numérico del backend ni las actualizaciones de entrenamiento. Los recuentos de uso informados son afirmaciones del proveedor sujetas a validación contractual. No se observa la identidad de los pesos alojados; una identidad local configurada o de disponibilidad no es una atestación de ejecución. Por tanto, en este análisis la generación del modelo es una transformación causalmente importante, pero internamente opaca. El análisis determinista del puente nativo puede inspeccionarse en etapas posteriores y no debe confundirse con una vista del cómputo latente del modelo. [I06]

### 6.3 La finalización como producto de estados

Utilicemos el producto explicativo de estados

\[
Z=(z_{admit},z_{dispatch},z_{body},z_{norm},z_{eval},
z_{posture},z_{review},z_{use},z_{payload},z_{cleanup}).
\tag{6}
\]

Un cuerpo puede estar completo mientras la limpieza sigue siendo incierta. Puede haberse producido inferencia remota aunque se pierda la confirmación local de captura. La ejecución histórica puede seguir completa después de que expire la carga útil conservada. CAPTURED puede coexistir con REFUSE nativo y HOLD de un revisor. La cancelación registra un intento de intervención, no una prueba de que cesara el cómputo remoto. Las identidades exactas permiten la conciliación en lugar de la suposición insegura de que una solicitud no confirmada nunca se ejecutó. Esta factorización es un modelo analítico de distinciones presentes en las fuentes, no un nuevo esquema unificado de estados de ejecución. [I06, I10, I14]

## 7 Transformaciones nativas desde el texto de respuesta hasta un candidato revisado

### 7.1 Afirmaciones deterministas y vinculación de evidencia

El puente semántico normaliza el texto terminal extraído y divide los intervalos de párrafos o líneas, una vez eliminados los espacios de sus extremos, en afirmaciones. No divide por puntos, con lo que evita algunos errores relacionados con decimales y abreviaturas, pero tampoco afirma extraer proposiciones. Para cada intervalo busca una subcadena exacta en los segmentos de fundamentación. La primera coincidencia exacta produce una referencia SUPPORTS declarada por el candidato; si no hay coincidencia, no se produce ninguna referencia. La operación propone respaldo de cita, no implicación semántica ni selección exhaustiva de fuentes. [I05]

El puente registra tres identidades separadas: el cuerpo del proveedor recibido en la etapa anterior, la envoltura normalizada del proveedor y la captura semántica derivada. La «salida sin procesar» que el adaptador de candidatos capturados entrega a las etapas posteriores es ese JSON semántico derivado. Su cuarentena contiene 684 bytes en este caso testigo, no el cuerpo original del proveedor. El adaptador es una fachada local sin invocación de modelos. Confundir ambos adaptadores implicaría falsamente que una auditoría posterior volvió a leer de manera independiente los bytes de la respuesta en vivo. [I05, I07]

El siguiente contrato de datos es una **proyección ilustrativa**, no una solicitud ejecutable del producto ni el esquema completo literal del candidato:

```json
{
  "representation": "claim_excerpt_projection",
  "evidence_class": "CONSTRUCTED_NOT_EXECUTED",
  "text": "Café.",
  "coordinate_domain": "normalized_source",
  "code_point_interval": [0, 5],
  "utf8_byte_interval": [0, 6],
  "source_sha256": "ead8f00c3b7dd22fe4ea6e1679b51bbbe2696e72b0692a278bf100aae0928b9d",
  "excerpt_sha256": "7d84df6634452499da807a641b387dbcb28193ef940a6fb297ac86c652d5ca75",
  "declared_relation": "SUPPORTS",
  "semantic_entailment_established": false,
  "authority_effect": "NONE"
}
```

La validación de afirmaciones reconstruye la identidad de fuente/segmento, la identidad del extracto, la identidad del texto de la afirmación, la inclusión de intervalos y la concordancia entre bytes y puntos de código; las referencias superpuestas dentro de una afirmación se marcan como no válidas. La categoría de respaldo se deriva de la integridad de la cita y de la relación declarada. Un tokenizador léxico fijo utiliza intervalos Unicode de tipo palabra, plegado de mayúsculas y minúsculas y palabras vacías en inglés. Su cobertura de tipos únicos de tokens es un diagnóstico, no el recuento de tokens del proveedor ni una probabilidad de veracidad factual. En el caso testigo, tanto la afirmación como el extracto se reducen a `{café}`, lo que da una cobertura de uno y ningún tipo de token residual. [I05]

Los identificadores de candidatos utilizan un prefijo de 24 caracteres hexadecimales del SHA-256 de la concatenación ASCII de dos cadenas completas de resúmenes criptográficos hexadecimales. Por tanto, la semilla contiene 128 bytes ASCII, no 64 bytes binarios de resúmenes criptográficos. Ese prefijo es una etiqueta de 96 bits; el resumen criptográfico completo del artefacto sigue siendo la identidad utilizada en las afirmaciones de integridad. De forma similar, las etiquetas de los paquetes de fundamentación utilizan un prefijo de 20 caracteres hexadecimales. Las etiquetas truncadas no deben sustituir silenciosamente a los hashes completos de los artefactos en demostraciones o argumentos sobre colisiones. [I05]

### 7.2 Clasificación UCM y el invariante de incertidumbre conservadora

Sea \(r\) la fracción de afirmaciones no marcadas como carentes de respaldo, y \(u\in[0,1]\) el campo de incertidumbre del candidato. Los ejes estructurales predeterminados son

\[
a=(E_{cpl},T_{tr},E_s,\lambda_{phase},\mu_{contain})
=(r,1,1,1-u,r),\qquad \psi_{CL}=E_{cpl}T_{tr}.
\tag{7}
\]

Estos son indicadores sustitutivos adimensionales definidos en las fuentes. Sus nombres no establecen simetría ética empírica, empatía psicológica ni estabilidad física de fase. Los metadatos suministrados de todos los ejes y las hipótesis declaradas por el invocador son entradas separadas bajo el contrato nativo. [I07]

Para una población no vacía de puntuaciones finitas \(s_i\), particionada según grupos de equivalencia declarados \(g\), UCM calcula

\[
p_i=\frac{\exp(s_i-s_{max})}{\sum_j\exp(s_j-s_{max})},\quad
P_g=\sum_{i\in g}p_i,\quad
m=P_{(1)}-P_{(2)}.
\tag{8}
\]

Las masas de los grupos se ordenan de forma descendente, y \(P_{(2)}=0\) cuando existe un solo grupo. La población completa determina el resultado; top-k afecta únicamente a la presentación, y se registran la masa mostrada retenida y la omitida. El código denomina a \(p_i\) probabilidades posteriores, pero las puntuaciones de entrada son logits declarados por el invocador, no logaritmos de verosimilitud medidos. Un único candidato recibe necesariamente masa uno, aunque esa única alternativa sea incorrecta. La normalización no es calibración, distinción también fundamental en la investigación empírica sobre calibración. [I07]. [Guo et al 2017](https://proceedings.mlr.press/v70/guo17a.html).

La precedencia implementada es no compensatoria. Se aplica REFUSE si faltan referencias de fuentes autenticadas, la transparencia es inferior a .20, la incertidumbre es al menos .85, quedan afirmaciones sin respaldo o alguna hipótesis suministrada está fuera de distribución. En caso contrario, se aplica HOLD cuando \(\psi_{CL}<.45\), el indicador sustitutivo de simetría ética es inferior a .50, la incertidumbre supera .40, el margen de equivalencia es inferior a .10 o la postura del patrón es nueva/ambigua. Los casos restantes producen PASS_SCREEN, con revisión humana obligatoria y autoridad NONE. Estos umbrales son hechos de las fuentes, no fronteras de decisión científicas validadas. [I07]

**Invariante condicional.** Toda invocación satisfactoria del constructor JOINED ordinario de modelo capturado inspeccionado fija \(u=1.0\), explícitamente como máximo conservador no medido. Si a continuación se alcanzan el constructor y el filtro UCM nativos sin cambios y con artefactos válidos, \(u\ge.85\), de modo que se sigue REFUSE independientemente de los demás ejes o logits. En el caso testigo, \(r=1\), \(a=(1,1,1,0,1)\), \(\psi_{CL}=1\), \(p_1=1\) y \(m=1\); aun así, la compuerta de incertidumbre rechaza. Esta es evidencia S+C+D sobre esta ruta, no una tasa de error observada ni una afirmación global sobre todas las respuestas. [I07]

CAPTURE_ONLY no ejecuta esta rama nativa. Los eventos sin modelo no tienen candidato de modelo. Una API de captura de nivel inferior puede recibir otro valor de incertidumbre válido según el esquema, bajo un contrato diferente. Ninguno de esos hechos justifica inventar una incertidumbre menor para que la ruta ordinaria supere el filtro. Un estimador alternativo necesitaría su propia definición, población de calibración, gestión de fallos e integración posterior cualificada. El comportamiento conservador actual preserva la inspección, pero declina elevar el estatus epistémico.

### 7.3 Forma de onda sintética y búsqueda acotada de contraejemplos

La forma de onda de referencia actual codifica los cinco ejes ordenados como

\[
x_j=\operatorname{round}_{12}\!\left[
\frac15\sum_{k=1}^5a_k\sin(2\pi kj/N)\right],\quad
E_{codec}=\operatorname{round}_{12}\left[N^{-1}\sum_jx_j^2\right].
\tag{9}
\]

El dominio de muestreo es el entero \(N\in[16,4096]\), con \(j=0,\ldots,N-1\) y valor predeterminado \(N=64\). La fase se expresa en ciclos por registro sintético, no en tiempo en segundos. Antes del redondeo, la ortogonalidad discreta da \(E_{codec}=\sum_k a_k^2/50\) para esos números de muestras, de ahí .08 para el caso testigo. Esta deducción no es una ejecución medida de la forma de onda. Vectores de ejes diferentes pueden tener la misma energía, de modo que la energía por sí sola pierde información sobre su distribución. No se mide ninguna frecuencia física de una persona, modelo o arquetipo, y explícitamente no se ha establecido la utilidad entre dominios. [I08]

La etapa de contraejemplos enumera las afirmaciones sin respaldo y busca en los tokens léxicos de los segmentos de fuente un conjunto finito de marcadores de limitación. El caso testigo no produce coincidencias. Ese cero significa que no se detectó ninguna coincidencia mediante este método acotado; no es una refutación exhaustiva, un debate adversarial entre modelos ni una prueba de que la proposición carezca de contraejemplos. [I08]

### 7.4 Revisión Aperture y salida útil

Aperture evalúa compuertas estrictas para el consentimiento de la tarea, el predicado de política de privacidad transmitido, el consentimiento opcional de retención PMR, la fundamentación, el contexto, la cuarentena, la evidencia de afirmaciones, el no rechazo de UCM y el no rechazo de AHA. El fallo de una compuerta estricta produce REFUSE antes de considerar las retenciones menos estrictas. Con entradas del caso testigo válidas en los demás aspectos, falla únicamente la compuerta UCM. La ausencia de AHA se conserva por separado, pero no sustituye el motivo de la compuerta estricta. PMR está desactivado en esta ruta ordinaria, mientras que la custodia de evidencia obligatoria sigue activa. Por tanto, «sin escritura PMR» no puede significar «no se almacenó contenido». [I08]

Sophia vuelve a calcular por separado determinadas relaciones entre artefactos, incluidos los intervalos, el mapa de afirmaciones, la proyección completa de UCM, los residuos, la forma de onda, AHA, los contraejemplos, Aperture y TEL. Utiliza una tolerancia numérica local de \(10^{-12}\) donde se especifica; la igualdad de hashes de bytes es otra condición. Lee comprobantes de verificación sin datos en bruto en lugar de bytes de cuarentena, e informa explícitamente de que no verificó por su cuenta esos bytes ausentes. No vuelve a ejecutar los predicados de políticas UCC. [I10]

Para el caso testigo condicionalmente válido, el rechazo UCM/Aperture correctamente registrado y la indisponibilidad de AHA producen HOLD en Sophia, no necesariamente REJECT. Los artefactos malformados o inconsistentes pueden producir rechazo. Atlas asigna este HOLD a quarantine/do_not_publish, con la decisión humana pendiente. Una auditoría PASS seguiría exigiendo revisión humana. La salida presentada puede mostrar la cita exacta, la evidencia, las condiciones sin resolver y la procedencia sin atribuir autoridad a la cita. Una devolución para aclaración es REQUESTED_NOT_EXECUTED; no prueba que se haya ejecutado un bucle de reparación automático. [I10]

El sellado sigue a la auditoría, la orientación y la finalización de TEL. Inventaría los bytes y hashes exactos de las cargas útiles y vincula los artefactos devueltos. No es una firma, inmutabilidad frente a privilegios del anfitrión ni certificación semántica. La exportación opcional a un archivo es otra representación con su propia identidad de bytes y sus propios supuestos sobre el compresor. El producto útil de este ejemplo es una explicación inspeccionable de por qué se retuvo una cita aparentemente perfecta. Ese es un resultado sustantivo, aunque no sea una respuesta final aprobada. [I10]

## 8 GUFT como gramática comparativa tipada

### 8.1 Preservar los espacios de nombres en lugar de seleccionar un escalar universal

Se conserva GUFT como término del proyecto. Este artículo no infiere un nuevo desarrollo de la sigla ni afirma que las magnitudes con nombres similares compartan un estimador. El registro apropiado para una magnitud es

\[
q=(\text{namespace},\text{formula version},\text{domain},\text{inputs},
\text{units},\text{producer},\text{consumer},\text{missingness},
\text{clipping},\text{evidence class}).
\tag{10}
\]

La ecuación (10) es un contrato de exposición. No se afirma que sea un esquema universal de ejecución ya aplicado en todas partes. Impide que una transformación de un benchmark, un indicador indirecto de cobertura de fuentes, una proporción de inversiones de signo en una serie temporal y una magnitud de sincronización de fase se vuelvan silenciosamente intercambiables por el mero hecho de llamarse E, T, Ψ o Λ. [I11]

El producto local acotado \(\Psi_{local}=ET\), bajo \(E,T\in[0,1]\), satisface \(0\le ET\le E\le1\). Este teorema elemental es válido para los operandos declarados. El código fuente de Lean conservado contiene los términos de demostración correspondientes, pero este estudio no los compiló ni auditó sus importaciones. Ninguna demostración algebraica puede establecer que un productor no calibrado mida transparencia o empatía. Una expresión exploratoria distinta de estabilidad es

\[
\Psi_{stability}=\frac{ET E_s\Lambda_{lock}}
 {\Delta S+D+\varepsilon}.
\tag{11}
\]

No tiene por qué pertenecer a [0,1], y \(\varepsilon>0\) no garantiza un denominador positivo si otros términos pueden tener signo negativo. \(\Lambda_{lock}\) no es la Λ de deriva máxima de la telemetría. No se ha recuperado la ecuación definitoria completa de un objeto denominado por separado Formula-of-Record en los fragmentos de código fuente comprendidos en el alcance; aquí no se reconstruye ninguna fórmula a partir de su etiqueta. [I11]

### 8.2 Telemetría histórica real de benchmarks

Uno de los estimadores conservados lee valores numéricos de archivos CSV de benchmarks, toma valores absolutos dentro de un prefijo acotado, filtra entradas grandes con apariencia de enteros conforme a una regla de respaldo y calcula

\[
p=\operatorname{mean}_{k\le4000}\log(1+|x_k|),\qquad
E=\operatorname{clip}_{01}(e^{-p/80}).
\tag{12}
\]

Los comentarios del código fuente indican que se eligió el divisor 80 para mantener E suficientemente alto para los controles de Ψ; se trata de una decisión de escala del diseño, no de una calibración semántica empírica. Su valor predeterminado cuando faltan números es \(E=1,p=0,count=0\). T procede de la cobertura de auditoría con valores de respaldo favorables; \(E_s\) procede de la finalización de secciones con otros valores de respaldo. Para la línea de base \(v_0=(E,T,\Psi,E_s)\) y las ejecuciones repetidas \(v_i\),

\[
d_i=\tfrac14\|v_i-v_0\|_1,\quad
\Delta S=m^{-1}\sum_i d_i,\quad
\Lambda=\max_i d_i,
\tag{13}
\]

ambas salidas son cero cuando no existen ejecuciones repetidas. La envoltura repite la carga de trabajo sin cambiar explícitamente la semilla de perturbación. El consumidor orientado a texto que se inspeccionó no utiliza el texto para construir la medición del benchmark. Son valores de benchmark/auditoría asociados a una trayectoria, no mediciones demostradas de la calidad semántica de ese candidato. Los campos numéricos heterogéneos del CSV carecen de normalización de unidades físicas. [I11]

El potencial de navegación es

\[
P=3\Psi+1.5E+1.5T+1.2E_s-2\Delta S-\Lambda+2b_{diversity}.
\tag{14}
\]

Una razón de integridad independiente divide la media histórica de Ψ multiplicada por los valores más recientes de T y \(E_s\) entre la varianza muestral de los valores históricos de \(\Delta S\), el máximo histórico de Λ, la penalización por contradicción y \(10^{-6}\). No está acotada y puede crecer porque su denominador sea pequeño. Las etiquetas del ciclo de vida siguen umbrales ordenados, y el código invocador inspeccionado solo excluye las trayectorias podadas. Los historiales de trayectorias en JSON no constituyen un grafo duradero de dependencias entre afirmaciones ni un mecanismo de supresión de datos por motivos de privacidad. [I11]

### 8.3 Familias de series temporales y de fase

Las variantes históricas de series temporales normalizan diferencias y después calculan la media, la desviación estándar poblacional, la media del cambio absoluto entre valores adyacentes, la proporción de inversiones estrictas de signo y el flujo neto. La suma de diferencias sucesivas se reduce telescópicamente a \(s_n-s_1\). No aparece ningún divisor de tiempo transcurrido, por lo que se trata de cambios por muestra y no de derivadas por segundo. Las variantes posteriores modifican el preprocesamiento y añaden constantes de dominio declaradas; sus salidas no deben volver a etiquetar retroactivamente las ejecuciones anteriores. Para una fuente discreta, la entropía de Shannon es el negativo de la esperanza de la log-probabilidad bajo un modelo de probabilidad y una base logarítmica declarados. Una desviación estándar o un cambio entre extremos no adquieren ese significado por el nombre de una variable. [I11]. [Shannon 1948](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf).

Una propuesta donante basada en formas de onda define tres diagnósticos ponderados por la fase,

\[
C^+=\Psi(1+\cos\Delta\phi)/2,\quad
C^-=\Psi(1-\cos\Delta\phi)/2,\quad
Q_\perp=\Psi\sin^2\Delta\phi.
\tag{15}
\]

Los diagnósticos heredan las unidades de la Ψ seleccionada. Aunque \(C^++C^-=\Psi\), \(Q_\perp\) es un diagnóstico independiente, no una tercera fracción aditiva de energía. Una interpretación en términos de potencia física requeriría especificar un modelo de señal y un intervalo de promediado. Para frecuencias fijas, la diferencia de fase cambia a una tasa de \(2\pi(f_2-f_1)\). Trasladar estas relaciones a la traducción cognitiva o a la indagación iterativa constituye una analogía declarada por separado. Esta familia donante no es el códec sintético de referencia de la ecuación (9), y una coherencia elevada o la sincronización de fase, por sí solas, no implican un beneficio constructivo ni permiso para actuar. [I11]

### 8.4 Un donante de cancelación coherente y una hipótesis de destino contrastable

Considérense las señales analíticas donantes \(x_1(t)=A\sin(\omega t)\) y \(x_2(t)=A\sin(\omega t+\pi)\), con la misma amplitud constante \(A>0\), frecuencia angular no nula \(\omega\) y relación de fase fija. Su suma es idénticamente cero, aunque cada señal es no nula y la fase relativa es estable. A lo largo de un número entero de períodos, cada una tiene un valor cuadrático medio de \(A^2/2\), mientras que la suma tiene un valor cuadrático medio de cero. Se trata de una identidad exacta de señales idealizadas, no de un nuevo experimento con formas de onda, de una afirmación sobre conservación de la energía física ni de un resultado sobre cognición. Bajo el diagnóstico donante, con una \(\Psi>0\) elegida, la oposición de fase da \(C^+=0,C^-=\Psi,Q_\perp=0\). Por tanto, la estructura puede seguir especificada cuando un agregado observado se anula. [I11]

La hipótesis de destino propuesta es más restringida: preservar una objeción bien fundamentada y su relación con un candidato puede reducir el acuerdo superficial y, al mismo tiempo, mejorar la suficiencia de la evidencia evaluada de forma independiente. Una prueba fijaría las poblaciones de fuentes, las tareas de destino, las objeciones y los presupuestos antes de la evaluación; compararía un tratamiento que preservara explícitamente las relaciones con una presentación equiparada del mismo material sin mapa relacional; y mantendría a los evaluadores ciegos a la condición experimental. Criterios de valoración definidos por separado medirían el respaldo factual, el disenso sustancial conservado, las afirmaciones sin respaldo y la carga de revisión. Una ausencia de mejora en el respaldo, declarada de antemano, o un aumento de las afirmaciones sin respaldo con el presupuesto indicado contarían en contra del beneficio de destino alegado. El acuerdo por sí solo no es el resultado. Se trata de un diseño de prueba de clase H/P sin resultados en el destino: el álgebra del donante no establece la adecuación de la analogía. [I09, I11, I13]

## 9 Corredores, ríos, terrazas y consecuencias numéricas

### 9.1 Especificación de investigación e implementación reducida

La especificación de investigación de campos sobre grafos distingue la densidad de corredores C, la densidad de ríos R, la densidad de terrazas \(T^{terr}\), el potencial Θ, la memoria M y los términos de inestabilidad. Define

\[
F_{ij}=w_{ij}\frac{C_i+C_j}{2}(\Theta_j-\Theta_i),\qquad
A_i=\frac{|\sum_jF_{ij}|}{\sum_j|F_{ij}|+\varepsilon},
\tag{16}
\]

y una ley de evolución de los ríos de la forma

\[
\dot R_i=D_R\sum_jw_{ij}(R_j-R_i)
-\operatorname{div}_G(R\nabla_G\Theta)_i
+C_iA_i(\alpha_R+\beta_RM_i)-\mu_RR_i
-\nu_R([\Delta S_i]_++[\Lambda_i]_+)R_i-\chi_RR_i^3.
\tag{17}
\]

Una ley de terrazas añade difusión transportada, un término fuente de río ponderado por la estabilidad, apoyo de memoria/coherencia, pérdida y saturación cúbica. Estas ecuaciones preservan las intenciones de diseño de exploración, acumulación y estabilización provisional. Requieren orientación explícita del grafo, discretización, condiciones de contorno, unidades de los coeficientes, definiciones de los estimadores y semántica de admisibilidad antes de que puedan derivarse afirmaciones numéricas o científicas. La acotación \(0\le A_i<1\), para entradas finitas y ε positivo, es una consecuencia aritmética de la desigualdad triangular, no una validación del «acuerdo». [I12]

El núcleo reducido inspeccionado es sustancialmente más sencillo. Para una lista de aristas no dirigidas con pesos w, calcula

\[
(LR)_i=\sum_jw_{ij}(R_j-R_i),\quad
g_i=\frac{\sum_jw_{ij}(\Psi_j-\Psi_i)^2}{\sum_jw_{ij}},
\tag{18}
\]

con g fijado en cero cuando el denominador no es positivo, y después

\[
R_i^{n+1}=\operatorname{clip}_{01}
\{R_i^n+h[D_r(LR^n)_i+\alpha g_i-\beta R_i^n]\}.
\tag{19}
\]

Los valores predeterminados del núcleo son \(h=.05,D_r=.08,\alpha=.6,\beta=.1\), con recorte opcional. El código invocador de la evolución que se inspeccionó proporciona explícitamente **h=1.0**. A continuación invoca la actualización reducida de terrazas con el mismo paso,

\[
T_i^{n+1}=\operatorname{clip}_{01}
\{T_i^n+h(\kappa R_i^{n+1}-\mu g_i-\nu T_i^n)\},
\tag{20}
\]

cuyos valores predeterminados de núcleo incluyen \(h=.1,\kappa=.15,\mu=.10,\nu=.03\). En este código invocador, la fase de terrazas consume el campo de ríos recién actualizado y recortado \(R^{n+1}\); vuelve a calcular g a partir del campo Ψ, que no cambia entre estas fases. Es una actualización secuencial, no una actualización simultánea a partir del estado anterior. Ninguna de las dos ecuaciones implementa todos los términos de transporte, memoria y términos cúbicos de la especificación más completa. Un puente heurístico que produce ríos con nombre es otro productor distinto, no una discretización de la ecuación (17). [I12]

### 9.2 Estabilidad con el paso real del código invocador

Las siguientes deducciones suponen pesos no dirigidos finitos y no negativos, Ψ fija, \(D_r\ge0\), \(\beta>0\) y ausencia de recorte. Sea \(L_+\) el laplaciano positivo del grafo, de modo que \(L=-L_+\). Entonces

\[
\dot R=-(D_rL_++\beta I)R+\alpha g,
\qquad R_* =\alpha(D_rL_++\beta I)^{-1}g.
\tag{21}
\]

En un modo propio con valor propio laplaciano \(\lambda_k\), Euler explícito multiplica el error por \(1-h(D_r\lambda_k+\beta)\). El disco de estabilidad estándar de Euler explícito proporciona el marco; su aplicación a esta ecuación del código fuente da la condición de decaimiento estricto

\[
0<h<\frac{2}{D_r\lambda_{max}+\beta}.
\tag{22}
\]

[Driscoll y Braun sobre estabilidad absoluta](https://fncbook.com/absstab-diffusion/).

Con el valor real h=1 y los coeficientes predeterminados, la ecuación (22) requiere \(\lambda_{max}<23.75\). En cambio, el valor predeterminado del núcleo h=.05 requiere \(\lambda_{max}<498.75\). Para R inicial no negativa y forzamiento no negativo \(\alpha g\), como ocurre con los valores predeterminados indicados, una condición suficiente de positividad coeficiente a coeficiente es \(h(D_rd_i+\beta)\le1\) para cada grado ponderado \(d_i\), lo que da \(d_i\le11.25\) con h=1. La positividad y el decaimiento espectral estricto son propiedades diferentes. Ninguna establece una cota superior de uno sin condiciones adicionales sobre el forzamiento. [D a partir de I12]

Un contraejemplo exacto de estabilidad universal utiliza un grafo hipotético de dos nodos con una arista de peso 20 y valores de Ψ fijos e iguales, de modo que \(g=0\) y \(\lambda_{max}=40\). El multiplicador del modo de diferencia es \(-2.3\) con h=1, frente a .835 con h=.05. Con recorte, se parte de \(R^0=(1,0)\). El siguiente estado sin proyectar es \((-.7,1.6)\), por lo que la proyección da \((0,1)\); el paso siguiente vuelve a \((1,0)\). La acotación coexiste con una órbita exacta de período dos en este núcleo aislado con entradas fijas. Se trata de un ejemplo algebraico construido, no de una prueba ejecutada ni de una afirmación sobre un grafo realmente desplegado.

Sin recorte, al sumar la ecuación (21) se cancela la difusión simétrica y se obtiene

\[
\frac{d}{dt}\sum_iR_i=\alpha\sum_i g_i-\beta\sum_iR_i.
\tag{23}
\]

La densidad de ríos no se conserva en general. El recorte aporta una corrección de proyección. El escalado uniforme de los pesos cambia la rigidez de la difusión, mientras que deja g normalizada sin cambios si el escalado es positivo. Las aristas duplicadas en sentido inverso también pueden cambiar la acumulación. Una evaluación numérica válida debe conservar la identidad del grafo, los pesos, el paso, los incrementos previos a la proyección y los residuos de proyección. Ningún espectro de grafo real ni ninguna ejecución de este estudio establecen que el código invocador de producción fuera inestable. [I12]

### 9.3 Indagación recursiva y regímenes de representación

La recursión principal de investigación es

\[
X_{n+1}=\mathcal M\circ\mathcal S\circ\mathcal R(X_n),
\tag{24}
\]

donde la entrada receptiva, la estructuración y la continuidad/metabolismo actúan sobre el estado de la tarea en evolución. Estas pasadas funcionales no corresponden biunívocamente a tres componentes con nombre ni a tres modelos fijos. El estado puede conservar hipótesis, contradicciones, presupuesto y pruebas sin terminar; repetir un mensaje de entrada por sí solo no establece un refinamiento. [I12]

Una propuesta reducida de estado complejo utiliza \(Z_n=\Psi_n+iK_n\) y \(Z_{n+1}=\rho_ne^{i\theta_n}Z_n+\eta_n\). Para \(a=\rho e^{i\theta}\ne1\) constante y η constante, \(Z_*=\eta/(1-a)\) y \(Z_n-Z_*=a^n(Z_0-Z_*)\). Por tanto, \(|\rho|<1\) contrae las perturbaciones; \(|\rho|>1\) las amplifica en general. Para \(|a_n|\le r<1\) y forzamiento acotado \(|\eta_n|\le B\),

\[
|Z_n|\le r^n|Z_0|+B(1-r^n)/(1-r).
\tag{25}
\]

Esta cota no garantiza la convergencia a un único valor, y la rotación puede desplazar la coordenada real fuera de [0,1]. Llamar río o terraza a un régimen no resuelve esas cuestiones matemáticas. Un campo vectorial plano no es un equilibrio a menos que se cumpla la condición definitoria de punto fijo o de derivada nula. [I12]

Las fórmulas ecológicas más amplias que relacionan transferencia, ramificación, captura, pluralidad y renovación siguen siendo definiciones de clase H. Sus tipos escalar/vectorial sin resolver, los dominios de sus denominadores y sus estimadores empíricos constituyen trabajo de investigación sustantivo. Las derivaciones ecológicas más completas y su operacionalización quedan fuera del análisis detallado de este artículo; no todas estas propuestas formales son hipótesis empíricas listas para someterse a prueba. Aquí no se utilizan para puntuar personas ni instituciones. Preservar las hipótesis con las condiciones que les faltan es más fiel que declararlas leyes establecidas o eliminarlas como lenguaje decorativo.

## 10 AHA y transformaciones explícitas entre dominios

Un caso AHA suministrado contiene de dos a cinco grafos donantes, un grafo de destino, correspondencias de nodos/relaciones/invariantes, disanalogías, transformaciones declaradas de unidad/escala, un observable de destino, un comparador o hipótesis nula, un horizonte, una observación que reduciría la confianza y una declaración de falsación. La envoltura nativa exige el conjunto exacto de referencias a segmentos/hashes de fundamentación. El motor inspeccionado comprueba la existencia, el tipo, la orientación y los pares de extremos correspondientes de las relaciones declaradas. Las relaciones donantes sin correspondencia siguen siendo visibles. Se rechazan los identificadores declarados de familias de fuentes que estén duplicados, pero las etiquetas diferentes por sí solas no establecen orígenes independientes. [I09]

Sean las estructuras donante y de destino \(G_D=(V_D,E_D)\) y \(G_T=(V_T,E_T)\), con una aplicación de nodos \(\phi\) suministrada. Una relación comprobada \((u,r,v)\in E_D\) se preserva estructuralmente cuando existe la relación de destino requerida \((\phi(u),r',\phi(v))\in E_T\) bajo la transformación de relaciones declarada. En el motor actual, los tipos y las orientaciones de las relaciones correspondientes deben coincidir exactamente; el mapa de relaciones suministrado asocia identificadores y no ejecuta una transformación semántica ni de unidades. La notación mostrada de r a r′ es una generalización conceptual cuyo caso particular implementado requiere esa igualdad. Determinar si las relaciones describen mecanismos causales comparables es una afirmación científica adicional. La teoría de la correspondencia estructural convierte la preservación de relaciones en un objeto de indagación con fundamento teórico; no certifica una transferencia particular de donante a destino. [Gentner 1983](https://groups.psych.northwestern.edu/gentner/papers/Gentner83.2b.pdf).

Las salidas reales conservan sus tipos: \(P_{epi}\) es una postura evidencial ordinal NOT_SCORABLE; \(C_{bridge}\) contiene hallazgos sobre componentes estructurales; \(V_{test}\) es información cualitativa sobre valor informativo/viabilidad/riesgo con un coste no suministrado; \(Q_{AHA}\) es un rango de atención fijo de uno, explícitamente no probabilístico. Varios valores PASS se derivan de declaraciones aceptadas o comprobaciones estructurales, no de experimentos observados en el destino. La envoltura etiqueta la cobertura de referencias de linaje y establece en falso tanto la evaluación de la no vacuidad semántica como la demostración de utilidad semántica. [I09]

La ausencia de un caso suministrado significa UNAVAILABLE. La respuesta de seis bytes del testigo no crea espontáneamente grafos donantes, no descubre una correspondencia ni ejecuta una prueba falsadora. REVIEWABLE significa que un caso puede inspeccionarse. No establece descubrimiento, corroboración ni adopción. El descubrimiento automático de donantes, la retroalimentación de AHA al proveedor y la falsación ejecutada en el destino siguen siendo uniones sin resolver en la ruta mantenida inspeccionada. Una propuesta que evoluciona por separado o un conjunto de elementos probados debe permanecer separado del estado de implementación aceptado. [I09, I20]

Por tanto, el papel constructivo de las magnitudes compartidas es orientar la recuperación o la atención: diagnósticos similares pueden sugerir que se examine una rama. Un puente admisible aún debe identificar la relación, las unidades nativas, la transformación, las excepciones y una posible prueba falsadora. La igualdad numérica por sí sola no puede determinar qué relación semántica se transfiere. Esto preserva el descubrimiento lateral como objetivo de investigación sin convertir una coincidencia de coordenadas en evidencia.

### 10.1 Una espiral de descubrimiento a partir de evidencia no resuelta

En el programa de investigación Waters of Gnosis, una condición no resuelta puede identificar tanto una dirección inexplorada como una limitación. La incertidumbre no medida puede revelar una observación ausente; la evidencia contradictoria puede distinguir explicaciones rivales; una discrepancia incómoda entre donante y destino puede revelar una relación que merezca formularse. El objetivo constructivo es el descubrimiento innovador y la obtención de nuevos candidatos AHA, preservando la incertidumbre original en lugar de convertirla en confianza. Un valor desconocido no es evidencia de que el candidato sea falso, y el desacuerdo no es evidencia suficiente de que alguna de las partes esté equivocada. Ninguna de estas cosas constituye por sí sola evidencia de novedad. [I09, I12, I15]

La espiral propuesta hace operativo este objetivo en el vocabulario original de las aguas del conocimiento. Un **corredor** registra una alternativa o pregunta acotada. Un **afluente** aporta una observación dirigida, una calibración, una reparación o una fuente de contraste. Un **río** registra una línea de indagación en desarrollo a lo largo de las iteraciones. El **trenzado** mantiene conectadas las relaciones complementarias y el disenso sustancial, preservando sus linajes separados; no los promedia para forzar un acuerdo. Una **terraza** representa respaldo provisional dentro de un alcance declarado, y la **ruptura o reapertura** reexamina ese respaldo cuando nuevas observaciones socavan sus condiciones. Estas son funciones de indagación que pueden expresarse mediante los roles existentes del banco de trabajo y los casos AHA suministrados; este artículo no exige nuevos componentes obligatorios ni los identifica con flujos físicos. [I12, I13, I15]

Una secuencia acotada propuesta consiste en conservar la condición no resuelta y su base evidencial; permitir que el usuario elija una pregunta, las fuentes permitidas y el presupuesto de exploración; formular relaciones alternativas o correspondencias donantes candidatas; cuestionar los supuestos concretos que las distinguen; y devolver un nuevo candidato, el disenso preservado y la siguiente observación discriminante. Una exploración exitosa puede revelar una relación antes no formulada incluso mientras el candidato original sigue retenido. En cambio, puede establecer que un corredor tiene poco respaldo. Son resultados útiles diferentes. Por tanto, el estado de exploración debe llevar un seguimiento de los candidatos de descubrimiento separado de los hallazgos validados y del permiso para actuar. [I09, I12, I13, I20]

Se trata de integración y diseño de pruebas de clase P/H, no de un bucle automático de retroalimentación actual. La regla ordinaria de rechazo de JOINED permanece sin cambios. Un resultado retenido no lanza más llamadas, no autoriza nuevos destinatarios ni convierte un mapa estructural suministrado en una demostración. El usuario conserva el control sobre si explorar, qué rama seguir y cuándo detenerse; cada operación con consecuencias sigue necesitando la autorización aplicable que le corresponda. Una evaluación equiparada podría comparar una espiral guiada por residuos con la aclaración ordinaria bajo los mismos datos y presupuesto, utilizando hipótesis nuevas útiles evaluadas por separado, relaciones recién respaldadas, disenso conservado y carga de revisión. La mera novedad de la redacción, un mayor número de salidas o un mayor acuerdo no establecerían el beneficio propuesto. [I07, I13, I15, I20]

## 11 Operadores de perturbación y cambio cognitivo

El término perturbación debe identificar un operador, los invariantes preservados y un objetivo de observación. En el espacio de diseño aparecen al menos seis operaciones diferentes:

| Familia de operadores | Objeto modificado | Relación preservada o sometida a prueba | Límite evidencial actual |
|---|---|---|---|
| Normalización de texto | Saltos de línea, espacios en blanco en los límites, representación Unicode | Identidad original conservada por separado; coordenadas normalizadas reconstruidas | Transformación implementada; preservación semántica general no demostrada |
| Envoltura de contexto | Mensajes efectivos y contexto previo seleccionado | Vínculos exactos con el elemento padre, la tarea y la fuente | Ruta implementada; efectos a nivel de tokens no observados |
| Cuestionamiento del candidato | Afirmaciones, objeciones o alternativas suministradas | Linaje de la misma raíz y respuesta explícita al cuestionamiento | Estructura local del banco de trabajo; no implica corroboración independiente |
| Perturbación numérica | Coeficientes, entradas, grafo o condiciones iniciales | Sensibilidad, residuos, estabilidad bajo una norma especificada | Las ejecuciones históricas repetidas suelen carecer de perturbación controlada; este artículo solo deriva condiciones |
| Correspondencia analógica | Interpretación del dominio y correspondencia relacional | Relaciones declaradas, transformaciones de unidades, disanalogías | Comprobaciones estructurales de casos suministrados; adecuación al destino no establecida |
| Corrección o revocación | Versión, uso permitido o elegibilidad de dependencias | Observación histórica separada del permiso actual | Existen controles acotados; propagación universal a todo el grafo no establecida |

Esta taxonomía es una síntesis analítica de mecanismos y propuestas inspeccionados, no una afirmación de que un único orquestador ya invoque los seis. Cada operador puede producir un nuevo candidato útil, un rechazo, un residuo, una solicitud de evidencia o un alcance más restringido. El progreso cognitivo no puede inferirse únicamente de la magnitud del cambio o de la reducción del desacuerdo. Una respuesta errónea estable sigue siendo errónea; la diversidad sin pertinencia no constituye una exploración útil. [I05, I11–I16]

Para un experimento controlado propuesto, sea \(T_\delta\) una perturbación declarada y \(F\) la ruta de evaluación acotada. Solo puede estudiarse \(F(T_\delta x)-F(x)\) después de especificar la representación de salida, la norma, los valores admisibles de δ, los controles equiparados y las observaciones disponibles. Comparar espacios de nombres escalares no relacionados hace que esa diferencia quede indefinida como medición. Esta formulación es un protocolo de investigación, no un experimento oculto realizado por la arquitectura.

## 12 Banco de trabajo local y enjambre distribuido

### 12.1 Funciones y dependencia

El banco de trabajo local Analyst→Challenge→Synthesis vincula los artefactos previos seleccionados de una misma raíz, las versiones de las fuentes y los controles, y la selección explícita. Synthesis debe preservar los acuerdos y desacuerdos sustanciales, así como las objeciones no resueltas, en lugar de tratar el consenso entre funciones como verdad. Los bucles históricos que realizan tres o siete llamadas a un mismo modelo con instrucciones distintas muestran diversidad de instrucciones y muestreo repetido; no demuestran cognición independiente distribuida. Los nombres de función distintos, e incluso los modelos distintos, no pueden demostrar por sí solos la independencia de la evidencia. [I13]

Para ilustrar por qué esto importa, supóngase que errores de igual varianza tienen varianza \(\sigma^2\) y una correlación común por pares r, con una matriz de covarianza semidefinida positiva admisible. Entonces

\[
\operatorname{Var}(\bar\epsilon)
=\frac{\sigma^2}{m}[1+(m-1)r],\qquad
m_{eff}=\frac{m}{1+(m-1)r}.
\tag{26}
\]

El tamaño muestral efectivo mostrado supone un denominador positivo; no se asigna un valor finito a su frontera singular de varianza cero. Para pesos generales w y covarianza Σ, la varianza es \(w^\top\Sigma w\). Estas son deducciones explicativas, no estimadores de confianza implementados. El entrenamiento compartido, la exposición a las mismas fuentes y la observación de una respuesta previa pueden generar dependencia. Ni el acuerdo verbal ni las etiquetas de modelo miden r. Las mejoras en pruebas comparativas comunicadas para el debate multiagente motivan experimentos controlados, pero no implican que aumentar los agentes o las rondas mejore universalmente los resultados. [I13]. [Du et al 2024](https://proceedings.mlr.press/v235/du24e.html).

N unidades de trabajo con concurrencia c no equivalen a N trabajadores simultáneos. Todas las comparaciones de pares ordenados tienen un coste de \(N(N-1)\) antes de contar las rondas. Un evento de usuario con N tareas analíticas hijas constituye un evento fuente y N trabajos, no N+1 observaciones independientes. Por tanto, un banco de trabajo validado necesita el denominador: los trabajos intentados, fallidos, desactualizados, cancelados y no resueltos, además de los resultados aceptados. Las objeciones dirigidas a supuestos distintos pueden ser preferibles a un intercambio ilimitado entre todos los participantes. Estas son consecuencias de diseño, no afirmaciones de velocidad o calidad medidas. [I13]

### 12.2 Transferencia de artefactos e interfaces de integración de modelos entre pares

La transferencia acotada de artefactos entre pares existe como un enlace autenticado con vinculación exacta entre archivo, referencia y oferta, emparejamiento aceptado, concesión vigente, plazo original, TLS y verificación a cargo del receptor. Las referencias de resumen criptográfico emitidas por el sistema de custodia fuera de un archivo no son firmas. Un paquete cuyos bytes se verifican puede seguir conteniendo una afirmación falsa, y una función verificadora autenticada por separado no implica corroboración independiente por parte de un modelo. [I14]

También existen contratos de emisor, receptor y solicitud/estado/resultado para modelos entre pares. El código fuente inspeccionado contiene envío de un solo intento desactivado por defecto, recepción desactivada por defecto, proyección de concesiones vigentes y puntos de integración con la custodia nativa. Los límites incluyen tramas canónicas de solicitud/estado/resultado de un máximo de 65,536 bytes, ventanas originales de trabajo de un máximo de 120,000 milisegundos, límites de salida declarados de un máximo de 4,096 tokens y texto devuelto de un máximo de 32,768 bytes UTF-8; la envoltura del resultado tiene su propio límite de trama. El receptor requiere un autenticador inyectado. La ejecución requiere un responsable nativo inyectado por separado que compruebe la política vigente, el reloj de confianza, la titularidad de los recursos y la reserva transaccional. La recepción heredada puede conservar un recibo retenido sin ese responsable, mientras que la recepción estructurada rechaza la admisión sin responsable; ninguno de estos resultados de recepción otorga autoridad de ejecución. Un objeto con forma de concesión dentro de una carga útil no puede concederse autoridad a sí mismo. [I14]

Sin embargo, la lista mantenida de elementos permitidos del transporte emparejado inspeccionada para este estudio encamina la recepción, verificación y cancelación de artefactos, no trabajos de modelos entre pares. No se constató ninguna construcción en producción del receptor del modelo ni ninguna invocación del emisor en el conjunto de cierre seleccionado. La evidencia respalda interfaces de implementación acotadas reales, junto con conexiones de extremo a extremo que faltan. No respalda un enjambre cognitivo operativo de tres nodos debidamente validado. Un piloto de tres nodos sigue siendo propuesto o parcialmente implementado hasta que se establezca, para cada enlace, la evidencia del transporte, el responsable, la concesión, la custodia y el consumo del resultado. La conectividad y los permisos no son transitivos. [I14, I20]

La retención de Challenge externo y los consumidores locales de síntesis preservan referencias exactas a las cargas útiles, manteniendo separadas las observaciones de entrega. Los derechos actuales de uso y compartición se vuelven a comprobar con independencia de la finalización histórica. La caducidad de una concesión de ejecución no demuestra que el trabajo anterior no se ejecutara ni resuelve automáticamente todas las inspecciones históricas autorizadas por separado. Esta distinción es necesaria tanto para una procedencia precisa como para una reutilización acotada. [I14]

## 13 Procedencia y confianza de la telemetría

### 13.1 Tres dominios de observación diferentes

La custodia, TEL nativo y la observación de la carga de acción responden a preguntas distintas. Los eventos de custodia calculan el hash de una tupla canónica formada por la identidad del registro, el tipo, el actor, el tiempo, los detalles y el resumen criptográfico anterior. Una secuencia de base de datos ordena los eventos locales, pero no se incluye en ese resumen. Los disparadores de solo anexado restringen las operaciones normales de actualización y eliminación bajo el esquema; un propietario privilegiado de la base de datos o del equipo anfitrión sigue siendo una dependencia de confianza. La cadena permite detectar alteraciones respecto de una vista conservada de confianza; no es un registro con sellado temporal independiente, atestiguado globalmente ni consistente frente a fallos bizantinos. [I16]

TEL nativo registra un orden determinista de etapas y las vinculaciones de artefactos. El núcleo produce 15 eventos de preauditoría y se detiene antes de Sophia/Atlas. La finalización verificada de la auditoría y orientación externas produce 18 filas de ruta, y una decisión humana posterior es una continuación separada que vincula el elemento padre sellado. Las etiquetas lógicas como T+000001 son identificadores de secuencia, no segundos transcurridos ni relojes causales entre equipos. El análisis de orden parcial de Lamport explica por qué la causalidad distribuida no puede inferirse simplemente de marcas temporales superficialmente comparables. Aquí no se afirma que exista una implementación de relojes de Lamport. [I16]. [Lamport 1978](https://lamport.azurewebsites.net/pubs/time-clocks.pdf).

El componente hoja TAF-A inspeccionado autentica una captura padre conservada e informa de los bytes lógicos conservados de respuesta del proveedor. Su unidad es el byte; los datos ausentes son UNAVAILABLE, no cero. Quince términos de diagnóstico heredados y los agregados de acción total siguen sin estar disponibles. No mide energía en julios, FLOPs, memoria del dispositivo, coste de opciones futuras ni carga ética del sistema completo. Su perfil de serialización también difiere del JSON nativo con LF final, lo que refuerza la necesidad de declarar el dominio del hash. [I16]

### 13.2 La composición de la procedencia no compone la verdad

Un grafo conceptual de procedencia puede utilizar entidades para los bytes y las evaluaciones, actividades para las transformaciones y agentes para los productores o revisores responsables. Esto corresponde al ámbito de PROV-DM, sin afirmar conformidad de implementación. [PROV](https://www.w3.org/TR/prov-dm/).

Para un resultado y, distínganse seis predicados:

\[
\operatorname{BytesMatch}(y),\quad
\operatorname{SenderAuthenticated}(y),\quad
\operatorname{LineageBound}(y),\quad
\operatorname{ProcedureObserved}(y),\quad
\operatorname{EvidenceAdequate}(y,q),\quad
\operatorname{UsePermitted}(y,p,r,t).
\tag{27}
\]

El último predicado depende del propósito p, el destinatario r y el tiempo t. Ninguno de estos predicados implica todos los posteriores. Su conjunción puede ser necesaria para un uso concreto, pero no constituye un teorema universal de verdad. La integridad de la fuente, la interpretación y la autoridad de acción tienen responsables y modos de fallo diferentes. [I03, I10, I14, I16]

La evidencia replicada no es automáticamente consenso sobre un registro replicado. Raft aborda el acuerdo sobre el estado de un registro bajo un protocolo especificado, no el acuerdo sobre la verdad científica. De manera similar, Certificate Transparency especifica pruebas de inclusión y consistencia, y preocupaciones sobre vistas inconsistentes; una cadena local de resúmenes criptográficos no se convierte por ello en un servicio de transparencia atestiguado globalmente. Estas son clases de contraste, no componentes cuya presencia se afirme. [Ongaro and Ousterhout 2014](https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro), [RFC 9162](https://www.rfc-editor.org/rfc/rfc9162.html).

## 14 Gramática compartida y reconstrucción retrospectiva

### 14.1 Comunicación por referencia con residuos

La gramática compartida prevista permite una referencia compacta a una estructura previamente establecida, versionada y permitida. Una ruta receptora defendible consiste en resolver la referencia; verificar la definición, la versión y los permisos de las dependencias; comparar el dominio y las unidades; expandir excepciones y residuos; y, después, aceptar únicamente la interpretación acotada respaldada o rechazar la correspondencia. Este es un contrato de diseño para el contexto compartido, no evidencia de experiencia subjetiva compartida. [I15]

El coste de comunicación debe incluir la distribución y sincronización de la biblioteca compartida, los bytes de referencia, los residuos, la procedencia, la búsqueda, la expansión, la verificación y las correcciones. Una frase breve no constituye un resultado completo de compresión. La teoría de codificación de Shannon proporciona un marco formal de comunicación; no equipara los códigos cortos con la verdad semántica o la utilidad cognitiva. [Shannon 1948](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf).

Los mecanismos históricos recuperados incluyen un diccionario versionado con vinculaciones de respaldo, registros de transformación que preservan dominio y unidades, y reconstrucción mediante copia de bytes y residuos con contabilidad explícita de costes. No demuestran aprendizaje automático actual de la gramática, recuperación GUFT por vecinos más próximos, transferencia semántica sin pérdida ni negociación de expansión entre nodos. La comparación finita de antecedentes suministrados es un componente hoja útil del lado receptor, no el constructor completo de la biblioteca. No se ha constatado ningún invocador de producción ni ningún emisor de autoridad para el componente hoja de comparación pura inspeccionado dentro del conjunto de cierre seleccionado. [I15]

### 14.2 Retrosíntesis como reconstrucción dirigida por dependencias

Aquí, retrosíntesis significa rastrear hacia atrás un resultado deseado o producido a través de las transformaciones y el respaldo necesarios para justificarlo o reproducirlo. Es una descripción analítica de un recorrido útil de la procedencia, no una afirmación de que ya se haya implementado un motor general de razonamiento inverso. Sea \(f_y=\operatorname{pr}_y\circ f\) la proyección de salida de la transformación con valores de tupla de la ecuación (1), con el contrato de evidencia y estado fijado por separado. Para \(y=f_y(x,\kappa,\pi)\), defínase el conjunto de predecesores admisibles

\[
\operatorname{Pre}(y)=\{(x,\kappa,\pi):f_y(x,\kappa,\pi)=y
\text{ under the declared identity and status contract}\}.
\tag{28}
\]

Para una normalización de muchos a uno, Pre puede contener múltiples historiales de bytes. Una referencia hash junto con un original no disponible no puede restaurar esos historiales. Para la inferencia estocástica u opaca, reproducir la salida exacta puede requerir además un estado de ejecución no observado. Por tanto, el resultado retrospectivo honesto puede ser «identidad registrada, carga útil no disponible», «recálculo estructural disponible» o «inferencia en tiempo de ejecución no reproducible», en lugar de una reproducción completa inventada. [I04, I06, I15]

Para una afirmación q, sea \(\mathcal S(q)\) la familia que contiene los conjuntos alternativos de respaldo declarados adecuados y no vacíos según un método y un alcance elegidos. La adecuación es un juicio científico separado a nivel de conjunto, no algo creado por las comprobaciones de disponibilidad y permiso que figuran a continuación. Con el propósito p, el destinatario r y el tiempo t explícitos, una condición explicativa de uso presente es

\[
\operatorname{SupportUsable}(q,p,r,t)
=\bigvee_{S\in\mathcal S(q)}\ \bigwedge_{e\in S}
\left[\operatorname{Available}(e,t)\land
\operatorname{UsePermitted}(e,p,r,t)\land
\operatorname{MethodApplicable}(e,q)\right].
\tag{29}
\]

Una familia vacía \(\mathcal S(q)=\varnothing\) da falso, y se excluyen los miembros vacíos; un teorema lógico sin evidencia requeriría su propia justificación declarada en lugar de un respaldo accidental por vacuidad. La ecuación (29) es una semántica de dependencias propuesta, no un evaluador global implementado. Muestra por qué perder una fuente no tiene por qué refutar q cuando permanece un respaldo independiente adecuado, y por qué un registro histórico no autoriza automáticamente la reutilización presente. Un motor general de reapertura consciente de las dependencias, un solucionador de conjuntos mínimos de reparación y la propagación de revocaciones entre nodos requieren implementación y validación adicionales. [I15, I20]

No obstante, el razonamiento retrospectivo puede orientar resultados útiles hoy: identificar el candidato exacto y la versión de entrada, mostrar qué comprobaciones se ejecutaron realmente, preservar el disenso, enumerar la evidencia ausente y formular una próxima prueba acotada. Una ruta que devuelve una solicitud de aclaración pero no ejecuta ninguna reparación debe indicarlo. El artefacto se convierte en un estado del banco de trabajo sujeto a rendición de cuentas, en lugar de una afirmación de que la incertidumbre ha desaparecido.

### 14.3 Reutilización de procedencia y autonomía en el trabajo compartido

La hipótesis de investigación es que la reutilización de un artefacto respaldado, respetando los permisos, puede reducir la derivación repetida con una calidad y cobertura aceptadas comparables. Los orígenes identificables, las versiones, los mapas de dependencias y las correcciones pueden ayudar a los destinatarios a evaluar qué puede reutilizarse. Las copias adicionales por sí solas no aportan evidencia más sólida ni corroboración independiente. La reutilización sigue sujeta a los límites de autoridad, dependencia y privacidad de las secciones 12–15. [I13–I17]

Una comparación propuesta fijaría la misma carga de tareas repetidas, instantánea de fuentes, salidas requeridas, condiciones de hardware y ejecución, reglas de detención y horizonte de observación para dos grupos. El grupo de recálculo deriva de nuevo cada resultado requerido conforme a una política declarada. El grupo de reutilización resuelve un artefacto previo, verifica su identidad, respaldo, aplicabilidad, vigencia y permisos, y después lo adapta con residuos registrados o recurre al recálculo. Deben prerregistrarse los criterios de aceptación y un margen de comparabilidad de calidad; debe utilizarse evaluación ciega cuando sea viable. Deben comunicarse las salidas aceptadas junto con las tareas intentadas, rechazadas, fallidas, desactualizadas, canceladas y no resueltas. Los ahorros para un servicio equivalente requieren calidad y cobertura aceptadas comparables.

Para cada unidad de recurso u, defínase la diferencia descriptiva ΔC_u = C_recompute,u − C_reuse,u sobre toda esa carga de trabajo. Ambos totales incluyen la producción inicial atribuible, la recuperación, la verificación, la adaptación, el almacenamiento y la replicación, el transporte, la coordinación, los intentos fallidos, el trabajo alternativo y las correcciones posteriores dentro del horizonte declarado. Contabilícese cada evento de recurso una sola vez, incluido el trabajo transferido a pares. Declárese la asignación de los costes de configuración compartida y almacenamiento persistente; distínganse los totales de arranque en frío de los resultados con caché caliente. Un ΔC_u positivo denota un ahorro únicamente en esa unidad y ese alcance medidos, sujeto a la comparabilidad de calidad y cobertura. [I15, I19, I20]

Debe informarse del cómputo en recuentos de operaciones medidos directamente o en segundos-dispositivo con especificación del hardware, de la energía en julios cuando esté instrumentada, del tráfico en bytes, de la ocupación de almacenamiento en bytes-segundo, de la latencia transcurrida en segundos y de la revisión humana en minutos-persona. Deben mantenerse separadas las dimensiones; la latencia transcurrida no es la suma del cómputo paralelo. Los tokens, las llamadas y los bytes de respuestas conservadas no establecen FLOPs, energía ni probabilidades de corrección. Las mediciones ausentes siguen sin estar disponibles. [I16]

La autonomía práctica es un objetivo de diseño principal que se evalúa por separado del ahorro de recursos: la capacidad de salir, elegir un modelo o proveedor, mantener el control local y participar en una gobernanza cooperativa sujeta a rendición de cuentas. Un estudio debe especificar las capacidades requeridas y evaluar si los participantes pueden ejercerlas, incluidos los fallos y las barreras. El ahorro de recursos no compensa la vulneración de un requisito mínimo de derechos declarado, y los usuarios pueden preferir mayor autonomía pese a un coste superior. La descentralización por sí sola no demuestra ninguno de estos resultados. Este es un compromiso normativo de diseño con criterios operativos de evaluación, no un término favorable añadido a la diferencia de costes. El estudio propuesto no se ha ejecutado; aquí no se comunica ningún resultado nuevo de eficiencia o autonomía. [I19, I20]

## 15 Análisis de seguridad, privacidad y fallos

El modelo de amenazas incluye instrucciones maliciosas en las fuentes, artefactos malformados, afirmaciones de identidad falsificadas, concesiones desactualizadas, entrega parcial, ataques de repetición, ejecución duplicada, errores de razonamiento correlacionados, nombres de métricas engañosos, compromiso de un custodio privilegiado y copias no resueltas fuera del responsable local. Este artículo evalúa límites de diseño, no la resistencia a ataques de un producto instalado.

| Fallo o amenaza | Límite inspeccionado | Limitación residual |
|---|---|---|
| El texto fuente solicita acciones privilegiadas | La fuente se trata como datos; actor autenticado y autoridad de despacho separada | El encuadre de las instrucciones por sí solo no demuestra la obediencia del modelo ni elimina la inyección |
| Una carga útil modificada reutiliza una clave de idempotencia | Vinculación exacta con la carga útil bruta | Un resultado previo incierto sigue requiriendo conciliación |
| Se denomina completa a una respuesta truncada | Longitudes y hashes observados y conservados; comprobaciones de finalización específicas del proveedor | La ejecución remota y el acuse local pueden divergir |
| Se confunde una cita con la verdad | Reconstrucción exacta del segmento y del resumen criptográfico; postura de revisión humana | La adecuación de la fuente, la verdad y la implicación semántica siguen siendo cuestiones separadas |
| Las métricas compensan un incumplimiento de política | Compuertas no compensatorias de Aperture | Los controles de negocio específicos del perfil pueden ser orientativos |
| Se cuenta una segunda función como evidencia independiente | Historial de la misma raíz e identidad explícita de la contribución | La dependencia estadística no se mide mediante etiquetas |
| Una concesión falsificada autoriza trabajo entre pares | Responsable autenticado inyectado y comprobaciones de la política vigente | No se ha establecido una ruta de modelos en producción de extremo a extremo |
| Se denomina consenso inmutable a un registro local | Cadena de hashes, esquema de solo anexado e inventario sellado | El equipo anfitrión o custodio privilegiado y la observación externa siguen siendo dependencias de confianza |
| Se denomina anónimo a un paquete sin datos brutos | Algunos bytes brutos se excluyen de la entrada de revisión | El texto derivado de la fuente y la respuesta pueden seguir siendo identificativos |
| Se denomina borrado completo a la caducidad de la carga útil | Caducidad de la carga útil con alcance controlado y marcadores de eliminación | Los eventos de solo anexado y las copias externas pueden conservar contenido |

[I03, I05–I10, I13–I17]

Estos controles no garantizan la confidencialidad frente a un punto de cómputo autorizado o un equipo anfitrión local privilegiado. Las rutas seleccionadas construyen valores legibles de fuente, contexto y solicitud, y conservan artefactos que contienen contenido; TLS protege el transporte entre los extremos. Este estudio no establece ninguna garantía de computación confidencial ni de retención remota verificada de forma independiente, y no audita protecciones del equipo anfitrión ajenas a su alcance. Por tanto, seleccionar una ruta requiere decidir que el destinatario y el alcance de las copias conservadas son apropiados para los datos. [I06, I14, I17]

La última fila es concreta. Los BLOBs de custodia seleccionados y los archivos derivados pueden caducar, sujetos a confirmación del custodio, retención legal y comprobaciones de evaluadores activos. Sin embargo, los eventos de intento de solo anexado pueden contener bytes de la solicitud original, los eventos de vinculación de contexto pueden contener mensajes efectivos y los eventos de confirmación de captura pueden contener texto de respuesta normalizado. La rutina de caducidad inspeccionada no elimina todos esos detalles de eventos. Las exportaciones, las copias de seguridad, los proveedores y los pares tienen ciclos de vida de copias separados. Por ello, una afirmación de borrado completo del contenido sería falsa para el alcance inspeccionado. [I17]

Los propios hashes pueden permitir la vinculación, especialmente en textos candidatos de baja entropía. Un recibo sin datos brutos es un límite de omisión, no una desidentificación. Un paquete de revisión puede preservar el contenido de la fuente y la respuesta mientras excluye los bytes del cuerpo del proveedor. El análisis de privacidad debe inventariar las copias que contienen contenido y los titulares de autoridad, en lugar de contar únicamente archivos etiquetados como brutos. Estas limitaciones no implican que falten los controles existentes de funciones, retención y despacho; definen lo que dichos controles cubren realmente. [I17]

Los valores predeterminados seguros ante fallos, el mínimo privilegio y la mediación completa siguen siendo criterios útiles: la ausencia de autorización no debe convertirse en permiso; cada uso debe comprobarse ante el responsable correspondiente. Orientan la revisión sin demostrar que todas las rutas de implementación los satisfagan. [Saltzer and Schroeder 1975](https://web.mit.edu/Saltzer/www/publications/protection/Basic.html).

## 16 Agenda de validación de la investigación

La siguiente evidencia debe cerrar conexiones específicas en lugar de maximizar el número de etiquetas impresionantes. Cada propuesta siguiente pertenece a la clase P y requiere su propio alcance autorizado; ninguna se ejecutó para este artículo.

1. **Experimento de representación con versiones fijadas.** Utilizar una compilación permitida del tokenizador, la plantilla y el entorno de ejecución, y casos sintéticos con texto multibyte, variantes de normalización y tareas sensibles a espacios en blanco. Conservar los bytes exactos, los identificadores de token cuando sean observables, los puntos de rechazo y los contratos completos. Separar la visibilidad del tokenizador de los cálculos ocultos del modelo.
2. **Calibración del filtrado.** Definir un productor de incertidumbre con un evento objetivo y una población explícitos. Evaluar la discriminación, la calibración, los compromisos asociados al rechazo y los casos adversos en tareas reservadas. Comparar con la ruta conservadora actual sin cambiar un umbral únicamente para aumentar la tasa de aprobación.
3. **Validación numérica.** Fijar la topología del grafo, la semántica de los pesos, las versiones de los coeficientes y los pasos de los invocadores reales. Analizar el espectro o una cota suficiente justificada, conservar las actualizaciones sin recorte, comparar refinamientos del paso e informar de los residuos de proyección. Probar por separado si las densidades predicen algún resultado cognitivo útil.
4. **Prueba de destino AHA.** Congelar los grafos y las correspondencias de origen y destino antes de observar los resultados en el destino. Registrar las desanalogías, el comparador, el criterio de refutación, el coste y la condición de detención. Comparar la posibilidad de revisión estructural con la validez observada en el destino, en lugar de tratarlas como la misma variable de resultado.
5. **Experimento de dependencia del banco de trabajo.** Comparar condiciones de una sola pasada, repetición con un único modelo, diversidad de funciones y auténtica diversidad de fuentes bajo presupuestos equivalentes. Realizar evaluación ciega cuando sea viable; conservar los fallos y el disenso. No inferir independencia a partir de etiquetas de función diferentes.
6. **Validación distribuida.** Establecer para cada enlace entre pares su punto de entrada instalado, autenticador, responsable de recursos, concesión vigente, transporte acotado, reserva transaccional y observación del receptor. Incluir acuses perdidos, concesiones desactualizadas y caducidad de cargas útiles. Informar de un piloto de tres nodos solo después de validar toda su población declarada.
7. **Contabilidad del ciclo de vida y de las copias.** Inventariar todos los responsables que conservan contenido, verificar el alcance exacto de la caducidad y preservar marcadores de eliminación veraces. Probar las decisiones de corrección y uso actual frente a grafos alternativos de respaldo. No prometer la retirada de copias situadas fuera del límite de aplicación de los controles.
8. **Evaluación de resultados y costes.** Definir el éxito de la tarea antes de la inspección, comparar líneas base equivalentes, separar el respaldo factual de la usabilidad e informar de la carga de revisión humana, la latencia, los bytes y los costes de recursos efectivamente medidos. Las mediciones de energía o acción total no disponibles siguen sin estar disponibles. Para la hipótesis de compartición de la sección 14.3, comparar la reutilización respetuosa con los permisos y el recálculo con calidad y cobertura equivalentes, incluyendo recuperación, verificación, almacenamiento, replicación y coordinación. Evaluar la libertad práctica y el control cooperativo por separado del ahorro de recursos.

La secuencia de revisión independiente debe congelar el manuscrito y el complemento legible por máquina, evaluar la fidelidad a las fuentes y las rutas de llamada, evaluar las matemáticas y las unidades, evaluar la seguridad, la privacidad y la distribución, evaluar las afirmaciones científicas y comparar cada afirmación legible por máquina con la prosa. Las correcciones sustanciales requieren una nueva versión y una nueva revisión dirigida. Esto es gobernanza de publicación para este artículo, no evidencia de que el sistema haya realizado automáticamente esas revisiones.

## 17 Discusión y conclusión

La unidad mínima de datos significativa en Triadic Brain depende de la operación. Los bytes permiten comprobar la identidad del contenido; los segmentos Unicode permiten localizar extractos; los registros de aplicación hacen explícitas las vinculaciones de actor y tarea; las afirmaciones y los mapas relacionales permiten revisar las interpretaciones propuestas; los grafos de eventos y artefactos permiten atribuir las derivaciones. Estas unidades pueden componerse sin fingir que identidad, verdad y autoridad son una sola propiedad.

La reconstrucción a partir del código fuente muestra mecanismos nativos concretos: intentos duraderos, despacho acotado, captura específica del proveedor, vinculación determinista de fuentes, filtros estructurales, recálculo independiente acotado y salida inspeccionable. También revela límites claros. La incertidumbre conservadora del puente JOINED ordinario fija una condición de rechazo; una única probabilidad normalizada no certifica la corrección; un códec de forma de onda no mide la cognición; una analogía estructural no ejecuta su criterio de refutación; un registro local no aporta consenso distribuido; y la caducidad acotada de cargas útiles no demuestra un borrado total.

El programa GUFT y de aguas cognitivas sigue teniendo contenido científico sustantivo cuando sus magnitudes conservan sus definiciones nativas y sus hipótesis conservan criterios de refutación. El núcleo reducido de grafo, la propuesta de campo más completa, la telemetría histórica y los indicadores indirectos UCM actuales son objetos distintos. Su relación es una cuestión de ingeniería e investigación, no una igualdad autorizada por la notación. El ejemplo analítico de dos nodos demuestra la importancia práctica de examinar los invocadores reales y el comportamiento de la proyección, incluso cuando las salidas permanecen acotadas.

La arquitectura resultante puede entenderse como un banco de trabajo para conocimiento revisable: preservar observaciones y alternativas, hacer inspeccionables las transformaciones, mostrar la incertidumbre y mantener el uso con consecuencias bajo su propia autoridad. Esa es la descripción respaldada por el artículo y su dirección de investigación. La ganancia semántica demostrada, la cooperación operativa de tres nodos, la transferencia calibrada entre dominios y el control integral del ciclo de vida de dependencias siguen siendo evidencia por obtener.

## Referencias

Las dieciocho referencias académicas y normativas se abrieron para la versión predecesora el 3 de noviembre de 2026. Las normas de versiones específicas se citan por el concepto indicado, no como certificaciones de despliegue ni como afirmación de que no exista una sucesora.

1. Yergeau, F. 2003. [UTF-8, a transformation format of ISO 10646. RFC 3629](https://www.rfc-editor.org/rfc/rfc3629.html).
2. Unicode Consortium. 2025. [Unicode Normalization Forms. UAX 15, revision 57, Unicode 17.0.0](https://www.unicode.org/reports/tr15/tr15-57.html).
3. Rundgren, A., Jordan, B., and Erdtman, S. 2020. [JSON Canonicalization Scheme. RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html).
4. NIST. 2015. [Secure Hash Standard. FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final).
5. Eddy, W., ed. 2022. [Transmission Control Protocol. RFC 9293](https://www.rfc-editor.org/rfc/rfc9293.html).
6. Fielding, R., Nottingham, M., and Reschke, J., eds. 2022. [HTTP/1.1. RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.html).
7. Rescorla, E. 2018. [The Transport Layer Security Protocol Version 1.3. RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.html).
8. Moreau, L., and Missier, P., eds. 2013. [PROV-DM The PROV Data Model. W3C Recommendation](https://www.w3.org/TR/prov-dm/).
9. Vaswani, A., et al. 2017. [Attention Is All You Need](https://arxiv.org/abs/1706.03762v7). Se consultó la versión 7 de arXiv, revisada el 2 de agosto de 2023.
10. Gentner, D. 1983. [Structure-Mapping A Theoretical Framework for Analogy. Cognitive Science 7, 155–170](https://groups.psych.northwestern.edu/gentner/papers/Gentner83.2b.pdf).
11. Guo, C., Pleiss, G., Sun, Y., and Weinberger, K. Q. 2017. [On Calibration of Modern Neural Networks. PMLR 70, 1321–1330](https://proceedings.mlr.press/v70/guo17a.html).
12. Shannon, C. E. 1948. [A Mathematical Theory of Communication. Bell System Technical Journal 27, 379–423 and 623–656](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf).
13. Driscoll, T. A., and Braun, R. J. [Fundamentals of Numerical Computation, Absolute stability](https://fncbook.com/absstab-diffusion/). Texto de análisis numérico mantenido por sus autores, capítulo 11, sección 11.3; consultado el 3 de noviembre de 2026.
14. Du, Y., Li, S., Torralba, A., Tenenbaum, J. B., and Mordatch, I. 2024. [Improving Factuality and Reasoning in Language Models through Multiagent Debate. PMLR 235, 11733–11763](https://proceedings.mlr.press/v235/du24e.html).
15. Lamport, L. 1978. [Time, Clocks, and the Ordering of Events in a Distributed System. Communications of the ACM 21, 558–565](https://lamport.azurewebsites.net/pubs/time-clocks.pdf).
16. Ongaro, D., and Ousterhout, J. 2014. [In Search of an Understandable Consensus Algorithm. USENIX ATC, 305–319](https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro).
17. Laurie, B., Messeri, E., and Stradling, R. 2021. [Certificate Transparency Version 2.0. RFC 9162](https://www.rfc-editor.org/rfc/rfc9162.html).
18. Saltzer, J. H., and Schroeder, M. D. 1975. [The Protection of Information in Computer Systems, Basic Principles](https://web.mit.edu/Saltzer/www/publications/protection/Basic.html).

## Índice de evidencia de fuentes

Las etiquetas siguientes describen los grupos de evidencia privada sin revelar ubicaciones de repositorios, registros operativos ni código fuente. El mapa de revisión, controlado por separado, proporciona localizadores y límites exactos.

- **I01** Inventario de identidad de fuentes, comparación actual de fuentes aceptadas y limitaciones de alcance.
- **I02** Canonicalización, dominios Unicode/JSON aceptados y análisis del formato de transmisión.
- **I03** Recepción, pasarela autenticada, intentos duraderos, admisión y controles efectivos.
- **I04** Testigo de bytes construido, dominios exactos de serialización y cálculos de coordenadas.
- **I05** Fundamentación, puente semántico determinista, cuarentena y contratos de candidatos y mapas de afirmaciones.
- **I06** Adaptadores de proveedores, transporte acotado, normalización y custodia de finalización.
- **I07** Ejes UCM, proyección de hipótesis, umbrales y alcance de incertidumbre de la ruta ordinaria.
- **I08** Forma de onda de referencia, búsqueda de contraejemplos, Aperture y ruta PMR ordinaria sin escritura.
- **I09** Modelos AHA existentes de casos suministrados, motor, envoltura y alcance de auditoría independiente.
- **I10** Recálculo Sophia, orientación Atlas, sellado y límite de revisión humana.
- **I11** Espacios de nombres GUFT conciliados y productores y consumidores históricos de pruebas comparativas y series temporales.
- **I12** Ecuaciones de investigación de aguas cognitivas, núcleos reducidos, sustituciones reales de parámetros por invocadores y recursión.
- **I13** Linaje local Analyst/Challenge/Synthesis e implementaciones históricas de múltiples funciones.
- **I14** Transferencia de artefactos entre pares, interfaces de integración de emisor/receptor de modelos, concesiones vigentes y consumidores de Challenge externo.
- **I15** Límites de diseño de gramática compartida, comparación, retención y ciclo de vida de dependencias.
- **I16** Procedencia de custodia/TEL y observación acotada de la carga de acción.
- **I17** Copias que contienen contenido, caducidad con alcance definido y límites de borrado no resueltos.
- **I18** Pruebas redactadas e informes históricos de validación vinculados al código fuente, no ejecutados de nuevo aquí.
- **I19** Complemento legible por máquina y contrato de consistencia elaborados para este artículo.
- **I20** Lagunas de evidencia restantes y separación entre propuestas y código fuente aceptado.

## Apéndice A Pseudocódigo de la ruta de llamadas

El siguiente pseudocódigo es explicativo y se ha reconstruido a partir de los responsables inspeccionados. No es código fuente privado, una integración ejecutable ni una especificación de protocolo de autorización. Las rutas de error están abreviadas; cada estado debe ser conservado por su responsable real. [I03–I10]

```text
procedure observed_application_task(task_bytes, authenticated_application):
    attempt := custody.register_attempt(task_bytes, authenticated_application)
    admitted := custody.admit(attempt, effective_controls, runtime_bindings)
    if admitted is not admissible: return inspectable_status(attempt, admitted)

    if admitted.kind is NON_MODEL_EVENT:
        return record_event_without_model_candidate(admitted)

    release := require_exact_dispatch_authority(admitted.identity)
    claim := custody.claim_and_reserve(admitted, release, current_limits)
    transport_observation := bounded_provider_call(claim.provider_body)
    captured := custody.commit_and_recompute_normalization(transport_observation)

    if effective_controls.analysis_mode is CAPTURE_ONLY:
        return retained_capture_with_native_stages_not_executed(captured)
    if captured.state is not CAPTURED:
        return noncandidate_completion_projection(captured)

    native_grounding := build_from_already_normalized_source(admitted)
    semantic_capture := exact_substring_claim_proposal(captured.text, native_grounding)
    semantic_capture.uncertainty := 1.0  // this exact bridge contract
    bind_distinct_identities(provider_body, normalized_envelope, semantic_capture)
    native_artifacts := captured_candidate_core(semantic_capture, native_grounding)
    audit := separately_claimed_sophia_recomputation(native_artifacts.raw_free_bundle)
    posture := atlas_orientation(native_artifacts, audit)
    tel := finalize_only_returned_stages(native_artifacts, audit, posture)
    sealed := seal_exact_inventory(native_artifacts, audit, posture, tel)
    return inspectable_result(sealed, separate_human_decision_pending)
```

## Apéndice B Complemento legible por máquina

`CLAIM_LEDGER.json` asigna a cada afirmación principal basada en las fuentes o deducción una clase de evidencia, un alcance, dependencias, limitaciones y una ubicación en el manuscrito. `TRANSFORMATION_GRAPH.json` distingue enlaces observados en las fuentes, deducciones condicionales y propuestas. `BYTE_WITNESS.json` contiene únicamente cargas útiles construidas no privadas e identidades exactas de bytes. `QUANTITY_CATALOG.json` es un catálogo selectivo que preserva alias de fórmulas y estimadores, entradas, unidades, productores, consumidores, clases de evidencia, datos ausentes y recorte o redondeo. La omisión de un elemento en este catálogo selectivo no implica falta de disponibilidad. Los alias opacos de estimadores se resuelven a versiones privadas exactas o a identidades matemáticas explícitamente genéricas. `COMPANION_SCHEMA.json` describe el contrato sintáctico del registro de afirmaciones. `validate_companion.py` comprueba invariantes de identificadores entre archivos, dependencias, enlaces del grafo, secciones, testigos y manifiesto, sin modificaciones ni uso de red; esas comprobaciones procedimentales exceden lo que expresa JSON Schema. Ninguna de las dos validaciones establece la verdad científica. `MANIFEST.json` vincula los archivos públicos candidatos sin incluir su propio hash. Estos archivos son nuevos artefactos explicativos, no estado exportado del producto ni una API de producción. [I19]

El grafo es un mapa selectivo de relaciones condicionales, no una secuencia de ejecución ni un grafo exhaustivo de flujo de control. Cada enlace declara su relación, evidencia y condición; las integraciones de modelos entre pares no establecidas siguen siendo conceptuales, y los nodos de propuesta tienen identificadores distintos de los identificadores de referencia. El complemento debe preservar tres invariantes: ningún resultado de clase D se reetiqueta como ejecutado; no se asigna cero a ninguna magnitud no disponible; y ningún enlace de identidad o procedencia se reetiqueta como verdad o autoridad de acción. El mapa privado de revisión queda excluido del conjunto público de archivos candidatos. Las dos rondas completas de revisión técnica y los 31 hallazgos cerrados pertenecen a la predecesora congelada, la versión 1. La sucesora añade las afirmaciones C078 y C079 con alcance explícito de hipótesis y diseño normativo; la revisión correspondiente a los cambios se registra por separado. La publicación sigue siendo una acción autorizada por separado.
