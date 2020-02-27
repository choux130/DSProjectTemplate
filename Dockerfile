FROM continuumio/miniconda3

#### Installing packages ======================================= 
## currently have some problems and need more investigation.
## install python pacakges based on conda environment.yml file
# COPY environment.yml /.
# RUN conda env create -f environment.yml --name myenv
# RUN conda activate myenv

## install python packages based on conda command directly
RUN pip install mlflow==1.6.0
RUN pip install azure-storage-blob==2.1.0
RUN conda install scikit-learn==0.22.1
RUN conda install -c conda-forge pyarrow==0.15.1
RUN conda install -c r r-base==3.6.1
RUN conda install -c conda-forge r-arrow==0.15.1
RUN conda install -c r r-dplyr==0.8.0.1
RUN conda install -c r r-jsonlite==1.6
RUN conda install -c conda-forge r-data.table==1.12.2
RUN conda install pandas==1.0.1

ENV AZURE_STORAGE_CONNECTION_STRING='xxx'