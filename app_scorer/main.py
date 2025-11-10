
from app_scorer.read_input import read
from app_scorer.read_output import read as reado
from loguru import logger
from dataclasses import dataclass

@dataclass
class CarPosition:
    car: list[str]
    position: int

class Street:
    street_id: str
    seconds_length: int
    positions: list[CarPosition]

class StreetSchedule:
    schedule: list[Street]
    current_index: int = 0

    def __init__(self, schedule_dict: dict[str, int], street_map: dict[str, Street]):
        self.schedule = []
        for street_id, seconds in schedule_dict.items():
            for _ in range(seconds):
                self.schedule.append(street_map[street_id])
        self.current_index = 0

    def next(self) -> Street:
        self.current_index += 1
        if self.current_index >= len(self.schedule):
            self.current_index = 0
        return self.schedule[self.current_index]
    
@dataclass
class Intersection:
    intersection_id: int
    streets: list[Street]
    schedule: list[Street] # [A, A, B, C, C, C]




class Simulation:
    sim_dur: int
    bonus_points: int

    def __init__(self, sim_dur, bonus_points, streets, cars):
        self.sim_dur = sim_dur
    
    # def simulate(sim_dur, bonus_points, streets, cars) -> int:
    # # Each second of the simulation, update each intersection
    # for second in range(sim_dur):
    #     for intersection in intersections:
    #         intersection.schedule.next()
    
    # score = sum(car.score for car in cars)
    #     return score

def main():
    sim_dur, num_intersections, num_streets, num_cars, bonus_points, streets, car_paths = read()
    logger.debug(sim_dur)
    objects = create_objects(sim_dur, bonus_points, streets, cars)

    schedules = reado()
    logger.debug(schedules)


if __name__ == "__main__":
    main()
