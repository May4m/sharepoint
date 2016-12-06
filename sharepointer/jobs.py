
from threading import Thread, Timer
import thread


def async(function):
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator


def new_job(function, *args, **kwargs):
    thread.start_new_thread(function, args, kwargs)


def job_schedular(function, time):
    schedular = Timer(function, time)
    schedular.start()
    return schedular