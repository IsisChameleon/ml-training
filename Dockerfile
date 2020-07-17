ARG CUDA="10.0"
ARG CUDNN="7"
FROM nvidia/cuda:9.2-base-ubuntu16.04
#FROM nvidia/cuda:${CUDA}-cudnn${CUDNN}-devel-ubuntu16.04
ENV LANG C.UTF-8
LABEL com.nvidia.volumes.needed="nvidia_driver"

RUN echo "deb http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list

RUN apt-get update -y \ 
    && apt-get install -y --allow-downgrades --no-install-recommends --allow-change-held-packages \
        build-essential \
        cmake \
        tree \
        git \
        curl \
        vim \
        ca-certificates \
        #libnccl2=2.0.5-3+cuda9.0 \
        #libnccl-dev=2.0.5-3+cuda9.0 \
        python-qt4 \
        libjpeg-dev \
	    zip \
	    unzip \
        libpng-dev \
    && rm -rf /var/lib/apt/lists/*

ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64
ENV PYTHON_VERSION=3.6


RUN curl -o ~/miniconda.sh -O  https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \   
    && chmod +x ~/miniconda.sh  \
    && ~/miniconda.sh -b -p /opt/conda  \
    && rm ~/miniconda.sh  \
    && /opt/conda/bin/conda install conda-build

ENV PATH=$PATH:/opt/conda/bin/
ENV USER ml-training

RUN mkdir /src
RUN chmod 777 /src
WORKDIR /src    
RUN git clone https://github.com/IsisChameleon/ml-training.git .

WORKDIR /src/ml-training
RUN conda env create -f conda-ml-training.yml 

RUN source activate ml-training
RUN source ~/.bashrc

WORKDIR /src/ml-training/nbs

#CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
