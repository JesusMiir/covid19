from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from covid19.agents import PersonaSaludable, PersonaInfectada, PersonaMalalta, PersonaImmunitzada, Virus
from covid19.model import Covid19


def covid19_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is PersonaSaludable:
        portrayal["Shape"] = "covid19/resources/persona_saludable.jpg"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    if type(agent) is PersonaInfectada:
        portrayal["Shape"] = "covid19/resources/persona_infectada.jpg"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
    
    if type(agent) is PersonaMalalta:
        portrayal["Shape"] = "covid19/resources/persona_malalta.jpg"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 3
    
    if type(agent) is PersonaImmunitzada:
        portrayal["Shape"] = "covid19/resources/persona_immune.jpg"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 4

    elif type(agent) is Virus:
        portrayal["Shape"] = "covid19/resources/virus.jpg"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 5

    return portrayal
        


canvas_element = CanvasGrid(covid19_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "PersonaSaludable", "Color": "#00FF0D"}, {"Label": "PersonaInfectada", "Color": "#FF8700"},
     {"Label": "PersonaMalalta", "Color": "#AB1103"}, {"Label": "PersonaImmunitzada", "Color": "#08F0EE"},
     {"Label": "Virus", "Color": "#EA08F0"}]
)

model_params = {
    "inicial_persones": UserSettableParameter(
        "slider", "Inici persones", 10, 0, 100
    ),
    "inicial_virus": UserSettableParameter(
        "slider", "Inici virus", 5, 0, 30
    ),
    "temps_deteccio": UserSettableParameter(
        "slider", "Temps detecció", 5, 0, 30
    ),
    "durada_malaltia": UserSettableParameter(
        "slider", "Durada malaltia", 5, 0, 30
    ),
    "mortalitat_virus": UserSettableParameter(
        "slider", "Mortalitat del virus", 1, 0, 100
    )
}

server = ModularServer(
    Covid19, [canvas_element, chart_element], "COVID19", model_params
)
server.port = 8521
