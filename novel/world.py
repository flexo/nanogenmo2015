import random
import operator

from . import terrains
from . import props

class World(list):
    def __init__(self, x, y):
        self.sizex = x
        self.sizey = y

    @classmethod
    def from_random(cls, x, y):
        self = cls(x, y)
        tiles = x * y

        # Generate blank grid:
        for i in range(x):
            row = []
            self.append(row)
            for j in range(y):
                tile = Tile(i, j)
                row.append(tile)

        # Generate some forests:
        for n in range(tiles // 10):
            sizex = random.randint(0, self.sizex // 2)
            sizey = random.randint(0, self.sizey // 2)
            origin = random.randint(0, x - sizex - 1), random.randint(0, y - sizey - 1)
            for i in range(origin[0], origin[0] + sizex):
                for j in range(origin[1], origin[1] + sizey):
                    self[i][j].populate(terrains.Forest)

        # Generate some lakes:
        for n in range(tiles // 8):
            centre = random.randint(0, x - 1), random.randint(0, y - 1)
            radius = random.randint(0, min(x // 8, y // 8))
            radius_sq = radius ** 2
            self[centre[0]][centre[1]].populate(terrains.Lake)
            for offset_i in range(- radius, radius + 1):
                i = centre[0] + offset_i
                if i < 0 or i >= self.sizex:
                    continue
                offset_i_sq = offset_i ** 2
                for offset_j in range(- radius, radius + 1):
                    j = centre[1] + offset_j
                    if j < 0 or j >= self.sizey:
                        continue
                    offset_j_sq = offset_j ** 2
                    if offset_i_sq * offset_j_sq < radius_sq:
                        self[i][j].populate(terrains.Lake)

        # Rest of the map is meadow:
        for i in range(x):
            for j in range(y):
                if self[i][j].terrain is None:
                    self[i][j].populate(terrains.Meadow)

        # Link up grid:
        for i in range(x):
            for j in range(y):
                if j:
                    tile.south = self[i][j - 1]
                    self[i][j - 1].north = tile
                if i:
                    tile.west = self[i - 1][j]
                    self[i - 1][j].east = tile
        return self
    
    def __str__(self):
        s = []
        for y in reversed(range(self.sizey)):
            for x in range(self.sizex):
                s.append("%s | " % (self[x][y]))
            s.append('\n')
        return ''.join(s)


class Tile:
    def __init__(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.terrain = None
        self.west = None
        self.east = None
        self.north = None
        self.south = None
        class PeopleSet(set):
            def __str__(self):
                return ', '.join(str(p) for p in self)
            def random(self, person, k):
                return random.sample(
                    [p for p in sorted(self) if p is not person], k)
        self.people = PeopleSet()
        self.props = []

    def __str__(self):
        s = "%02s" % (self.terrain.symbol,)
        return s

    def __repr__(self):
        return "<Tile terrain=%r people=%r>" % (self.terrain, self.people)

    @property
    def neighbours(self):
        d = {}
        for direction in ('north', 'east', 'south', 'west'):
            if getattr(self, direction) is not None:
                d[direction] = getattr(self, direction)
        return d

    def populate(self, terrain_cls):
        """Set the terrain and generate props"""
        self.terrain = terrain_cls()
        for prop_cls, likelihood in self.terrain.props_available:
            if random.random() < likelihood:
                self.props.append(prop_cls())

    def path_to(self, target_cls):
        visited_nodes = set()
        distances = {}
        parents = {}
        if issubclass(target_cls, terrains.Terrain):
            def target_fn(tile):
                return isinstance(tile, target_cls)
        elif issubclass(target_cls, props.Prop):
            def target_fn(tile):
                for prop in tile.props:
                    if isinstance(prop, target_cls):
                        return True
                return False
        else:
            raise RuntimeError('path_to() for unknown class %r' % (target_cls,))
        dest = _find(self, visited_nodes, distances, parents,
            target_fn=target_fn)
        if dest is not None:
            path = [(dest, '')]
            while path[0][0] != self:
                path = [parents[path[0][0]]] + path
            return path
        return None

    def recursive_update(self, action):
        visited_nodes = set()
        distances = {}
        parents = {}
        _find(self, visited_nodes, distances, parents,
            target_fn=None, action=action)

def _find(current, visited_nodes, distances, parents, target_fn=None, action=None):
    # Dijkstra's algorithm.
    if target_fn and target_fn(current):
        return current
    for direction, neighbour in current.neighbours.items():
        if neighbour not in visited_nodes:
            dist = distances.setdefault(current, 0) + 1
            if neighbour in distances:
                if dist < distances[neighbour]:
                    distances[neighbour] = dist
                    parents[neighbour] = current, direction
            else:
                distances[neighbour] = dist
                parents[neighbour] = current, direction
    if action:
        action(current)
    visited_nodes.add(current)
    unvisited_distances = [
        (k, v) for k, v in distances.items() if k not in visited_nodes]
    if unvisited_distances:
        sorted_distances = sorted(
            unvisited_distances,
            key=operator.itemgetter(1))
        nearest_unvisited, dist = sorted_distances[0]
        return _find(nearest_unvisited, visited_nodes, distances, parents,
            target_fn=target_fn, action=action)
    else:
        # no unvisted nodes, unable to find target
        return None


def opposite_direction(direction):
    d = {'north': 'south',
        'east': 'west',
        'south': 'north',
        'west': 'east'}
    return d[direction]


