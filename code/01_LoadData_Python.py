import os
import boto3


if __name__ == "__main__":
    # bucket credentials
    # make sure the credentials are saved as environment variables.
    access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']

    # file and directory info
    bucket_name = 'choux130' 
    file_name = 'wine-quality.csv'
    project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    # project_dir = '/Users/chou/Desktop/mlflow_dvc_cookiecutter/DS_project_template'
    
    s3 = boto3.client('s3', 
                      aws_access_key_id = access_key_id, 
                      aws_secret_access_key = secret_access_key)
   
    
    # save the file to the assigned directory
    final_file_dir = os.path.join(project_dir, 'data/raw', file_name)
    s3.download_file(bucket_name, 'DS_project_data/wine-quality.csv', final_file_dir)