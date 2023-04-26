function createNChessboard(n){
    for (let i = 0; i < n; i++) {
        const row = chessboard.insertRow();
    for (let j = 0; j < n; j++) {
        const cell = row.insertCell();
        cell.className = (i + j) % 2 === 0 ? "blue" : "white";
    }
}
}

createNChessboard();

