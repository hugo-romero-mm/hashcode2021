from app_scorer.read_input import read
from app_scorer.read_output import read as reado
from app_scorer.read_output import IntersectionSchedule
from loguru import logger
from dataclasses import dataclass
import uuid


@dataclass
class Car:
    path: list[str]  # path of streets
    current_path: list[str]
    position: int  # from -length to 0 negative or zero
    score: int
    last_t: int

    def __repr__(self):
        return f"Car{'->'.join(self.path)} Pos: {self.position} Score: {self.score} PathLeft: {len(self.current_path)}"

    def set_position(self, position: int):
        logger.info(f"Setting position of car {'->'.join(self.path)} from {self.position} to {position}")
        self.position = position
    
    def set_score(self, score: int):
        logger.info(f"Setting score of car {'->'.join(self.path)} from {self.score} to {score}")
        self.score = score
    
    def change_street(self) -> str:
        if not self.current_path:
            raise Exception("No more streets in path")
        logger.info(f"Car {'->'.join(self.path)} changing street to {self.current_path[0]}")
        return self.current_path.pop(0)

class Street:
    street_id: str
    seconds_length: int
    cars: list[Car]

    def __init__(self, street_id: str, seconds_length: int):
        self.street_id = street_id
        self.seconds_length = seconds_length
        self.cars = []
    
    def __repr__(self):
        repr = f"Street - {self.street_id}. Length: {self.seconds_length}. Cars: {len(self.cars)}"
        repr += f"\n  Cars detail: {[str(car) for car in self.cars]}"
        return repr


class Intersection:
    intersection_id: int
    streets_in: list[str]
    # streets_out: list[Street]
    schedule: list[str]  # [A, A, B, C, C, C]
    current_index = 0

    def __init__(self, intersection_id: int):
        self.intersection_id = intersection_id
        self.streets_in = []
        self.streets_out = []
        self.schedule = []
        self.current_index = 0

    def __repr__(self):
        repr = f"Intersection - {self.intersection_id}. In: {[st for st in self.streets_in]}"
        return repr

    def update(
        self,
        streets_dict: dict[str, Street],
        total_seconds,
        current_second,
        BONUS,
        current_score: int,
    ):
        for street_id in self.streets_in:
            street = streets_dict[street_id]
            scored = []
            for car in street.cars:
                if car.last_t == current_second:
                    continue
                car.last_t = current_second
                car.set_position(car.position + 1)
                if car.position == 0 and not car.current_path:
                    # SCORE CAR
                    car.set_score(BONUS + total_seconds - current_second)
                    scored.append(car)

            logger.debug(f"Street {street.street_id} cars after moving: {[str(car) for car in street.cars]}")
            for scored_car in scored:
                logger.debug(f"Car {scored_car} scored at intersection {self.intersection_id} on street {street.street_id} at T={current_second} with score {scored_car.score}")
                current_score += scored_car.score
                street.cars.remove(scored_car)
                logger.debug(f"Street {street.street_id} cars after scoring: {[str(car) for car in street.cars]}")

        logger.debug(f"Intersection {self.intersection_id} - Current schedule index: {self.current_index} - Schedule: {self.schedule}")
        if not self.schedule:
            return current_score
        
        open_street: str = self.schedule[self.current_index]
        street = streets_dict[open_street]
        if street.cars and street.cars[0].position >= 0:  # TODO: review if only >
            car = street.cars[0]
            logger.debug(f"Car {car} moving from {street.street_id}")
            new_street_name = car.change_street()
            
            new_street = streets_dict[new_street_name]
            car.set_position(-new_street.seconds_length)
            new_street.cars.append(car)
            logger.debug(f"Car {car} moving from {street.street_id} to {new_street_name} at T={current_second}")
        self.current_index = (self.current_index + 1) % len(self.schedule)
        return current_score



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
        self.intersections, self.streets = self._generate_intersections(num_intersections, streets)
        for car_path in car_paths:
            car = Car(car_path, car_path.copy(), 0, 0, -1)
            first_street = car.current_path.pop(0)
            self.streets[first_street].cars.append(car)

    def _generate_intersections(self, num_intersections, streets: list[tuple]) -> tuple[
        dict[int, Intersection], dict[str, Street]
    ]:
        intersections = {i: Intersection(i) for i in range(num_intersections)}
        parsed_streets = {}
        for st in streets:
            start, end, name, length = st
            street = Street(name, length)
            # intersections[start].streets_out.append(street)
            intersections[end].streets_in.append(name)
            parsed_streets[name] = street
        return intersections, parsed_streets

    def __repr__(self):
        repr = f"""
        Simulation - Duration: {self.sim_dur}, Bonus: {self.bonus_points}
        Intersections: {'\n'.join([str(inter) for inter in self.intersections.values()])}
        Streets: {'\n'.join([str(st) for st in self.streets.values()])}
        """
        return repr

    def simulate(self, schedules: list[IntersectionSchedule]) -> int:
        for schedule in schedules:
            intersection = self.intersections[schedule.intersection_id]
            for inter_schedule in schedule.schedules:
                for _ in range(inter_schedule.seconds):
                    intersection.schedule.append(inter_schedule.street_id)
            intersection.schedule = [st.street_id for st in schedule.schedules]


        current_score = 0


        for second in range(self.sim_dur):
            logger.debug(f"--- Second {second} ---")
            for intersection in self.intersections.values():
                current_score = intersection.update(self.streets, self.sim_dur, second, self.bonus_points, current_score)
                logger.debug(f"Second {second} - Current score: {current_score}")
        return current_score

def main():
    simulation_input = read()
    simulation: Simulation = Simulation(*simulation_input)

    logger.debug(simulation)
    schedules = reado()
    final_score = simulation.simulate(schedules)
    logger.info(f"Final score: {final_score}")

    schedules = reado()
    logger.debug(schedules)


if __name__ == "__main__":
    main()
