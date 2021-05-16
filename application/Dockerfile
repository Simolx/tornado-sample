FROM centos:7
LABEL maintainer="lx"

ENV TZ=Asia/Shanghai \
    LANG=en_US.UTF-8 \
    TERM=xterm \
    PATH=/usr/local/python3/bin:${PATH}
RUN yum update -y \
    && yum install -y which unzip \
    && yum clean all -y \
    && rm -rf /var/cache/yum
RUN ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime
RUN localedef -i en_US -f UTF-8 en_US.UTF-8
RUN curl -L -o conda.sh https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && bash conda.sh -b -f -p /usr/local/python3 \
    && rm -f conda.sh
RUN conda update --all -y \
    && conda install poetry -y \
    && conda clean --all -y \
    && rm -rf ~/.cache/pip/*
COPY tornado-sample /opt/application
WORKDIR /opt/application
RUN poetry install \
    && rm -rf ~/.cache/pip/*
ENTRYPOINT [ "poetry", "run" ]
EXPOSE 9000
CMD ["python", "application.py"]