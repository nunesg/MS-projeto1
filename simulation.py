# pip3 install tabulate

from server import Server
import tabulate


class Simulation:
    def __init__(self, arrival_time_gen, service_time_gen,
                 max_queue_size=float('inf'), nclients=15):
        self.arrival_time_gen = arrival_time_gen
        self.service_time_gen = service_time_gen
        self.max_queue_size = max_queue_size
        self.nclients = nclients
        self.clients_summary = []
        self.dropped_clients_summary = []
        self.server = Server()

        self.total_idle_time = 0
        self.total_queue_time = 0
        self.total_service_time = 0

    def simulate(self):
        for i in range(self.nclients):
            rel_arrival_time = self.arrival_time_gen.gen()
            service_time = self.service_time_gen.gen()
            self.client_arrived(i, rel_arrival_time, service_time)
        self.print_statistics()

    def client_arrived(self, id, rel_arrival_time, service_time):
        arrival_time = self.get_last_arrival_time() + rel_arrival_time
        if self.get_queue_size(arrival_time) == self.max_queue_size:
            self.drop_client(id, arrival_time, service_time)
            return
        queue_time = self.get_queue_time(arrival_time)
        start_service_time = arrival_time + queue_time
        finish_service_time = start_service_time + service_time

        self.total_idle_time += start_service_time - self.get_last_finish_service_time()
        self.total_queue_time += queue_time
        self.total_service_time += service_time

        client_summary = {
            "id": id,
            "rel_arrival_time": rel_arrival_time,
            "arrival_time": arrival_time,
            "service_time": service_time,
            "start_service_time": start_service_time,
            "finish_service_time": finish_service_time,
            "queue_time": queue_time,
            "system_time": finish_service_time - arrival_time,
            "idle_time": start_service_time - self.get_last_finish_service_time()
        }
        self.clients_summary.append(client_summary)
        self.server.work(start_service_time, service_time)

    def drop_client(self, id, arrival_time, service_time):
        self.dropped_clients_summary.append({
            "id": id,
            "arrival_time": arrival_time
        })

    def get_last_arrival_time(self):
        if len(self.clients_summary) > 0:
            return self.clients_summary[-1]['arrival_time']
        return 0

    def get_last_finish_service_time(self):
        if len(self.clients_summary) > 0:
            return self.clients_summary[-1]['finish_service_time']
        return 0

    def get_queue_time(self, arrival_time):
        if len(self.clients_summary) == 0:
            return 0
        return max(0, self.clients_summary[-1]['finish_service_time'] - arrival_time)

    def get_queue_size(self, arrival_time):
        qsize = 0
        for client in reversed(self.clients_summary):
            if client['start_service_time'] > arrival_time:
                qsize += 1
            else:
                break
        return qsize

    def print_statistics(self):
        dataset = self.clients_summary
        header = dataset[0].keys()
        rows = [x.values() for x in dataset]
        print(tabulate.tabulate(rows, header))

        total_time = dataset[self.nclients-1]['finish_service_time']

        # b) OBS -> ONLY ONE SERVANT
        print("Avg rate of servant occupation: {:.2f}".format(1 - self.total_idle_time/total_time))
        # c)
        print("Avg queue time: {:.2f}".format(self.total_queue_time / self.nclients))
        # d)
        print("Avg system time: {:.2f}".format((self.total_service_time+self.total_queue_time) / self.nclients))

        # print("Avg service time: {:.2f}".format(self.total_service_time / self.nclients))
