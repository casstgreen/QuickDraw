# Main script for Quick Draw game

import random, sys
from character import CharacterClass

# TODO:  keep splitting up into appropriate files
#           maybe one for lists

def main():

    peopleList = ["BANKER", "BARMAN", "BARTENDER", "BLACKSMITH", "CUSTOMER", "DRUNK", \
        "GAMBLER", "GANGSTER", "GENTLEMAN", "GUARD", "INNKEEPER", "JAILER", "LADY", \
        "MAN", "OUTLAW", "PRISONER", "SHERIFF", "SHOPKEEPER", "WOMAN"]
    townList = ["CANYON", "RED", "SANTA", "SANTORINO", "SILVERTHORNE", "WILD"]
    siteList = ["ABANDONED", "BANK", "BARBER", "BLACKSMITH", "GENERAL", "GRAND", \
        "GREEN", "HOLE", "INN", "JAIL", "PRANCING", "SALOON", "SHERIFF'S", "STREET", \
        "UNDERTAKER'S", "WESTERN"]
    itemList = ["BEER", "BREAD", "CASH", "CHEESE", "GUN", "HAM", "MEAT", "MONEY", \
        "PEANUTS", "PINT", "WHISKEY"]
    locationList = townList + siteList
    gunList = ["COMMON", "EPIC", "LEGENDARY", "PEARLESCENT", "PISTOL", "RARE", \
        "REVOLVER", "RIFLE", "SHOTGUN", "UNCOMMON"]
    containerList = ["CHEST", "DRAWER", "REGISTER"]

    primaryCommands = ["ATTACK", "BUY", "CHALLENGE", "CLIMB", "DIAGNOSTIC", \
        "DOWN", "DOWNSTAIRS", "DUEL", "ENTER", "EXIT", "GET", "GO", "HELLO", \
        "HI", "INVENTORY", "KILL", "LOOK", "NO", "OPEN", "PICK", "PURCHASE", "QUIT", \
        "RESTART", "SHOOT", "SHOP", "SPEAK", "STATS", "TAKE", "TALK", "UP", \
        "UPSTAIRS", "YES"]
    secondaryCommands = ["EDIT"]

    player = CharacterClass()
    player = intro(townList, siteList)

    while player.health > 0:
        response = parse(raw_input("\n>").upper(), peopleList, locationList, \
            itemList, gunList, containerList, primaryCommands, secondaryCommands)
        print response  # delete
        player = action(player, response, townList, siteList)

    #exit()


def action(playerAction, responseAction, townList, siteList):

    # Initialize primary and secondary responses
    primaryResponse = responseAction[0]
    secondaryResponse = responseAction[1]

    # List of actions
    if primaryResponse in townList or primaryResponse in siteList:
        playerAction = go(playerAction, primaryResponse, responseAction, townList, \
            siteList)

    elif primaryResponse == "ENTER":
        if secondaryResponse == "BLANK":
            print "Enter what?"
        else:
            playerAction = go(playerAction, secondaryResponse, responseAction, townList, \
                siteList)

    elif primaryResponse == "EXIT":
        if secondaryResponse in siteList:
            playerAction = go(playerAction, "STREET", responseAction, townList, \
                siteList)
        else:
            answer = raw_input("\nEnd game?\n\n>").upper()
            if answer == "YES":
                print
                sys.exit()  # End game

    elif primaryResponse == "GO":
        if secondaryResponse == "BLANK":
            print "Go where?"
        else:
            playerAction = go(playerAction, secondaryResponse, responseAction, townList, \
                siteList)

    elif primaryResponse == "INVENTORY":
        print "\nHere's what you're carrying:\n"
        print "\t%s" % playerAction.gun.shortDescription()
        print "\tPistol Ammo: %d" % playerAction.inventory.pistolAmmo
        print "\tRevolver Ammo: %d" % playerAction.inventory.revolverAmmo
        print "\tShotgun Ammo: %d" % playerAction.inventory.shotgunAmmo
        print "\tRifle Ammo: %d" % playerAction.inventory.rifleAmmo
        print "\tBounty List: %s" % playerAction.inventory.bountyList

    elif primaryResponse == "LOOK":
        look(playerAction)

    elif primaryResponse == "STATS":
        print "\nHere are your player stats:\n"
        print "\tName: %s" % playerAction.name
        print "\tHealth: %s" % playerAction.health
        print "\tMoney: %s" % playerAction.money
        print "\tHonor: %s" % playerAction.honor
        if secondaryResponse == "EDIT":
            editResponse = raw_input("\n>").upper()
            while editResponse <> "DONE":
                editArray = editResponse.split()
                if editArray[0] == "NAME":
                    playerAction.name = editArray[1]
                elif editArray[0] == "HEALTH":
                    playerAction.health = int(editArray[1])
                elif editArray[0] == "MONEY":
                    playerAction.money = int(editArray[1])
                elif editArray[0] == "HONOR":
                    playerAction.honor = int(editArray[1])
                else:
                    print "\nType STAT NAME and VALUE, or DONE to exit."
                editResponse = raw_input("\n>").upper()
            print "\nSTATS saved."
    elif primaryResponse == "TALK":
        if secondaryResponse == "BLANK":
            print "Talk to who?"
        else:
            playerAction = talk(playerAction, secondaryResponse)

    return playerAction


