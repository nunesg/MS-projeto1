from simulation import Simulation
import generators


def main():
    generator = generators.DummyGenerator(5, 10)
    simulation = Simulation(generator, generator)
    simulation.simulate()


if __name__ == "__main__":
    main()
