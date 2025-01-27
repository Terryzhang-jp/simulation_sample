class EpidemicVisualization {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.isRunning = false;
        this.simulator = null;
        this.animationFrame = null;
    }

    initialize(params) {
        this.params = params;
        this.fetchInitialState();
    }

    async fetchInitialState() {
        try {
            const response = await fetch('http://localhost:8000/epidemic/initialize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(this.params)
            });
            console.log('Sending params:', this.params);
            const data = await response.json();
            console.log('Received data:', data);
            this.updateVisualization(data);
            if (this.isRunning) {
                this.startAnimation();
            }
        } catch (error) {
            console.error('Error:', error);
            console.error('Response:', await response.text());
        }
    }

    async updateState() {
        try {
            const response = await fetch('http://localhost:8000/epidemic/update');
            const data = await response.json();
            console.log('Update received:', data);
            this.updateVisualization(data);
        } catch (error) {
            console.error('Error:', error);
        }
    }

    updateVisualization(data) {
        this.drawMainSimulation(data);
        this.drawTrendChart(data);
        this.updateStats(data);
    }

    drawMainSimulation(data) {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw agents
        data.agents.forEach(agent => {
            this.ctx.beginPath();
            this.ctx.arc(agent.x, agent.y, 6, 0, Math.PI * 2);
            
            // Add border to make agents more visible
            this.ctx.strokeStyle = '#000';
            this.ctx.lineWidth = 1;
            
            switch(agent.state) {
                case 'S':
                    this.ctx.fillStyle = '#b8e6ff';
                    break;
                case 'I':
                    this.ctx.fillStyle = '#ffb8b8';
                    break;
                case 'R':
                    this.ctx.fillStyle = '#b8ffb8';
                    break;
                case 'D':
                    this.ctx.fillStyle = '#e6e6e6';
                    break;
            }
            
            this.ctx.fill();
            this.ctx.stroke();
        });
    }

    drawTrendChart(data) {
        const charts = [
            { id: 'susceptible-chart', data: data.history.S, color: '#b8e6ff', label: 'Susceptible' },
            { id: 'infected-chart', data: data.history.I, color: '#ffb8b8', label: 'Infected' },
            { id: 'recovered-chart', data: data.history.R, color: '#b8ffb8', label: 'Recovered' },
            { id: 'deceased-chart', data: data.history.D, color: '#e6e6e6', label: 'Deceased' }
        ];

        charts.forEach(chart => {
            const ctx = document.getElementById(chart.id).getContext('2d');
            const width = ctx.canvas.width;
            const height = ctx.canvas.height;
            ctx.clearRect(0, 0, width, height);

            // 设置样式
            ctx.lineWidth = 2;
            ctx.font = '12px Arial';

            // 计算最大值和合适的刻度
            const maxValue = Math.max(...chart.data, 1); // 确保最小值为1，避免除零
            const days = chart.data.length;
            
            // 计算合适的Y轴刻度
            const yScale = this.calculateNiceScale(0, maxValue);

            // 设置边距
            const margin = { top: 20, right: 30, bottom: 30, left: 50 };
            const plotWidth = width - margin.left - margin.right;
            const plotHeight = height - margin.top - margin.bottom;

            // 绘制坐标轴
            ctx.beginPath();
            ctx.strokeStyle = '#000';
            ctx.moveTo(margin.left, margin.top);
            ctx.lineTo(margin.left, height - margin.bottom);
            ctx.lineTo(width - margin.right, height - margin.bottom);
            ctx.stroke();

            // 绘制Y轴刻度
            const yTicks = 5;
            for (let i = 0; i <= yTicks; i++) {
                const value = Math.round(yScale.min + (yScale.max - yScale.min) * (i / yTicks));
                const y = margin.top + plotHeight * (1 - i / yTicks);
                
                ctx.fillStyle = '#666';
                ctx.textAlign = 'right';
                ctx.fillText(value.toString(), margin.left - 5, y);

                // 绘制网格线
                ctx.beginPath();
                ctx.strokeStyle = '#eee';
                ctx.moveTo(margin.left, y);
                ctx.lineTo(width - margin.right, y);
                ctx.stroke();
            }

            // 计算合适的X轴刻度间隔
            const xTickCount = Math.min(10, days);
            const xTickInterval = Math.max(1, Math.floor(days / xTickCount));

            // 绘制X轴刻度
            for (let i = 0; i < days; i += xTickInterval) {
                const x = margin.left + (plotWidth * i) / (days - 1);
                ctx.fillStyle = '#666';
                ctx.textAlign = 'center';
                ctx.fillText(i.toString(), x, height - margin.bottom + 15);

                // 绘制网格线
                ctx.beginPath();
                ctx.strokeStyle = '#eee';
                ctx.moveTo(x, margin.top);
                ctx.lineTo(x, height - margin.bottom);
                ctx.stroke();
            }

            // 绘制数据线
            ctx.beginPath();
            ctx.strokeStyle = chart.color;
            chart.data.forEach((value, index) => {
                const x = margin.left + (plotWidth * index) / (days - 1);
                const y = margin.top + plotHeight * (1 - (value - yScale.min) / (yScale.max - yScale.min));
                if (index === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            });
            ctx.stroke();

            // 添加标题
            ctx.fillStyle = '#000';
            ctx.textAlign = 'center';
            ctx.font = 'bold 14px Arial';
            ctx.fillText(chart.label, width / 2, margin.top / 2);
        });
    }

    // 计算合适的刻度范围
    calculateNiceScale(min, max) {
        const range = this.niceNumber(max - min, false);
        const tickSpacing = this.niceNumber(range / 10, true);
        const niceMin = Math.floor(min / tickSpacing) * tickSpacing;
        const niceMax = Math.ceil(max / tickSpacing) * tickSpacing;
        return { min: niceMin, max: niceMax, tickSpacing };
    }

    // 计算易读的刻度数值
    niceNumber(range, round) {
        const exponent = Math.floor(Math.log10(range));
        const fraction = range / Math.pow(10, exponent);
        let niceFraction;

        if (round) {
            if (fraction < 1.5) niceFraction = 1;
            else if (fraction < 3) niceFraction = 2;
            else if (fraction < 7) niceFraction = 5;
            else niceFraction = 10;
        } else {
            if (fraction <= 1) niceFraction = 1;
            else if (fraction <= 2) niceFraction = 2;
            else if (fraction <= 5) niceFraction = 5;
            else niceFraction = 10;
        }

        return niceFraction * Math.pow(10, exponent);
    }

    updateStats(data) {
        console.log('Updating stats with:', data.stats);
        // 更新当前状态数据
        document.getElementById('susceptible-count').textContent = data.stats.S;
        document.getElementById('infected-count').textContent = data.stats.I;
        document.getElementById('recovered-count').textContent = data.stats.R;
        document.getElementById('deceased-count').textContent = data.stats.D;
        document.getElementById('day-count').textContent = data.day;
    }

    startAnimation() {
        this.isRunning = true;
        const animate = async () => {
            if (this.isRunning) {
                await this.updateState();
                // 每200ms更新一次，模拟一天
                setTimeout(() => {
                    this.animationFrame = requestAnimationFrame(animate);
                }, 200);
            }
        };
        animate();
    }

    pause() {
        this.isRunning = false;
        if (this.animationFrame) {
            cancelAnimationFrame(this.animationFrame);
        }
    }

    reset() {
        this.pause();
        this.fetchInitialState();
    }
}

