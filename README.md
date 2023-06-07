# Faustedition Facsimile Download Server

This is a tiny server that will offer to get all facsimiles of a Faustedition witness in a ZIP file.

## Deployment

* Use `./bootstrap.sh` to install the required python environment.
* Use `./run-server.sh` to actually run the Gunicorn server. 

## Configuration

You can create an optional `.env` file to configure some settings:

```sh 
IMAGE_ROOT=/path/to/images/folder   # default /faust 
APP_ROOT=/url/prefix                # default /downloads/facsimiles 
DOWNLOADS_FILE=downloads.json.gz    # file that lists the individual images
```

The binding port can be configured in `gunicorn.conf.py`.

## Usage

At an endpoint like /downloads/facsimiles/2_H.zip, it will zip and deliver the JPEGs. There is no more API.
