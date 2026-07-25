from datetime import datetime
from pathlib import Path
from uuid import uuid4
from fastapi import HTTPException, UploadFile, status
from app.services.parser_service import ParserService

from app.config import settings
from app.schemas.upload_schema import UploadMetadata


class UploadService:

    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".pptx",
    }

    def __init__(self):
        self.upload_dir = Path(settings.upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

        self.parser = ParserService()

    def validate_file(self, file: UploadFile) -> str:
        extension = Path(file.filename).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type: {extension}",
            )

        return extension

    def generate_filename(self, extension: str) -> tuple[str, str]:
        file_id = str(uuid4())
        stored_name = f"{file_id}{extension}"

        return file_id, stored_name

    async def save_file(self, file: UploadFile, stored_name: str) -> Path:
        file_path = self.upload_dir / stored_name

        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        return file_path

    async def upload_file(self, file: UploadFile) -> UploadMetadata:
        extension = self.validate_file(file)

        file_id, stored_name = self.generate_filename(extension)

        file_path = await self.save_file(file, stored_name)

        markdown = self.parser.parse_document(file_path)
        
        print(markdown)

        return UploadMetadata(
            id=file_id,
            original_name=file.filename,
            stored_name=stored_name,
            content_type=file.content_type,
            extension=extension,
            size=file.size,
            uploaded_at=datetime.now(),
        )
