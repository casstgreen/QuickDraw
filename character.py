from gun import GunClass

# The main character class
class CharacterClass:

    def description(self):
        descriptionString = "$%d %s %s: %d Damage, %d%% Accuracy, %d-Shot Capacity, %s Draw Time, %s Reload Time" % \
            (self.cost, self.rarity, self.type, self.damage, self.accuracy, self.capacity, self.draw, self.reload)
        return descriptionString

    def shortDescription(self):
        shortDescriptionString = "%s %s: %d Damage, %d%% Accuracy, %d-Shot Capacity, %s Draw Time, %s Reload Time" % \
            (self.rarity, self.type, self.damage, self.accuracy, self.capacity, self.draw, self.reload)
        return shortDescriptionString

    class InventoryClass:
        pistolAmmo = 0
        revolverAmmo = 0
        shotgunAmmo = 0
        rifleAmmo = 0
        bountyList = []

    class MapClass:
        towns = []
        sites = []
        people = []

    name = ""
    health = 100
    money = 0
    honor = 0
    town = ""
    townDescription = False
    site = ""
    siteDescription = False
    gun = GunClass()
    inventory = InventoryClass()
    map = MapClass()
    gunShop = []
