# src/web/api/v1/__init__.py
from flask import Blueprint
from flask_restx import Api

from .time_service import TimeService
from .simulation_continue import SimulationContinue
from .simulation_pause import SimulationPause
from .simulation_start import SimulationStart
from .simulation_stop import SimulationStop
from .simulation_status import SimulationStatus

blueprint = Blueprint("api_v1", __name__)
api_v1 = Api(
    blueprint,
    version="1.0",
    title="API Gateway - Version 1",
    description="API Gateway with Swagger support - Version 1",
)

namespace_v1 = api_v1.namespace("v1", description="API version 1")
namespace_v1.add_resource(TimeService, "/time")
namespace_v1.add_resource(SimulationStart, "/simulation_start")
namespace_v1.add_resource(SimulationPause, "/simulation_pause")
namespace_v1.add_resource(SimulationContinue, "/simulation_continue")
namespace_v1.add_resource(SimulationStop, "/simulation_stop")
namespace_v1.add_resource(SimulationStatus, "/simulation_status")
