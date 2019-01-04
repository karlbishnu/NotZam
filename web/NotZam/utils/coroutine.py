def coroutine(func):
    def start(*args,**kwargs):
        g = func(*args,**kwargs)
        g.next( )
        return g
    return start