def changeLocation(playerChangeLocation, locationString, locationType):

    # Get map array
    locationArray = map(playerChangeLocation)

    if locationType == "TOWN":
        if locationString == "WILD":
            print "\nYou're not ready for the WILD COUNTRY yet."
            return playerChangeLocation
        else:
            for town in playerChangeLocation.map.towns:
                if keyword(locationString) == town:
                    playerChangeLocation.town = town
                    playerChangeLocation = map(playerChangeLocation)
    elif locationType == "SITE":
        for site in playerChangeLocation.map.sites:
            if locationString == site.partition(' ')[0]:
                playerChangeLocation.site = site

    return playerChangeLocation


def go(playerGo, location, fullResponse, townList, siteList):

    # If Town
    if keyword(location) in playerGo.map.towns:
        if playerGo.site == "STREET":
            changeLocation(playerGo, location, "TOWN")
            look(playerGo)
        else:
            print "\nYou must go be in the STREET before you can leave town!"
    # If Site
    elif keyword(location) in playerGo.map.sites:
        changeLocation(playerGo, location, "SITE")
        print "\nYou're now in the %s." % playerGo.site
    # If Person
    elif keyword(location) in playerGo.map.people:
        talk(playerGo, location)
    else:
        print "\nThat's not an option."
    return playerGo


