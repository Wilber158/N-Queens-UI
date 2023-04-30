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

function createNChessboard(n) {
    const maxBoardSize = Math.min(window.innerWidth, window.innerHeight) * 0.8; // 80% of the smallest screen dimension
    const cellSize = Math.floor(maxBoardSize / n);
    // Remove the old chessboard
    removeChessboard();
    for (let i = 0; i < n; i++) {
        const row = chessboard.insertRow();
        for (let j = 0; j < n; j++) {
            const cell = row.insertCell();
            cell.className = `cell ${(i + j) % 2 === 0 ? "blue" : "white"}`;
            cell.style.width = `${cellSize}px`;
            cell.style.height = `${cellSize}px`;
        }
    }
}

function setQueenSize(cellSize) {
    // Set queen size based on cellSize
    const queenSize = Math.floor(cellSize * 0.8); // Adjust the scaling factor as needed
    const style = document.createElement('style');
    style.innerHTML = `
        .queen {
            font-size: ${queenSize}px;
        }
    `;
    document.head.appendChild(style);
}



//displays chessboard given a state
eel.expose(display_Board);//expose this javascript function to the python side
async function display_Board(state, time){
    console.log("state:", state)
    clearChessboard();
    const cellSize = chessboard.rows[0].cells[0].clientWidth;
    const fontSize = Math.floor(cellSize * 0.8); // 80% of the cell size
    const chessPiece = `&#9819;`;
    for (i = 0; i < state.length; i++){
        chessboard.rows[state[i]].cells[i].innerHTML = chessPiece;
        chessboard.rows[state[i]].cells[i].style.fontSize = `${fontSize}px`;
    }
    const num_queens_attacking = await eel.numQueensAttack(state)();
    document.getElementById("num_attacking").innerText = "Number of Queens attacking: " + num_queens_attacking
    document.getElementById("time").innerText = "Elapsed Time: " + time
    if(num_queens_attacking == 0){
        document.getElementById("is_successful").innerText = "Success!"
    }
    else{
        document.getElementById("is_successful").innerText = "Failure (hopefully we aren't presenting when this is shown)"
    }
    document.getElementsByClassName("info")[0].style.visibility = "visible";

}

//adds the queen icon to a certain (row, column)
function addQueen(row, col) {
    const chessPiece = "<span class='queen'>&#9819;</span>"; //Black queen: &#9819;
    chessboard.rows[row].cells[col].innerHTML = chessPiece;
}


function clearChessboard() {
    const rowCount = chessboard.rows.length;
    if (rowCount == 0) {
        return; //empty chessboard
    }
    const colCount = chessboard.rows[0].cells.length;
    for (let i = 0; i < rowCount; i++) {
        for (let j = 0; j < colCount; j++) {
            chessboard.rows[i].cells[j].innerHTML = "";
        }
    }
    document.getElementsByClassName("info")[0].style.visibility = "hidden";

}

function removeChessboard(){
    const rowCount = chessboard.rows.length;
    if(rowCount == 0){
        return;
    }
    for(let i = 0; i < rowCount; i++){
       chessboard.deleteRow(0);
    }
}

async function backtracking(){
    clearChessboard();
    removeChessboard();
    var tempString = document.getElementById("n").value;
    var n = parseInt(tempString);
    createNChessboard(n);
    const [state, time] = await eel.backtracking_search(n)(); //must await till python is done
    display_Board(state, time)
}

//
function simulation(){
    clearChessboard();

}