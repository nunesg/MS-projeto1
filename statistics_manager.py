import tabulate


class StatisticsManager:
    def __init__(self):
        self.clients_summary = []
        self.nclients = 0
        self.dropped_clients_summary = []
        self.ndclients = 0
        self.average_queue_sizes = []
        self.arrival_times = []
        self.service_times = []
        self.total_queue_time = 0
        self.total_service_time = 0
        self.total_time = 0

    def add_client(self, client):
        self.nclients += 1
        self.total_queue_time += client.queue_time
        self.total_service_time += client.service_time
        self.total_time = client.finish_service_time
        self.clients_summary.append(client)
        self.arrival_times.append(client.rel_arrival_time)
        self.service_times.append(client.service_time)
        self.average_queue_sizes.append(self.get_average_queue_size())

    def add_dropped_client(self, client):
        self.dropped_clients_summary.append(client)
        self.ndclients += 1

    def clients_size(self):
        return self.nclients

    def dropped_clients_size(self):
        return self.ndclients

    def get_client(self, idx):
        if idx > self.nclients:
            raise Exception(
                f"Client index {idx} is out of range {self.nclients}")
        return self.clients_summary[idx]

    def get_clients(self):
        return self.clients_summary

    def print_statistics(self, servers):
        self.print_table(self.clients_summary, "Served Clients Simulation:")
        self.print_dropped()

        print("Number of dropped clients: {}\n".format(self.ndclients))

        print("===== Statistics considering the served clients =====\n")

        # a)
        print("Avg number of entities on the queue: {:.2f}".format(
            self.get_average_queue_size()
        ))

        # b)
        avg_total_idle_time = sum(
            server['server'].get_total_idle_time() for server in servers)/len(servers)
        print("Avg rate of servants occupation: {:.2f}".format(
            1 - avg_total_idle_time/self.total_time))
        # c)
        print("Avg client queue time: {:.2f}".format(
            self.total_queue_time / self.nclients))
        # d)
        print("Avg time of client on the system: {:.2f}".format(
            (self.total_service_time+self.total_queue_time) / self.nclients))

        print("Avg service time: {:.2f}".format(
            self.total_service_time / self.nclients))
        print("Total time of the simulation: {:.2f}".format(self.total_time))

        self.plot_figures()

    # create array of events:
    #  1. time of arrival on queue
    #  2. time in which the client leaves the queue
    # between each event on the array the queue size is constant, so we
    # calculate the size of the queue * the time in which it stayed that way
    def get_average_queue_size(self):
        events = []
        for client in self.clients_summary:
            events.append((client.arrival_time, client.id))
            events.append((client.start_service_time, client.id))

        events.sort()
        n_total_clients = self.nclients+self.ndclients
        checked = [False for i in range(n_total_clients)]
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
        if self.ndclients != 0:
            self.print_table(self.dropped_clients_summary, "Dropped clients:")

    def print_table(self, dataset, title):
        print(title)
        header = dataset[0].keys()
        rows = [x.values() for x in dataset]
        print(tabulate.tabulate(rows, header))
        print()

    def plot_figures(self):
        print("plot figures!")
