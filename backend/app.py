"""
Main app backend module for FastAPI app.
"""

import uvicorn
from endpoints.analyze_endpoints import router as analyze_router
from endpoints.cv_data_crud_endpoints import router as cv_data_crud_router
from endpoints.embeddings_data_crud_endpoints import (
    router as embeddings_data_crud_router,
)
from endpoints.interview_prep_endpoints import router as interview_prep_router
from endpoints.upload_endpoints import router as upload_router
from endpoints.users_crud_endpoints import router as users_crud_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(upload_router)
app.include_router(analyze_router)
app.include_router(interview_prep_router)
app.include_router(users_crud_router)
app.include_router(cv_data_crud_router)
app.include_router(embeddings_data_crud_router)


@app.get("/")
async def root():
    return {"message": "Test backend app for job research assistant project!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=18080, reload=True)
