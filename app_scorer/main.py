from app_scorer.read_input import read
from app_scorer.read_output import read as reado
from loguru import logger
from dataclasses import dataclass


@dataclass
class CarPosition:
    car: list[str] #path
    position: int # from -length to 0 negative or zero


class Street:
    street_id: str
    seconds_length: int
    positions: list[CarPosition]

    def __init__(self, street_id: str, seconds_length: int):
        self.street_id = street_id
        self.seconds_length = seconds_length
        self.positions = []


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


class Intersection:
    intersection_id: int
    streets_in: list[Street]
    streets_out: list[Street]
    schedule: list[Street]  # [A, A, B, C, C, C]

    def __init__(self, intersection_id: int):
        self.intersection_id = intersection_id
        self.streets_in = []
        self.streets_out = []
        self.schedule = []
    
    def __repr__(self):
        repr = f"Intersection - {self.intersection_id}. In: {[st.street_id for st in self.streets_in]}"
        return repr

        


class Simulation:
    sim_dur: int
    bonus_points: int

    def __init__(
        self,
        sim_dur: int,
        num_intersections: int,
        num_streets: int,
        num_cars: int,
        bonus_points: int,
        streets: list[tuple],  # street (start, end, name, length) 0 1 rue-d-amsterdam 1
        car_paths: list[list[str]],  # car_path rue-d-amsterdam rue-de-moscou
    ):
        self.sim_dur = sim_dur
        self.bonus_points = bonus_points
        self.intersections = self._generate_intersections(num_intersections, streets)
        for inters in self.intersections.values():
            logger.debug(inters)
    
    def _generate_intersections(self, num_intersections, streets: list[tuple]) -> dict: 
        intersections = {i:Intersection(i) for i in range(num_intersections)}
        for st in streets:
            start, end, name, length = st
            street = Street(name, length)
            intersections[start].streets_out.append(street)
            intersections[end].streets_in.append(street)
        return intersections


        

    # def simulate(sim_dur, bonus_points, streets, cars) -> int:
    # # Each second of the simulation, update each intersection
    # for second in range(sim_dur):
    #     for intersection in intersections:
    #         intersection.schedule.next()

    # score = sum(car.score for car in cars)
    #     return score


def main():
    simulation_input = read()
    simulation: Simulation = Simulation(*simulation_input)

    schedules = reado()
    logger.debug(schedules)


if __name__ == "__main__":
    main()
