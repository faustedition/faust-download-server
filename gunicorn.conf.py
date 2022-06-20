worker_class = 'uvicorn.workers.UvicornWorker'
proc_name = 'faust-download-server'
wsgi_app = 'faust_download_server:app'
bind = '127.0.0.1:5051'