def gunShop(playerGunShop):

    gunOption0 = playerGunShop.GunClass()
    gunOption1 = playerGunShop.GunClass()
    gunOption2 = playerGunShop.GunClass()
    gunOption3 = playerGunShop.GunClass()
    gunOption4 = playerGunShop.GunClass()

    playerGunShop.gunShop = [gunOption0, gunOption1, gunOption2, gunOption3, \
        gunOption4]

    i = 0

    for gun in playerGunShop.gunShop:
        # Type Random Number Generator (RNG)
        typeRand = random.randint(1, 100)

        # Rarity RNG
        if abs(playerGunShop.honor) < 20:
            rarityRand = random.randint(1, 15)
        elif abs(playerGunShop.honor) < 40:
            rarityRand = random.randint(5, 30)
        elif abs(playerGunShop.honor) < 60:
            rarityRand = random.randint(15, 55)
        elif abs(playerGunShop.honor) < 80:
            rarityRand = random.randint(30, 85)
        elif abs(playerGunShop.honor) <= 100:
            rarityRand = random.randint(50, 100)

        # Rarity Classification and Raw Damage Determiner
        if rarityRand <= 10:
            gun.rarity = "Common"
            gun.damage = random.randint(10, 17)
        elif rarityRand <= 20:
            gun.rarity = "Uncommon"
            gun.damage = random.randint(18, 25)
        elif rarityRand <= 40:
            gun.rarity = "Rare"
            gun.damage = random.randint(26, 45)
        elif rarityRand <= 70:
            gun.rarity = "Epic"
            gun.damage = random.randint(46, 70)
        elif rarityRand <= 94:
            gun.rarity = "Legendary"
            gun.damage = random.randint(71, 94)
        elif rarityRand <= 100:
            gun.rarity = "Pearlescent"
            gun.damage = random.randint(110, 150)

        # Type Classification and Final Damage Determiner
        if typeRand <= 30:
            gun.type = "Pistol"
            gun.damage *= 0.75
            gun.damage = int(round(gun.damage))
        elif typeRand <= 60:
            gun.type = "Revolver"
        elif typeRand <= 85:
            gun.type = "Shotgun"
            gun.damage *= 0.75
            gun.damage = int(round(gun.damage))
        elif typeRand <= 100:
            gun.type = "Rifle"
            gun.damage *= 1.25
            gun.damage = int(round(gun.damage))

        # Capacity Determiner
        if gun.type == "Revolver":
            gun.capacity = 6
        else:
            gun.capacity = random.randint(2, 12)

        # Draw Determiner
        if (gun.type == "Pistol" or gun.type == "Revolver"):
            drawRand = random.randint(3, 5)
        else:
            drawRand = random.randint(1, 3)

        # Reload Determiner
        if gun.type == "Pistol":
            reloadRand = random.randint(3, 5)
        elif gun.type == "Revolver":
            reloadRand = random.randint(2, 4)
        else:
            reloadRand = random.randint(1, 3)

        # Associate Draw and Reload Rand's with words
        speedDictionary = {
            "1": "VERY SLOW",
            "2": "SLOW",
            "3": "AVERAGE",
            "4": "FAST",
            "5": "VERY FAST",
        }
        gun.draw = speedDictionary[str(drawRand)]
        gun.reload = speedDictionary[str(reloadRand)]

        # Accuracy Determiner
        if type == "Pistol":
            gun.accuracy = random.randint(0, 25)
        elif type == "Revolver":
            gun.accuracy = random.randint(15, 35)
        else:
            gun.accuracy = random.randint(25, 50)

        # Cost Determiner
        gun.cost = int(100*(float(gun.capacity)/12) + 500*(float(gun.damage)/100) + \
            100*(float(drawRand)/5) + 50*(float(reloadRand)/5) + \
            500*(float(gun.accuracy)/50))

        playerGunShop.gunShop[i] = gun
        i += 1

    print
    for i in range(0, 5):
        print playerGunShop.gunShop[i].description()

    return playerGunShop


def intro(townList, siteList):

    # Initialize intro stats
    playerIntro = CharacterClass()
    playerIntro.name = raw_input("\nPlease enter your name\n\n>").upper()
    playerIntro.health = 100
    playerIntro.money = 0
    playerIntro.honor = 0
    playerIntro.town = "SILVERTHORNE"
    playerIntro.townDescription = True
    playerIntro.site = "STREET"
    playerIntro.siteDescription = True

    #gunIntro = playerIntro.GunClass() 12/16/17 changed to
    gunIntro = playerIntro.gun

    gunIntro.cost = 300
    gunIntro.rarity = "COMMON"
    gunIntro.type = "REVOLVER"
    gunIntro.damage = 12
    gunIntro.accuracy = 20
    gunIntro.capacity = 6
    gunIntro.draw = "AVERAGE"
    gunIntro.reload = "SLOW"

    inventoryIntro = playerIntro.InventoryClass()
    inventoryIntro.revolverAmmo = 12

    playerIntro.gun = gunIntro
    playerIntro.inventory = inventoryIntro
    playerIntro = map(playerIntro)

    # Print intro sequence
    print "\nWelcome to the Old West."
    look(playerIntro)
    print "\nType HELP to see a command list."

    return playerIntro


def keyword(keywordString):

    # Return correct phrase based on keyword
    keywordDictionary = {
        "CANYON": "CANYON SPRINGS",
        "RED": "RED RIDGE",
        "SANTA": "SANTA MARIA",
        "SANTORINO": "SANTORINO",
        "SILVERTHORNE": "SILVERTHORNE",
        "WILD": "WILD COUNTRY",
        "ABANDONED": "ABANDONED THEATRE",
        "BANK": "BANK",
        "BARBER": "BARBER SHOP",
        "BLACKSMITH": "BLACKSMITH",
        "GENERAL": "GENERAL STORE",
        "GRAND": "GRAND PALACE INN",
        "GREEN": "GREEN DRAGON PUB",
        "HOLE": "HOLE IN THE WALL PUB",
        "INN": "INN",
        "JAIL": "JAIL",
        "PRANCING": "PRANCING PONY PUB",
        "SALOON": "SALOON",
        "SHERIFF'S": "SHERIFF'S DEPARTMENT",
        "STREET": "STREET",
        "UNDERTAKER'S": "UNDERTAKER'S",
        "WESTERN": "WESTERN UNION"
    }

    return keywordDictionary[keywordString]


