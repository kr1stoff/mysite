from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import samplesheet

app = FastAPI()


# CORS 设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite 默认端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 路由
app.include_router(samplesheet.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
