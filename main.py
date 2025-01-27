import fastapi
import uvicorn
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from database.database import async_db, test_connection
from settings.base import BackendBaseSettings as settings
from test import get_sql
from utils.schema import get_schema, schema_to_json

settings = settings()
load_dotenv()


def initialize_backend_application() -> fastapi.FastAPI:
    app_attributes = settings.set_backend_app_attributes
    app = fastapi.FastAPI(**app_attributes)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )

    # app.include_router(router=endpoints)

    # app.include_router(router=endpoints, prefix=settings.API_PREFIX)

    @app.on_event("startup")
    async def startup():
        await async_db.initialize()
        await test_connection()
        async with async_db.connection() as conn:
            schema = await get_schema(conn)
            schema_json = schema_to_json(schema)
            # print(schema_json)
            q = 'How many users are in the database?'
            response = get_sql(q, schema_json)
            print(response)

    @app.on_event("shutdown")
    async def shutdown():
        await async_db.close()

    return app


backend_app: fastapi.FastAPI = initialize_backend_application()

if __name__ == "__main__":
    uvicorn.run(
        app="main:backend_app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        workers=settings.SERVER_WORKERS,
        log_level=settings.LOGGING_LEVEL,
    )
