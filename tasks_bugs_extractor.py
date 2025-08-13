import os
import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

# --- CONFIGURACIÓN ---
# ¡IMPORTANTE! Se recomienda usar variables de entorno para el PAT por seguridad.
# El script intentará leer la variable 'AZURE_DEVOPS_PAT'.
# Si no la encuentra, usará el valor de fallback (NO RECOMENDADO para producción).
# PAT = os.getenv('AZURE_DEVOPS_PAT', 'TU_PAT_DE_FALLBACK_AQUI') 
PAT = ''
ORGANIZATION = 'BlacknBlue'
PROJECT = 'Black and Blue'

# Define los tipos de Work Items que quieres extraer
WORK_ITEM_TYPES = ['Task', 'Bug', 'Issue']

# Define los campos que quieres en tu Excel final.
FIELDS_TO_EXTRACT = [
    'System.Title',
    'System.AssignedTo',
    'System.State',
    'System.CreatedBy',
    'System.IterationPath',
    'System.Tags',
    'System.CreatedDate',
    'Microsoft.VSTS.Common.ClosedDate',
    'Microsoft.VSTS.Scheduling.OriginalEstimate',
    'Microsoft.VSTS.Scheduling.RemainingWork',
    'Microsoft.VSTS.Scheduling.CompletedWork',
]

# Nombre del archivo de salida
OUTPUT_FILENAME = 'azure_devops_work_items.xlsx'
# --------------------

def fetch_work_item_details(ids, auth_headers):
    """Obtiene los detalles completos de los work items en lotes."""
    work_item_details = []
    batch_size = 200
    for i in range(0, len(ids), batch_size):
        batch_ids = ids[i:i + batch_size]
        ids_str = ','.join(map(str, batch_ids))
        details_url = f'https://dev.azure.com/{ORGANIZATION}/_apis/wit/workitems?ids={ids_str}&$expand=relations&api-version=7.0'
        
        try:
            response = requests.get(details_url, headers=auth_headers['headers'], auth=auth_headers['auth'])
            response.raise_for_status()
            data = response.json().get('value', [])
            work_item_details.extend(data)
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener detalles del lote de work items: {e}")
            continue
            
    return work_item_details

def fetch_parent_titles(parent_ids, auth_headers):
    """Obtiene los títulos de los work items padres."""
    if parent_ids.size == 0:
        return {}
    
    ids_str = ','.join(map(str, parent_ids))
    parent_url = f'https://dev.azure.com/{ORGANIZATION}/_apis/wit/workitems?ids={ids_str}&fields=System.Title&api-version=7.0'
    
    try:
        response = requests.get(parent_url, headers=auth_headers['headers'], auth=auth_headers['auth'])
        response.raise_for_status()
        parent_details = response.json().get('value', [])
        return {str(parent['id']): parent['fields']['System.Title'] for parent in parent_details}
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener títulos de los padres: {e}")
        return {}


