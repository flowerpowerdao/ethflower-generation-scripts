from pathlib import Path
from bs4 import BeautifulSoup


def manipulate_template(soup):
    # insert flower
    current_flower = soup.find('image', {"id": "flower"})['href']
    soup.find('image', {"id": "flower"})[
        'href'] = current_flower.replace("https://n6au6-3aaaa-aaaae-qaaxq-cai.raw.ic0.app/", "",1)

    # insert background
    current_background = soup.find('image', {"id": "background"})['href']
    soup.find('image', {"id": "background"})[
        'href'] = current_background.replace("https://n6au6-3aaaa-aaaae-qaaxq-cai.raw.ic0.app/", "",1)

    # insert coin
    current_coin = soup.find('image', {"id": "coin"})['href']
    soup.find('image', {"id": "coin"})[
        'href'] = current_coin.replace("https://n6au6-3aaaa-aaaae-qaaxq-cai.raw.ic0.app/", "",1)

    # insert grave
    current_grave = soup.find('image', {"id": "grave"})['href']
    soup.find('image', {"id": "grave"})[
        'href'] = current_grave.replace("https://n6au6-3aaaa-aaaae-qaaxq-cai.raw.ic0.app/", "",1)

    # return manipulated template
    return soup


def main():
    for i in range(2009):

        template = Path(f"../assets/{i+1}.svg")

        with template.open() as svg_template:
            soup = BeautifulSoup(svg_template, 'xml')

        new_soup = manipulate_template(soup)

        with Path(f"../assets/{i+1}.svg").open('w') as random_svg:
            random_svg.write(str(new_soup))

        # template = Path(f"../assets/{i+1}_low.svg")

        # with template.open() as svg_template:
        #     soup = BeautifulSoup(svg_template, 'xml')

        # new_soup = manipulate_template(soup)

        # with Path(f"../assets/{i+1}_low.svg").open('w') as random_svg:
        #     random_svg.write(str(new_soup))

        # template = Path(f"../assets/{i+1}_thumbnail.svg")

        # with template.open() as svg_template:
        #     soup = BeautifulSoup(svg_template, 'xml')

        # new_soup = manipulate_template(soup)

        # with Path(f"../assets/{i+1}_thumbnail.svg").open('w') as random_svg:
        #     random_svg.write(str(new_soup))

if __name__ == "__main__":
    main()