def look(playerLook):

    print "\nThis here's %s.\n" % playerLook.town
    print "You're currently in the %s. Around town you'll also find:\n" % \
        playerLook.site
    for site in playerLook.map.sites:
        if site <> playerLook.site:
            print "\t" + site
    print "\nIf you're looking to leave town, you have %s on one side and %s on the other." % \
        (playerLook.map.towns[0], playerLook.map.towns[1])
    return


def map(playerMap):

    # Attribute Towns and Sites
    if playerMap.town == "CANYON SPRINGS":
        playerMap.map.towns = ["SANTA MARIA", "SILVERTHORNE"]
        playerMap.map.sites = ["STREET", "GENERAL STORE", "INN", "PRANCING PONY PUB", \
            "SHERIFF'S DEPARTMENT"]
    elif playerMap.town == "RED RIDGE":
        playerMap.map.towns = ["SILVERTHORNE", "SANTORINO"]
        playerMap.map.sites = ["STREET", "BARBER SHOP", "GENERAL STORE", \
            "HOLE IN THE WALL PUB", "UNDERTAKER'S", "WESTERN UNION"]
    elif playerMap.town == "SANTA MARIA":
        playerMap.map.towns = ["CANYON SPRINGS", "WILD COUNTRY"]
        playerMap.map.sites = ["STREET", "BLACKSMITH", "BANK", "GENERAL STORE", \
            "GRAND PALACE INN"]
    elif playerMap.town == "SANTORINO":
        playerMap.map.towns = ["RED RIDGE", "WILD COUNTRY"]
        playerMap.map.sites = ["STREET", "ABANDONED THEATRE", "GENERAL STORE", \
            "GREEN DRAGON PUB", "JAIL"]
    elif playerMap.town == "SILVERTHORNE":
        playerMap.map.towns = ["CANYON SPRINGS", "RED RIDGE"]
        playerMap.map.sites = [
            "STREET", "BANK", "GENERAL STORE", "JAIL", "SALOON"
        ]

    #["BANKER", "BARMAN", "BARTENDER", "CUSTOMER", "DRUNK", \
    #    "GAMBLER", "GANGSTER", "GENTLEMAN", "GUARD", "INNKEEPER", "JAILER", "LADY", \
    #    "MAN", "OUTLAW", "PRISONER", "SHERIFF", "WOMAN"]

    # Attribute People (and bounty boards?)
    if playerMap.town == "CANYON SPRINGS":
        if playerMap.site == "STREET":
            playerMap.map.people = ["DRUNK", "MAN", "WOMAN"]
        elif playerMap.site == "GENERAL STORE":
            playerMap.map.people = ["CUSTOMER", "GENTLEMAN", "SHOPKEEPER"]
        elif playerMap.site == "INN":
            playerMap.map.people = ["INNKEEPER", "LADY", "GENTLEMAN"]
        elif playerMap.site == "PRANCING PONY PUB":
            playerMap.map.people = [
                "BARMAN", "DRUNK", "GAMBLER", "GANGSTER", "LADY", "MAN"
            ]
        elif playerMap.site == "SHERIFF'S DEPARTMENT":
            playerMap.map.people = ["PRISONER", "SHERIFF"]
    elif playerMap.town == "RED RIDGE":
        if playerMap.site == "STREET":
            playerMap.map.people = []
        elif playerMap.site == "BARBER SHOP":
            playerMap.map.people = []
        elif playerMap.site == "GENERAL STORE":
            playerMap.map.people = []
        elif playerMap.site == "HOLE IN THE WALL PUB":
            playerMap.map.people = []
        elif playerMap.site == "UNDERTAKER'S":
            playerMap.map.people = []
        elif playerMap.site == "WESTERN UNION":
            playerMap.map.people = []
    elif playerMap.town == "SANTA MARIA":
        if playerMap.site == "STREET":
            playerMap.map.people = []
        elif playerMap.site == "BLACKSMITH":
            playerMap.map.people = []
        elif playerMap.site == "BANK":
            playerMap.map.people = []
        elif playerMap.site == "GENERAL STORE":
            playerMap.map.people = []
        elif playerMap.site == "GRAND PALACE INN":
            playerMap.map.people = []
    elif playerMap.town == "SANTORINO":
        if playerMap.site == "STREET":
            playerMap.map.people = []
        elif playerMap.site == "ABANDONED THEATRE":
            playerMap.map.people = []
        elif playerMap.site == "GENERAL STORE":
            playerMap.map.people = []
        elif playerMap.site == "GREEN DRAGON PUB":
            playerMap.map.people = []
        elif playerMap.site == "JAIL":
            playerMap.map.people = []
    elif playerMap.town == "SILVERTHORNE":
        if playerMap.site == "STREET":
            playerMap.map.people = []
        elif playerMap.site == "GENERAL STORE":
            playerMap.map.people = []
        elif playerMap.site == "JAIL":
            playerMap.map.people = []
        elif playerMap.site == "BANK":
            playerMap.map.people = []
        elif playerMap.site == "SALOON":
            playerMap.map.people = []

    return playerMap

