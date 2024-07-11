import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

# Configuración
organization = 'BlacknBlue'
project = 'Black and Blue'
pat = 'azgsb76j63h63t777rejgvbxgc4avedwglrtqodrxrq22iszbwpq'
azure_devops_url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$Task?api-version=6.0'

# ***************************CREATE USER STORIES SCRIPT**************************************

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
    ]

    response = requests.post(
        azure_devops_url,
        auth=HTTPBasicAuth('', pat),
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        print(f'User Story "{title}" creada con éxito.')
    else:
        print(f'Error al crear la User Story "{title}". Status Code: {response.status_code}')
        print(response.json())

# Crear User Stories a partir del DataFrame
for index, row in user_stories_df.iterrows():
    create_user_story(row['Title'], row['Description'], row['Priority'], row['Sprint'])
