const canvas = document.getElementById("gameCanvas");

const ctx = canvas.getContext("2d");

const CELL_SIZE = canvas.width / 8;

var done = false;

var click = 0;

var row = [];
var col = [];

function draw_board(draw_checkers) {
  for (var i = 0; i < 8; i++) {
    for (var j = 0; j < 8; j++) {
      var even = i % 2 == 0 ? 0 : 1;

      if (j % 2 == even) ctx.fillStyle = "#e0d2bf";
      else ctx.fillStyle = "#613f2d";

      ctx.fillRect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE);

      ctx.strokeStyle = "White";
      ctx.lineWidth = 5;

      if (j != 3 && j != 4 && j % 2 != even && draw_checkers) {
        ctx.fillStyle = j > 4 ? "Black" : "White";
        ctx.beginPath();
        ctx.arc(
          i * CELL_SIZE + CELL_SIZE / 2,
          j * CELL_SIZE + CELL_SIZE / 2,
          CELL_SIZE / 2.5,
          0,
          Math.PI * 2
        );
        ctx.fill();
        ctx.closePath();
      }
    }
  }
}

draw_board(true);

document.getElementById("newGame").addEventListener(
  "click",
  (event) => {
    done = false;

    const Http = new XMLHttpRequest();
    var url = `../checkers`;
    Http.open("GET", url);
    Http.send();

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    draw_board();
  },
  false
);

canvas.addEventListener(
  "click",
  (event) => {
    if (done) return;

    var x = event.x - canvas.offsetLeft;
    var y = event.y - canvas.offsetTop;

    for (var i = 0; i < 8; i++)
      for (var j = 0; j < 8; j++) {
        if (
          CELL_SIZE * j <= x &&
          CELL_SIZE * j + CELL_SIZE >= x &&
          CELL_SIZE * i <= y &&
          CELL_SIZE * i + CELL_SIZE >= y
        ) {
          row.push(i);
          col.push(j);
        }
      }

    click++;

    if (click < 2) return;

    click = 0;

    const Http = new XMLHttpRequest();
    var url = `../checkers/board/set/${row[0]},${col[0]},${row[1]},${col[1]}`;
    Http.open("GET", url);
    Http.send();
    
    row = []
    col = []

    Http.onreadystatechange = (e) => {
      var res = JSON.parse(Http.responseText);

      if (res.success == false) return;

      board = res.board;

      draw_board(false);
      for (var i = 0; i < 8; i++)
        for (var j = 0; j < 8; j++) {
          if (board[i][j] != 0 && board[i][j] != -1) {
            if (board[i][j] == 1 || board[i][j] == 11)
              ctx.fillStyle = "Black";
            else if (board[i][j] == 2 || board[i][j] == 22)
              ctx.fillStyle = "White";

            ctx.beginPath();
            ctx.arc(
              j * CELL_SIZE + CELL_SIZE / 2,
              i * CELL_SIZE + CELL_SIZE / 2,
              CELL_SIZE / 2.5,
              0,
              Math.PI * 2
            );
            ctx.fill();
            
            if (board[i][j] == 11)
            {
              ctx.strokeStyle = "White";
              ctx.lineWidth = 5;
              ctx.stroke();
            }
            else if (board[i][j] == 22)
            {

              ctx.strokeStyle = "Black";
              ctx.lineWidth = 5;
              ctx.stroke();

            }
            
            ctx.closePath();
          }
        }

      if (res.state != undefined) {
        if (res.state != 0) {
          ctx.beginPath();
          ctx.moveTo(
            CELL_SIZE * res.col1 + CELL_SIZE / 2,
            CELL_SIZE * res.row1 + CELL_SIZE / 2
          );
          ctx.lineTo(
            CELL_SIZE * res.col2 + CELL_SIZE / 2,
            CELL_SIZE * res.row2 + CELL_SIZE / 2
          );
          ctx.strokeStyle = "Black";
          ctx.lineWidth = 5;
          ctx.stroke();
          ctx.closePath();
        }
        done = true;
      }
    };
  },
  false
);
