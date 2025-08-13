import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import json
import os

# Configuración
organization = 'BlacknBlue'
project = 'Black and Blue'
pat = os.getenv('AZURE_DEVOPS_PAT')
azure_devops_url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$Task?api-version=6.0'

# Configuración de Deepseek API
deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
deepseek_api_url = 'https://api.deepseek.com/v1/chat/completions'

csv_file_path = './tasks.csv'
tasks_df = pd.read_csv(
    csv_file_path,
    sep='\t',                   # Usa tabulaciones como separador
    encoding='utf-8'            # Especifica UTF-8 explícitamente
)
# Lista para almacenar la información de las tareas creadas
created_tasks = []

# Función para generar descripción y sugerencia con IA
def generate_ai_content(title, module, description):
    prompt = f"""
Instrucciones Generales:
Eres un asistente especializado en la generación de tareas técnicas para el desarrollo de software. Tu objetivo es crear tareas claras, detalladas y estructuradas para los desarrolladores del proyecto Black & Blue. A continuación, se describe el contexto del proyecto, las tecnologías utilizadas y las instrucciones específicas para la creación de tareas.

Descripción del Proyecto Black & Blue:
El proyecto Black & Blue es una aplicación de videovigilancia diseñada para monitorear eventos en tiempo real y gestionar grabaciones históricas (playbacks). La aplicación está dividida en varios módulos clave:

Backend Core API: Servicios principales implementados en Python, que manejan la lógica central del sistema, como la gestión de usuarios, alarmas y eventos.
Auth: Módulo de autenticación implementado en Python, que utiliza OAuth 2.0 para permitir el inicio de sesión con email y password.
Local Core API: Servicios locales implementados en Python, que interactúan con dispositivos físicos como cámaras y procesan flujos de video.
Notifier: Servicio de notificaciones implementado en Python, que envía alertas en tiempo real a los usuarios cuando se detecta un evento relevante.
LiveViews: Módulo de visualización en vivo que utiliza Go2RTC para transmitir streams de video desde las cámaras.
Frontend: Interfaz de usuario desarrollada en Flutter, compatible con plataformas Web, Windows y Mobile (Android/iOS).

Basado en la siguiente información de tarea:
- Título: {title}
- Módulo: {module}
- Descripción: {description}

Por favor, proporciona:
1. Una descripción detallada y técnica de la tarea (máximo 150 palabras)
2. Una sugerencia concreta para resolver la tarea (máximo 300 palabras)

Responde en formato JSON con dos campos: "description" y "suggestion".
"""

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {deepseek_api_key}'
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    try:
        response = requests.post(deepseek_api_url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Intentar parsear el JSON de la respuesta
            try:
                json_content = json.loads(content)
                ai_description = json_content.get('description', '')
                ai_suggestion = json_content.get('suggestion', '')
                
                return {
                    'description': ai_description,
                    'suggestion': ai_suggestion
                }
            except json.JSONDecodeError:
                # Si no es JSON válido, intentar extraer manualmente
                print(f"Error al parsear JSON para la tarea '{title}'. Usando extracción manual.")
                
                # Buscar descripción y sugerencia en el texto
                description_start = content.find('"description"')
                suggestion_start = content.find('"suggestion"')
                
                if description_start != -1 and suggestion_start != -1:
                    # Determinar cuál viene primero
                    if description_start < suggestion_start:
                        ai_description = content[content.find(':', description_start) + 1:suggestion_start].strip()
                        ai_description = ai_description.strip('"').strip(',').strip()
                        
                        ai_suggestion = content[content.find(':', suggestion_start) + 1:].strip()
                        ai_suggestion = ai_suggestion.strip('"').strip('}').strip()
                    else:
                        ai_suggestion = content[content.find(':', suggestion_start) + 1:description_start].strip()
                        ai_suggestion = ai_suggestion.strip('"').strip(',').strip()
                        
                        ai_description = content[content.find(':', description_start) + 1:].strip()
                        ai_description = ai_description.strip('"').strip('}').strip()
                    
                    return {
                        'description': ai_description,
                        'suggestion': ai_suggestion
                    }
                
                return {
                    'description': 'No se pudo generar una descripción con IA.',
                    'suggestion': 'No se pudo generar una sugerencia con IA.'
                }
        else:
            print(f"Error en la API de Deepseek para la tarea '{title}'. Status Code: {response.status_code}")
            print(response.text)
            return {
                'description': 'No se pudo generar una descripción con IA debido a un error en la API.',
                'suggestion': 'No se pudo generar una sugerencia con IA debido a un error en la API.'
            }
    except Exception as e:
        print(f"Excepción al llamar a la API de Deepseek para la tarea '{title}': {str(e)}")
        return {
            'description': 'No se pudo generar una descripción con IA debido a un error de conexión.',
            'suggestion': 'No se pudo generar una sugerencia con IA debido a un error de conexión.'
        }

# Función para crear una tarea en Azure DevOps y asignarla a un User Story
def create_task(title, module, description, priority, user_story_id, sprint, assigned_to, original_estimate):
    headers = {
        'Content-Type': 'application/json-patch+json',
    }

    # Convertir original_estimate a float, manejando tanto enteros como decimales con coma
    try:
        if isinstance(original_estimate, str):
            original_estimate = original_estimate.replace(',', '.')
        original_estimate = float(original_estimate)
    except ValueError:
        print(f"Advertencia: El valor de 'OriginalEstimate' para la tarea '{title}' no es un número válido. Se ignorará esta tarea.")
        return

    # Calcular tiempos para la tarea y pruebas unitarias
    unit_testing_time = round(original_estimate * 0.3, 2)  # 30% del tiempo original
    task_time = round(original_estimate - unit_testing_time, 2)
    
    # Generar contenido con IA
    print(f"Generando contenido con IA para la tarea: {title}")
    ai_content = generate_ai_content(title, module, description)
    
    # Crear la descripción completa con formato HTML para Azure DevOps
    full_description = (
        f"<h2>Description</h2>"
        f"<p>{module} - {description}</p>"
        f"<h2>AI-Generated Description</h2>"
        f"<p>{ai_content['description']}</p>"
        f"<h2>AI Suggestion</h2>"
        f"<p>{ai_content['suggestion']}</p>"
        f"<h2>Inversión de horas</h2>"
        f"<ul>"
        f"<li><b>Tarea</b>: {task_time} horas</li>"
        f"<li><b>Unit Testing</b>: {unit_testing_time} horas</li>"
        f"<li><b>Total horas</b>: {original_estimate} horas</li>"
        f"</ul>"
        f"<p><i>Aplicar principios de Clean Code.</i></p>"
    )

    data = [
        {
            'op': 'add',
            'path': '/fields/System.Title',
            'value': f'[Tarea]: {title}',
        },
        {
            'op': 'add',
            'path': '/fields/System.Description',
            'value': full_description,
        },
        {
            'op': 'add',
            'path': '/fields/Microsoft.VSTS.Common.Priority',
            'value': priority,
        },
        {
            'op': 'add',
            'path': '/fields/System.IterationPath',
            'value': sprint,
        },
        {
            'op': 'add',
            'path': '/fields/System.AssignedTo',
            'value': assigned_to,
        },
        {
            'op': 'add',
            'path': '/fields/Microsoft.VSTS.Scheduling.OriginalEstimate',
            'value': original_estimate,
        },
        {
            'op': 'add',
            'path': '/fields/System.Tags',
            'value': 'New task', 
        }
    ]

    # Crear la tarea
    response = requests.post(
        azure_devops_url,
        auth=HTTPBasicAuth('', pat),
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        task = response.json()
        task_id = task['id']
        created_date = task['fields']['System.CreatedDate']
        print(f'Tarea "{title}" creada con éxito con ID {task_id}.')

        # Guardar la información en la lista
        created_tasks.append({
            'Task ID': task_id,
            'Task Title': title,
            'Module': module,
            'Description': description,
            'Estimate': original_estimate,
            'User Story ID': user_story_id,
            'Sprint': sprint,
            'Assigned To': assigned_to,
            'Created Date': created_date
        })
        
        # Asignar la tarea al User Story
        link_url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{task_id}?api-version=6.0'
        link_data = [
            {
                'op': 'add',
                'path': '/relations/-',
                'value': {
                    'rel': 'System.LinkTypes.Hierarchy-Reverse',
                    'url': f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{user_story_id}'
                }
            }
        ]
        
        link_response = requests.patch(
            link_url,
            auth=HTTPBasicAuth('', pat),
            headers=headers,
            json=link_data
        )

        if link_response.status_code == 200:
            print(f'Tarea "{title}" asociada al User Story ID {user_story_id} con éxito.')
        else:
            print(f'Error al asociar la tarea "{title}" al User Story. Status Code: {link_response.status_code}')
            print(link_response.json())
    else:
        print(f'Error al crear la tarea "{title}". Status Code: {response.status_code}')
        print(response.json())

# Crear tareas a partir del DataFrame y asignarlas a User Stories
for index, row in tasks_df.iterrows():
    create_task(
        row['Title'], 
        row['Module'],
        row['Description'], 
        row['Priority'], 
        row['UserStoryID'], 
        row['Sprint'], 
        row['AssignedTo'], 
        row['OriginalEstimate']
    )

# Convertir la lista de tareas creadas a un DataFrame de pandas
created_tasks_df = pd.DataFrame(created_tasks)

# Exportar el DataFrame a un archivo Excel
output_file = './created_tasks.xlsx'
created_tasks_df.to_excel(output_file, index=False)

print(f'Datos exportados a {output_file}')
