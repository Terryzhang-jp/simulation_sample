from pydantic import BaseModel
from typing import List, Optional, Dict

class Agent(BaseModel):
    id: int
    x: float
    y: float
    state: str  # 'S', 'I', 'R', or 'D'
    days_infected: Optional[int] = None
    immunity: float = 1.0  # 个体免疫力 (0-1)
    viral_load: float = 0.0  # 病毒载量 (0-1)

class SimulationState(BaseModel):
    agents: List[Agent]
    stats: dict
    day: int
    history: Dict[str, List[int]]  # 添加历史数据追踪

class SimulationParams(BaseModel):
    population: int
    infection_rate: float
    recovery_time: int
    mortality_rate: float
    social_distance: float = 20.0  # 社交距离
    movement_speed: float = 5.0  # 移动速度
    social_activity: float = 0.5  # 社交活动水平 (0-1)
    immunity_variation: float = 0.2  # 免疫力变异程度
    infection_radius: float = 30.0  # 感染半径
    viral_load_threshold: float = 0.3  # 感染所需的最小病毒载量
    recovery_immunity_boost: float = 0.8  # 康复后的免疫力提升
    mask_usage: float = 0.0  # 口罩使用率 (0-1)
    vaccination_rate: float = 0.0  # 疫苗接种率 (0-1) 