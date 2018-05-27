from threading import Timer


class RTimer(Timer):
    """
    Thread object to repeat a function every interval
    """
    def run(self):
        while not self.finished.is_set():
            self.finished.wait(self.interval)
            self.function(*self.args, *self.kwargs)


def make_tick(interval, func, repeat=False, args=None, kwargs=None):
    """
    Convenience function to return Thread objects which either run once on a timer (Timer) or repeatedly at an
    interval (RTimer)
    """
    if repeat:
        return RTimer(interval, func, args=args, kwargs=kwargs)
    return Timer(interval, func, args=args, kwargs=kwargs)

