from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from covid19.agents import PersonaSaludable, PersonaInfectada, PersonaMalalta, PersonaMortaPelVirus, PersonaImmunitzada, Virus
from covid19.schedule import RandomActivationByBreed


class Covid19(Model):

    height = 10
    width = 10

    inicial_perones = 20
    inicial_virus = 10
    reproduccio_persones = 5
    reproduccio_virus = 5
    
    temps_vida_virus = 5

    temps_deteccio = 1
    durada_malaltia = 1
    mortalitat_virus = 1

    verbose = False  # Print-monitoring

    description = (
        "El model vol simular la capacitat que te un virus d'infectar a la població."
    )

    def __init__(
        self,
        height=20,
        width=20,
        inicial_persones=10,
        inicial_virus=5,
        reproduccio_persones = 2,
        reproduccio_virus = 2,

        temps_vida_virus = 5,

        temps_deteccio=3,
        durada_malaltia=3,
        mortalitat_virus=1
    ):

        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.inicial_persones = inicial_persones
        self.inicial_virus = inicial_virus
        self.reproduccio_persones = reproduccio_persones
        self.reproduccio_virus = reproduccio_virus
        
        self.temps_vida_virus = temps_vida_virus
        
        self.temps_deteccio = temps_deteccio
        self.durada_malaltia = durada_malaltia
        self.mortalitat_virus = mortalitat_virus


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
            energia = self.temps_vida_virus * self.random.random() * 500
            virus = Virus(self.next_id(), (x, y), self, True, energia)
            self.grid.place_agent(virus, (x,y))
            self.schedule.add(virus)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
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
