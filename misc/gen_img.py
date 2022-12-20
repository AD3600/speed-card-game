template = '<img src="{{url_for(\'static\', filename=\'cards/{}_of_{}.png\')}}" style="display: none;" />'

for rank in ['ace', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']:
    for suit in ['hearts', 'spades', 'clubs', 'diamonds']:
        print(template.format(rank, suit))