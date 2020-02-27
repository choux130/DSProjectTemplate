import mlflow.pyfunc
import os
import pickle
import sklearn
import pandas as pd
import shutil

# Define the model class
class WineQualityRegressionPyfunc(mlflow.pyfunc.PythonModel):

    def load_context(self, context):
        print(os.path.join(os.path.dirname(__file__)))
        with open(context.artifacts["model"], 'rb') as file:
            pickle_model = pickle.load(file)
        self.model = pickle_model
        
    # def fit(self, X, Y):
        
    def predict(self, context, model_input):
        project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) 
        src_folder = "/code/"
        
        tmp_folder = '/tmp/'
        os.mkdir(project_dir + tmp_folder)
        
        modelinput = pd.DataFrame(model_input)
        modelinput.to_parquet(project_dir + tmp_folder + "pred" + ".parquet")  
        script_path = project_dir + src_folder + "s04_PrepareDataForModel_R.R" 
        os.system("Rscript %s %s %s" % (script_path, "pred.parquet", "pred"))
        pred_X = pd.read_parquet(project_dir + tmp_folder + 'pred_X.parquet') 
        
        shutil.rmtree(project_dir + tmp_folder)   
        
        return self.model.predict(pred_X)
        
