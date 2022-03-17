# Instructions 🛠

## preparation 🍱

-   create folder in root of project called `assets`
-   add the folders `flowers`, `coins`, `backgrounds` and `graves` to the `assets` folder
-   fill them with the images you want to use
-   cd into `ethflower-generator`
-   run `poetry install`
-   adapt the `generator.py`, `oracle.py` and `utils.py` files to your needs
-   change `generator = 'ethflower_generator.generator:stop_mint'` to `generator = 'ethflower_generator.generator:assemble_svgs'`
-   run `poetry run generator`
-   profit? 💫

## uploading 💾

-   you cant upload the entire collection at once, split it in half and upload each half
