import os
from azure.storage.blob import BlockBlobService

if __name__ == "__main__":
    
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    # file and directory info
    container_name = 'datascience-data' 
    file_name = 'winequality-red.csv'
    project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    final_file_dir = os.path.join(project_dir, 'data/raw', file_name)
    
    blob = BlockBlobService(connection_string=connect_str)
    blob.get_blob_to_path(container_name, 
                          file_name, 
                          final_file_dir)