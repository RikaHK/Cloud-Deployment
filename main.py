from routers.post_router import router as post_router

from routers.login import router as login_router

app.include_router(login_router)


from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from auth.auth_router import router as auth_router
from database import Base, engine
import models  # registers models
from models import user, city, province

import psycopg2
import os
import boto3
from dotenv import load_dotenv
from uuid import uuid4

# Load .env file
load_dotenv()

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include auth router
app.include_router(auth_router)

# --- Test root route ---
@app.get("/")
def read_root():
    return {"message": "FastAPI is working"}

# --- Test DB connection ---
@app.get("/test-db")
def test_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT", 5432)
        )
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return {"message": "Connected to RDS!", "timestamp": result[0]}
    except Exception as e:
        return {"error": str(e)}

# --- S3 File Upload Route ---
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")

s3 = boto3.client("s3", region_name=AWS_REGION)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_ext = os.path.splitext(file.filename)[1]
        s3_key = f"{uuid4()}{file_ext}"

        s3.upload_fileobj(
            file.file,
            S3_BUCKET,
            s3_key,
            ExtraArgs={"ACL": "public-read"}  # Or "private"
        )

        file_url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"
        return JSONResponse(content={"message": "Upload successful", "url": file_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
