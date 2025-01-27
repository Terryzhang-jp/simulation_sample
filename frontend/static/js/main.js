document.addEventListener('DOMContentLoaded', function() {
    // Test connection to backend
    fetch('http://localhost:8000/')
        .then(response => response.json())
        .then(data => {
            console.log('Backend response:', data);
            document.getElementById('simulation-results').textContent = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('simulation-results').textContent = 'Error connecting to backend';
        });

    // Handle form submission
    const simulationForm = document.getElementById('simulation-form');
    const resultsDiv = document.getElementById('simulation-results');

    simulationForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = {
            arrival_rate: parseFloat(document.getElementById('arrival-rate').value),
            service_rate: parseFloat(document.getElementById('service-rate').value),
            num_servers: parseInt(document.getElementById('num-servers').value),
            simulation_time: 480  // 8 hours in minutes
        };

        try {
            const response = await fetch('http://localhost:8000/simulate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();
            
            // Display summary results
            resultsDiv.innerHTML = `
                <h3>Summary Results:</h3>
                <p>Average Wait Time: ${data.average_wait_time.toFixed(2)} minutes</p>
                <p>Average Queue Length: ${data.average_queue_length.toFixed(2)} customers</p>
                <p>Server Utilization: ${(data.server_utilization * 100).toFixed(1)}%</p>
                <p>Total Customers Served: ${data.total_customers_served}</p>
            `;

            // Create queue length plot
            Plotly.newPlot('queue-length-plot', [{
                x: data.time_points,
                y: data.queue_lengths_over_time,
                type: 'scatter',
                name: 'Queue Length'
            }], {
                title: 'Queue Length Over Time',
                xaxis: { title: 'Time (minutes)' },
                yaxis: { title: 'Number of Customers in Queue' }
            });

            // Create wait time plot
            Plotly.newPlot('wait-time-plot', [{
                x: data.time_points,
                y: data.wait_times_over_time,
                type: 'scatter',
                name: 'Wait Time'
            }], {
                title: 'Average Wait Time Over Time',
                xaxis: { title: 'Time (minutes)' },
                yaxis: { title: 'Wait Time (minutes)' }
            });

            // Create utilization plot
            Plotly.newPlot('utilization-plot', [{
                x: data.time_points,
                y: data.server_utilization_over_time,
                type: 'scatter',
                name: 'Server Utilization'
            }], {
                title: 'Server Utilization Over Time',
                xaxis: { title: 'Time (minutes)' },
                yaxis: { 
                    title: 'Utilization Rate',
                    range: [0, 1]
                }
            });

        } catch (error) {
            console.error('Error:', error);
            resultsDiv.innerHTML = '<p class="error">Error running simulation</p>';
        }
    });
}); 