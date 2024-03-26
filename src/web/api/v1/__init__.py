# src/web/api/v1/__init__.py
from flask import Blueprint
from flask_restx import Api

from src.web.api.v1.time.time_service import TimeService
from src.web.api.v1.simulation.simulation_start import SimulationStart
from src.web.api.v1.simulation.simulation_pause import SimulationPause
from src.web.api.v1.simulation.simulation_continue import SimulationContinue
from src.web.api.v1.simulation.simulation_stop import SimulationStop
from src.web.api.v1.simulation.simulation_status import SimulationStatus


blueprint = Blueprint("api_v1", __name__)
api_v1 = Api(
    blueprint,
    version="1.0",
    title="API Gateway - Version 1",
    description="API Gateway with Swagger support - Version 1",
)

namespace_v1 = api_v1.namespace("v1", description="API version 1")
namespace_v1.add_resource(TimeService, "/time")
namespace_v1.add_resource(SimulationStart, "/simulation/start")
namespace_v1.add_resource(SimulationPause, "/simulation/pause")
namespace_v1.add_resource(SimulationContinue, "/simulation/continue")
namespace_v1.add_resource(SimulationStop, "/simulation/stop")
namespace_v1.add_resource(SimulationStatus, "/simulation/status")
