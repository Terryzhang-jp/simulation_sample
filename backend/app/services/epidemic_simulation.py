import numpy as np
from typing import List, Dict
from app.models.epidemic import Agent, SimulationState

class EpidemicSimulator:
    def __init__(self, population: int, infection_rate: float, 
                 recovery_time: int, mortality_rate: float,
                 social_distance: float = 20.0,
                 movement_speed: float = 5.0,
                 social_activity: float = 0.5,
                 immunity_variation: float = 0.2,
                 infection_radius: float = 30.0,
                 viral_load_threshold: float = 0.3,
                 recovery_immunity_boost: float = 0.8,
                 mask_usage: float = 0.0,
                 vaccination_rate: float = 0.0):
        
        self.population = population
        # 基础感染率更高，使传播更明显
        self.infection_rate = (infection_rate / 100) * 2
        self.recovery_time = recovery_time
        self.mortality_rate = mortality_rate / 100
        self.social_distance = social_distance
        self.movement_speed = movement_speed
        self.social_activity = social_activity
        self.immunity_variation = immunity_variation
        self.infection_radius = infection_radius
        self.viral_load_threshold = viral_load_threshold
        self.recovery_immunity_boost = recovery_immunity_boost
        self.mask_usage = mask_usage
        self.vaccination_rate = vaccination_rate
        
        self.agents: List[Agent] = []
        self.day = 0
        self.history = {
            'S': [], 'I': [], 'R': [], 'D': []
        }
        self.initialize_agents()

    def initialize_agents(self):
        self.agents = []
        for i in range(self.population):
            # 基础免疫力随机分布，降低基础免疫力使疫苗效果更明显
            base_immunity = np.random.normal(0.3, self.immunity_variation)
            base_immunity = max(0.1, min(0.7, base_immunity))
            
            # 考虑疫苗接种带来的免疫力提升
            if np.random.random() < self.vaccination_rate:
                base_immunity *= 2.0  # 增强疫苗效果
                base_immunity = min(0.95, base_immunity)
            
            self.agents.append(Agent(
                id=i,
                x=np.random.uniform(0, 800),
                y=np.random.uniform(0, 600),
                state='S',
                immunity=base_immunity,
                viral_load=0.0
            ))
        
        # 增加初始感染者数量
        # Multiple initial infected cases
        initial_infected = max(1, int(self.population * 0.02))  # 2% 初始感染者
        for i in range(initial_infected):
            self.agents[i].state = 'I'
            self.agents[i].days_infected = 0
            self.agents[i].viral_load = 1.0

    def update(self) -> SimulationState:
        # Update positions with social distancing
        self.update_positions()
        
        # Update infections and disease progression
        self.update_disease_state()
        
        # Update history
        stats = self.get_stats()
        for state in ['S', 'I', 'R', 'D']:
            self.history[state].append(stats[state])
        
        self.day += 1
        return self.get_state()

    def update_positions(self):
        for agent in self.agents:
            if agent.state != 'D':  # Dead agents don't move
                # 根据社交活动水平决定是否移动
                if np.random.random() < self.social_activity:
                    # 简化移动逻辑，使用随机游走
                    angle = np.random.uniform(0, 2 * np.pi)
                    # 增强社交活动水平对移动速度的影响
                    movement_factor = self.social_activity * 2
                    dx = np.cos(angle) * self.movement_speed * movement_factor
                    dy = np.sin(angle) * self.movement_speed * movement_factor
                    
                    # 应用社交距离
                    nearby_agents = [other for other in self.agents 
                                   if other.id != agent.id and other.state != 'D']
                    for other in nearby_agents:
                        dist_x = agent.x - other.x
                        dist_y = agent.y - other.y
                        distance = np.sqrt(dist_x**2 + dist_y**2)
                        if distance < self.social_distance:
                            # 增强社交距离的影响
                            repulsion_force = (self.social_distance - distance) / self.social_distance
                            dx += (dist_x/distance) * self.movement_speed * repulsion_force * 2
                            dy += (dist_y/distance) * self.movement_speed * repulsion_force * 2
                    
                    agent.x += dx
                    agent.y += dy
                    
                    # Keep within bounds
                    agent.x = max(0, min(800, agent.x))
                    agent.y = max(0, min(600, agent.y))

    def update_disease_state(self):
        newly_infected = []
        
        # 首先处理已感染者的疾病进展（恢复或死亡）
        for agent in self.agents:
            if agent.state == 'I':
                agent.days_infected += 1
                if agent.days_infected >= self.recovery_time:
                    # 计算死亡概率（基于个体免疫力）
                    mortality_chance = self.mortality_rate * (1 - agent.immunity)
                    if np.random.random() < mortality_chance:
                        agent.state = 'D'
                    else:
                        agent.state = 'R'
                        # 康复后获得额外免疫力
                        agent.immunity = min(1.0, agent.immunity * (1 + self.recovery_immunity_boost))
                        agent.viral_load = 0.0
        
        # 然后处理新的感染传播
        for agent in self.agents:
            if agent.state == 'I':
                # Spread infection
                for other in self.agents:
                    if other.state == 'S':
                        distance = np.sqrt(
                            (agent.x - other.x)**2 + 
                            (agent.y - other.y)**2
                        )
                        if distance < self.infection_radius:
                            # Calculate transmission probability
                            transmission_prob = self.infection_rate
                            
                            # Adjust for masks
                            if np.random.random() < self.mask_usage:
                                transmission_prob *= 0.1
                            
                            # Adjust for immunity
                            transmission_prob *= (1 - other.immunity)
                            
                            # 根据距离调整传播概率
                            distance_factor = 1 - (distance / self.infection_radius)
                            transmission_prob *= distance_factor
                            
                            # Attempt infection
                            if np.random.random() < transmission_prob:
                                newly_infected.append(other)
        
        # 最后更新新感染者的状态
        for agent in newly_infected:
            agent.state = 'I'
            agent.days_infected = 0
            agent.viral_load = 1.0

    def get_stats(self) -> Dict[str, int]:
        return {
            'S': sum(1 for a in self.agents if a.state == 'S'),
            'I': sum(1 for a in self.agents if a.state == 'I'),
            'R': sum(1 for a in self.agents if a.state == 'R'),
            'D': sum(1 for a in self.agents if a.state == 'D')
        }

    def get_state(self) -> SimulationState:
        return SimulationState(
            agents=self.agents,
            stats=self.get_stats(),
            day=self.day,
            history=self.history
        ) 