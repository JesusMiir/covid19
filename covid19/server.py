from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from covid19.agents import PersonaInfectada, Virus
from covid19.model import Covid19


def covid19_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is PersonaInfectada:
        portrayal["Shape"] = "covid19/resources/persona_immune.jpg"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Virus:
        portrayal["Shape"] = "covid19/resources/virus.jpg"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2

    return portrayal
        


canvas_element = CanvasGrid(covid19_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "PersonaInfectada", "Color": "#666666"}, {"Label": "Virus", "Color": "#AA0000"}]
)

model_params = {
    "inicial_persones": UserSettableParameter(
        "slider", "Inici persones", 10, 0, 30
    ),
    "persones_reproduccio": UserSettableParameter(
        "slider", "PersonaInfectada Reproduction Rate", 0.04, 0.01, 1.0, 0.01
    ),
    "inicial_virus": UserSettableParameter(
        "slider", "Inici virus", 10, 0, 30
    ),
    "virus_reproduccio": UserSettableParameter(
        "slider", "Virus Reproduction Rate", 0.04, 0.01, 1.0, 0.01
    )
}

server = ModularServer(
    Covid19, [canvas_element, chart_element], "COVID19", model_params
)
server.port = 8521
