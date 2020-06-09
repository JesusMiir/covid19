from mesa import Agent
from covid19.random_walk import RandomWalker


class PersonaSaludable(RandomWalker):

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)

    def step(self):
        self.random_move()
        living = True
        

class PersonaInfectada(RandomWalker):

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)

    def step(self):
        self.random_move()
        living = True

class PersonaMalalta():

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)

    def step(self):
        self.random_move()
        living = True

class PersonaImmunitzada():

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)

    def step(self):
        self.random_move()
        living = True

class Virus(RandomWalker):

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        living = True

        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        persona = [obj for obj in this_cell if isinstance(obj, Persona)]

        if len(persona) > 0:
            persona = self.random.choice(persona)        
            self.model.grid._persona_infectada(self.pos, persona_infectada)
            
        

