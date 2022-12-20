from game import Game
from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins='*')

# Global variables for tracking the game state
player_queue = []
all_games = dict()


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connects')
def connects():
    global playing, player_queue, all_games

    you_id = request.sid
    if not player_queue:
        player_queue.append(you_id)
        socketio.emit('waiting')
    else:
        opponent_id = player_queue[0]
        game_id = you_id + opponent_id

        all_games[game_id] = Game(you_id, opponent_id)

        you_hand = all_games[game_id].players[you_id].hand
        middle = all_games[game_id].middle
        opponent_hand = all_games[game_id].players[opponent_id].hand

        socketio.emit('player_joined', data=(game_id,
                      you_hand, middle, opponent_hand), room=you_id)
        socketio.emit('player_joined', data=(game_id,
                      opponent_hand, middle, you_hand), room=opponent_id)

        player_queue.pop()


@socketio.on('card_played')
def play_card(game_id, suite, rank, middle_suite, middle_rank):
    game = all_games[game_id]
    if not game.validate_card(request.sid, (suite, rank), (middle_suite, middle_rank)):
        socketio.emit('invalid_card', room=request.sid)
        print('Invalid card')
        return
    print('Valid card')
    res = game.update_game_state(request.sid, (suite, rank),
                                 (middle_suite, middle_rank))
    print('Game state updated.')
    status = game.game_status
    if status != 'playing':
        if status == 'win':
            socketio.emit('card_played', 'win', True, suite, rank,
                          middle_suite, middle_rank, None, None, room=request.sid)
            socketio.emit('card_played', 'lose', False, suite, rank,
                          middle_suite, middle_rank, None, None, room=res)
        if status == 'tie':
            socketio.emit('card_played', 'tie', True, suite, rank, middle_suite,
                          middle_rank, res[1][0], res[1][1], room=request.sid)
            socketio.emit('card_played', 'tie', False, suite, rank,
                          middle_suite, middle_rank, res[1][0], res[1][1], room=res[0])
    else:
        print('Starting to emit card_played')
        socketio.emit('card_played', data=('playing', True, suite, rank,
                                           middle_suite, middle_rank, res[1][0], res[1][1]), room=request.sid)
        socketio.emit('card_played', data=('playing', False, suite, rank,
                                           middle_suite, middle_rank, res[1][0], res[1][1]), room=res[0])
        print('emitted card_played !')


if __name__ == '__main__':
    socketio.run(app)
