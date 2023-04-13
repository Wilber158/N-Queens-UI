
const chessboard = document.getElementById("chessboard");
function createChessboard() {
    for (let i = 0; i < 8; i++) {
        const row = chessboard.insertRow();
        for (let j = 0; j < 8; j++) {
            const cell = row.insertCell();
            cell.className = (i + j) % 2 === 0 ? "blue" : "white";
        }
    }
}

function addQueen(row, col) {
    const chessPiece = "&#9819;"; // White queen: &#9813; | Black queen: &#9819;
    chessboard.rows[row].cells[col].innerHTML = chessPiece;
}

function clearChessboard() {
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            chessboard.rows[i].cells[j].innerHTML = "";
        }
    }
}               

async function simulatedAnnealing(){
    var tempString = document.getElementById("temp").value;
    var temp = parseInt(tempString);
    const state = await eel.eight_queens(8, temp)();
    clearChessboard();
    const chessPiece = "&#9819;";
    for(i = 0; i < state.length; i++){
        chessboard.rows[state[i]].cells[i].innerHTML = chessPiece;
    }
}

function display_Board(state){
    console.log("state:", state)
    clearChessboard();
    const chessPiece = "&#9819;";
    for(i = 0; i < state.length; i++){
        chessboard.rows[state[i]].cells[i].innerHTML = chessPiece;
    }
}

async function simulation(){
    var tempString = document.getElementById("temp").value;
    var temp = parseInt(tempString);
    var success = 0;
    for(i = 0; i < 5; i++){
        const state = await eel.eight_queens(8, temp)();
        display_Board(state);
        if(await eel.isGoalState(state)()){
            success = success + 1;
        }

    }
    document.getElementById("sim_times").innerHTML = success;
}


createChessboard();