# pip3 install tabulate

from server import Server
import tabulate


class Simulation:
    def __init__(self, arrival_time_gen, service_time_gen,
                 max_queue_size=float('inf'), nclients=15, nservers=2):
        self.arrival_time_gen = arrival_time_gen
        self.service_time_gen = service_time_gen
        self.max_queue_size = max_queue_size
        self.nclients = nclients
        self.clients_summary = []
        self.dropped_clients_summary = []
        self.servers = [
            {
                'server': Server(),
                'id': i
            } for i in range(nservers)
        ]

        self.total_queue_time = 0
        self.total_service_time = 0
        self.total_time = 0

    def simulate(self):
        for i in range(self.nclients):
            rel_arrival_time = self.arrival_time_gen.gen()
            service_time = self.service_time_gen.gen()
            self.client_arrived(i, rel_arrival_time, service_time)
        for server in self.servers:
            server['server'].finish(self.total_time)
        self.print_statistics()

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

        self.total_queue_time += queue_time
        self.total_service_time += service_time
        self.total_time = finish_service_time

        client_summary = {
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
        }
        self.clients_summary.append(client_summary)
        server.work(start_service_time, service_time)

    def drop_client(self, id, arrival_time):
        self.dropped_clients_summary.append({
            "id": id,
            "arrival_time": arrival_time
        })
    
    def get_next_free_server(self):
        best = 0
        nservers = len(self.servers)
        for i in range(nservers):
            if self.servers[i]['server'].get_free_time() < self.servers[best]['server'].get_free_time():
                best = i;
        return self.servers[best];

    def get_last_arrival_time(self):
        if len(self.clients_summary) > 0:
            return self.clients_summary[-1]['arrival_time']
        return 0

    def get_queue_time(self, arrival_time, server):
        if len(self.clients_summary) == 0:
            return 0
        return max(0, server.get_free_time() - arrival_time)

    def get_queue_size(self, arrival_time):
        qsize = 0
        for client in reversed(self.clients_summary):
            if client['start_service_time'] > arrival_time:
                qsize += 1
            else:
                break
        return qsize

    def print_statistics(self):
        self.print_table(self.clients_summary, "Served Clients Simulation:")
        self.print_dropped()

        served_clients = len(self.clients_summary)
        print("Number of dropped clients: {}\n".format(
            len(self.dropped_clients_summary)))

        print("===== Statistics considering the served clients =====\n")

        # a)
        print("Avg number of entities on the queue: {:.2f}".format(
            self.get_average_queue_size()
        ))

        # b)
        avg_total_idle_time = sum(server['server'].get_total_idle_time() for server in self.servers)/len(self.servers)
        print("Avg rate of servants occupation: {:.2f}".format(
            1 - avg_total_idle_time/self.total_time))
        # c)
        print("Avg client queue time: {:.2f}".format(
            self.total_queue_time / served_clients))
        # d)
        print("Avg time of client on the system: {:.2f}".format(
            (self.total_service_time+self.total_queue_time) / served_clients))

        print("Avg service time: {:.2f}".format(
            self.total_service_time / served_clients))
        print("Total time of the simulation: {:.2f}".format(self.total_time))

    # create array of events:
    #  1. time of arrival on queue
    #  2. time in which the client leaves the queue
    # between each event on the array the queue size is constant, so we
    # calculate the size of the queue * the time in which it stayed that way
    def get_average_queue_size(self):
        events = []
        for client in self.clients_summary:
            events.append((client["arrival_time"], client["id"]))
            events.append((client["start_service_time"], client["id"]))

        events.sort()
        checked = [False for i in range(self.nclients)]
        last_t = 0
        qsize = 0
        weighted_sum = 0
        for e in events:
            (t, client_id) = e
            weighted_sum += qsize * (t - last_t)
            # if checked then the client is leaving the queue
            qsize += -1 if checked[client_id] else 1
            checked[client_id] = not checked[client_id]
            last_t = t
        return weighted_sum/self.total_time

    def print_dropped(self):
        if len(self.dropped_clients_summary) == 0:
            return
        self.print_table(self.dropped_clients_summary, "Dropped clients:")
        return

    def print_table(self, dataset, title):
        print(title)
        header = dataset[0].keys()
        rows = [x.values() for x in dataset]
        print(tabulate.tabulate(rows, header))
        print()
