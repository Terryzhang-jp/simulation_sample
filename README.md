# Starbucks Queue Simulation System

This project is a simulation system that models customer queuing behavior at Starbucks, including both standard queue simulation and epidemic spread simulation in queuing scenarios.

## Features

- **Queue Simulation**
  - Models customer arrival and service rates
  - Calculates average wait times
  - Tracks queue lengths over time
  - Monitors server utilization

- **Epidemic Simulation**
  - Simulates disease spread in queuing scenarios
  - Configurable parameters (infection rate, recovery time, etc.)
  - Real-time visualization of spread patterns
  - Includes factors like social distancing and mask usage

## Project Structure

```
starbucks_simulation/
├── backend/               # FastAPI backend server
│   ├── app/
│   │   ├── main.py       # Main application file
│   │   ├── models/       # Data models
│   │   └── services/     # Business logic
│   └── requirements.txt  # Python dependencies
└── frontend/             # Static frontend files
    ├── static/
    │   ├── css/
    │   └── js/
    └── index.html
```

## Prerequisites

- Python 3.8 or higher
- Node.js (optional, for development)
- Web browser

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone [your-repository-url]
   cd simulation_sample
   ```

2. Set up the backend:
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the backend server:
   ```bash
   cd backend
   source venv/bin/activate
   PYTHONPATH=$PYTHONPATH:. uvicorn app.main:app --reload
   ```
   The backend will run on http://localhost:8000

2. Start the frontend server (in a new terminal):
   ```bash
   cd frontend
   python3 -m http.server 8080
   ```
   The frontend will be available at http://localhost:8080

3. Access the application:
   - Open http://localhost:8080 in your web browser
   - API documentation is available at http://localhost:8000/docs

## API Endpoints

- `GET /`: Welcome message
- `POST /simulate`: Run queue simulation
- `POST /epidemic/initialize`: Initialize epidemic simulation
- `GET /epidemic/update`: Update epidemic simulation state

## Configuration

You can modify simulation parameters through the frontend interface or by sending requests directly to the API endpoints.

Key configurable parameters include:
- Arrival rate
- Service rate
- Number of servers
- Simulation time
- Infection rate
- Recovery time
- Social distancing factor
- Mask usage rate

## Development

To modify the simulation parameters or add new features:
1. Backend changes: Modify files in the `backend/app` directory
2. Frontend changes: Update the HTML/JS/CSS files in the `frontend` directory

## License

[Your License Here]

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request 