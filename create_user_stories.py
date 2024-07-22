import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

# Configuración
organization = 'BlacknBlue'
project = 'Black and Blue'
pat = 'PATH'
azure_devops_url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$User%20Story?api-version=6.0'

# Leer el archivo CSV
us_csv_file = './user_stories.csv'
user_stories_df = pd.read_csv(us_csv_file)

# Función para crear una User Story en Azure DevOps
def create_user_story(title, description, priority, sprint):
    headers = {
        'Content-Type': 'application/json-patch+json',
    }

    data = [
        {
            'op': 'add',
            'path': '/fields/System.Title',
            'value': f'[KeyResult]: {title}',
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

    response = requests.post(
        azure_devops_url,
        auth=HTTPBasicAuth('', pat),
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        user_story_id = response.json()['id']
        print(f'User Story "{title}" creada con éxito con ID {user_story_id}.')
    else:
        print(f'Error al crear la User Story "{title}". Status Code: {response.status_code}')
        try:
            print(response.json())
        except ValueError:
            print(response.text)

# Crear User Stories a partir del DataFrame
for index, row in user_stories_df.iterrows():
    create_user_story(
        row['Title'], 
        row['Description'], 
        row['Priority'], 
        row['Sprint']
    )
