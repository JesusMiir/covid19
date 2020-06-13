from mesa import Agent
from covid19.random_walk import RandomWalker


class PersonaSaludable(RandomWalker):

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)

    def step(self):
        self.random_move()
        living = True
        

class PersonaInfectada(RandomWalker):

    def __init__(self, unique_id, pos, model, moore, temps_deteccio=10):
        super().__init__(unique_id, pos, model, moore=moore)
        self.temps_deteccio = temps_deteccio

    def step(self):
        self.random_move()
        self.temps_deteccio -= 1

        if self.temps_deteccio < 0:
            x, y = self.pos
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            persona = [obj for obj in this_cell if isinstance(obj, PersonaInfectada)]
            persona = self.random.choice(persona)        
            self.model.grid._remove_agent(self.pos, persona)
            self.model.schedule.remove(persona)
            persona_malalta = PersonaMalalta(
                self.model.next_id(), self.pos, self.model, self.moore, 10, 1
            )
            self.model.grid.place_agent(persona_malalta, self.pos)
            self.model.schedule.add(persona_malalta)
            



class PersonaMalalta(RandomWalker):

    def __init__(self, unique_id, pos, model, moore, temps_malalta=10, mortalitat_virus = 1):
        super().__init__(unique_id, pos, model, moore=moore)
        self.temps_malalta=temps_malalta
        self.mortalitat_virus = mortalitat_virus

    def step(self):
        self.random_move()
        self.temps_malalta -= 1
        print(self.random.random())
        if ((self.random.random() * 100) < self.mortalitat_virus) or (self.temps_malalta < 0):
            x, y = self.pos
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            persona = [obj for obj in this_cell if isinstance(obj, PersonaMalalta)]
            persona = self.random.choice(persona)        
            self.model.grid._remove_agent(self.pos, persona)
            self.model.schedule.remove(persona)

            if self.temps_malalta < 0:
                persona_immunitzada = PersonaImmunitzada(
                self.model.next_id(), self.pos, self.model, self.moore
                )
                self.model.grid.place_agent(persona_immunitzada, self.pos)
                self.model.schedule.add(persona_immunitzada)
            

class PersonaImmunitzada(RandomWalker):

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
        persona = [obj for obj in this_cell if isinstance(obj, PersonaSaludable)]

        if len(persona) > 0:
            persona = self.random.choice(persona)        
            self.model.grid._remove_agent(self.pos, persona)
            self.model.schedule.remove(persona)
            persona_infectada = PersonaInfectada(
                self.model.next_id(), self.pos, self.model, self.moore, 10
            )
            self.model.grid.place_agent(persona_infectada, self.pos)
            self.model.schedule.add(persona_infectada)
            
        

