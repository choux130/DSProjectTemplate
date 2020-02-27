# Data Science Project Template 

### Goals
1. Create an easy understand project structure for people who are not involved in the project can also understand the code as quickly as possible. 
2. By splitting steps into multiple notebooks and scripts with common format input and output (like parquet and json), we are achieving the idea of language-agnostic in this project. 
3. Takes advantage of MLflow and S3 bucket/ Azure blob to make people on the same team easy to collaborate and communicate. 
4. Using Dockerfile and MLproject to increase the reproducibility of the project and ease the process of deployment on production. 

### Reference and Inspiration
* [Complete Data Science Project Template with Mlflow for Non-Dummies](https://towardsdatascience.com/complete-data-science-project-template-with-mlflow-for-non-dummies-d082165559eb)
* [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/)

### Requirements

1. Create a project specific conda environment which supports both R and python kernel. <code>conda create -n < env-name > python=3.7</code>

2. Install common used packages  
    * **Production**
        * mlflow (<code>pip install mlflow==1.6.0</code>)
        * boto3 (<code>conda install -c conda-forge boto3==1.11.15</code>) -- for S3 bucket
        * azure-storage-blob (<code>pip install azure-storage-blob==2.1.0</code>) -- for Azure Storage blob
        * scikit-learn (<code>conda install scikit-learn==0.22.1</code>)
        * pyarrow (<code>conda install -c conda-forge pyarrow==0.15.1</code>) -- for the parquet format file
        * r-base (<code>conda install -c r r-base==3.6.1</code>) 
        * r-arrow (<code>conda install -c conda-forge r-arrow==0.15.1</code>) -- for the parquet format file, [arrow R package](https://arrow.apache.org/docs/r/). In Win10, it can not be installed from conda ([since it is currently not supported](https://anaconda.org/conda-forge/r-arrow)) and have to be installed from R. 
        * r-dplyr (<code>conda install -c r r-dplyr==0.8.0.1</code>)
        * r-data.table(<code>conda install -c conda-forge r-data.table==1.12.2</code>)
        * pandas (<code>conda install pandas=1.0.1</code>) -- because of the error <code>ImportError: cannot import name 'check_array_indexer' from 'pandas.core.indexers'....</code> in os, need to reinstall. 
       
   * **Experiments**
       * jupyterlab (<code>conda install -c conda-forge jupyterlab==1.2.6</code>)
       * irkernel (<code>conda install -c r r-irkernel==0.8.15</code>)
       * ipykernel (<code>conda install ipykernel==5.1.4</code>)

3. Make sure all the R and python packages should be installed under the directory of the created conda environment. 
    * **Python**
        ```python
        import site
        print(site.getsitepackages())
        ```
    * **R**
        ```r
        print(.libPaths())
        ```
4. Make sure the R and Python kernel are up and run at the right environment successfully. 
    * [ipykernel - Kernels for different environments](https://ipython.readthedocs.io/en/stable/install/kernel_install.html#kernels-for-different-environments)
        * After installation, run the following code to point the the right conda environment.
            ```bash
            python -m ipykernel install --user --name { env-name } --display-name "{ display-name }"
            ```
    * [irkernel - installation](https://irkernel.github.io/installation/)
        * Open R under the conda environment and run the following code in the console. 
            ```R
            > IRkernel::installspec()
            > IRkernel::installspec(user = FALSE)
            ```
    * Some useful links,
        * [Using the R programming language in Jupyter Notebook](https://docs.anaconda.com/anaconda/navigator/tutorials/r-lang/)
        * [R language packages for Anaconda](https://docs.anaconda.com/anaconda/packages/r-language-pkg-docs/) 
   
4. Before finishing up the project, run the following code to generate the <code>environment.yml</code> file for the current conda environment. 
    ```bash
    # no build and no prefix
    conda env export --no-builds| grep -v "prefix" > environment.yml
    ```
    ```bash
    # no build, no prefix and no version
    conda env export --no-builds| grep -v "prefix" | cut -f -2 -d "=" > environment.yml
    ```
    So, if other people want to reproduct the environment they can run the following code to recreate the environment. 
    ```bash
    conda env create -f environment.yml --name { env-name }
    ```
    
### Workflow
1. Do the data exploration and idea tests on your preferred IDE like RStudio or Pycharm.  
2. Write clean example code with comments in the Jupyter Notebook and save it to the folder <code><project_name>/notebooks/</code>. Then, test it and make sure everything looks good. Install packages and set the environment variables (like <code>MLFLOW_TRACKING_URI</code>, <code>AWS_ACCESS_KEY_ID</code> and <code>AWS_SECRET_ACCESS_KEY</code>, <code>AZURE_STORAGE_CONNECTION_STRING</code>, ...etc), if needed. 
3. Convert code from the notebooks to the scripts and save to <code><project_name>/code/</code>. Then test the scripts using <code>python { python-script } { params(for example, --random_seed 123 --percent_train 0.8) }</code>. 
    * Tools for helping conversion
        * [nbconvert](https://nbconvert.readthedocs.io/en/latest/)
        * In Jupyter Lab, go to <code>File > Export Notebook As > Export Notebook to Executable Script</code>. 
4. In the end, containerize it.
    1. Create  <code>Dockerfile</code>, <code>.dockerignore</code> and <code>MLproject</code> files.
    2. Build a image. Go to project directory and run <code>docker build -t { image-name-should-match-the-name-on-MLproject } .</code>
    3. Run <code>mlflow run { project-folder-name } --experiment-name { expriment-name }</code> at the parent directory of project directory. For more information about what happens, [Running MLflow Projects](https://www.mlflow.org/docs/latest/quickstart.html#running-mlflow-projects).
    4. Run <code>mlflow ui --port { port-number }</code> to see the local tracking ui if <code>MLFLOW_TRACKING_URI</code> is not specified.
5. If everything looks good, check in the code to the remote repository (like Github).

### Reproduce other peoples' projects
1. Clone a remote project to local from Github.
2. Build the base image using <code>docker build -t { image-name-should-match-the-name-on-MLproject } . </code>
3. Run the image using <code>mlflow run { project-directory }</code> or <code>mlflow run { project-directory }:{ commit }</code>. Make sure the environment variables has been set correctly. Or directly run the code like this, <code>mlflow run https://github.com/xxx/xxx.git -v { commit } --experiment-name { experiment-name } -P { parmas-name }={ value }</code>
4. Deploy the model to localhost. <code>mlflow models serve -m < path-to-model-folder > -p 1234</code> and do the prediction by running
   <code>curl http://127.0.0.1:1234/invocations -H "Content-Type:application/json; format=pandas-split" --data '{"columns":["alcohol", "chlorides", "citric acid", "density", "fixed acidity", "free sulfur dioxide", "pH", "residual sugar", "sulphates", "total sulfur dioxide", "volatile acidity"],"data":[[1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]}'</code>. [MLflow Models](https://mlflow.org/docs/latest/models.html#deploy-a-python-function-model-on-microsoft-azure-ml).
5. If we want to run other poeples' code chuck by chuck, 
    * Use the <code>environment.yml</code> to create a conda environment. If some packages can not be found, then we have to manually install the package one by one.
    * To make sure the kernel is runnning in the specified environment like what we did before. 
    * Everything should work now. 

### Bugs for MLflow
These are the bugs that I have encoutered when I try to reproduce in Win10 system. 
1. [BUG] can't run MLFlow project on Windows #1670 (Ting ran into the same issue)
[https://github.com/mlflow/mlflow/issues/1670](https://github.com/mlflow/mlflow/issues/1670)
2. [BUG] Running a MLflow project with docker_env fails to create the docker container. (Ting ran into the same issue)
[https://github.com/mlflow/mlflow/issues/2501](https://github.com/mlflow/mlflow/issues/2501)

### More MLflow (<span style="color:red;font-size:15px">definitely check it out!</span>)

1. Hyperparameter tuning using bayesian optimization python package [GpyOpt](https://sheffieldml.github.io/GPyOpt/) and [Hyperopt](Hyperopt) or random search. [mlflow/examples/hyperparam/](https://github.com/mlflow/mlflow/tree/master/examples/hyperparam)
2. [Orchestrating Multistep Workflows](https://github.com/mlflow/mlflow/tree/master/examples/multistep_workflow)
3. [MLflow Command-Line Interface](https://www.mlflow.org/docs/latest/cli.html)

### Some Useful Commands
1. List all the kernels. <code>jupyter kernelspec list</code>
2. Let the hidden files show up in Jupyter lab. <code>jupyter lab --ContentsManager.allow_hidden=True</code> 
2. Connect to the database in Postregs. <code>psql -U { database username you want to connect with } -d { database name }</code>
3. Show all the tables using psql. <code>/d</code>

   

