from pathlib import Path
from bs4 import BeautifulSoup


def manipulate_template(soup):
    # insert flower
    # current_flower = soup.find('image', {"id": "flower"})['href']
    new_script = soup.new_tag("script")
    new_script.append("""
      fetch("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true")
      .then(response => response.json())
      .then( priceChange => {
         let usd24HourChange = priceChange.bitcoin.usd_24h_change.toFixed(2);
         updateAnimationDuration(usd24HourChange);
      })
      .catch(err => console.log(err))

      function calculateAnimationDuration(usd24HourChange, initialValue) {
         let g = initialValue*2;
         let k = 1/(50*initialValue);
         let newValue = g * (1 / (1 + Math.exp(k * g * usd24HourChange) * (g / initialValue - 1))).toFixed(3);
         return newValue === 0 ? 0.001 : newValue;
      }

      function updateAnimationDuration (usd24HourChange) {
         let styleSheets = document.styleSheets;
         for (let i = 2; i < 22; i++){
            let animationDuration = parseFloat(styleSheets[0].rules[i].style.animationDuration);
            let updatedDuration = calculateAnimationDuration(usd24HourChange, animationDuration);
            let updatedDurationString = updatedDuration.toString()+"s";
            styleSheets[0].rules[i].style.animationDuration = updatedDurationString;
         }
      }
      """)
    soup.svg.append(new_script)
    return soup


def main():
    for i in range(2009):

        template = Path(f"../assets/{i+1}.svg")

        with template.open() as svg_template:
            soup = BeautifulSoup(svg_template, 'xml')

        new_soup = manipulate_template(soup)

        with Path(f"../mint/assets/{i+1}_high.svg").open('w') as random_svg:
            random_svg.write(str(new_soup))



        template = Path(f"../assets/{i+1}_low.svg")

        with template.open() as svg_template:
            soup = BeautifulSoup(svg_template, 'xml')

        new_soup = manipulate_template(soup)

        with Path(f"../mint/assets/{i+1}.svg").open('w') as random_svg:
            random_svg.write(str(new_soup))



        template = Path(f"../assets/{i+1}_thumbnail.svg")

        with template.open() as svg_template:
            soup = BeautifulSoup(svg_template, 'xml')

        new_soup = manipulate_template(soup)

        with Path(f"../mint/assets/{i+1}_low.svg").open('w') as random_svg:
            random_svg.write(str(new_soup))

if __name__ == "__main__":
    main()
