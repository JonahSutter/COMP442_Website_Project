var PIECES = ["Blank", "W.Pawn", "B.Pawn", "W.Rook", "B.Rook", "W.Knight", "B.Knight", "W.Bishop", "B.Bishop", "W.Queen", "B.Queen", "W.King", "B.King"];
// In order: Pawn, Rook, Knight, Bishop, Queen, King
var BOARD = [
[4, 6, 8, 10, 12, 8, 6, 4],
[2, 2, 2, 2, 2, 2, 2, 2],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 1],
[3, 5, 7, 11, 9, 7, 5, 3]
];
var SELECTEDPIECE = 0;
var SELECTEDX = -1;
var SELECTEDY = -1;
var TURN = 1;  // odd = White, even = Black


window.addEventListener("DOMContentLoaded", function() {
    console.log("JS loaded");
    // Do something, Taipu
    let boardElement = document.getElementById("chessboard");
    let boardBody = boardElement.children[0];  // Get the tbody
    for (i=0; i<8; i++) {  // For each row
        let row = boardBody.children[i];
        for (j=0; j<8; j++) {  // For each cell
            let pieceId = BOARD[i][j];
            let pieceType = PIECES[pieceId];
            let cell = row.children[j];
            //console.log(cell);  // We should get 64 of these
            console.log(j + ", " + i);
            console.log(pieceId);
            console.log(pieceType);
            if (cell != undefined) {
                cell.textContent = pieceType;
                // Add event listeners to the cells so we can detect when they're clicked
                let x = j.valueOf();
                let y = i.valueOf();
                cell.addEventListener("click", function() {
                    registerClick(x, y);
                });
            }
        }
    }
    i=9;
    j=9;
    console.log("Setup complete")
});

function registerClick(x, y) {
    // Do something, Taipu
    console.log("Clicked (" + x + ", " + y + ")");
    // Get the piece at that spot
    let pieceType = BOARD[y][x];
    if (SELECTEDPIECE == 0) {  // If we haven't selected a piece
        if ((pieceType != 0) && ((pieceType % 2) == (TURN % 2))) {  // Check to see if the current player owns that piece (and isn't a blank space)
            SELECTEDPIECE = pieceType.valueOf();  // Store for later use
            SELECTEDX = x.valueOf();
            SELECTEDY = y.valueOf();
            console.log("Selected " + PIECES[SELECTEDPIECE]);
        }
    } else {  // We've already selected a piece
        let deltaX = x - SELECTEDX;
        let deltaY = y - SELECTEDY;
        if (validMove(x, y)) {  // Check that move.  Varies per piece
            console.log("Valid move")
            // Make that move if possible
            BOARD[SELECTEDY][SELECTEDX] = 0;
            BOARD[y][x] = SELECTEDPIECE;
            // Increment the turn counter
            TURN += 1;
            console.log("Move complete.  Turn = " + TURN);
        }
        SELECTEDPIECE = 0;  // No piece selected
        updateBoard();
    }
}

function updateBoard() {
    let boardElement = document.getElementById("chessboard");
    let boardBody = boardElement.children[0];  // Get the tbody
    for (i=0; i<8; i++) {  // For each row
        let row = boardBody.children[i];
        for (j=0; j<8; j++) {  // For each cell
            let pieceId = BOARD[i][j];
            let pieceType = PIECES[pieceId];
            let cell = row.children[j];
            
            if (cell != undefined) {
                cell.textContent = pieceType;
            }
        }
    }
    console.log("Board updated")
}

function validMove(x, y) {
    let deltaX = x - SELECTEDX;
    let deltaY = y - SELECTEDY;
    
    if (SELECTEDPIECE == 1) {  // W.Pawn
        if ((deltaX == 0) && (deltaY == -1)) {
            return true;
        }
    } else if (SELECTEDPIECE == 2) {  // B.Pawn
        if ((deltaX == 0) && (deltaY == 1)) {
            return true;
        }
        // Note: Add code for En Passant and the first double-move.
    } else if ((SELECTEDPIECE == 3) || (SELECTEDPIECE == 4)) {  // Rook
        if ((deltaY == 0) || (deltaX == 0)) {
            return true;
        }
    } else if ((SELECTEDPIECE == 5) || (SELECTEDPIECE == 6)) {  // Knight
        // Do something, Taipu
        if ((Math.abs(deltaX) == 2 && Math.abs(deltaY) == 1) || (Math.abs(deltaX == 1) && Math.abs(deltaY == 2))) {
            return true;
        }
    } else if ((SELECTEDPIECE == 7) || (SELECTEDPIECE == 8)) {  // Bishop
        if (Math.abs(deltaY) == Math.abs(deltaX)) {
            return true;
        }
    } else if ((SELECTEDPIECE == 9) || (SELECTEDPIECE == 10)) {  // Queen
        if ((Math.abs(deltaY) == Math.abs(deltaX)) || ((deltaY == 0) || (deltaX == 0))) {  // Rook and Bishop's checks mashed together
            return true;
        }
    } else if ((SELECTEDPIECE == 11) || (SELECTEDPIECE == 12)) {  // King
        if (Math.abs(deltaX + deltaY) == 1) {
            return true;
        }
    }
    return false;
}