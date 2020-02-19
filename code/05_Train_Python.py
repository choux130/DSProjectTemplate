import os
import sys
import argparse
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn

from sklearn import tree
from sklearn.metrics import explained_variance_score, mean_squared_error

# functions
def eval_metrics(actual, pred):
    exp_var = explained_variance_score(actual, pred)
    mse = mean_squared_error(actual, pred)
    return exp_var, mse

if __name__ == "__main__":
    # params 
    parser = argparse.ArgumentParser()
    parser.add_argument('--random_seed')
    parser.add_argument('--percent_train')
    parser.add_argument('--method')
    parser.add_argument('--criterion')
    parser.add_argument('--max_depth')
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
    script_path = project_dir + src_folder + "01_LoadData_Python.py" 
    os.system("python %s" % (script_path))

    # SplitData
    script_path = project_dir + src_folder + "02_SplitData_R.R" 
    os.system("Rscript %s %f %f" % (script_path, random_seed, percent_train))

    # CreateEncoder
    script_path = project_dir + src_folder + "03_CreateEncoder_R.R" 
    os.system("Rscript %s %s" % (script_path, method))

    # Feture
    script_path = project_dir + src_folder + "04_Feature_R.R" 
    os.system("Rscript %s" % (script_path))

    train_X = pd.read_parquet(project_dir + interim_folder + 'train_X.parquet')
    train_Y = pd.read_parquet(project_dir + interim_folder + 'train_Y.parquet')
    test_X = pd.read_parquet(project_dir + interim_folder + 'test_X.parquet')
    test_Y = pd.read_parquet(project_dir + interim_folder + 'test_Y.parquet')
    test_Y = test_Y.iloc[:,0].to_numpy()
    
    with mlflow.start_run():
        model = tree.DecisionTreeRegressor(criterion = criterion, max_depth = max_depth)
        model = model.fit(train_X, train_Y)

        test_pred = model.predict(test_X)
        (exp_var, mse) = eval_metrics(test_Y, test_pred)

        print("  DecisionTreeRegressor model (criterion=%s, max_depth=%f):" % (criterion, max_depth))
        print("  Explained Variance Score : %s" % exp_var)
        print("  MSE: %s" % mse)
        
        mlflow.log_param("random_seed", random_seed)
        mlflow.log_param("percent_train", percent_train)
        mlflow.log_param("method", method)
        mlflow.log_param("criterion", criterion)
        mlflow.log_param("max_depth", max_depth)
        
        mlflow.log_metric("exp_var", exp_var)
        mlflow.log_metric("mse", mse)

        mlflow.sklearn.log_model(model, "model")