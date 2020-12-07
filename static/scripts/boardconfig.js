var board,
    game = new Chess('rnbqkbnr/ppppp2p/8/5pp1/4P2Q/8/PPPP1PPP/RNB1KBNR w KQkq - 1 3');

// Actions after any move
var onMoveEnd = function(oldPos, newPos) {
  // Alert if game is over
  if (game.game_over() === true) {
    alert('Game Over');
    console.log('Game Over');
    
    let request = new XMLHttpRequest();
    request.open("POST", "/submitgame/");
    request.setRequestHeader("Content-Type", "application/json");
    console.log(game.turn())
    if (game.turn() === 'b') {
      //console.log("Black check");
      if (game.in_checkmate()) { // Black (CPU) is in checkmate
        request.send(JSON.stringify({"status":"win"}));  // Player wins
      }
    } else if (game.turn() === 'w') {
      //console.log("White check");
      if (game.in_checkmate()) {  // White (player) is in checkmate
        request.send(JSON.stringify({"status":"lose"}));  // Player loses
      }
    } else {
      request.send(JSON.stringify({"status":"draw"}));
    }
    
  }

  // Log the current game position
  console.log(game.fen());
};

// Check before pick pieces that it is white and game is not over
var onDragStart = function(source, piece, position, orientation) {
  if (game.game_over() === true || piece.search(/^b/) !== -1) {
    return false;
  }
};

// Update the board position after the piece snap
// for castling, en passant, pawn promotion
var onSnapEnd = function() {
  board.position(game.fen());
};

// Configure board
var cfg = {
  draggable: true,
  position: 'rnbqkbnr/ppppp2p/8/5pp1/4P2Q/8/PPPP1PPP/RNB1KBNR w KQkq - 1 3',  //'start',
  // Handlers for user actions
  onMoveEnd: onMoveEnd,
  onDragStart: onDragStart,
  onDrop: onDrop,
  onSnapEnd: onSnapEnd
}
board = ChessBoard('board', cfg);