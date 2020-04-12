"""Gunicorn Configuration"""
import os
from multiprocessing import cpu_count

import dotenv


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
    return min(cpu_count() + 1, 12)


dotenv.load_dotenv()

bind = ":".join(["0.0.0.0", os.getenv("PORT", "8000")])
worker_class = "gevent"
workers = max_workers()
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")

# If we run Gunicorn within a docker command, the worker heartbeat mechanism will
# be created in /tmp within the container which is actually on the disk and hence can be
# slow when it comes to responding to the heartbeat request
# Setting the location to a tmpfs mount will help with quick response to the hearbeat requests
# Details: http://docs.gunicorn.org/en/stable/faq.html#how-do-i-avoid-gunicorn-excessively-blocking-in-os-fchmod
worker_tmp_dir = "/dev/shm"
