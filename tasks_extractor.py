import os
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

# Configuración
organization = 'BlacknBlue'
project = 'Black and Blue'
pat = ''

# URL base de Azure DevOps
azure_devops_url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=6.0'

# WIQL query para obtener las tareas (Tasks)
wiql_query = {
    "query": """
        SELECT [System.Id], [System.Title], [System.AssignedTo], [System.State], [System.IterationPath], 
               [Microsoft.VSTS.Scheduling.CompletedWork], [Microsoft.VSTS.Scheduling.OriginalEstimate], 
               [System.WorkItemType]
        FROM workitems
        WHERE [System.WorkItemType] = 'Task'
        ORDER BY [System.Id]
    """
}

# Encabezados de la solicitud
headers = {
    'Content-Type': 'application/json',
}

# Realizar la solicitud WIQL
response = requests.post(azure_devops_url, auth=HTTPBasicAuth('', pat), headers=headers, json=wiql_query)

if response.status_code == 200:
    work_items = response.json().get('workItems', [])
    if not work_items:
        print("No se encontraron tareas.")
        exit()

    # Extraer IDs de Work Items
    work_item_ids = [item['id'] for item in work_items]

    # Procesar en lotes para evitar errores por límite de IDs
    batch_size = 100
    work_items_data = []
    for i in range(0, len(work_item_ids), batch_size):
        batch = work_item_ids[i:i + batch_size]
        ids_url = f'https://dev.azure.com/{organization}/_apis/wit/workitems?ids={",".join(map(str, batch))}&$expand=relations&api-version=6.0'
        details_response = requests.get(ids_url, auth=HTTPBasicAuth('', pat), headers=headers)

        if details_response.status_code == 200:
            work_item_details = details_response.json().get('value', [])
            for work_item in work_item_details:
                fields = work_item['fields']

                # Obtener ID de la User Story (Parent)
                parent_id = 'N/A'
                if 'relations' in work_item:
                    for relation in work_item['relations']:
                        if relation['rel'] == 'System.LinkTypes.Hierarchy-Reverse':
                            parent_url = relation['url']
                            parent_id = parent_url.split('/')[-1]
                            break

                # Obtener el nombre del asignado
                assigned_to = 'Unassigned'
                if 'System.AssignedTo' in fields and fields['System.AssignedTo'] is not None:
                    assigned_to = fields['System.AssignedTo'].get('displayName', 'Unassigned')

                task_data = {
                    'ID User Story': parent_id,
                    'Title User Story': 'To be fetched later',
                    'ID Tarea': work_item['id'],
                    'Nombre Tarea': fields.get('System.Title', 'N/A'),
                    'Assigned To': assigned_to,
                    'State': fields.get('System.State', 'N/A'),
                    'Iteration': fields.get('System.IterationPath', 'N/A'),
                    'Completed Work': fields.get('Microsoft.VSTS.Scheduling.CompletedWork', 0),
                    'Original Estimate': fields.get('Microsoft.VSTS.Scheduling.OriginalEstimate', 0),
                    # Nuevas columnas añadidas
                    'Created Date': fields.get('System.CreatedDate', 'N/A'),
                    'Closed Date': fields.get('Microsoft.VSTS.Common.ClosedDate', 'N/A')
                }
                work_items_data.append(task_data)
        else:
            print(f"Error al obtener detalles del batch: {details_response.status_code}")
            print(f"Detalles: {details_response.text}")
            continue

    # Obtener los títulos de las User Stories relacionadas
    parent_ids = {item['ID User Story'] for item in work_items_data if item['ID User Story'] != 'N/A'}
    if parent_ids:
        parent_ids_url = f'https://dev.azure.com/{organization}/_apis/wit/workitems?ids={",".join(parent_ids)}&api-version=6.0'
        parent_response = requests.get(parent_ids_url, auth=HTTPBasicAuth('', pat), headers=headers)

        if parent_response.status_code == 200:
            parent_details = parent_response.json().get('value', [])
            parent_titles = {str(parent['id']): parent['fields']['System.Title'] for parent in parent_details}

            # Asignar los títulos de las User Stories a las tareas
            for task in work_items_data:
                if task['ID User Story'] in parent_titles:
                    task['Title User Story'] = parent_titles[task['ID User Story']]
        else:
            print(f"Error al obtener títulos de User Stories: {parent_response.status_code}")
            print(f"Detalles: {parent_response.text}")

    # Convertir los datos a un DataFrame
    df = pd.DataFrame(work_items_data)

    # Exportar a un archivo Excel
    output_file = './azure_devops_tasks.xlsx'
    df.to_excel(output_file, index=False)

    print(f'Datos exportados a {output_file}')
else:
    print(f"Error en la consulta WIQL: {response.status_code}")
    print(f"Detalles: {response.text}")