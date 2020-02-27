import os
import time
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
import pyarrow.parquet as pq
import argparse
import pickle

import pyarrow
import sklearn
import cloudpickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import explained_variance_score, mean_squared_error

from s06_Predict_pyfunc import WineQualityRegressionPyfunc

# functions
def eval_metrics(actual, pred):
    exp_var = explained_variance_score(actual, pred)
    mse = mean_squared_error(actual, pred)
    return exp_var, mse

if __name__ == "__main__":
    # params 
    parser = argparse.ArgumentParser()
    parser.add_argument('--random_seed', default='123')
    parser.add_argument('--percent_train', default='0.8')
    parser.add_argument('--method', default='mean')
    parser.add_argument('--criterion', default='mse')
    parser.add_argument('--max_depth', default='50')
    args = parser.parse_args()
    
    random_seed = int(args.random_seed)
    percent_train = float(args.percent_train)
    method = str(args.method)
    criterion = str(args.criterion)
    max_depth = int(args.max_depth)
    
    # file and directory info
    project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    # print(project_dir)
    interim_folder = "/data/interim/"
    processed_folder = "/data/processed/"
    src_folder = "/code/"
       
    # LoadData
    script_path = project_dir + src_folder + "s01_LoadData_Python.py" 
    os.system("python %s" % (script_path))

    # SplitData
    script_path = project_dir + src_folder + "s02_SplitData_R.R" 
    os.system("Rscript %s %f %f" % (script_path, random_seed, percent_train))

    # CreateEncoder
    script_path = project_dir + src_folder + "s03_CreateEncoder_R.R" 
    os.system("Rscript %s %s" % (script_path, method))

    # PrepareDataForModel
    script_path = project_dir + src_folder + "s04_PrepareDataForModel_R.R" 
    os.system("Rscript %s %s %s" % (script_path, "train.parquet", "train"))
    os.system("Rscript %s %s %s" % (script_path, "test.parquet", "train"))

    # Train
    train_X = pd.read_parquet(project_dir + interim_folder + 'train_X.parquet')
    train_Y = pd.read_parquet(project_dir + interim_folder + 'train_Y.parquet')
    test_X = pd.read_parquet(project_dir + interim_folder + 'test_X.parquet')
    test_Y = pd.read_parquet(project_dir + interim_folder + 'test_Y.parquet')
    
    # Launch the experiment on mlflow
    experiment_name = "test_experiment"
    mlflow.set_experiment(experiment_name)
    
    with mlflow.start_run(nested=True):
        uri = os.getenv('MLFLOW_TRACKING_URI')
        if uri == None:
            uri = 'localhost'
        print('MLFLOW_TRACKING_URI = localhost')

        # train model 
        tic = time.time()
        model = RandomForestRegressor(criterion = criterion, max_depth = max_depth)
        model = model.fit(train_X, train_Y.values.ravel())
        duration_training = time.time() - tic

        # make prediction
        tic1 = time.time()
        test_pred = model.predict(test_X)
        duration_prediction = time.time() - tic1

        (exp_var, mse) = eval_metrics(test_Y, test_pred)
        print("DecisionTreeRegressor model (criterion=%s, max_depth=%f):" % (criterion, max_depth))
        print("  Explained Variance Score : %s" % exp_var)
        print("  MSE: %s" % mse)

        params = {
            "random_seed" : random_seed,
            "percent_train" : percent_train,
            "method" : method, 
            "criterion" : criterion, 
            "max_depth" : max_depth
        }
        mlflow.log_params(params)
   
        metrics = {
            "exp_var" : exp_var,
            "mse" : mse,
            "duration_training" : duration_training,
            "duration_prediction" : duration_prediction
        }
        mlflow.log_metrics(metrics)

        artifact_path = "model"
        print('run_id: ' + mlflow.active_run().info.run_id)
        
        # save model as pickle to local as pickle
        model_path = 'model.pkl'
        pickle.dump(model, open(model_path, 'wb'))
    
        conda_env = {
            'channels': ['defaults', 'conda-forge', 'r'],
            'dependencies': ['python=3.7.6', 
                             'r-base=3.6.1',
                             'r-arrow=0.15.1',
                             'r-dplyr=0.8.0.1',
                             'r-jsonlite=1.6',
                             'r-vctrs=0.2.3',
                             {'pip': [
                'scikit-learn=={}'.format(sklearn.__version__),
                'mlflow=={}'.format(mlflow.__version__),
                'cloudpickle=={}'.format(cloudpickle.__version__),
                'pyarrow=={}'.format(pyarrow.__version__)
            ]}],
            'name': 'pyfunc-env'}  
        
        mlflow.pyfunc.log_model(artifact_path=artifact_path, 
                                python_model=WineQualityRegressionPyfunc(),
                                conda_env=conda_env, 
                                artifacts = { "model": model_path, 
                                              "encoder_num": project_dir + processed_folder + "encoder_num.json" },
                                code_path = [project_dir + src_folder + "s06_Predict_pyfunc.py", 
                                             project_dir + src_folder + "s04_PrepareDataForModel_R.R"] 
                               )

        # delete the model in local directory
        if os.path.exists(model_path):
          os.remove(model_path)
        else:
          print("The file does not exist")
        
        mlflow.end_run()