from simulation import Simulation
from statistics_manager import StatisticsManager
import generators
import json


def get_generator(gen_type, data):
    if gen_type == 'uniform':
        return generators.Uniform(data['min_value'], data['max_value'])
    if gen_type == "uniform_int":
        return generators.UniformInt(data['min_value'], data['max_value'])
    if gen_type == 'deterministic':
        return generators.Deterministic(data)
    if gen_type == 'normal':
        return generators.Normal(data['mean'], data['std_deviation'])
    if gen_type == 'exp':
        return generators.Exponential(data["lambda"])
    if gen_type == 'mmc':
        return generators.MonteCarlo(data)
    raise Exception("invalid generator type")


def main():
    with open("config.json", "r") as read_file:
        config = json.load(read_file)

    tec_generator = get_generator(config['tec_type'], config['tec'])
    ts_generator = get_generator(config['ts_type'], config['ts'])
    simulation = Simulation(
        arrival_time_gen=tec_generator,
        service_time_gen=ts_generator,
        statistics_manager=StatisticsManager(),
        max_queue_size=config.get('max_queue_size', float('inf')),
        nclients=config['clients'],
        nservers=config['servers']
    )
    simulation.simulate()


if __name__ == "__main__":
    main()
