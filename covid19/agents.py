from mesa import Agent
from covid19.random_walk import RandomWalker


class PersonaSaludable(RandomWalker):

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)

    def step(self):

        if (self.model.perill < self.model.perill_model): 
            self.random_move()

        if  (self.random.random() * 100) < (self.model.reproduccio_persones):
            virus = PersonaSaludable(
                self.model.next_id(), self.pos, self.model, self.moore
            )       
            self.model.grid.place_agent(virus, self.pos)
            self.model.schedule.add(virus)
        
        elif  (self.random.random() * 250) < (self.model.reproduccio_virus):
            virus = Virus(
                self.model.next_id(), self.pos, self.model, self.moore, self.model.n_random * 50
            )       
            self.model.grid.place_agent(virus, self.pos)
            self.model.schedule.add(virus)
        

class PersonaInfectada(RandomWalker):

    def __init__(self, unique_id, pos, model, moore, temps_deteccio=1, mortalitat_virus=1):
        super().__init__(unique_id, pos, model, moore=moore)
        self.temps_deteccio = temps_deteccio
        self.mortalitat_virus = mortalitat_virus

    def step(self):
        self.temps_deteccio -= 1

        if (self.model.perill < self.model.perill_model): 
            self.random_move()
        
        if  (self.random.random() * 100) < (self.model.reproduccio_virus):
            virus = Virus(
                self.model.next_id(), self.pos, self.model, self.moore, self.model.n_random * 50
            )       
            self.model.grid.place_agent(virus, self.pos)
            self.model.schedule.add(virus)
        
        if self.temps_deteccio < 0:
            x, y = self.pos
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            persona = [obj for obj in this_cell if isinstance(obj, PersonaInfectada)]
            persona = self.random.choice(persona)        
            self.model.grid._remove_agent(self.pos, persona)
            self.model.schedule.remove(persona)
            persona_malalta = PersonaMalalta(
                self.model.next_id(), self.pos, self.model, self.moore, self.model.durada_malaltia, self.mortalitat_virus
            )
            self.model.grid.place_agent(persona_malalta, self.pos)
            self.model.schedule.add(persona_malalta)
            



class PersonaMalalta(RandomWalker):

    def __init__(self, unique_id, pos, model, moore, durada_malaltia=10, mortalitat_virus = 1):
        super().__init__(unique_id, pos, model, moore=moore)
        self.durada_malaltia=durada_malaltia
        self.mortalitat_virus = mortalitat_virus

    def step(self):
       
        self.durada_malaltia -= 1
        if self.durada_malaltia < 0 or self.random.random() * 10 < self.model.mortalitat_virus:
            x, y = self.pos
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            persona = [obj for obj in this_cell if isinstance(obj, PersonaMalalta)]
            persona = self.random.choice(persona)        
            self.model.grid._remove_agent(self.pos, persona)
            self.model.schedule.remove(persona)

            if self.durada_malaltia < 0:
                persona_immunitzada = PersonaImmunitzada(
                    self.model.next_id(), self.pos, self.model, self.moore
                )
                self.model.grid.place_agent(persona_immunitzada, self.pos)
                self.model.schedule.add(persona_immunitzada)

            else: 
                persona_morta = PersonaMortaPelVirus(
                    self.model.next_id(), self.pos, self.model, self.moore
                )       
                self.model.grid.place_agent(persona_morta, self.pos)
                self.model.schedule.add(persona_morta)     

class PersonaMortaPelVirus(RandomWalker):
    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)
        

class PersonaImmunitzada(RandomWalker):

    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)

    def step(self):
        if (self.model.perill < self.model.perill_model):
            self.random_move()

        if   self.random.random() * 10 < self.model.mutacio_virus:
            x, y = self.pos
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            persona = [obj for obj in this_cell if isinstance(obj, PersonaImmunitzada)]
            persona = self.random.choice(persona)        
            self.model.grid._remove_agent(self.pos, persona)
            self.model.schedule.remove(persona)
            persona_saludable = PersonaSaludable(
                self.model.next_id(), self.pos, self.model, self.moore
            )
            self.model.grid.place_agent(persona_saludable, self.pos)
            self.model.schedule.add(persona_saludable)
            

        elif  (self.random.random() * 100) < (self.model.reproduccio_persones):
            virus = PersonaSaludable(
                self.model.next_id(), self.pos, self.model, self.moore
            )       
            self.model.grid.place_agent(virus, self.pos)
            self.model.schedule.add(virus)
            
        elif  (self.random.random() * 250) < (self.model.reproduccio_virus):
            virus = Virus(
                self.model.next_id(), self.pos, self.model, self.moore, self.model.n_random * 50
            )       
            self.model.grid.place_agent(virus, self.pos)
            self.model.schedule.add(virus)

class Virus(RandomWalker):

    energia = None

    def __init__(self, unique_id, pos, model, moore, energia=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energia = energia

    def step(self):
        
        self.energia -= 1

        if (self.random.random() * 10) < (self.model.infeccio_virus):
            x, y = self.pos
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            persona = [obj for obj in this_cell if isinstance(obj, PersonaSaludable)]
            if len(persona) > 0:
                persona = self.random.choice(persona)        
                self.model.grid._remove_agent(self.pos, persona)
                self.model.schedule.remove(persona)
                persona_infectada = PersonaInfectada(
                    self.model.next_id(), self.pos, self.model, self.moore, self.model.temps_deteccio, self.model.mortalitat_virus
                )
                self.model.grid.place_agent(persona_infectada, self.pos)
                self.model.schedule.add(persona_infectada)
                
        elif  (self.energia < 0):
            x, y = self.pos
            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            virus = [obj for obj in this_cell if isinstance(obj, Virus)]
            virus = self.random.choice(virus)        
            self.model.grid._remove_agent(self.pos, virus)
            self.model.schedule.remove(virus)

