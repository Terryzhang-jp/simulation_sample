from pydantic import BaseModel
from typing import List

class SimulationInput(BaseModel):
    arrival_rate: float
    service_rate: float
    simulation_time: int = 480  # 8 hours in minutes
    num_servers: int = 2

class SimulationResult(BaseModel):
    average_wait_time: float
    average_queue_length: float
    server_utilization: float
    total_customers_served: int
    time_points: List[float]
    queue_lengths_over_time: List[float]
    wait_times_over_time: List[float]
    server_utilization_over_time: List[float] 