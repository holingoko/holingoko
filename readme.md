## About:
HoLingoko is a tool for language learners and translators. It allows users to 
create customizable dictionaries that can be used to look up characters, words,
or phrases while reading or translating text.

![Screenshot of application.](/website/screenshot.png)
## Download Application:
https://holingoko.github.io/holingoko/
## Build Application From Source:
Instructions below assume git and python (version >= 3.12) are installed.
### Windows:
```
git clone https://github.com/holingoko/holingoko.git
cd holingoko
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m nuitka HoLingoko.py --output-dir=build --enable-plugin=pyside6 --include-data-dir=resources=resources --standalone --show-scons --windows-console-mode=disable --windows-icon-from-ico=resources\images\icon.png
```
### Mac OS:
```
git clone https://github.com/holingoko/holingoko.git
cd holingoko
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
python3 -m nuitka HoLingoko.py --output-dir=build --enable-plugin=pyside6 --include-data-dir=resources=resources --standalone --show-scons --macos-create-app-bundle --macos-app-icon=resources/images/icon.png
```
## Translate Application Into New Language:
Language translation (.po) files are located under:

https://github.com/holingoko/holingoko/resources/languages

Pull requests to add new language translations to the above directory are welcome.

Users can also add translations for additional languages without having to 
modify the source code of the application by moving language translation files 
to the directory set via:

File > Settings... > Application > User-Added Languages Directory

Note that {} in translations indicates a word or phrase will be substituted in 
at runtime, and numbers within curly braces {0}, {1}, etc. indicate order of 
substitutions. Order will likely need to be reversed for right-to-left languages.
## Create New Theme For Application:
Theme (Qt style sheet, .qss) files are located under:

https://github.com/holingoko/holingoko/resources/themes

Pull requests to add new themes to the above directory are welcome.

Users can also add new themes without having to modify the source code of the 
application by moving theme files to the directory set via:

Settings... > Application > User-Added Themes Directory

Note that these are not normal Qt style sheets as they have been set up as 
python format strings to allow the user to change the font independent of the 
style. It is recommended to leave the font substitution lines unchanged.
Otherwise, font choices made by the user in settings will be overridden by the 
theme-specified font.
## Report An Issue:
Please report any issues with the application:

https://github.com/holingoko/holingoko/issues
## Donate:
<ul>
    <li><img src="website/logos/bitcoin.svg" alt="Bitcoin logo." style="height:25px;"> Bitcoin: bc1q3gaka4kjg9zjthzhcx7ktjw34udjkc4qehthzh</li>
    <li><img src="website/logos/dogecoin.svg" alt="Dogecoin logo." style="height:25px;"> Dogecoin: DGt7Srw1zta1kEVTG5uoF6g4ty973NfgbH</li>
    <li><img src="website/logos/ethereum.svg" alt="Ethereum logo." style="height:25px;"> Ethereum: 0x582eFc63B4FC7c608ca1D7C0dAf081E79b0501BF</li>
    <li><img src="website/logos/solana.svg" alt="Solana logo." style="width:25px;"> Solana: 6GxNAmS5fcX3Gi7zAMS2x5sFvWqU89JQX2uT6f2peTyx</li>
    <li><img src="website/logos/cardano.svg" alt="Cardano logo." style="height:25px;"> Cardano: addr1q8qgp2cjsj6x3xvl8gwlgvx8sqgw6qps3g7zgtv90ayr547s503c8mk83hq7j8637n3rzse8kry8ufr9tcq0ths95wwslhu4w0</li>
</ul>