def parse(parseString, peopleList, locationList, itemList, gunList, \
    containerList, primaryCommands, secondaryCommands):

    # Split string into array
    rawArray = parseString.split()
    parseArray = []

    primaryToCharacter = ["ATTACK", "CHALLENGE", "DUEL", "HELLO", "HI", "KILL", \
        "SHOOT", "SPEAK", "TALK"]
    primaryToLocation = ["ENTER", "EXIT", "GO"]
    primaryToItem = ["BUY", "GET", "PICK", "PURCHASE", "TAKE"]
    primaryToContainer = ["CLOSE", "OPEN", "SEARCH"]
    primaryToGeneral = ["STATS"]

    # loop through words in user input
    for rawPrimary in rawArray:

        if rawPrimary in primaryCommands:
            parseArray.append(rawPrimary)
            if rawPrimary in primaryToCharacter:
                for rawSecondary in rawArray:
                    if rawSecondary in peopleList:
                        parseArray.append(rawSecondary)
                        break
            elif rawPrimary in primaryToLocation:
                for rawSecondary in rawArray:
                    if rawSecondary in locationList:
                        parseArray.append(rawSecondary)
                        break
            elif rawPrimary in primaryToItem:
                for rawSecondary in rawArray:
                    if rawSecondary in itemList:
                        parseArray.append(rawSecondary)
                        break
                    elif rawSecondary in gunList:
                        parseArray.append(rawSecondary)
                        break
            elif rawPrimary in primaryToContainer:
                for rawSecondary in rawArray:
                    if rawSecondary in containerList:
                        parseArray.append(rawSecondary)
                        break
            elif rawPrimary in primaryToGeneral:
                for rawSecondary in rawArray:
                    if rawSecondary in secondaryCommands:
                        parseArray.append(rawSecondary)
                        break
            break

        elif rawPrimary in peopleList:
            parseArray.append(rawPrimary)
            break

        elif rawPrimary in locationList:
            parseArray.append(rawPrimary)
            break

        elif rawPrimary in itemList:
            parseArray.append(rawPrimary)
            break

        elif rawPrimary in containerList:
            parseArray.append(rawPrimary)
            break

    # If no keywords are found
    if not parseArray:
        parseArray.append("BLANK")
        print "\nI beg your pardon?"
    if len(parseArray) == 1:
        parseArray.append("BLANK")

    return parseArray


def talk(playerTalk, person):

    talkKeyword = "%s %s %s" % (playerTalk.town, playerTalk.site, person)

    # Dictionary of Character Text
    talkDictionary = {
        "CANYON SPRINGS STREET DRUNK": "Eh? What do you want? Leave me alone!",
        "CANYON SPRINGS STREET MAN": "Are you looking at my wife?!",
        "CANYON SPRINGS STREET WOMAN": "Please don't follow me.",
        "SILVERTHORNE GENERAL STORE SHOPKEEPER": "What're ya lookin' for?"
    }

    print "\n%s" % talkDictionary[talkKeyword]

    if person == "SHOPKEEPER" or person == "BLACKSMITH":
        playerTalk = gunShop(playerTalk)

    return playerTalk


main()
