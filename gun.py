# gun class script

class GunClass:

    # gun constructor
    def __init__(self, cost=0, rarity="", kind="", damage=0, accuracy=0, capacity=0, draw="", reload_status="", loaded=0):

        # the cost of the gun
        self.cost = cost

        # how rare the gun is;  could be ...
        self.rarity = rarity

        # what kind of gun this is; could be pistol, revolver, shotgun, rifle
        self.kind = kind

        # how much damage this gun gives; could be [1, ...]
        self.damage = damage

        # how accurate this gun is; could be [1, ...]
        self.accuracy = accuracy

        # how much capacity this gun ha`s; could be [1, ...]
        self.capacity = capacity

        # ?
        self.draw = draw

        # ?
        self.reload_status = reload_status

        # ? (whether this gun is loaded or not) (how many rounds are loaded into this gun)
        self.loaded = loaded


    # gun methods
