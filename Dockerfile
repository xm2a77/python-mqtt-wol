# 使用官方Debian精简镜像作为基础
FROM debian:bullseye-slim

# 设置非交互模式
ENV DEBIAN_FRONTEND=noninteractive

# 仅安装Python运行所需的基础组件
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    python3-setuptools \
    # 添加net rpc所需的包
    samba-common-bin \
    cifs-utils \
    && rm -rf /var/lib/apt/lists/*

# 设置Python3为默认Python
RUN if [ ! -f /usr/bin/python ]; then ln -s /usr/bin/python3 /usr/bin/python; fi && \
    if [ ! -f /usr/bin/pip ]; then ln -s /usr/bin/pip3 /usr/bin/pip; fi

# 设置工作目录
WORKDIR /python-mqtt-wol

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 声明环境变量
ENV IP=""
ENV USER=""
ENV PASSWORD=""
ENV MAC=""
ENV BEMFA_PRIVATE_KEY=""
ENV TOPIC=""


# 启动命令
CMD ["python", "main.py"]
    