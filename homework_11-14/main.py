import pathlib
import time
from ipaddress import ip_address
from typing import Callable

import redis.asyncio as rds
import uvicorn
from fastapi import FastAPI, File, Request, status, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_limiter import FastAPILimiter
from starlette.middleware.cors import CORSMiddleware

from src.conf.config import settings
from src.routes import auth, contacts, users

app = FastAPI()


@app.on_event("startup")
async def startup():
    """
    The startup function is called when the application starts up.
    It's a good place to initialize things that are needed by your app, such as database connections.

    :return: A coroutine, so we need to run it with asyncio
    :doc-author: Trelent
    """
    r = await rds.Redis(host=settings.redis_host, port=settings.redis_port, db=0)
    await FastAPILimiter.init(r)


app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(users.router, prefix="/api")
BASE_DIR = pathlib.Path(__file__).parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This block is "hashed" because allowed IPs prevent from testing main.py

# ALLOWED_IPS = [ip_address("127.0.0.1")]


# @app.middleware("http")
# async def limit_access_by_ip(request: Request, call_next: Callable):
#     """
#     The limit_access_by_ip function is a middleware function that limits access to the API by IP address.
#     It checks if the client's IP address is in ALLOWED_IPS, and if not, returns a 403 Forbidden response.

#     :param request: Request: Get the client's ip address
#     :param call_next: Callable: Pass the next function in the chain of middleware
#     :return: A jsonresponse object
#     :doc-author: Trelent
#     """
#     ip = ip_address(request.client.host)  # type: ignore
#     if ip not in ALLOWED_IPS:
#         return JSONResponse(
#             status_code=status.HTTP_403_FORBIDDEN,
#             content={"detail": "Not allowed IP address"},
#         )
#     response = await call_next(request)
#     return response


templates = Jinja2Templates(directory="templates")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    The add_process_time_header function adds a header to the response called &quot;Process-Time&quot; that contains the time it took for the request to be processed.

    :param request: Request: Pass the request object to the function
    :param call_next: Pass the request to the next middleware in line
    :return: A response object
    :doc-author: Trelent
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["Process-Time"] = str(process_time)
    return response


@app.get("/", response_class=HTMLResponse, description="Main Page")
async def root(request: Request):
    """
    The root function is the entry point of the application.
    It returns a TemplateResponse object, which renders an HTML template using Jinja2.
    The template is located in templates/index.html and uses data from the request object to render itself.

    :param request: Request: Pass the request object to the template
    :return: A templateresponse object
    :doc-author: Trelent
    """
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Contacts App",
            "description": "REST API: Modul 2: Homeworks 11, 12, 13, 14",
        },
    )


# alembic init migrations <- initialize alembic, after that modify migrations/versions/env.py
# alembic revision --autogenerate -m 'Init' <- create migration
# alembic upgrade head <- apply migration, create tables in db
# uvicorn main:app --reload <- launch uvicorn server (--reload <- automatic reload after each modification of code)
# docker-compose up <- to run all containers from docker-compose.yml
# docker-compose down <- to shut down all containers
# docker-compose up -d <- to run all container after shut down


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File()):
    """
    The create_upload_file function creates a file in the uploads directory.

    :param file: UploadFile: Specify the file that is being uploaded
    :return: A file_path value
    :doc-author: Trelent
    """
    pathlib.Path("uploads").mkdir(exist_ok=True)
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:  # type: ignore
        f.write(await file.read())
    return {"file_path": file_path}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
