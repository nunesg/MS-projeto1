# pip3 install tabulate

from server import Server
from client import ClientSummary, DroppedClientSummary


class Simulation:
    def __init__(self, arrival_time_gen, service_time_gen, statistics_manager,
                 max_queue_size=float('inf'), nclients=15, nservers=2):
        self.arrival_time_gen = arrival_time_gen
        self.service_time_gen = service_time_gen
        self.max_queue_size = max_queue_size
        self.nclients = nclients
        self.statistics_manager = statistics_manager
        self.servers = [
            {
                'server': Server(),
                'id': i
            } for i in range(nservers)
        ]

    def simulate(self):
        for i in range(self.nclients):
            rel_arrival_time = self.arrival_time_gen.gen()
            service_time = self.service_time_gen.gen()
            self.client_arrived(i, rel_arrival_time, service_time)
        last_client = self.statistics_manager.get_client(-1)
        for server in self.servers:
            server['server'].finish(last_client.finish_service_time)
        self.statistics_manager.print_statistics(self.servers)

    def client_arrived(self, id, rel_arrival_time, service_time):
        arrival_time = self.get_last_arrival_time() + rel_arrival_time
        server_obj = self.get_next_free_server()
        server = server_obj.get('server')
        server_id = server_obj.get('id')
        if (
            self.get_queue_size(arrival_time) == self.max_queue_size
            and server.get_free_time() > arrival_time
        ):
            self.drop_client(id, arrival_time)
            return
        queue_time = self.get_queue_time(arrival_time, server)
        start_service_time = arrival_time + queue_time
        finish_service_time = start_service_time + service_time

        client_summary = ClientSummary({
            "id": id,
            "rel_arrival_time": rel_arrival_time,
            "arrival_time": arrival_time,
            "service_time": service_time,
            "start_service_time": start_service_time,
            "finish_service_time": finish_service_time,
            "queue_time": queue_time,
            "system_time": finish_service_time - arrival_time,
            "server_id": server_id+1,
            "idle_time": start_service_time - server.get_free_time()
        })
        self.statistics_manager.add_client(client_summary)
        server.work(start_service_time, service_time)

    def drop_client(self, id, arrival_time):
        self.statistics_manager.add_dropped_client(DroppedClientSummary({
            "id": id,
            "arrival_time": arrival_time
        }))

    def get_next_free_server(self):
        best = 0
        nservers = len(self.servers)
        for i in range(nservers):
            if self.servers[i]['server'].get_free_time() < self.servers[best]['server'].get_free_time():
                best = i
        return self.servers[best]

    def get_last_arrival_time(self):
        if self.statistics_manager.clients_size() > 0:
            return self.statistics_manager.get_client(-1).arrival_time
        return 0

    def get_queue_time(self, arrival_time, server):
        if self.statistics_manager.clients_size() == 0:
            return 0
        return max(0, server.get_free_time() - arrival_time)

    def get_queue_size(self, arrival_time):
        qsize = 0
        clients = self.statistics_manager.get_clients()
        for client in reversed(clients):
            if client.start_service_time > arrival_time:
                qsize += 1
            else:
                break
        return qsize
