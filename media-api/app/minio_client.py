import os
from minio import Minio
from fastapi import UploadFile
import uuid
import time


class MinioClient:
    def __init__(self):
        self.client = None
        self.bucket_name = "memes"
        self.connect()

    def connect(self):
        minio_url = os.getenv("MINIO_HOST", "minio:9000")  # Используйте имя сервиса MinIO
        for _ in range(5):
            try:
                self.client = Minio(
                    minio_url,
                    access_key=os.getenv("MINIO_ROOT_USER", "minioadmin"),
                    secret_key=os.getenv("MINIO_ROOT_PASSWORD", "minioadmin"),
                    secure=False
                )
                if not self.client.bucket_exists(self.bucket_name):
                    self.client.make_bucket(self.bucket_name)
                break
            except Exception as e:
                print(f"Failed to connect to Minio: {e}")
                time.sleep(5)

    async def upload_file(self, file: UploadFile):
        file_id = str(uuid.uuid4())
        file_name = f"{file_id}_{file.filename}"
        self.client.put_object(
            self.bucket_name, file_name, file.file, length=-1, part_size=10 * 1024 * 1024
        )
        return f"http://{os.getenv('MINIO_HOST', 'minio:9000')}/{self.bucket_name}/{file_name}"
