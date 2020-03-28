from copy import deepcopy


class Body:
    def __init__(self, mass: float = 1, position: list = None, velocity: list = None):
        if position is None:
            position = [0, 0, 0]
        if velocity is None:
            velocity = [0, 0, 0]
        self.position = position
        self.velocity = velocity
        self.mass = mass

    def __repr__(self):
        return "\nmass: %s, position: %s, velocity: %s" % (self.mass, self.position, self.velocity)


class Universe:
    def __init__(self, bodies: list):
        self.bodies = bodies
        self.previous_state = []
        self.gravity_constant = 6.6732 * pow(10, -11)

    def __repr__(self):
        return "Universe()"

    def __str__(self):
        return str(self.bodies)

    def influence(self, a: Body, b: Body) -> list:
        """ return velocity of body a with influence of body b """
        # calculate distance between bodies
        distance = 0
        for x in range(len(a.position)):
            distance += pow(a.position[x] - b.position[x], 2)

        # calculate Newton force
        force = self.gravity_constant * a.mass * b.mass / distance

        # calculate vector of influence from body b
        influence_vector = []
        for x in range(len(a.velocity)):
            influence_vector.append(round((a.velocity[x] - b.velocity[x]) * force, 10))

        return [sum(x) for x in zip(a.velocity, influence_vector)]

    def tick(self):
        """ simulate next state of universe """
        # set current state of universe as previous one
        self.previous_state = deepcopy(self.bodies)
        # erase current state of universe
        self.bodies = []
        # for all bodies in universe
        for a in self.previous_state:
            # calculate impact from other bodies (impact of current body on itself is 0)
            _ = deepcopy(a)
            for b in self.previous_state:
                if a != b:
                    _.velocity = self.influence(_, b)
            # TODO move body to new position

            # add body with all influence from other bodies to the universe
            self.bodies.append(_)


if __name__ == '__main__':
    # init bodies list
    bodies_ = [
        Body(mass=10000000000000, position=[1, 0, 0], velocity=[0, 0, 0]),
        Body(mass=10000000000000, position=[0, 1, 0], velocity=[0, 0, 0]),
        Body(mass=10000000000000, position=[0, 0, 1], velocity=[0, 0, 0]),
    ]
    # init universe
    universe = Universe(bodies=bodies_)

    # print universe
    print(universe)

    # run simulation of universe
    universe.tick()

    # print universe
    print(universe)
