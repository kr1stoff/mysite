# mysite

## 部署

1. Vite

    ```bash
    cnpm install
    # 开启服务
    npm run dev
    ```

2. FastAPI
    启动

    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```

    需要创建环境安装 fastapi, uvicorn, python-multipart

    ```bash
    mamba create -n web python=3.12
    mamba install -c conda-forge fastapi uvicorn python-multipart
    ```

3. NGINX
    配置文件 `/etc/nginx/sites-available/vite-app.conf`, 然后 `sudo nginx -s reload` 重启 NGINX

    ```conf
    server {
        listen 80;
        server_name 10.255.24.60;

        proxy_read_timeout 120s;
        proxy_send_timeout 120s;
        send_timeout 120s;
        proxy_buffer_size 128k;
        proxy_buffers 4 128k;
        proxy_busy_buffers_size 256k;
        client_body_buffer_size 128k;
        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        proxy_buffering off;
        gzip on;
        gzip_min_length 1k;
        gzip_types application/vnd.ms-excel;

        root /data/mengxf/GitHub/Web/mysite/vite-project;
        index index.html;

        location / {
            try_files $uri $uri/ /index.html;
        }

        location /api/templates/ {
            alias /data/mengxf/mysite/templates/;
            autoindex on;  # Optional: Enable directory listing if needed
        }

        location /api/results/ {
            alias /data/mengxf/mysite/results/;
            autoindex on;
        }
    }
    ```

4. 创建网站相关目录

    ```bash
    mkdir -p /data/mengxf/mysite/results
    mkdir -p /data/mengxf/mysite/nginx/templates
    ```

5. MySQL 数据库
    创建数据库 `mysite`, 然后使用 `prepare/build_mysql_database.sql` 创建表

6. 轮询任务

    ```bash
    poetry run python -m workflow_monitor
    ```
