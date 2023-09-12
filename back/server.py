from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.routing import Route
from data_base.db import DataMember

import uvicorn


save = DataMember()


app = Starlette()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.route('/', methods=['POST'])
async def recived(request):
    data = await request.json()

    save.write(data['message'])

    return JSONResponse({'message': 'Данные получены'})


@app.route('/data')
async def transfer(request):
    return JSONResponse(save.read())


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
