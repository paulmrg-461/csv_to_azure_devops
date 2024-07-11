
# Azure DevOps Automation: Creating User Stories and Tasks

This project contains scripts to automate the creation of User Stories and Tasks in Azure DevOps from a CSV file. The scripts will also assign tasks to User Stories within specific Sprints.

## Prerequisites

- Python 3.x installed on your machine
- Azure DevOps account and organization
- Personal Access Token (PAT) with sufficient permissions to create and manage work items
- CSV files containing User Stories and Tasks

## Setup

1. **Clone the repository** (if you are using version control):

    ```bash
    git clone https://github.com/your-repo/azure-devops-automation.git
    cd azure-devops-automation
    ```

2. **Install required Python packages**:

    ```bash
    pip install pandas requests
    ```

## Generate a Personal Access Token (PAT)

1. Sign in to [Azure DevOps](https://dev.azure.com/).
2. Click on your profile picture in the top right corner and select `Security`.
3. In the `Personal Access Tokens` section, click `New Token`.
4. Configure the token with the necessary permissions (`Work Items: Read & Write`) and click `Create`.
5. Copy the token and keep it secure. You will not be able to view it again.

## Creating User Stories

1. **Prepare the CSV file**:
    - Create a CSV file (`user_stories.csv`) with the following columns: `Title`, `Description`, `Priority`, `Sprint`.
    - Example:

        | Title            | Description        | Priority | Sprint                  |
        |------------------|--------------------|----------|-------------------------|
        | User Story 1     | Description of US1 | 1        | Project\Sprint 1        |
        | User Story 2     | Description of US2 | 2        | Project\Sprint 1        |
        | User Story 3     | Description of US3 | 3        | Project\Sprint 2        |

2. **Run the script to create User Stories**:

    ```python
    import pandas as pd
    import requests
    from requests.auth import HTTPBasicAuth

    # Configuración
    organization = 'your-organization'  # Replace with your organization
    project = 'your-project'  # Replace with your project
    pat = 'your-pat-token'  # Replace with your PAT
    azure_devops_url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$User%20Story?api-version=6.0'

    # Leer el archivo CSV
    csv_file = 'user_stories.csv'
    user_stories_df = pd.read_csv(csv_file)

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
    ```

## Creating Tasks and Associating them with User Stories

1. **Prepare the CSV file**:
    - Create a CSV file (`tasks.csv`) with the following columns: `Title`, `Description`, `Priority`, `UserStoryID`, `Sprint`.
    - Example:

        | Title             | Description          | Priority | UserStoryID | Sprint                  |
        |-------------------|----------------------|----------|-------------|-------------------------|
        | Task 1            | Description of Task1 | 1        | 12345       | Project\Sprint 1        |
        | Task 2            | Description of Task2 | 2        | 12345       | Project\Sprint 1        |
        | Task 3            | Description of Task3 | 3        | 67890       | Project\Sprint 2        |

2. **Run the script to create Tasks and associate them with User Stories**:

    ```python
    import pandas as pd
    import requests
    from requests.auth import HTTPBasicAuth

    # Configuración
    organization = 'your-organization'  # Replace with your organization
    project = 'your-project'  # Replace with your project
    pat = 'your-pat-token'  # Replace with your PAT
    azure_devops_url = f'https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$Task?api-version=6.0'

    # Leer el archivo CSV
    csv_file_path = 'tasks.csv'
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
    ```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Feel free to customize the scripts and CSV files according to your specific requirements. If you encounter any issues or have questions, please refer to the Azure DevOps REST API documentation or reach out for support.
