from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.simulation import SimulationInput, SimulationResult
from app.services.queue_simulation import QueueSimulator
from app.models.epidemic import SimulationParams, SimulationState
from app.services.epidemic_simulation import EpidemicSimulator

app = FastAPI(title="Starbucks Queue Simulation System")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Should set specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store simulator instance
epidemic_simulator = None

@app.get("/")
async def root():
    return {"message": "Welcome to Starbucks Queue Simulation System"}

@app.post("/simulate", response_model=SimulationResult)
async def run_simulation(input_data: SimulationInput):
    simulator = QueueSimulator(
        arrival_rate=input_data.arrival_rate,
        service_rate=input_data.service_rate,
        num_servers=input_data.num_servers,
        simulation_time=input_data.simulation_time
    )
    
    avg_wait, avg_queue, utilization, customers = simulator.run_simulation()
    
    return SimulationResult(
        average_wait_time=avg_wait,
        average_queue_length=avg_queue,
        server_utilization=utilization,
        total_customers_served=customers,
        time_points=simulator.time_points,
        queue_lengths_over_time=simulator.queue_lengths_over_time,
        wait_times_over_time=simulator.wait_times_over_time,
        server_utilization_over_time=simulator.server_utilization_over_time
    )

# Epidemic simulation endpoints
@app.post("/epidemic/initialize")
async def initialize_epidemic(params: SimulationParams):
    print("Received params:", params)
    global epidemic_simulator
    epidemic_simulator = EpidemicSimulator(
        population=params.population,
        infection_rate=params.infection_rate,
        recovery_time=params.recovery_time,
        mortality_rate=params.mortality_rate,
        social_distance=params.social_distance,
        movement_speed=params.movement_speed,
        immunity_variation=params.immunity_variation,
        infection_radius=params.infection_radius,
        viral_load_threshold=params.viral_load_threshold,
        recovery_immunity_boost=params.recovery_immunity_boost,
        mask_usage=params.mask_usage,
        vaccination_rate=params.vaccination_rate
    )
    state = epidemic_simulator.get_state()
    print("Initial state:", state)
    return epidemic_simulator.get_state()

@app.get("/epidemic/update")
async def update_epidemic():
    global epidemic_simulator
    if epidemic_simulator is None:
        return {"error": "Simulation not initialized"}
    return epidemic_simulator.update()