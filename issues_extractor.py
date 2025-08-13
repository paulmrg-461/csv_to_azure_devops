import os
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd

# Configuración
organization = 'BlacknBlue'
project = 'Black and Blue'
pat = ''

azure_devops_url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=6.0'

# WIQL query para obtener los Work Items de tipo 'Issue' o 'Bug'
wiql_query = {
    "query": """
        SELECT [System.Id], 
               [System.Title], 
               [System.AssignedTo], 
               [System.State], 
               [System.IterationPath],
               [System.WorkItemType]
        FROM workitems
        WHERE [System.WorkItemType] IN ('Issue', 'Bug')
        ORDER BY [System.Id]
    """
}

# Realizar la solicitud POST para obtener la lista de Work Items
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
    work_items = response.json().get('workItems', [])

    if not work_items:
        print("No se encontraron Issues ni Bugs.")
        exit()

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
        work_item_details = details_response.json().get('value', [])

        # Preparar los datos para exportarlos
        work_items_data = []
        for work_item in work_item_details:
            fields = work_item.get('fields', {})

            # Tipo del Work Item (Issue o Bug)
            tipo = fields.get('System.WorkItemType', 'N/A')

            # Nombre del asignado (si existe)
            assigned_info = fields.get('System.AssignedTo', {})
            assigned_to = assigned_info.get('displayName', 'Unassigned')

            item_data = {
                'ID': work_item['id'],
                'Title': fields.get('System.Title', 'N/A'),
                'Assigned To': assigned_to,
                'State': fields.get('System.State', 'N/A'),
                'Iteration': fields.get('System.IterationPath', 'N/A'),
                'Type': tipo,
                'Created Date': fields.get('System.CreatedDate', 'N/A'),          # Nueva columna
                'Closed Date': fields.get('Microsoft.VSTS.Common.ClosedDate', 'N/A'),  # Nueva columna
                'Comments': ''  
            }

            # Obtener los comentarios del Work Item
            comments_url = (
                f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/'
                f'{work_item["id"]}/comments?api-version=6.0-preview.3'
            )
            comments_response = requests.get(comments_url, auth=HTTPBasicAuth('', pat), headers=headers)

            if comments_response.status_code == 200:
                comments = comments_response.json().get('comments', [])
                if comments:
                    # Concatenar los comentarios en una sola cadena separada por " | "
                    comments_text = ' | '.join([comment.get('text', '') for comment in comments])
                    item_data['Comments'] = comments_text if comments_text else 'No comments'
                else:
                    item_data['Comments'] = 'No comments'
            else:
                item_data['Comments'] = 'Error fetching comments'

            # Añadir los datos a la lista
            work_items_data.append(item_data)

        # Convertir los datos a un DataFrame
        df = pd.DataFrame(work_items_data)

        # Exportar a un archivo Excel
        output_file = './azure_devops_issues_bugs_with_comments.xlsx'
        df.to_excel(output_file, index=False)

        print(f'Datos exportados a {output_file}')
    else:
        print(f'Error al obtener detalles de los Work Items: {details_response.status_code}')
        print(details_response.text)
else:
    print(f'Error en la solicitud WIQL: {response.status_code}')
    print(response.text)