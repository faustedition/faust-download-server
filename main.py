import gzip
import json
from datetime import tzinfo, timezone
from email.utils import format_datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from urllib.parse import urlparse, unquote
from pathlib import Path
from zipstream.ng import ZipStream

app = FastAPI()

IMAGE_ROOT = '/faust'

with gzip.open("downloads.json.gz", "rt") as f:
    downloads = json.load(f)


@app.get("/downloads/facsimiles/{sigil}.zip",
         responses={200: { 'content': {'application/zip': {}}}},
         description="Stream a ZIP file with all facsimiles of that sigil that are available for download.")
def get_sigil(sigil: str) -> StreamingResponse:
    try:
        pages = downloads[sigil]
        zs = ZipStream(sized=True)
        for page, images in pages.items():
            for variant, url in enumerate(images):
                suffix = '' if variant == 0 else chr(ord('a') + variant - 1)  # some pages have more than one image
                zs.add_path(IMAGE_ROOT + unquote(urlparse(url).path), f'{sigil}/{sigil}-{int(page):03}{suffix}.jpg')

        response = StreamingResponse(iter(zs),
                                     media_type='application/zip',
                                     headers={'Content-Disposition': f'attachment; filename="{sigil}.zip"',
                                              'Content-Length': str(len(zs)),
                                              'Last-Modified': format_datetime(zs.last_modified.astimezone(timezone.utc), usegmt=True)})
        return response
    except KeyError:
        raise HTTPException(status_code=404, detail=f"{sigil} is not a valid sigil.")