# Documentation
# https://github.com/googleapis/google-api-python-client
# https://developers.google.com/resources/api-libraries/documentation/cloudresourcemanager/v2/python/latest/

# Library Installation
# pip install -U google-api-python-client
# pip install -U oauth2client

# Requires one of the following scopes
# https://www.googleapis.com/auth/cloud-platform
# https://www.googleapis.com/auth/cloud-platform.read-only
# https://www.googleapis.com/auth/cloudplatformprojects
# https://www.googleapis.com/auth/cloudplatformprojects.readonly


from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from google.oauth2 import service_account
from google.cloud import bigquery

def get_tables(project):
    client = bigquery.Client(project=project)
    datasets = list(client.list_datasets())  # Make an API request.
    project = client.project
    #print("Project : {}".format(project))

    if datasets:
        #print("== Datasets in project {}:".format(project))
        for dataset in datasets:
            #print("= DATASET: {}".format(dataset.dataset_id))
            tables = client.list_tables(dataset.dataset_id)

            #print("Tables contained in '{}':".format(dataset.dataset_id))
            for table in tables:
                print("{}.{}.{}".format(table.project, table.dataset_id, table.table_id))

# Example using the Python Client Library

#print('{:<20}\t\t\t{:<22}\t\t\t{:<21}'.format('PROJECT_ID', 'NAME', 'PROJECT_NUMBER'))

# Uncomment to use Application Default Credentials (ADC)
credentials = GoogleCredentials.get_application_default()

# Uncomment to use Service Account Credentials in Json format
# credentials = service_account.Credentials.from_service_account_file('service-account.json')

service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)

request = service.projects().list()

while request is not None:
    response = request.execute()

    for project in response.get('projects', []):
        #print('{:<20}\t\t\t{:<22}\t\t\t{:<21}'.format(project['projectId'], project['name'], project['projectNumber']))
        try:
            get_tables(project['projectId'])
        except:
            #print()
            Ok=False
    request = service.projects().list_next(previous_request=request, previous_response=response)


