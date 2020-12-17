import random
import sys  # only needed for debugging, see seed-code immediately below

# print what seed was used for debugging, unnecessary for final bot
seed = random.randrange(sys.maxsize)
rng = random.Random(seed)
print("Seed was:", seed)

# Names of factions for IO
factions = ["Guild", "Atreides", "Fremen", "Emperor", "Harkonnen", "BeneGesserit"]

# possible traitors by faction
Guild = [
    ("Guild", 5, "Staban Tuek"),
    ("Guild", 3, "Master Bewt"),
    ("Guild", 3, "Esmar Tuek"),
    ("Guild", 2, "Soo-Soo Sook"),
    ("Guild", 1, "Guild Rep."),
]
Atreides = [
    ("Atreides", 5, "Thufir Hawat"),
    ("Atreides", 5, "Lady Jessica"),
    ("Atreides", 4, "Gurney Halleck"),
    ("Atreides", 2, "Duncan Idaho"),
    ("Atreides", 1, "Dr.Wellington Yueh"),
]
Fremen = [
    ("Fremen", 7, "Stilgar"),
    ("Fremen", 6, "Chani"),
    ("Fremen", 5, "Otheym"),
    ("Fremen", 3, "Shadout Mapes"),
    ("Fremen", 2, "Jamis"),
]
Emperor = [
    ("Emperor", 6, "Hasimir Fenring"),
    ("Emperor", 5, "Captain Aramsham"),
    ("Emperor", 3, "Caid"),
    ("Emperor", 3, "Burseg"),
    ("Emperor", 2, "Bashar"),
]
Harkonnen = [
    ("Harkonnen", 6, "Feyd-Rautha"),
    ("Harkonnen", 4, "Beast Raban"),
    ("Harkonnen", 3, "Piter De Vries"),
    ("Harkonnen", 2, "Captain Iakin Nefud"),
    ("Harkonnen", 1, "Umman Kudu"),
]
BeneGesserit = [
    ("Bene Gesserit", 5, "Alia"),
    ("Bene Gesserit", 5, "Margot Lady Fenrig"),
    ("Bene Gesserit", 5, "Mother Ramallo"),
    ("Bene Gesserit", 5, "Princess Irulan"),
    ("Bene Gesserit", 5, "Wanna Yueh"),
]

# pool of all possible traitors
masterpool = [Guild, Atreides, Fremen, Emperor, Harkonnen, BeneGesserit]

# shuffle turn order (indexes to factions)
turnOrder = range(6)
random.shuffle(turnOrder)

for playerIdx in turnOrder:
    # sending/receiving messages from this player
    print(
        "----------------------------------------\nCurrent player is now",
        factions[playerIdx],
        "\n",
    )

    # create a new pool for the individual player
    pool = []

    # add only *other* factions leaders to it
    for factionIdx in turnOrder:
        if factionIdx != playerIdx:
            pool += masterpool[factionIdx]

    # randomly draw 4 from personal pool
    # this might need different implementation depending on random library availablity
    random.shuffle(pool)
    pool = pool[:4]

    # Harkonnens keep all cards
    if factions[playerIdx] == "Harkonnen":
        print("Your traitors are:")

        # for each of the 4 traitors
        for i in range(4):
            # notify player
            print("the", pool[i][0], "leader,", pool[i][2])

            # remove from master pool for future players
            for factionIdx in range(6):
                try:
                    masterpool[factionIdx].remove(pool[choice])
                except ValueError:
                    pass

        print(
            "take their cards out of the traitor deck in front of your zone and put them in your hand."
        )

    # other factions must choose 1 of the 4
    else:
        # Expect response of A B C D
        choice = ""
        while choice not in ["a", "b", "c", "d"]:
            # Send them the options
            print("Choose one by responding with the letter (a ,b ,c , d):")
            print("a: ", pool[0])
            print("b: ", pool[1])
            print("c: ", pool[2])
            print("d: ", pool[3])
            choice = str(input())
            print(choice)

        # convert to index
        if choice == "a":
            choice = 0
        elif choice == "b":
            choice = 1
        elif choice == "c":
            choice = 2
        elif choice == "d":
            choice = 3

        # Confirm response
        print(
            "You have chosen the",
            pool[choice][0],
            "leader,",
            pool[choice][2],
            "; take his/her card out of the traitor deck in front of your zone and put it in your hand.",
        )

        # remove from master pool for future players
        for factionIdx in range(6):
            try:
                masterpool[factionIdx].remove(pool[choice])
            except ValueError:
                pass
