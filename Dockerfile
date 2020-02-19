FROM continuumio/miniconda3

#### Installing packages ======================================= 
## currently have some problems and need more investigation.
## install python pacakges based on conda environment.yml file
# COPY environment.yml /.
# RUN conda env create -f environment.yml --name myenv
# RUN conda activate myenv

## install python packages based on conda command directly
RUN conda install -c conda-forge mlflow==1.6.0
RUN conda install -c conda-forge boto3==1.11.15
RUN conda install -c anaconda scipy=1.4.*
RUN pip install -U numpy scipy scikit-learn==0.22.*
RUN conda install -c r r-dplyr==0.8.*
RUN conda install -c conda-forge r-arrow==0.15.*
RUN conda install -c conda-forge pyarrow==0.15.*
RUN conda install -c conda-forge jupyterlab==1.2.*
RUN conda install -c conda-forge r-data.table==1.12.*

USER root
RUN mkdir /DS_project/

# ENV AWS_ACCESS_KEY_ID=
# ENV AWS_SECRET_ACCESS_KEY=
# ENV MLFLOW_TRACKING_URI=

