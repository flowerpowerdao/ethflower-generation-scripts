from pathlib import Path
from random import choice, uniform
from typing import List


def calculate_weights(weights_1, weights_2):
    """Returns the product of the two lists, starting from the first element in weights_1 multiplied by all the elemnts in weights_2"""

    all_weights = []

    for weight_1 in weights_1:
        for weight_2 in weights_2:
            all_weights.append(weight_1*weight_2)

    return all_weights


def get_filenames(path, exclude_list: List[str]):
    """Returns a list of filenames in the given path relative to assets"""

    folder_path = Path(path)
    # filter out files that have lowres in their path so we don't
    # have twice the same flower
    relative_filenames = [str(file_path.relative_to("../assets/"))
                          for file_path in sorted(folder_path.glob("*")) if not any(excluded in file_path.stem for excluded in exclude_list)]
    return relative_filenames


def add_assets(soup, flower, background, coin, grave):
    """Changes the layers of the template svg file"""

    # insert flower
    soup.find('image', {"id": "flower"})['href'] = flower

    # insert background
    soup.find('image', {"id": "background"})['href'] = background

    # insert coin
    soup.find('image', {"id": "coin"})['href'] = coin

    # insert grave
    soup.find('image', {"id": "grave"})['href'] = grave


def add_petal_animation(soups: list):
    """Add petal animations to the provided soups. This ensures all petals animations are the same accross the different resolutions"""

    base_styles = '''
    .st0 {
        fill: #00FD00;
    }

    /* The animation code */
    @keyframes example {
        from {
            opacity: 0.7;
        }

        to {
            opacity: 0;
        }
    }

'''

    for i in range(20):
        base_styles += (f'\t#petal{i+1} {{\n'
                        f'\t\tanimation-timing-function: {choice(["linear", "ease", "ease-in","ease-out"])};\n'
                        f'\t\tanimation-delay: {uniform(0,2):.2f}s;\n'
                        f'\t\tanimation-duration: {uniform(0.5,4):.2f}s;\n'
                        f'\t\tanimation-name: example;\n'
                        f'\t\tanimation-iteration-count: infinite;\n'
                        f'\t\tanimation-direction: alternate;\n'
                        f'\t\topacity: 0.7;\n'
                        '\t}\n\n'
                        )
    for soup in soups:
        soup.style.string = base_styles

    return soups


def get_trait(s):
    first = "/"
    last = ".png"
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""