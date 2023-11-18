# Python Milioner

[![Download](https://img.shields.io/badge/Download-2ea44f?style=for-the-badge)](https://github.com/matijakljajic/milionerpy/releases/download/2023.01.23/Milioner20230123.exe) [![Developer](https://img.shields.io/badge/Developer-2ea44f?style=for-the-badge)](https://matijakljajic.github.io/) [![Views](https://img.shields.io/endpoint?style=for-the-badge&color=2ea44f&label=Views&url=https%3A%2F%2Fhits.dwyl.com%2Fmatijakljajic%2Fmilionerpy.json)](https://github.com/matijakljajic/milionerpy) [![Stars](https://img.shields.io/github/stars/matijakljajic/milionerpy?style=for-the-badge&color=2ea44f&label=Stars)](https://github.com/matijakljajic/milionerpy/stargazers)

  A rendition of the popular TV quiz "Želite li da postanete milioner?" (eng. [Who wants to be a millionaire?](https://en.wikipedia.org/wiki/Who_Wants_to_Be_a_Millionaire%3F)) for one of the uni courses called "Seminarski rad A". The game and the questions are in Serbian. All questions were imported from an earlier version of the game done around 2002/03.

*If you want to read the official paper behind this work, you can do so over this [link](https://raw.githubusercontent.com/matijakljajic/milionerpy/main/Skript%20jezici%20-%20Seminarski%20rad%20A.pdf). (It's in Serbian)*

## How to run

### Regular installation

- Download the executable over the download button at the top of this README
- Install the program (It's preferable if you leave the default installation location, you can uninstall over control panel later if you want)
- Run as administrator

> When updating, it is recommended to uninstall the old version before installing the new one. You can ignore this recommendation if you find it inconvenient.

### Over code

- If on Windows, execute run.bat to install needed libraries
- If on Linux/Mac, execute run.sh to install needed libraries
- Open main.py and run


## Screenshots

![Screenshots](screenshots/readme-gallery.png)

## Updating the question list manually

Questions that the game uses can be updated through "pitanja.xlsx". Following template in each row must be used and the first row mustn't be changed:

`YOUR QUESTION | THE RIGHT ANSWER | FIRST WRONG ANSWER | SECOND WRONG ANSWER | THIRD WRONG ANSWER`

## Question Contributors

A big thanks to all the people who helped build the question set. Contributor list is available in [CREDITS](CREDITS.txt).

## Copyright Notice

This work does not intend to infringe any copyrights. The copyright holder to any symbols related to the TV quiz is the team behind the official quiz.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
