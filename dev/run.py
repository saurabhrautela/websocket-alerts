import asyncio
from signal import signal, SIGINT

from alerts.alerts import app, loop

if __name__ == "__main__":

    serv_coro = app.create_server(host="0.0.0.0", port=7777, return_asyncio_server=True)

    serv_task = asyncio.ensure_future(serv_coro, loop=loop)
    signal(SIGINT, lambda s, f: loop.stop())
    server = loop.run_until_complete(serv_task)
    server.after_start()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()
    finally:
        server.before_stop()

        close_task = server.close()
        loop.run_until_complete(close_task)

        for connection in server.connection:
            connection.close_if_idle()

        server.after_stop()
