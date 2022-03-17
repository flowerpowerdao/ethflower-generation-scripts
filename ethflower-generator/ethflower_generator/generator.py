from bs4 import BeautifulSoup
from pathlib import Path
from random import choices
from ethflower_generator.utils import calculate_weights, check_for_triples, get_filenames, add_assets, add_petal_animation, get_trait, print_progress_bar
from ethflower_generator.oracle import add_oracle
from ethflower_generator.plot import plot_bar
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

materials = [
    "acrylic",
    "gold",
    "diamond",
    "silver",
    "bronze",
    "marble",
    "chrome",
    "ceramic",
]

grave_weights = calculate_weights(material_weights, symbol_weights)


def assemble_svgs():
    """assemble the svgs for the collection"""

    # get all the relative filenames for the different layers.
    # specify substrings in exclude_list to exclude certain files by substrings
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

    # the oracle code has to be added to the template only once
    add_oracle(soup)
    add_oracle(lowres_soup)

    btcflower = []

    triples_data = [0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(2015):

        print_progress_bar(i, 2015, "Progress", "Complete")

        flower = choices(flowers, material_weights)[0]
        # this also creates a thumbnail version of the NFT.
        # add the assets to the folders accordingly!
        lowres_flower = flower[:flower.find(
            "/")+1] + "_thumbnail_" + flower[flower.find("/")+1:]

        background = choices(backgrounds, background_weights)[0]
        lowres_background = background[:background.find(
            "/")+1] + "_thumbnail_" + background[background.find("/")+1:]

        coin = choices(coins, material_weights)[0]
        lowres_coin = coin[:coin.find("/")+1] + \
            "_thumbnail_" + coin[coin.find("/")+1:]

        grave = choices(graves, grave_weights)[0]
        lowres_grave = grave[:grave.find(
            "/")+1] + "_thumbnail_" + grave[grave.find("/")+1:]

        add_assets(
            soup,
            flower,
            background,
            coin,
            grave,
            "https://cdfps-iyaaa-aaaae-qabta-cai.raw.ic0.app/"
        )

        add_assets(
            lowres_soup,
            lowres_flower,
            lowres_background,
            lowres_coin,
            lowres_grave,
            "https://cdfps-iyaaa-aaaae-qabta-cai.raw.ic0.app/"
        )

        soups = add_petal_animation(
            [soup, lowres_soup])

        check_for_triples(triples_data, materials, flower, coin, grave)

        with Path("../assets/"+str(i+1)+".svg").open('w') as random_svg:
            random_svg.write(str(soups[0]))
        with Path("../assets/"+str(i+1)+"_thumbnail.svg").open('w') as random_svg_low:
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

    plot_bar(triples_data, materials, "materials",
             "count", "ethflower", "triple_distribution")