def main():
    """Función principal para orquestar la extracción y el procesamiento de datos."""
    print("🚀 Iniciando extracción de Work Items de Azure DevOps...")
    
    auth_headers = {
        'headers': {'Content-Type': 'application/json'},
        'auth': HTTPBasicAuth('', PAT)
    }

    # 1. Construir y ejecutar la consulta WIQL para obtener IDs
    types_str = ', '.join(f"'{item_type}'" for item_type in WORK_ITEM_TYPES)
    
    wiql_query = {
        "query": f"""
            SELECT [System.Id]
            FROM workitems
            WHERE [System.WorkItemType] IN ({types_str})
              AND [System.TeamProject] = @project
            ORDER BY [System.Id]
        """
    }

    wiql_url = f'https://dev.azure.com/{ORGANIZATION}/{PROJECT}/_apis/wit/wiql?api-version=7.0'
    
    try:
        response = requests.post(wiql_url, json=wiql_query, headers=auth_headers['headers'], auth=auth_headers['auth'])
        response.raise_for_status()
        work_items_ref = response.json().get('workItems', [])
        work_item_ids = [item['id'] for item in work_items_ref]
    except requests.exceptions.RequestException as e:
        print(f"Error fatal en la consulta WIQL inicial: {e}")
        print(f"Detalles: {response.text if 'response' in locals() else 'No response'}")
        return

    if not work_item_ids:
        print("✅ No se encontraron work items para los tipos especificados. ¡Todo listo!")
        return

    print(f"🔍 Se encontraron {len(work_item_ids)} work items. Obteniendo detalles...")

    # 2. Obtener detalles completos de todos los work items
    all_details = fetch_work_item_details(work_item_ids, auth_headers)

    # 3. Procesar los detalles
    processed_items = []
    for item in all_details:
        fields = item.get('fields', {})
        
        data_row = {field: fields.get(field) for field in FIELDS_TO_EXTRACT}
        
        # Corrección: Obtener el ID del nivel superior para evitar que esté vacío
        data_row['ID'] = item.get('id')
        
        data_row['Work Item Type'] = fields.get('System.WorkItemType', 'N/A')
        
        # Limpiar nombres de campos complejos (Assigned To, Created By)
        assigned_to = fields.get('System.AssignedTo')
        data_row['System.AssignedTo'] = assigned_to['displayName'] if assigned_to else 'Unassigned'
        
        created_by = fields.get('System.CreatedBy')
        data_row['System.CreatedBy'] = created_by['displayName'] if created_by else 'N/A'
        
        # Formatear Tags
        tags = data_row.get('System.Tags')
        data_row['System.Tags'] = tags.replace(';', ',') if tags else ''
        
        # Buscar ID del padre
        parent_id = None
        if 'relations' in item:
            for relation in item['relations']:
                if relation.get('rel') == 'System.LinkTypes.Hierarchy-Reverse':
                    parent_url = relation.get('url', '')
                    parent_id = parent_url.split('/')[-1]
                    break
        data_row['Parent ID'] = parent_id
        
        processed_items.append(data_row)
        
    if not processed_items:
        print("❌ No se pudieron procesar los detalles de los work items.")
        return

    # 4. Convertir a DataFrame y enriquecer con títulos de padres
    df = pd.DataFrame(processed_items)
    
    df.rename(columns={
        'System.Title': 'Title',
        'System.AssignedTo': 'Assigned To',
        'System.State': 'State',
        'System.CreatedBy': 'Created By',
        'System.IterationPath': 'Iteration Path',
        'System.Tags': 'Tags',
        'System.CreatedDate': 'Created Date',
        'Microsoft.VSTS.Common.ClosedDate': 'Closed Date',
        'Microsoft.VSTS.Scheduling.OriginalEstimate': 'Original Estimate',
        'Microsoft.VSTS.Scheduling.RemainingWork': 'Remaining Work',
        'Microsoft.VSTS.Scheduling.CompletedWork': 'Completed Work'
    }, inplace=True)

    parent_ids_to_fetch = df[df['Parent ID'].notna()]['Parent ID'].unique()
    print(f"📚 Obteniendo títulos para {len(parent_ids_to_fetch)} padres...")
    parent_titles = fetch_parent_titles(parent_ids_to_fetch, auth_headers)
    
    df['Parent Title'] = df['Parent ID'].map(parent_titles).fillna('N/A')

    # 5. Organizar columnas y guardar el archivo Excel
    final_columns = [
        'ID', 'Work Item Type', 'Title', 'State', 'Assigned To', 'Created By',
        'Parent ID', 'Parent Title', 'Iteration Path', 'Tags', 'Created Date', 'Closed Date',
        'Original Estimate', 'Remaining Work', 'Completed Work'
    ]
    
    df_final = df.reindex(columns=final_columns)

    try:
        df_final.to_excel(OUTPUT_FILENAME, index=False, engine='openpyxl')
        print(f"✅ ¡Éxito! Datos exportados correctamente a '{OUTPUT_FILENAME}'")
    except Exception as e:
        print(f"❌ Error al guardar el archivo Excel: {e}")

if __name__ == '__main__':
    main()