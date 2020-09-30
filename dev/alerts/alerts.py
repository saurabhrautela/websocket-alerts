import json
import asyncio
from sanic import Sanic
from sanic import response


app = Sanic(__name__)

asyncio.set_event_loop(asyncio.new_event_loop())
loop = asyncio.get_event_loop()
queue = asyncio.Queue()


@app.websocket('/subscribe')
async def subscribe(request, ws):
    while True:
        data = await queue.get()
        queue.task_done()
        await ws.send(data)


@app.route("/health")
async def test(request):
    return response.json({"status": "running"})


@app.route("/alert", methods=["POST"])
async def test(request):
    queue.put_nowait(json.dumps(request.json))
    return response.json({"message": "Alert registered."}, status=200)
