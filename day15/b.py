from tqdm import tqdm
class Sensor:

    cut = 4000000
    def __init__(self, x, y, beacon):
        self.x = x
        self.y = y
        self.beacon = beacon
    
    @property
    def beacon_dist(self):
        return Sensor.manhattan_dist(self, self.beacon)

    @staticmethod
    def manhattan_dist(cls, other):
        x = abs(cls.x-other.x)
        y = abs(cls.y-other.y)

        return (x+y)

    def blocked_at_line(self, line):

        dil = self.beacon_dist - abs(line - self.y)
        if dil > 0:
            start = self.x-dil
            end = self.x+dil
            if start < 0:
                start = 0
            if start > self.cut:
                return None
            if end < 0:
                return None
            if end > self.cut:
                end = self.cut

            return (start, end)
        return None

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.beacon))

    def __str__(self) -> str:
        return f'Sensor x:{self.x} y:{self.y} b_dist:{self.beacon_dist}'


class Beacon:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    
    def __str__(self) -> str:
        return f'Beacon: x={self.x}, y={self.y}'


def blocked(sensors, line):
    blocked_inter = []
    for s in sensors:
        b_iter = s.blocked_at_line(line)
        if b_iter is not None:
            blocked_inter.append(b_iter)
    return blocked_inter

def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    n_intervals = [intervals[0]]
    for i in intervals[1:]:
        if i[0] <= n_intervals[-1][1]+1:
            if i[1] >= n_intervals[-1][1]:
                n_intervals[-1] = (n_intervals[-1][0],i[1])
        else:
            n_intervals.append(i)
    return n_intervals

sensors = set([])
beacons = set([])
max_dist = 0

x_dim = (0, 0)
y_dim = (0, 0)

input = [line.strip() for line in open('input.txt')]

for line in input:
    line = line.split()

    beacon_x = int(line[8].split('=')[1][:-1])
    beacon_y = int(line[9].split('=')[1])

    beacon = Beacon(beacon_x, beacon_y)

    beacons.add(beacon)

    sensor_x = int(line[2].split('=')[1][:-1])
    sensor_y = int(line[3].split('=')[1][:-1])

    sensor = Sensor(sensor_x, sensor_y, beacon)

    sensors.add(sensor)

    if sensor.beacon_dist > max_dist:
        max_dist = sensor.beacon_dist

x_dim = (x_dim[0]-max_dist, x_dim[1]+max_dist)



the_line = None

for line in tqdm(range(0, 4000001)):
    merged_blocked = merge_intervals(blocked(sensors, line))
    if len(merged_blocked) == 2:
        the_line = merged_blocked
        break

print(the_line)
ans = (the_line[0][1]+1) * 4000000 + line
print(ans)