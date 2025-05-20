# Model Context Protocol (MCP)
>>> Curso seguido de este [enlace](https://mcp.collabnix.com/labs/01-getting-started/index.html)

Estándar que proporciona una manera universal de conectar modelos IA y aplicaciones de agentes con varios conjuntos de datos y herramientas. Esto permite a los modelos de inteligencia arificial interactuar con sistemas y datos externos.

**MCP** esta formado de una arquitectura cliente servidor con una asignación de roles.
- *Host*:  La aplicación que necesita utilizar herramientas externas. *Ejemplo IDE como Cursor, VSCODE*.
- *Server*: Componente que expone diferentes capacidades(tools) a través del protocolo.
- *Client*:  Librería que maneja la comunicación entre *host* y * servidor*.


Componentes del model context protocol:

- **Recursos**: Similar en el protocolo HTTP las peticiones GET, en este caso proporciona contexto al modelo.
```python
@mcp.resource("users://{user_id}/profile")
def get_user_name(user_id:str)->str:
    return "PepeDomingo"
```
- **Tools**: Similar en el protocolo HTTP las peticiones POST, proporciona las acciones que puede realizar el modelo.
```python
@mcp.tool()
def calculate_max_squat(weight_Ñkg:float, height_m:float)-> float:
    return weight_kg * height_m
```
- **Prompts**: plantillas de prompts para el modelo.

```python
@mcp.prompt()
def build_routine(workouts_per_week:int)->str
    return f"Build workout routine for training {workouts_per_weeek} times per week"

```


Como funciona:
1. Inicialización:
2. Intercambio de mensajes: Usando el formato JSON-RPC 
3. Transporte: Existen 3 modos de transporte actualmente soportados.


| **Modo de Transporte** | **Descripción**                                                                                     | **Ventajas**                                                                                       | **Desventajas**                                                                                   |
|-------------------------|-----------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `stdio`                | Utiliza la entrada y salida estándar (stdin/stdout) para la comunicación entre procesos locales.    | - Fácil de configurar. <br> - No depende de la red, rápido y seguro para entornos locales.         | - Limitado a procesos locales. <br> - No es adecuado para aplicaciones distribuidas.             |
| `sse`                  | Utiliza eventos enviados por el servidor a través de HTTP para mantener una conexión unidireccional en tiempo real. | - Permite actualizaciones en tiempo real. <br> - Más eficiente que el sondeo continuo.            | - Solo permite comunicación unidireccional (del servidor al cliente).                            |
| `streamable-http`      | Utiliza HTTP para establecer una conexión bidireccional que permite intercambiar datos en tiempo real. | - Compatible con redes y aplicaciones distribuidas. <br> - Permite flujos de datos más completos. | - Requiere una configuración más compleja. <br> - Puede ser menos eficiente en entornos locales. |



## Primer MCP SERVER

Con el objetivo de implementar nuestro primer servidor MCP utilizamos la librería`FastMCP`.

En el servidor definimos la siguiente counfiguración.


```
mcp = FastMCP(
    name="MLExpert Server",
    host="localhost",
    port=9999,
    sse_path="/sse"
)
```

Los parámetros definidos son los siguientes:
* **name**: Nombre que le vamos a asignar al servidor.
* **host**: URL en la que el servidor se va desplegar.
* **port**: Puerto del servidor que va a antender a las conexiones restantes will use to listen for incoming connections
* **sse_path**: Dirección del servidor que va atender las peticiones `Server-Sent Events (SSE)`.

> `sse_path`se utiliza cuando se define como medio de transporte sse_path.



In order to test our server we use a tool called **model contextprotocol inspector**, in which we can test our **mcp elements**. In order to use it we execute this command.

Para poder probar nuestro servidor utilizamos una herrarmienta denominada **model contextprotocol inspector**, en la cual podemos probar diferentes **mcp elements**. El comando a ejecutar es el sigiuente.

```bash
npx @modelcontextprotocol/inspector
```

Tras ejecutar este comando tendremos disponible una url en la que podemos testear los diferentes parámetros.

# Primer MCP Client.

La librería que utilizaremos para desarrollar nuestro cliente es [`langchain-mcp-adapters`](https://github.com/langchain-ai/langchain-mcp-adapters). Esta librería proporiciona un wrapper ligerito que hace que herramientas desarrolladas con MCP sean compatibles con `Langchain` y `Langraph`

En nuestro caso, al no disponer de acceso a modelos privados como **ChatGPT** y **CLAUDE** usamos esta librería en combinación con **Ollama** que permite desplegar modelos generativos en local. Listado de modelos con compatibilidad para utilizar modelos de Ollama se encuentran en este [enlace](https://ollama.com/search?c=tools)


El cliente funciona de la siguiente manera:
1. Inicializamos los servidores MCP que vamos a consumir.
2. Consultamos a los servidores las **tools** que vamos a utilizar.
3. Cargamos el modelo y le pasamos el prompt al problema que le planteamos.
4. Obtenemos la salida del modelo.







