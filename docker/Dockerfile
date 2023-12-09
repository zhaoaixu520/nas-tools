FROM alpine:3.15

ENV LANG="C.UTF-8" \
    TZ="Asia/Shanghai" \
    NASTOOL_CONFIG="/config/config.yaml" \
    NASTOOL_AUTO_UPDATE=false \
    NASTOOL_CN_UPDATE=false \
    NASTOOL_VERSION="3.0.1" \
    PS1="\u@\h:\w \$ " \
    REPO_URL="https://github.com/zhaoaixu520/nas-tools.git" \
    PYPI_MIRROR="https://pypi.tuna.tsinghua.edu.cn/simple" \
    ALPINE_MIRROR="mirrors.ustc.edu.cn" \
    PUID=0 \
    PGID=0 \
    UMASK=000 \
    WORKDIR="/nas-tools"

RUN apk add bash \
    fuse \
    libffi-dev \
    # && apk add --no-cache $(echo $(wget --no-check-certificate -qO- https://raw.githubusercontent.com/zhaoaixu520/nas-tools/v2.9.1-e3a43d4/package_list.txt)) \
    git \
    gcc \
    musl-dev \
    python3-dev \
    py3-pip \
    libxml2-dev \
    libxslt-dev \
    tzdata \
    su-exec \
    zip \
    curl \
    xvfb \
    inotify-tools \
    chromium-chromedriver \
    npm \
    dumb-init \
    ffmpeg \
    && ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo "${TZ}" > /etc/timezone \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && curl https://rclone.org/install.sh | bash \
    && if [ "$(uname -m)" = "x86_64" ]; then ARCH=amd64; elif [ "$(uname -m)" = "aarch64" ]; then ARCH=arm64; fi \
    && curl https://dl.min.io/client/mc/release/linux-${ARCH}/mc --create-dirs -o /usr/bin/mc \
    && chmod +x /usr/bin/mc \
    && pip install --upgrade pip setuptools wheel \
    && pip install cython \
    && pip install alembic==1.8.1 aniso8601==9.0.1 APScheduler==3.9.1 asttokens==2.0.8 async-generator==1.10 attrs==22.1.0 backcall==0.2.0 backports.shutil-get-terminal-size==1.0.0 beautifulsoup4==4.11.1 better-exceptions==0.3.3 bs4==0.0.1 cacheout==0.14.1 certifi==2022.6.15 cffi==1.15.1 charset-normalizer==2.1.1 click==8.1.3 cn2an==0.5.17 colorama==0.4.4 colored==1.3.93 cssselect==1.1.0 DBUtils==3.0.2 dateparser==1.1.4 decorator==5.1.1 executing==1.1.0 Flask==2.1.2 Flask-Login==0.6.2 fast-bencode==1.1.3 flask-compress==1.13 flask-restx==0.5.1 greenlet==1.1.3.post0 h11==0.12.0 humanize==4.4.0 idna==3.3 influxdb==5.3.1 itsdangerous==2.1.2 jedi==0.18.1 Jinja2==3.1.2 jsonpath==0.82 jsonschema==4.16.0 loguru==0.6.0 lxml==4.9.1 Mako==1.2.3 MarkupSafe==2.1.1 matplotlib-inline==0.1.6 msgpack==1.0.4 outcome==1.2.0 parse==1.19.0 parsel==1.6.0 parso==0.8.3 pexpect==4.8.0 pickleshare==0.7.5 pikpakapi==0.1.1 proces==0.1.2 prompt-toolkit==3.0.31 ptyprocess==0.7.0 pure-eval==0.2.2 pycparser==2.21 pycryptodome==3.15.0 Pygments==2.13.0 PyJWT==2.5.0 pymongo==4.2.0 PyMySQL==1.0.2 pyperclip==1.8.2 pypushdeer==0.0.3 pyquery==1.4.3 pyrsistent==0.18.1 PySocks==1.7.1 python-dateutil==2.8.2 python-dotenv==0.20.0 pytz==2022.2.1 pytz-deprecation-shim==0.1.0.post0 PyVirtualDisplay==3.0 redis==3.5.3 redis-py-cluster==2.1.3 regex==2022.9.13 requests==2.28.1 ruamel.yaml==0.17.21 ruamel.yaml.clib==0.2.7 selenium==4.4.3 six==1.16.0 slack-sdk==3.19.5 sniffio==1.2.0 sortedcontainers==2.4.0 soupsieve==2.3.2.post1 SQLAlchemy==1.4.42 stack-data==0.5.1 terminal-layout==2.1.2 tqdm==4.64.0 traitlets==5.4.0 trio==0.21.0 trio-websocket==0.9.2 typing_extensions==4.3.0 tzdata==2022.2 tzlocal==4.2 undetected-chromedriver==3.1.7 urllib3==1.26.12 w3lib==2.0.1 watchdog==2.1.9 wcwidth==0.2.5 webdriver-manager==3.8.5 websockets==10.3 Werkzeug==2.1.2 wsproto==1.2.0 zhconv==1.4.3 \
    && apk del libffi-dev \
    && npm install pm2 -g \
    && rm -rf /tmp/* /root/.cache /var/cache/apk/*
WORKDIR ${WORKDIR}
RUN python_ver=$(python3 -V | awk '{print $2}') \
    && echo "${WORKDIR}/" > /usr/lib/python${python_ver%.*}/site-packages/nas-tools.pth \
    && echo 'fs.inotify.max_user_watches=524288' >> /etc/sysctl.conf \
    && echo 'fs.inotify.max_user_instances=524288' >> /etc/sysctl.conf \
    && git config --global pull.ff only \
    && git clone -b v3.0.1 ${REPO_URL} ${WORKDIR} --depth=1 --recurse-submodule \
    && git config --global --add safe.directory ${WORKDIR}
EXPOSE 3000
VOLUME ["/config"]
ENTRYPOINT ["/nas-tools/docker/entrypoint.sh"]
