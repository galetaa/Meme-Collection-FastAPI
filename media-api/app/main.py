from fastapi import FastAPI, File, UploadFile
from app.minio_client import MinioClient

app = FastAPI()

minio_client = MinioClient()


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_url = await minio_client.upload_file(file)
    return {"file_url": file_url}
