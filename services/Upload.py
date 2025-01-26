from aiohttp import ClientError
from fastapi import HTTPException
from starlette import status
import io
import boto3
import magic
from ..secret import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from loguru import logger
from PyPDF2 import PdfReader
from uuid import uuid4
from documentor import document_list

KB = 1024
MB = 1024 * KB

SUPPORTED_FILE_TYPES = {
    'application/pdf': 'pdf',
    'text/plain': 'txt',
}

client = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

AWS_BUCKET = 'selfragfiles'

s3 = client.resource('s3')
bucket = s3.Bucket(AWS_BUCKET)


async def s3_upload(contents: bytes, key: str):
    logger.info(f'Uploading {key} to s3')
    bucket.put_object(Key=key, Body=contents)


async def s3_download(key: str):
    try:
        return s3.Object(bucket_name=AWS_BUCKET, key=key).get()['Body'].read()
    except ClientError as err:
        logger.error(str(err))


async def file_upload(file):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No file found!!'
        )

    contents = await file.read()
    size = len(contents)

    if not 0 < size <= 20 * MB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Supported file size is 0 - 1 MB'
        )

    file_type = magic.from_buffer(buffer=contents, mime=True)
    if file_type not in SUPPORTED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Unsupported file type: {file_type}. Supported types are {SUPPORTED_FILE_TYPES}'
        )
    else:
        if file_type == 'application/pdf':
            reader = PdfReader(io.BytesIO(contents))
            contents = ""
            for page in reader.pages:
                contents += page.extract_text()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Unsupported file type: {file_type}. Supported types are {SUPPORTED_FILE_TYPES}'
            )

    file_name = f'{uuid4()}.{SUPPORTED_FILE_TYPES[file_type]}'

    await s3_upload(contents = contents, key=file_name)

    contents = await s3_download(key=file_name)

    message = document_list(contents, False)

    return message, file_name
