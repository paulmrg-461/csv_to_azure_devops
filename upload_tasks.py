import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

# Configuración
organization = 'BlacknBlue'
project = 'Black and Blue'
pat = 'YOUR_PATH'
azure_devops_url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$Task?api-version=6.0'

# Leer el archivo CSV
csv_file_path = './tasks.csv'
tasks_df = pd.read_csv(csv_file_path)

# Función para crear una tarea en Azure DevOps y asignarla a un User Story
def create_task(title, description, priority, user_story_id, sprint):
    headers = {
        'Content-Type': 'application/json-patch+json',
    }

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
        task_id = response.json()['id']
        print(f'Tarea "{title}" creada con éxito con ID {task_id}.')
        
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
    create_task(row['Title'], row['Description'], row['Priority'], row['UserStoryID'], row['Sprint'])