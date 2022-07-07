import gzip
import json
from datetime import timezone
from email.utils import format_datetime

from pydantic import BaseSettings
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from urllib.parse import urlparse, unquote
from zipstream.ng import ZipStream


class Settings(BaseSettings):
    image_root: str = '/faust'
    downloads_file: str = "downloads.json.gz"
    app_root: str = "/downloads/facsimiles"

    class Config:
        env_file = '.env'


settings = Settings()
app = FastAPI(root_path=settings.app_root) #, openapi_prefix=settings.app_root)

with gzip.open(settings.downloads_file, "rt") as f:
    downloads = json.load(f)


@app.get("/{sigil}.zip",
         responses={200: {'content': {'application/zip': {}}}},
         description="Stream a ZIP file with all facsimiles of that sigil that are available for download.")
def get_sigil(sigil: str) -> StreamingResponse:
    try:
        pages = downloads[sigil]
        zs = ZipStream(sized=True)
        for page, images in pages.items():
            for variant, url in enumerate(images):
                suffix = '' if variant == 0 else chr(ord('a') + variant - 1)  # some pages have more than one image
                zs.add_path(settings.image_root + unquote(urlparse(url).path),
                            f'{sigil}/{sigil}-{int(page):03}{suffix}.jpg')

        response = StreamingResponse(iter(zs),
                                     media_type='application/zip',
                                     headers={'Content-Disposition': f'attachment; filename="{sigil}.zip"',
                                              'Content-Length': str(len(zs)),
                                              'Last-Modified': format_datetime(
                                                  zs.last_modified.astimezone(timezone.utc), usegmt=True)})
        return response
    except KeyError:
        raise HTTPException(status_code=404, detail=f"{sigil} is not a valid sigil.")
