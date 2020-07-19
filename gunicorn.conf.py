"""Gunicorn Configuration"""
import multiprocessing
import os

import dotenv

# Parameters
GUNICORN_PORT = os.getenv("GUNICORN_PORT", "8080")
LOG_DIR = os.getenv(
    "LOG_DIR",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "server_logs.txt")),
)


def max_workers() -> int:
    """
    Maximum number of gunicorn workers to run.
    Gunicorn documents recommend no more than 4-12 workers for
    a system doing hundereds/thousands of requests per second.

    Container practices say it is a good idea to only run a single process within
    a container - for Gunicorn, we are better off running atleast 2 processes

    The number 12 comes from the following line:

    `DO NOT scale the number of workers to the number of clients you expect to have.
    Gunicorn should only need 4-12 worker processes to handle hundreds or thousands of requests
    per second.`

    Link: http://docs.gunicorn.org/en/stable/design.html#how-many-workers
    """
    # Number of workers = 2*CPU + 1 (recommendation from Gunicorn documentation)
    num_workers = multiprocessing.cpu_count() * 2 + 1
    return min(num_workers, 12)


dotenv.load_dotenv()


# Bind to localhost on specified port
bind = f"0.0.0.0:{GUNICORN_PORT}"
worker_class = "gevent"
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "debug")

# Access log
accesslog = os.path.join(LOG_DIR, "gunicorn_access.log")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Error log
errorlog = os.path.join(LOG_DIR, "gunicorn_error.log")
capture_output = True

# Max requests settings - a worker restarts after handling this many
# requests.
# max_requests = 0

workers = max_workers()

# If we run Gunicorn within a docker command, the worker heartbeat mechanism will
# be created in /tmp within the container which is actually on the disk and hence can be
# slow when it comes to responding to the heartbeat request
# Setting the location to a tmpfs mount will help with quick response to the hearbeat requests
# Details: http://docs.gunicorn.org/en/stable/faq.html#how-do-i-avoid-gunicorn-excessively-blocking-in-os-fchmod
worker_tmp_dir = "/dev/shm"
