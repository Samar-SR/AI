from fastapi import FastAPI, HTTPException, Response, UploadFile, status
from fastapi.params import Query
from ragfile.schema import Response
from .services.Upload import file_upload
from .services.services import result
from .services import documentor

app = FastAPI()
documentor = documentor


@app.post("/chat")
async def chat(response: Response):
    print(response.question)

    inputs = {"question": response.question}
    output = result(inputs)
    return {"question": response.question, "answer": output}


@app.post('/upload')
async def upload(file: UploadFile | None = None):
    message, file_name = file_upload(file)

    if message is False:
        return {'message ': f'check the file you have shared it we found some issue with it'}
    else:
        return {'message ': f'{file_name} uploaded, you can ask question now'}


@app.post('/urlupload')
def urlupload(link=str):
    message = documentor.document_list(link, True)
    if message is False:
        return {'message ': f'check the link you have shared it is not accessible'}
    else:
        return {'message ': f'your {link} data uploaded, you can ask question now'}
