from _threading_local import local

_thread_locals = local()


def set_cid(cid):
    setattr(_thread_locals, 'cid', cid)


def get_cid():
    return getattr(_thread_locals, 'cid', '')
