# Design
The project was build using [Flask](https://flask.palletsprojects.com/en/2.2.x/) for the backend and basic HTML/JS/CSS (no frameworks) for the frontend. 

Player moves are communicated to the server using a [Socket library built on top of Flask](https://flask-socketio.readthedocs.io/en/latest/). This was chosen because Speed 
is a very fast-paced game, so minute differences in time can contribute to the outcome of a game, and thus a fast communication protocol was necessary. 
The backend manages the game state and determines if moves are valid or not, as well as connecting players together.

## Backend
`src/player.py` contains a class `Player` that contains all information about an active player (there current hand, remaining cards, etc.)

`src/game.py` contains a class `Game` that contains all information about an active game (including two `Player` objects)

`src/helpers.py` contains multiple auxillary methods for various card operations, such as `create_deck()`, `shuffle()`, and a generic `valid_card()` method.

## Frontend
Only a single `html` file is used throughout the duration of a game, `src\templates\index.html`.

`src/static/client.js` contains all of the necessary `Socket.emit()` and `Socket.on()` functions to receive/communicate with the backend.

`src/static/cards/` contains `.png` images for all `52` cards in a standard deck of playing cards which are all loaded immediately for minimum delay during actual gameplay.

`src/static/styles.css` contains the various styles used to add color and position the various elements on the webpage.

## Misc
`misc/gen_img.py` is a script to generate all the HTML `img` elements for the 52 cards, though I realize now I could have done this more
organically within `src/client.js` itself