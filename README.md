# DS Project Template & MLflow

### Goals

1. Unified project structure.

   * Easy for other poeple to understand the code and know how to execute the code

2. Reproducibility

   * Easy for deployment
   * Better learning from others 
   * Easy to test, also means solid code and results

3. One place to track all the experiments. 

   * Not just share results in stand up or from e-mail

   

### Reference

* [Complete Data Science Project Template with Mlflow for Non-Dummies](https://towardsdatascience.com/complete-data-science-project-template-with-mlflow-for-non-dummies-d082165559eb)

  

### Requirements

1. Create project specific conda python and R environment. [Using the R programming language in Jupyter Notebook](https://docs.anaconda.com/anaconda/navigator/tutorials/r-lang/)

   * R package management
     * <code>.libPaths()</code> will be in the conda environment folder
     * [R language packages for Anaconda](https://docs.anaconda.com/anaconda/packages/r-language-pkg-docs/)
     * If the desired R package is not in conda packages, then it is not easy to install. Need more investigation for this situation.

2. Install packages  

   * mlflow (<code>conda install -c conda-forge mlflow</code>)
   * boto3 (<code>conda install -c conda-forge boto3</code>) -- for S3 bucket
   * numpy (<code>conda install -c anaconda numpy</code>)
   * scipy (<code>conda install -c anaconda scipy</code>)
   * scikit-learn (<code>conda install scikit-learn</code>)
   * pyarrow (<code>conda install -c conda-forge pyarrow</code>) -- for the parquet file
   * arrow (<code>conda install -c conda-forge r-arrow</code>) -- for the parquet file, [arrow R package](https://arrow.apache.org/docs/r/) 
   * jupyterlab (<code>conda install -c conda-forge jupyterlab</code>) -- for easily testing by running notebook directly 
3. Use code <code>conda env export -f environment.yml --name repro</code> to generate the yaml file for the current conda environment. 



### Workflow

1. Do the exploration and idea test on your preferred IDE like RStudio or Pycharm (make sure everything is running on the created conda environment).  

2. Write clean test code with comments in the Jupyter Notebook and save it to the folder <code><project_name>/notebooks/</code>. Then, test it and make sure everything looks good. 

3. Convert code from the notebooks to the scripts and save to <code><project_name>/code/</code>. Then test it using <code>python { python-script } { params(for example, --random_seed 123 --percent_train 0.8) }</code>. When doing the test don't forget to set the environment variables, 

   * <code>MLFLOW_TRACKING_URI</code> (if not specified, then the folder <code>mlruns</code> folder will be created for saving artifacts and metrics)
   * Credentials (<code>AWS_ACCESS_KEY_ID</code> and <code>AWS_SECRET_ACCESS_KEY</code>)

4. In the end, Dockerize it.

   1. Create  <code>Dockerfile</code>, <code>.dockerignore</code> and <code>MLproject</code> files.
   2. Build and test to run the image locally 
      1. Go to project directory and run <code>docker build -t { image-name } .</code>
      2. Go to ther parent directory of the project directory and run <code>mlflow run { project-folder-name } --experiment-name { expriment-name }</code>. For more information [Running MLflow Projects](https://www.mlflow.org/docs/latest/quickstart.html#running-mlflow-projects). Run <code>docker images -a</code> to see the two created images.
      3. Run <code>mlflow ui --port { port-number }</code> to see the local tracking ui if <code>MLFLOW_TRACKING_URI</code> is not specified.
      4. If needed, we can create a container based on the created image and run the bash code in the container. 
         * <code>docker run --rm -d --name { container-name } -t { image-name }</code>  
         * <code>docker exec -t -i { container-name } /bin/bash</code>

5. Check in the code to the remote repository.




### Reproduce other peoples projects

1. Clone the project to local from Github.

2. Build the base image using <code>docker build -t { image-name-should-match-the-name-on-MLproject } . </code>

3. Run the image using <code>mlflow run { project-directory }</code> or <code>mlflow run { project-directory }:{ commit }</code>. Make sure the environment variables has been set correctly.

4. Use the <code>environment.yml</code> to create a conda environment and open the R/Python Jupyter Notebook to have some tests if needed. <code>conda env create -f environment.yml --name { env-name }</code>

   To make sure the kernel is runnning in the specified environment,

   * Run in command line, <code>python -m ipykernel install --user --name { env-name }</code>. Change the <code>kernel.json</code> file for the correct python path, if needed.

   * Open R and run the following code,

     <code>IRkernel::installspec()</code>

     <code>IRkernel::installspec(user = FALSE)</code>

     

### More MLflow (<span style="color:red;font-size:15px">definitely check it out!</span>)

1. Hyperparameter tuning using bayesian optimization python package [GpyOpt](https://sheffieldml.github.io/GPyOpt/) and [Hyperopt](Hyperopt) or random search. mlflow/examples/hyperparam/](https://github.com/mlflow/mlflow/tree/master/examples/hyperparam)
2. [Orchestrating Multistep Workflows](https://github.com/mlflow/mlflow/tree/master/examples/multistep_workflow)

3. [MLflow Command-Line Interface](https://www.mlflow.org/docs/latest/cli.html)



### Some Useful Commands

1. List all the kernels. <code>jupyter kernelspec list</code>
2. Let the hidden files show up in Jupyter lab. <code>jupyter lab --ContentsManager.allow_hidden=True</code> 

2. Connect to the database in Postregs. <code>psql -U <database username you want to connect with> -d <database name></code>

3. Show all the tables using psql. <code>/d</code>

   

