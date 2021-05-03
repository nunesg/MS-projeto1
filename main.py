from simulation import Simulation
import configparser
import generators

from numpy import random as npr



def main():
    config = configparser.ConfigParser()
    config.read('config.env')

    generator = generators.DummyGenerator(5, 10)
    simulation = Simulation(generator, generator)
    simulation.simulate()


if __name__ == "__main__":
    main()
