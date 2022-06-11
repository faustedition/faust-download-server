import gzip
import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from urllib.parse import urlparse, unquote
from pathlib import Path
from zipstream import AioZipStream

app = FastAPI()

IMAGE_ROOT = '/faust'

with gzip.open("downloads.json.gz", "rt") as f:
    downloads = json.load(f)


@app.get("/download/facsimiles/{sigil}",
         responses={200: { 'content': {'application/zip': {}}}},
         description="Stream a ZIP file with all facsimiles of that sigil that are available for download.")
async def get_sigil(sigil: str) -> StreamingResponse:
    try:
        pages = downloads[sigil]
        spec = []
        for page, images in pages.items():
            for variant, url in enumerate(images):
                suffix = '' if variant == 0 else chr(ord('a') + variant - 1)  # some pages have more than one image
                spec.append({
                    'file': IMAGE_ROOT + unquote(urlparse(url).path), # JSON contains an URL, we need a path
                    'name': f'{sigil}-{int(page):03}{suffix}.jpg',         # new file name
                    'compression': None
                })
        zipstream = AioZipStream(spec)
        response = StreamingResponse(zipstream.stream(), media_type='application/zip')
        return response
    except KeyError:
        raise HTTPException(status_code=404, detail=f"{sigil} is not a valid sigil.")
