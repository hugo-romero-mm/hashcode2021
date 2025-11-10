output_path = "outputs"
from dataclasses import dataclass
from loguru import logger

files = ["example.out"]

@dataclass
class StreetSchedule:
    street_id: str
    seconds: int

@dataclass
class IntersectionSchedule:
    intersection_id: int
    num_streets_scheduled: int
    schedules: list[StreetSchedule]




def read(index = 0):
    file_path = f"./{output_path}/{files[index]}"
    schedules = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        intersections_scheduled = int(lines.pop(0))
        while lines:
            intersection_id = int(lines.pop(0))
            num_scheduled = int(lines.pop(0))
            intersection_schedule = IntersectionSchedule( intersection_id, num_scheduled, [])
            for i in range(num_scheduled):
                schedule_line = lines.pop(0)
                street, period = schedule_line.split()
                intersection_schedule.schedules.append((street, int(period)))
            schedules.append(intersection_schedule)

    return schedules
