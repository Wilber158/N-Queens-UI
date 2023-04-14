
const chessboard = document.getElementById("chessboard");
//create chessboard using table in html, and adding the table rows and columns
function createChessboard() {
    for (let i = 0; i < 8; i++) {
            const row = chessboard.insertRow();
        for (let j = 0; j < 8; j++) {
            const cell = row.insertCell();
            cell.className = (i + j) % 2 === 0 ? "blue" : "white";
        }
    }
}
//adds the queen icon to a certain (row, column)
function addQueen(row, col) {
    const chessPiece = "&#9819;"; //Black queen: &#9819;
    chessboard.rows[row].cells[col].innerHTML = chessPiece;
}


function clearChessboard() {
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            chessboard.rows[i].cells[j].innerHTML = "";
        }
    }
}
//async function is neccessary here because it must wait for the python code to finish executing before continuing    
async function simulatedAnnealing(){
    clearChessboard();
    var tempString = document.getElementById("temp").value;
    var temp = parseInt(tempString);
    const state = await eel.animated_annealing(temp)(); //must await till python is done
    const chessPiece = "&#9819;";
    for(i = 0; i < state.length; i++){
        chessboard.rows[state[i]].cells[i].innerHTML = chessPiece;
    }
}

//displays chessboard given a state
eel.expose(display_Board);//expose this javascript function to the python side
function display_Board(state){
    console.log("state:", state)
    clearChessboard();
    const chessPiece = "&#9819;";
    for(i = 0; i < state.length; i++){
        chessboard.rows[state[i]].cells[i].innerHTML = chessPiece;
    }
}
//
function simulation(){
    clearChessboard();

}

createChessboard();