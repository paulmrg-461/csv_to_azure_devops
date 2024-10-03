import os
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

# Configuración
organization = 'BlacknBlue'
project = 'Black and Blue'
pat = os.getenv('AZURE_DEVOPS_PAT') 

azure_devops_url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=6.0'

wiql_query = {
    "query": """
        SELECT [System.Id], [System.Title], [System.AssignedTo], [System.State], [System.IterationPath], [System.WorkItemType]
        FROM workitems
        WHERE [System.WorkItemType] = 'Issue'
        ORDER BY [System.Id]
    """
}

headers = {
    'Content-Type': 'application/json',
}

response = requests.post(
    azure_devops_url,
    auth=HTTPBasicAuth('', pat),
    headers=headers,
    json=wiql_query
)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    work_items = response.json()['workItems']

    # Extraer IDs de los Work Items obtenidos
    work_item_ids = [item['id'] for item in work_items]

    # URL para obtener los detalles de los Work Items por ID
    ids_url = f'https://dev.azure.com/{organization}/_apis/wit/workitems?ids={",".join(map(str, work_item_ids))}&api-version=6.0'

    # Obtener los detalles de cada Work Item
    details_response = requests.get(
        ids_url,
        auth=HTTPBasicAuth('', pat),
        headers=headers
    )

    if details_response.status_code == 200:
        work_item_details = details_response.json()['value']

        # Preparar los datos para exportarlos
        work_items_data = []
        for work_item in work_item_details:
            item_data = {
                'ID': work_item['id'],
                'Title': work_item['fields'].get('System.Title', 'N/A'),
                'Assigned To': work_item['fields'].get('System.AssignedTo', {}).get('displayName', 'Unassigned'),
                'State': work_item['fields'].get('System.State', 'N/A'),
                'Iteration': work_item['fields'].get('System.IterationPath', 'N/A')
            }
            
            # Añadir los datos a la lista
            work_items_data.append(item_data)

        # Convertir los datos a un DataFrame
        df = pd.DataFrame(work_items_data)

        # Exportar a un archivo Excel
        output_file = './azure_devops_issues2.xlsx'
        df.to_excel(output_file, index=False)

        print(f'Datos exportados a {output_file}')
    else:
        print(f'Error al obtener detalles de los Work Items: {details_response.status_code}')
else:
    print(f'Error en la solicitud WIQL: {response.status_code}')