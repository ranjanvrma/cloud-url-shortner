import multiprocessing

# Binds on all interfaces so VM1 (Nginx) can reach it over the private network.
# Restrict access at the security-group/firewall level to VM1's private IP only.
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 30
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
loglevel = "info"
