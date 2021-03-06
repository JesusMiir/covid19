from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from covid19.agents import PersonaSaludable, PersonaInfectada, PersonaMalalta, PersonaMortaPelVirus, PersonaImmunitzada, Virus
from covid19.model import Covid19


def covid19_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is PersonaSaludable:
        portrayal["Shape"] = "covid19/resources/persona_saludable.jpg"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 5

    if type(agent) is PersonaInfectada:
        portrayal["Shape"] = "covid19/resources/persona_infectada.jpg"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 4
    
    if type(agent) is PersonaMalalta:
        portrayal["Shape"] = "covid19/resources/persona_malalta.jpg"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 3

    if type(agent) is PersonaImmunitzada:
        portrayal["Shape"] = "covid19/resources/persona_immune.jpg"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2

    elif type(agent) is Virus:
        portrayal["Shape"] = "covid19/resources/virus.jpg"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    return portrayal
        


canvas_element = CanvasGrid(covid19_portrayal, 8, 8, 500, 500)
chart_element = ChartModule(
    [{"Label": "PersonaSaludable", "Color": "#00FF0D"}, {"Label": "PersonaInfectada", "Color": "#FF8700"},
     {"Label": "PersonaMalalta", "Color": "#AB1103"}, {"Label": "PersonaMortaPelVirus", "Color": "#333333"},
     {"Label": "PersonaImmunitzada", "Color": "#08F0EE"},{"Label": "Virus", "Color": "#EA08F0"}]
)


model_params = {
    "inicial_persones": UserSettableParameter(
        "slider", "Inici persones", 5, 0, 10
    ),
    "inicial_virus": UserSettableParameter(
        "slider", "Inici virus", 3, 0, 10
    ),
    "reproduccio_persones": UserSettableParameter(
        "slider", "Reproducció persones", 2, 0, 10
    ),
    "infeccio_virus": UserSettableParameter(
        "slider", "Infecció virus", 6, 0, 10
    ),
    "reproduccio_virus": UserSettableParameter(
        "slider", "Reproducció virus", 3, 0, 10
    ),
    "temps_deteccio": UserSettableParameter(
        "slider", "Temps detecció", 6, 0, 10
    ),
    "durada_malaltia": UserSettableParameter(
        "slider", "Durada malaltia", 8, 0, 10
    ),
    "temps_vida_virus": UserSettableParameter(
        "slider", "Temps de vida del virus", 5, 0, 10
    ),
    "mortalitat_virus": UserSettableParameter(
        "slider", "Mortalitat del virus", 2, 0, 10
    ),
    "mutacio_virus": UserSettableParameter(
        "slider", "Mutació del virus", 2, 0, 5
    ),
    "perill_model": UserSettableParameter(
        "slider", "Nombre de persones afectades per aïllament", 5, 0, 10
    )
}

server = ModularServer(
    Covid19, [canvas_element, chart_element], "COVID19", model_params
)
server.port = 8521
