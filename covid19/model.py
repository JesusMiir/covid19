from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from covid19.agents import PersonaSaludable, PersonaInfectada, PersonaMalalta, PersonaMortaPelVirus, PersonaImmunitzada, Virus
from covid19.schedule import RandomActivationByBreed


class Covid19(Model):

    height = 8
    width = 8

    inicial_perones = 5
    inicial_virus = 3
    reproduccio_persones = 2
    infeccio_virus = 6
    reproduccio_virus = 3
    
    temps_vida_virus = 5

    temps_deteccio = 6
    durada_malaltia = 8
    mortalitat_virus = 1
    mutacio_virus = 1

    perill_model = 2
    n_random = 0
    perill = 5

    verbose = False  # Print-monitoring

    description = (
        "El model vol simular la capacitat que te un virus d'infectar a la població."
    )

    def __init__(
        self,
        height=8,
        width=8,
        inicial_persones=5,
        inicial_virus=3,
        reproduccio_persones = 2,
        infeccio_virus=6,
        reproduccio_virus = 3,

        temps_vida_virus = 5,

        temps_deteccio=6,
        durada_malaltia=8,
        mortalitat_virus=2,
        mutacio_virus=2,

        perill_model = 2,
        n_random=0,
        perill=5
    ):

        super().__init__()
        # Parameters
        self.height = height
        self.width = width
        self.inicial_persones = inicial_persones
        self.inicial_virus = inicial_virus
        self.reproduccio_persones = reproduccio_persones
        self.infeccio_virus = infeccio_virus
        self.reproduccio_virus = reproduccio_virus
        
        self.temps_vida_virus = temps_vida_virus
        
        self.temps_deteccio = temps_deteccio
        self.durada_malaltia = durada_malaltia
        self.mortalitat_virus = mortalitat_virus
        self.mutacio_virus = mutacio_virus

        self.perill_model = perill_model
        self.n_random = n_random
        self.perill = perill

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "PersonaSaludable": lambda m: m.schedule.get_breed_count(PersonaSaludable),
                "PersonaInfectada": lambda m: m.schedule.get_breed_count(PersonaInfectada),
                "PersonaMalalta": lambda m: m.schedule.get_breed_count(PersonaMalalta),
                "PersonaMortaPelVirus": lambda m: m.schedule.get_breed_count(PersonaMortaPelVirus),
                "PersonaImmunitzada": lambda m: m.schedule.get_breed_count(PersonaImmunitzada),
                "Virus": lambda m: m.schedule.get_breed_count(Virus)
            }
        )

        # Crear persones:
        for i in range(self.inicial_persones):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            persona = PersonaSaludable(self.next_id(), (x, y), self, True)
            self.grid.place_agent(persona, (x, y))
            self.schedule.add(persona)
        
        #Crear virus:
        for i in range(self.inicial_virus):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energia = 50
            virus = Virus(self.next_id(), (x, y), self, True, energia)
            self.grid.place_agent(virus, (x,y))
            self.schedule.add(virus)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.n_random = self.random.random()
        self.perill = (self.schedule.get_breed_count(PersonaInfectada) + self.schedule.get_breed_count(PersonaMalalta))

        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                    self.schedule.get_breed_count(PersonaSaludable),
                    self.schedule.get_breed_count(PersonaInfectada),
                    self.schedule.get_breed_count(PersonaMalalta),
                    self.schedule.get_breed_count(PersonaMortesPelVirus),
                    self.schedule.get_breed_count(PersonaImmunitzada),
                    self.schedule.get_breed_count(Virus)
                ]
            )

    def run_model(self, step_count=200):

        if self.verbose:
            print("Nombre inicial de persones: ", self.schedule.get_breed_count(PersonaSaludable))
            print("Nombre inicila de virus: ", self.schedule.get_breed_count(Virus))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print("Nombre final de persones saludables: ", self.schedule.get_breed_count(PersonaSaludable))
            print("Nombre final de persones infectades: ", self.schedule.get_breed_count(PersonaInfectada))
            print("Nombre final de persones malaltes: ", self.schedule.get_breed_count(PersonaMalalta))
            print("Nombre final de persones mortes pel virus: ", self.schedule.get_breed_count(PersonaMortaPelVirus))
            print("Nombre final de persones immunitzades: ", self.schedule.get_breed_count(PersonaImmunitzada))
            print("Nombre final de virus: ", self.schedule.get_breed_count(Virus))
