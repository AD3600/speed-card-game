var socket = io();
socket.emit("connects");

var game_id;

const game = document.getElementById("game");

const you = document.getElementById("you");
const you_cards = document.querySelectorAll("#you .card");
const opponent = document.getElementById("opponent");
const opponent_cards = document.querySelectorAll("#opponent .card");
const middlePiles = document.querySelectorAll("#middle-piles .card");

socket.on("player_joined", (game__id, you_hand, middle, opponent_hand) => {
  game_id = game__id;
  for (let i = 0; i < 5; i++) {
    you_cards[i].innerHTML = `<img class="card-img" src="static/cards/${
      you_hand[i][1] + "_of_" + you_hand[i][0]
    }.png" data-rank=${you_hand[i][1]} data-suite=${
      you_hand[i][0]
    } style="max-width:100%; max-height:100%;"/>`;
    opponent_cards[i].innerHTML = `<img class="card-img" src="static/cards/${
      opponent_hand[i][1] + "_of_" + opponent_hand[i][0]
    }.png" data-rank=${opponent_hand[i][1]} data-suite=${
      opponent_hand[i][0]
    } style="max-width:100%; max-height:100%;"/>`;
  }
  middlePiles[0].innerHTML = `<img class="card-img" src="static/cards/${
    middle[0][1] + "_of_" + middle[0][0]
  }.png" data-rank=${middle[0][1]} data-suite=${
    middle[0][0]
  } style="max-width:100%; max-height:100%;"/>`;
  middlePiles[1].innerHTML = `<img class="card-img" src="static/cards/${
    middle[1][1] + "_of_" + middle[1][0]
  }.png" data-rank=${middle[1][1]} data-suite=${
    middle[1][0]
  } style="max-width:100%; max-height:100%;"/>`;
});

socket.on(
  "card_played",
  // prettier-ignore
  (game_status, your_cards, suite, rank, middle_suite, middle_rank, replace_suite, replace_rank) => {
    let middleIndex = Array.from(middlePiles).filter((card) => {
      card = card.children[0];
      return (
        card.dataset.suite == middle_suite && card.dataset.rank == middle_rank
      );
    })[0];

    let middleChange = middleIndex.children[0];
    middleChange.dataset.suite = suite;
    middleChange.dataset.rank = rank;
    middleChange.src = `static/cards/${rank}_of_${suite}.png`;

    if (your_cards) {
      let cardIndex = Array.from(you_cards).filter((card) => {
        card = card.children[0];
        return card.dataset.suite == suite && card.dataset.rank == rank;
      })[0];


      let handChange = cardIndex.children[0];
      handChange.dataset.suite = replace_suite;
      handChange.dataset.rank = replace_rank;
      handChange.src = `static/cards/${replace_rank}_of_${replace_suite}.png`;

      console.log(cardIndex, handChange, replace_rank, replace_suite);

    } else {
      let cardIndex = Array.from(opponent_cards).filter((card) => {
        card = card.children[0];
        return card.dataset.suite == suite && card.dataset.rank == rank;
      })[0];

      let handChange = cardIndex.children[0];
      handChange.dataset.suite = replace_suite;
      handChange.dataset.rank = replace_rank;
      handChange.src = `static/cards/${replace_rank}_of_${replace_suite}.png`;
    }
  }
);

var selected_card;

you_cards.forEach((card) => {
  card.addEventListener("click", (event) => {
    if (event.currentTarget.id != selected_card) {
      if (selected_card) {
        document.getElementById(selected_card).style["box-shadow"] = null;
      }
      event.currentTarget.style["box-shadow"] =
        "0 0 31px 10px rgba(255, 33, 33, 1)";
      selected_card = event.currentTarget.id;
    }
  });
});

middlePiles.forEach((card) => {
  card.addEventListener("click", (event) => {
    if (selected_card) {
      let highlighted_card = document.getElementById(selected_card).children[0],
        middle_card = event.currentTarget.children[0];
      socket.emit(
        "card_played",
        game_id,
        highlighted_card.dataset.suite,
        highlighted_card.dataset.rank,
        middle_card.dataset.suite,
        middle_card.dataset.rank
      );
    }
  });
});

window.addEventListener("beforeunload", (event) => {
  socket.emit("left");
});
