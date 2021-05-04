from simulation import Simulation
import generators
import json


def get_generator(config):
    if config['tec_type'] == 'uniform':
        return generators.DummyGenerator(config['tec']['min_value'], config['tec']['max_value'])
    raise Exception("invalid tec_type")


def main():
    with open("config.json", "r") as read_file:
        config = json.load(read_file)

    generator = get_generator(config)
    simulation = Simulation(generator, generator)
    simulation.simulate()


if __name__ == "__main__":
    main()
