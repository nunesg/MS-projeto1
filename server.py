class Server:
    def __init__(self):
        self.next_free_time = 0
        self.wasted_time = 0

    def get_free_time(self):
        return self.next_free_time

    def get_total_idle_time(self):
        return self.wasted_time

    def work(self, start, time):
        if start < self.next_free_time:
            raise Exception("Can't start while server is still working!")
        self.wasted_time += start - self.next_free_time
        self.next_free_time = start + time

    def finish(self, time):
        self.wasted_time += max(0, time - self.next_free_time)
