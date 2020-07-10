FROM nvidia/cuda:9.0-cudnn7-devel-ubuntu16.04

LABEL com.nvidia.volumes.needed="nvidia_driver"

RUN echo "deb http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list

RUN apt-get update && apt-get install -y --allow-downgrades --no-install-recommends \
         build-essential \
         cmake \
         git \
         curl \
         vim \
         ca-certificates \
         libnccl2=2.0.5-3+cuda9.0 \
         libnccl-dev=2.0.5-3+cuda9.0 \
         python-qt4 \
         libjpeg-dev \
	 zip \
	 unzip \
         libpng-dev &&\
     rm -rf /var/lib/apt/lists/*


ENV PYTHON_VERSION=3.6
RUN curl -o ~/miniconda.sh -O  https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh  && \
     chmod +x ~/miniconda.sh && \
     ~/miniconda.sh -b -p /opt/conda && \
     rm ~/miniconda.sh && \
    /opt/conda/bin/conda install conda-build


WORKDIR /src
RUN git clone https://github.com/IsisChameleon/ml-training .


RUN ls && /opt/conda/bin/conda env create
RUN /opt/conda/bin/conda clean -ya

ENV PATH /opt/conda/envs/ml-training/bin:$PATH
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64
ENV USER ml-training

WORKDIR /src/ml-training
RUN conda env create -f conda-ml-training.yml

RUN source activate ml-training
RUN source ~/.bashrc


WORKDIR /nbs
ENV PATH /opt/conda/bin:$PATH
ENV PATH /opt/conda/envs/ml-training/bin:$PATH

#CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
