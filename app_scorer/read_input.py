input_path = "hashcode_2021_qualification_round.in"

files = ["a_example.in","b_ocean.in","c_checkmate.in","d_daily_commute.in","e_etoile.in","f_forever_jammed.in"]


def read(index = 0):
    file_path = f"./{input_path}/{files[index]}"
    sim_dur, num_intersections, num_streets, num_cars, bonus_points = 0,0,0,0,0
    streets = []
    car_paths = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i,line in enumerate(lines):
            if i==0:
                sim_dur, num_intersections, num_streets, num_cars, bonus_points = map(int, line.split())
            if i>0 and i<=num_streets:
                start, end, name, length = map(str, line.split())
                start, end, length = map(int, (start, end, length))
                street = (start, end, name, length)
                streets.append(street)
            # Car paths
            if i > num_streets:
                _, *car_path = line.split()
                car_paths.append(car_path)


    return sim_dur, num_intersections, num_streets, num_cars, bonus_points, streets, car_paths