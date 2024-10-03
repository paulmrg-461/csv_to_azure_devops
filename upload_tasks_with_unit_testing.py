import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

# Configuración
organization = 'BlacknBlue'
project = 'Black and Blue'
pat = os.getenv('AZURE_DEVOPS_PAT') 
azure_devops_url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$Task?api-version=6.0'

# Leer el archivo CSV
csv_file_path = './tasks.csv'
tasks_df = pd.read_csv(csv_file_path)

# Lista para almacenar la información de las tareas creadas
created_tasks = []

# Función para crear una tarea en Azure DevOps y asignarla a un User Story
def create_task(title, description, priority, user_story_id, sprint, assigned_to, original_estimate, unit_test=False):
    headers = {
        'Content-Type': 'application/json-patch+json',
    }

    # Ajustar título y descripción si es una tarea de pruebas unitarias
    if unit_test:
        title = f'[Tarea][Pruebas Unitarias]: {title}'
        description = f'{description}\n\nEsta tarea corresponde a las pruebas unitarias.'
        original_estimate = round(original_estimate * 0.3, 2)  # 30% del tiempo de la tarea original

    data = [
        {
            'op': 'add',
            'path': '/fields/System.Title',
            'value': title,
        },
        {
            'op': 'add',
            'path': '/fields/System.Description',
            'value': description,
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

# Crear tareas y tareas de pruebas unitarias a partir del DataFrame y asignarlas a User Stories
for index, row in tasks_df.iterrows():
    # Crear la tarea principal
    create_task(
        row['Title'], 
        row['Description'], 
        row['Priority'], 
        row['UserStoryID'], 
        row['Sprint'], 
        row['AssignedTo'], 
        row['OriginalEstimate']
    )

    # Crear la tarea adicional para pruebas unitarias
    create_task(
        row['Title'], 
        row['Description'], 
        row['Priority'], 
        row['UserStoryID'], 
        row['Sprint'], 
        row['AssignedTo'], 
        row['OriginalEstimate'],
        unit_test=True  # Indica que es una tarea de pruebas unitarias
    )

# Convertir la lista de tareas creadas a un DataFrame de pandas
created_tasks_df = pd.DataFrame(created_tasks)

# Exportar el DataFrame a un archivo Excel
output_file = './created_tasks_with_unit_tests.xlsx'
created_tasks_df.to_excel(output_file, index=False)

print(f'Datos exportados a {output_file}')
