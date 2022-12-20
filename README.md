# Speed Card Game

## Setup
Optionally create a virtual environment

```bash
python -m venv venv && venv\Scripts\activate
```

Then install the required dependencies

```bash
pip install -r requirements.txt
```

Now move into the `/src` directory which contains the main `app.py` script

```
cd src
```

And now you can host the project locally (at <http://127.0.0.1:5000/> by default) by running

```bash
flask run
```
with `--debug` used for hot reloading.

## Game Instructions
Once you connect you will see empty cards until another user connects. From there on the game
rules are like that of Speed (see [here](https://gathertogethergames.com/speed)) with the 5 cards on the left belonging to you.
Click one of your cards (the most recently clicked card will be glowing red) and the corresponding middle card to play it. 
The card will only be played if it is a valid move. The first player to get rid of all of their cards wins.

# Demonstration Video
<https://youtu.be/hYiX-eXp22c>