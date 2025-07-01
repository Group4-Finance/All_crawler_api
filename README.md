# api

# 環境設定

#### 安裝 pipenv

    pip install pipenv==2022.4.8

#### set pipenv

    pipenv --python ~/.pyenv/versions/3.8.10/bin/python

#### 安裝 repo 套件

    pipenv sync

#### 建立環境變數

    ENV=DEV python genenv.py
    ENV=DOCKER python genenv.py
    ENV=PRODUCTION python genenv.py

#### 排版

    black -l 80 api/

# API

#### 啟動 fastapi

    pipenv run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8888

# Docker

#### build docker image

    docker build -f with.env.Dockerfile -t <dockerhub>/<自己取>:<版本> .

ex: docekr build -f with.env.Dockerfile -t kong567/api:0.0.1 .

#### push docker image

    docker push <dockerhub>/<自己取>:<版本>

ex: docker push kong567/api:0.0.1 

#### 啟動 api

    DOCKER_IMAGE_FULL=<dockerhub>/<自己取>:<版本> docker compose 
    -f docker-compose-api-network-version.yml up -d

ex: DOCKER_IMAGE_FULL=kong567/api:0.0.1 docker compose 
    -f docker-compose-api-network-version.yml up -d

### 進入api docs 和 redoc
    
    http://127.0.0.1:8888/docs

    http://127.0.0.1:8888/redoc


### 注意事項

    在 docker-compose-api-network-version 檔案裡
    image 改成 image : ${DOCKER_IMAGE_FULL}
    所以啟動container時，在docker compose 前要再加入
    DOCKER_IMAGE_FULL=<dockerhub>/<自己取>:<版本>
    
    下面出現 422 Validation Error 是因為沒填入參數，
    所以 FastAPI 擋下來，並不會影響整體運作，只要輸入參數
    一樣能獲得想要資訊

    如果try it out 輸入完參數，沒有出現code 200 的 responsebody
    就要回去看api的 docker logs，查看問題出在哪
    例如 可能是在main.py裡設定的參數錯誤，導致在mysql裡找不到
    對應的欄位名稱，或是輸入時參數的格式錯誤

    