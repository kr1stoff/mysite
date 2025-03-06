# mysite

## 部署

1. vite

    ```bash
    cnpm install
    # 开启服务
    npm run dev
    ```

2. fastapi
    启动

    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

    需要创建环境安装 fastapi, uvicorn, python-multipart

    ```bash
    mamba create -n web python=3.12
    mamba install -c conda-forge fastapi uvicorn python-multipart
    ```

3. 创建网站相关目录

    ```bash
    mkdir -p /data/mengxf/mysite/upload
    mkdir -p /data/mengxf/mysite/result
    mkdir -p /data/mengxf/mysite/template
    ```
