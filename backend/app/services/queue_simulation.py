import numpy as np
from typing import List, Tuple
from app.models.simulation import SimulationInput, SimulationResult

class QueueSimulator:
    def __init__(self, arrival_rate: float, service_rate: float, num_servers: int, simulation_time: int):
        self.arrival_rate = arrival_rate / 60  # Convert to per minute
        self.service_rate = service_rate / 60  # Convert to per minute
        self.num_servers = num_servers
        self.simulation_time = simulation_time
        self.time_points = []
        self.queue_lengths_over_time = []
        self.wait_times_over_time = []
        self.server_utilization_over_time = []

    def generate_arrival_times(self) -> List[float]:
        # Generate inter-arrival times using exponential distribution
        inter_arrival_times = np.random.exponential(1/self.arrival_rate, size=1000)
        arrival_times = np.cumsum(inter_arrival_times)
        return arrival_times[arrival_times <= self.simulation_time].tolist()

    def generate_service_times(self, num_customers: int) -> List[float]:
        # Generate service times using exponential distribution
        return np.random.exponential(1/self.service_rate, size=num_customers).tolist()

    def run_simulation(self) -> Tuple[float, float, float, int]:
        arrival_times = self.generate_arrival_times()
        service_times = self.generate_service_times(len(arrival_times))
        
        # Initialize tracking variables
        server_free_times = [0.0] * self.num_servers
        wait_times = []
        queue_lengths = []
        current_time = 0
        
        # For time series data
        time_step = 5  # Record data every 5 minutes
        next_record_time = 0
        
        for i, arrival_time in enumerate(arrival_times):
            # Find earliest available server
            earliest_free_server = min(range(self.num_servers), key=lambda x: server_free_times[x])
            service_start = max(arrival_time, server_free_times[earliest_free_server])
            
            # Calculate wait time
            wait_time = service_start - arrival_time
            wait_times.append(wait_time)
            
            # Update server free time
            server_free_times[earliest_free_server] = service_start + service_times[i]
            
            # Record queue length at this point
            current_queue_length = sum(1 for t in server_free_times if t > arrival_time)
            queue_lengths.append(current_queue_length)
            
            # Record time series data
            while arrival_time >= next_record_time:
                self.time_points.append(next_record_time)
                self.queue_lengths_over_time.append(current_queue_length)
                self.wait_times_over_time.append(np.mean(wait_times[-10:]) if wait_times else 0)
                busy_servers = sum(1 for t in server_free_times if t > next_record_time)
                self.server_utilization_over_time.append(busy_servers / self.num_servers)
                next_record_time += time_step

        return (
            np.mean(wait_times),
            np.mean(queue_lengths),
            np.sum(service_times) / (self.simulation_time * self.num_servers),
            len(arrival_times)
        ) 