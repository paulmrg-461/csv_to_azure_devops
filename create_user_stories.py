import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

# Configuración
# organization = 'GrupoLevapan'
# project = 'IA_aplicada'
organization = 'BlacknBlue'
project = 'Black and Blue'
pat = os.getenv('AZURE_DEVOPS_PAT') 
azure_devops_url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$User%20Story?api-version=6.0'

# Leer el archivo CSV
us_csv_file = './user_stories.csv'
user_stories_df = pd.read_csv(us_csv_file)

created_user_stories = []

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
        user_story = response.json()
        user_story_id = user_story['id']
        created_date = user_story['fields']['System.CreatedDate']
        print(f'User Story "{title}" creada con éxito con ID {user_story_id}.')

        # Guardar la información en la lista
        created_user_stories.append({
            'ID': user_story_id,
            'Title': title,
            'Description': description,
            'Sprint': sprint,
            'Created Date': created_date
        })
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

# Convertir la lista de User Stories creadas a un DataFrame de pandas
created_user_stories_df = pd.DataFrame(created_user_stories)

# Exportar el DataFrame a un archivo Excel
output_file = './created_user_stories1.xlsx'
created_user_stories_df.to_excel(output_file, index=False)

print(f'Datos exportados a {output_file}')