// Initialize the visualization
document.addEventListener('DOMContentLoaded', () => {
    const viz = new EpidemicVisualization('simulation-canvas');
    
    document.getElementById('simulation-form').addEventListener('submit', (e) => {
        e.preventDefault();
        const params = {
            population: parseInt(document.getElementById('population').value),
            infection_rate: parseFloat(document.getElementById('infection-rate').value),
            recovery_time: parseInt(document.getElementById('recovery-time').value),
            mortality_rate: parseFloat(document.getElementById('mortality-rate').value),
            social_distance: parseFloat(document.getElementById('social-distance').value),
            social_activity: parseFloat(document.getElementById('social-activity').value) / 100,
            mask_usage: parseFloat(document.getElementById('mask-usage').value) / 100,
            vaccination_rate: parseFloat(document.getElementById('vaccination-rate').value) / 100,
            movement_speed: 5.0,
            immunity_variation: 0.2,
            infection_radius: 30.0,
            viral_load_threshold: 0.3,
            recovery_immunity_boost: 0.8
        };
        viz.initialize(params);
        viz.startAnimation();
    });

    document.getElementById('pause-btn').addEventListener('click', () => {
        if (viz.isRunning) {
            viz.pause();
            document.getElementById('pause-btn').textContent = 'Resume';
        } else {
            viz.startAnimation();
            document.getElementById('pause-btn').textContent = 'Pause';
        }
    });

    document.getElementById('reset-btn').addEventListener('click', () => {
        viz.reset();
    });
}); 