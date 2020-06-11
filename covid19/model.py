from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from covid19.agents import PersonaSaludable, PersonaInfectada, PersonaMalalta, PersonaImmunitzada, Virus
from covid19.schedule import RandomActivationByBreed


class Covid19(Model):

    height = 20
    width = 20

    inicial_perones = 10
    inicial_virus = 10
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
        inicial_virus=10,
        mortalitat_virus=1
    ):

        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.inicial_persones = inicial_persones
        self.inicial_virus = inicial_virus
        self.mortalitat_virus = mortalitat_viurs

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "PersonaSaludable": lambda m: m.schedule.get_breed_count(PersonaSaludable),
                "PersonaInfectada": lambda m: m.schedule.get_breed_count(PersonaInfectada),
                "PersonaMalalta": lambda m: m.schedule.get_breed_count(PersonaMalalta),
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
            energy = 10
            virus = Virus(self.next_id(), (x, y), self, True, energy)
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
                    self.schedule.get_breed_count(PersonaImmunitzada),
                    self.schedule.get_breed_count(Virus)
                ]
            )

    def run_model(self, step_count=200):

        if self.verbose:
            print("Nombre inicial de persones: ", self.schedule.get_breed_count(PersonaSaludable))
            print("Nombre inicial de persones: ", self.schedule.get_breed_count(PersonaInfectada))
            print("Nombre inicial de persones: ", self.schedule.get_breed_count(PersonaMalalta))
            print("Nombre inicial de persones: ", self.schedule.get_breed_count(PersonaImmunitzada))
            print("Nombre inicila de virus: ", self.schedule.get_breed_count(Virus))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print("Nombre final de persones: ", self.schedule.get_breed_count(PersonaSaludable))
            print("Nombre final de persones: ", self.schedule.get_breed_count(PersonaInfectada))
            print("Nombre final de persones: ", self.schedule.get_breed_count(PersonaMalalta))
            print("Nombre final de persones: ", self.schedule.get_breed_count(PersonaImmunitzada))
            print("Nombre final de virus: ", self.schedule.get_breed_count(Virus))
