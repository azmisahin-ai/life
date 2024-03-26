# src/web/controller/signals.py


def simulation_signal(simulation):
    simulation.status()


def sampler_signal(sampler):
    sampler.status()


def instance_signal(instance):
    instance.status()
