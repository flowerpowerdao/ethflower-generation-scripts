import re
from bs4 import BeautifulSoup
from pathlib import Path
from random import choices
from ethflower_generator.utils import calculate_weights, get_filenames, add_assets, add_petal_animation, get_trait
import json
import csv

# its important that the different material files are in this order!
# the order is following the order in the folder the assets live in
material_weights = [
    0.09,  # acrylic
    0.13,  # bronze
    0.16,  # ceramic white
    0.15,  # chrome black
    0.11,  # diamond
    0.10,  # gold
    0.14,  # marble
    0.12,  # silver
]

symbol_weights = [
    0.03,  # banking
    0.05,  # control
    0.13,  # finance
    0.20,  # inflation
    0.16,  # maximalism
    0.09,  # nasdaq
    0.16,  # oligarchy
    0.11,  # wall street
    0.07  # web2
]

background_weights = [
    0.25,  # black
    0.35,  # grey
    0.40  # white
]


grave_weights = calculate_weights(material_weights, symbol_weights)


def assemble_svgs():
    # delete json if it exists
    Path("btcflower.json").unlink(missing_ok=True)

    # get all the relative filenames for the different layers
    # specify substrings in exclude_list to exclude certain files
    flowers = get_filenames("../assets/flowers",
                            exclude_list=["lowres", "thumbnail"])
    backgrounds = get_filenames(
        "../assets/backgrounds", exclude_list=["lowres", "thumbnail"])
    coins = get_filenames(
        "../assets/coins", exclude_list=["lowres", "thumbnail"])
    graves = get_filenames(
        "../assets/graves", exclude_list=["lowres", "thumbnail"])

    # get the path to the template svg file the assets will be embedded in
    template = Path(__file__).parent / "template.svg"

    # open the template file and get the soup
    # this has to be done twice because we have call by reference
    with template.open() as svg_template:
        soup = BeautifulSoup(svg_template, 'xml')

    with template.open() as svg_template:
        lowres_soup = BeautifulSoup(svg_template, 'xml')

    btcflower = []

    for i in range(2015):
        flower = choices(flowers, material_weights)[0]
        lowres_flower = Path(flower)
        lowres_flower = str(Path(lowres_flower.parent /
                                 ("_lowres_" + lowres_flower.name)))

        background = choices(backgrounds, background_weights)[0]
        lowres_background = Path(background)
        lowres_background = str(Path(lowres_background.parent /
                                     ("_lowres_" + lowres_background.name)))

        coin = choices(coins, material_weights)[0]
        lowres_coin = Path(coin)
        lowres_coin = str(Path(lowres_coin.parent /
                               ("_lowres_" + lowres_coin.name)))

        grave = choices(graves, grave_weights)[0]
        lowres_grave = Path(grave)
        lowres_grave = str(Path(lowres_grave.parent /
                                ("_lowres_" + lowres_grave.name)))

        add_assets(
            soup,
            flower,
            background,
            coin,
            grave
        )

        add_assets(
            lowres_soup,
            lowres_flower,
            lowres_background,
            lowres_coin,
            lowres_grave
        )

        soups = add_petal_animation(
            [soup, lowres_soup])

        if "gold" in flower and "gold" in coin and "gold" in grave:
            print("triple gold")

        if "acrylic" in flower and "acrylic" in coin and "acrylic" in grave:
            print("triple acrylic")

        if "diamond" in flower and "diamond" in coin and "diamond" in grave:
            print("triple diamond")

        with Path("../assets/"+str(i+1)+".svg").open('w') as random_svg:
            random_svg.write(str(soups[0]))
        with Path("../assets/"+str(i+1)+"_low.svg").open('w') as random_svg_low:
            random_svg_low.write(str(soups[1]))

        btcflower.append(
            {
                "mint_number": i+1,
                "background": get_trait(background),
                "flower": get_trait(flower),
                "coin": get_trait(coin),
                "grave": get_trait(grave)
            }
        )

    with open('ethflower.json', 'w') as f:
        json.dump(btcflower, f, ensure_ascii=False, indent=4)

    with open('ethflower.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(
            ["mint_number", "background", "flower", "coin", "grave"])
        for entry in btcflower:
            spamwriter.writerow(
                [entry["mint_number"], entry["background"], entry["flower"], entry["coin"], entry["grave"]])
