// Computer makes a move with algorithm choice and skill/depth level
var makeMove = function(algo, skill=3) {  // CPU's move
  // exit if the game is over
  if (game.game_over() === true) {
    console.log('game over');
    if (game.in_checkmate()) {  // CPU has been checkmated, player wins
      let request = new XMLHttpRequest();
      request.open("POST", "http://localhost:5000/submitgame/");
      request.send(JSON.stringify({"status":"win"}));
    }
  }
  // Calculate the best move, using chosen algorithm
  if (algo === 1) {
    var move = randomMove();
  } else if (algo === 2) {
    var move = calcBestMoveOne(game.turn());
  } else if (algo === 3) {
    var move = calcBestMoveNoAB(skill, game, game.turn())[1];
  } else {
    var move = calcBestMove(skill, game, game.turn())[1];
  }
  // Make the calculated move
  game.move(move);
  // Update board positions
  board.position(game.fen());
}

// Computer vs Computer
var playGame = function(algo=4, skillW=2, skillB=2) {
  if (game.game_over() === true) {
    console.log('game over');
    return;
  }
  var skill = game.turn() === 'w' ? skillW : skillB;
  makeMove(algo, skill);
  window.setTimeout(function() {
    playGame(algo, skillW, skillB);
  }, 250);
};

// Handles what to do after human makes move.
// Computer automatically makes next move
var onDrop = function(source, target) {
  // see if the move is legal
  var move = game.move({
    from: source,
    to: target,
    promotion: 'q' // NOTE: always promote to a queen for example simplicity
  });

  // If illegal move, snapback
  if (move === null) return 'snapback';

  // Log the move
  console.log(move)

  // make move for black
  window.setTimeout(function() {
    makeMove(4, 3);
  }, 250);
  
  // Check to see the game's status
  if (game.game_over()) {
    if (game.in_checkmate()) {  // Player in checkmate, player loses
      let request = new XMLHttpRequest();
      request.open("POST", "http://localhost:5000/submitgame/");
      request.send(JSON.stringify({"status":"loss"}));
    } else {  // Draw
      let request = new XMLHttpRequest();
      request.open("POST", "http://localhost:5000/submitgame/");
      request.send(JSON.stringify({"status":"draw"}));
    }
  }
};