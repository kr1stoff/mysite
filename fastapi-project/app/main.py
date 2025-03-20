from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import router_samplesheet, router_settings, router_workflow, router_tasks

myapp = FastAPI()


# CORS 设置
myapp.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite 默认端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 路由
myapp.include_router(router_samplesheet.router)
myapp.include_router(router_settings.router)
myapp.include_router(router_workflow.router)
myapp.include_router(router_tasks.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(myapp, host="0.0.0.0", port=8000, reload=True)
