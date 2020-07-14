# ml-training-fastai-wimlds
Repo for a sample training job for a model in fastai course-v3 using paperspace gradient


## How to build the container if you don't have a GPU on local

https://docs.paperspace.com/gradient/jobs/create-a-job/building-docker-containers-with-jobs
https://docs.paperspace.com/gradient/notebooks/notebook-containers/building-a-custom-container
/home/isischameleon/miniconda3/envs/ml-training/lib/python3.7/site-packages/gradient/api_sdk/clients/job_client.py



```  gradient jobs create \
        --apiKey a89b1d82aa901f10194447412e9b83 \
        --projectId prr6d2y9i \
        --machineType 'GPU+' \
        --workspace 'https://github.com/IsisChameleon/ml-training.git' \
        --useDockerfile true \
        --buildOnly   \
        --registryTarget isischameleon/ml-training:0.1 \
        --registryTargetUsername isischameleon \
        --registryTargetPassword '@8!C)iN[6ji*jsS' ```

https://hub.docker.com/repository/docker/isischameleon/ml-training