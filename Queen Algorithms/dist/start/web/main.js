const chessboard = document.getElementById("chessboard");

document.getElementById("back_button").addEventListener("click", function(){
    window.location.href = "index.html"
})
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

function createNChessboard(n){
    for (let i = 0; i < n; i++) {
            const row = chessboard.insertRow();
        for (let j = 0; j < n; j++) {
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

    document.getElementsByClassName("results")[0].style.visibility = "hidden";

}
//async function is neccessary here because it must wait for the python code to finish executing before continuing    
async function simulatedAnnealing(){
     // Get the current state of the board
    clearChessboard()
    user_state = setInitialState()
    var tempString = document.getElementById("temp").value;
    var temp = parseInt(tempString);
    let statePromise;
    if(user_state == false){
        statePromise = await eel.animated_annealing(temp)(); //must await till python is done
    }
    else{
        statePromise = await eel.animated_annealing(temp, user_state)();
    }
    const state = await statePromise
    const chessPiece = "&#9819;";
    for(i = 0; i < state.length; i++){
        chessboard.rows[state[i]].cells[i].innerHTML = chessPiece;
    }
    const num_queens_attacking = await eel.numQueensAttack(state)();
    if(num_queens_attacking == 0){
        document.getElementById("is_successful").innerText = "Successful!";
    }
    else{
        document.getElementById("is_successful").innerText = "Fail -_-";
    }
    document.getElementById("num_attacking").innerText = "Number of Queens attacking: " + num_queens_attacking;
    document.getElementsByClassName("results")[0].style.visibility = "visible";
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

function setInitialState() {
    const initialStateString = document.getElementById("initial_state").value;
    if(initialStateString == ""){
        console.log("empty initial")
        return false
    }
    const initialState = initialStateString.split(",").map(Number);
    if (initialState.length === 8 && initialState.every(n => n >= 0 && n <= 7)) {
        clearChessboard();
        for (let i = 0; i < initialState.length; i++) {
            addQueen(initialState[i], i);
        }
        return initialState
    } else {
        alert("Invalid initial state. Please enter a comma-separated list of 8 integers between 0 and 7.");
    }
    return false
}

createChessboard();