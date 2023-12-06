#!/usr/bin/env python3

import aiohttp
from fastapi import (
    FastAPI,
    Request,
    Response,
)
from fastapi.responses import StreamingResponse


app = FastAPI()


PROXY_HOST = "https://uat.golf.tv/geo-US"

OVERRIDE_HEADERS = {
    "Host": "uat.golf.tv",
    "X-Forwarded-Proto": "https",
    "X-Forwarded-Port": "443",
}

# @app.get("/")


# @app.get("/")
# async def root():
#     return "OK"



@app.get('/')
async def root(req: Request):
    return await proxy("", req)


def local_background():
    with open("./background.jpg", "rb") as f:
        return f.read()
    return


@app.get('/{full_path:path}')
async def proxy(full_path: str, req: Request):
    if full_path == "assets/images/background.jpg":
        return Response(
            local_background(),
            headers={
                "local-serve": "1",
            },
            media_type="image/jpg"
        )

    proxy_path = "/".join([PROXY_HOST, full_path])
    print("proxy GET", proxy_path)
    async with aiohttp.ClientSession() as s:
        async with s.get(
                proxy_path,
                headers={
                    **req.headers,
                    **OVERRIDE_HEADERS,
                }
        ) as r:
            return Response(
                await r.read(),
                media_type=r.headers["content-type"],
            )
    return {"message": path}


def main():
    return


if __name__ == '__main__':
    main()
