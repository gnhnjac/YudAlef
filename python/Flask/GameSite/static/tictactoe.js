const canvas = document.getElementById("gameCanvas");

const ctx = canvas.getContext("2d");

const CELL_SIZE = canvas.width / 3;

var done = false;

function draw_board()
{


  ctx.beginPath();
  ctx.moveTo(CELL_SIZE, 0);
  ctx.lineTo(CELL_SIZE, canvas.height);
  ctx.stroke();
  ctx.moveTo(CELL_SIZE * 2, 0);
  ctx.lineTo(CELL_SIZE * 2, canvas.height);
  ctx.stroke();
  ctx.moveTo(0, CELL_SIZE);
  ctx.lineTo(canvas.width, CELL_SIZE);
  ctx.stroke();
  ctx.moveTo(0, CELL_SIZE * 2);
  ctx.lineTo(canvas.width, CELL_SIZE * 2);
  ctx.stroke();
  ctx.closePath();


}

draw_board();

document.getElementById("newGame").addEventListener("click", (event) => {

  done = false;

  const Http = new XMLHttpRequest();
  var url = `../tictactoe`;
  Http.open("GET", url);
  Http.send();

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  draw_board();

}, false);

canvas.addEventListener(
  "click",
  (event) => {
    if (done) return;

    var x = event.x - canvas.offsetLeft;

    var y = event.y - canvas.offsetTop;

    var row;
    var col;

    for (var i = 0; i < 3; i++) {
      for (var j = 0; j < 3; j++) {
        if (
          CELL_SIZE * i <= x &&
          CELL_SIZE * i + CELL_SIZE >= x &&
          CELL_SIZE * j <= y &&
          CELL_SIZE * j + CELL_SIZE >= y
        ) {
          row = i;
          col = j;
        }
      }
    }

    const Http = new XMLHttpRequest();
    var url = `../tictactoe/board/set/${row},${col}`;
    Http.open("GET", url);
    Http.send();

    Http.onreadystatechange = (e) => {
      var res = JSON.parse(Http.responseText);

      if (res.success == false) return;

      if (res.state != undefined) {
        ctx.beginPath();
        ctx.moveTo(
          CELL_SIZE * res.row1 + CELL_SIZE / 2,
          CELL_SIZE * res.col1 + CELL_SIZE / 2
        );
        ctx.lineTo(
          CELL_SIZE * res.row2 + CELL_SIZE / 2,
          CELL_SIZE * res.col2 + CELL_SIZE / 2
        );
        ctx.strokeStyle = "Red";
        ctx.lineWidth = 5;
        ctx.stroke();
        ctx.closePath();
        done = true;
      }

      ctx.beginPath();
      ctx.strokeStyle = "Black";
      ctx.lineWidth = 1;
      ctx.moveTo(
        CELL_SIZE * res.row + CELL_SIZE / 5,
        CELL_SIZE * res.col + CELL_SIZE / 5
      );
      ctx.lineTo(
        CELL_SIZE * res.row + (CELL_SIZE * 4) / 5,
        CELL_SIZE * res.col + (CELL_SIZE * 4) / 5
      );
      ctx.stroke();
      ctx.moveTo(
        CELL_SIZE * res.row + (CELL_SIZE * 4) / 5,
        CELL_SIZE * res.col + CELL_SIZE / 5
      );
      ctx.lineTo(
        CELL_SIZE * res.row + CELL_SIZE / 5,
        CELL_SIZE * res.col + (CELL_SIZE * 4) / 5
      );
      ctx.stroke();
      ctx.closePath();

      ctx.beginPath();
      ctx.arc(
        CELL_SIZE * row + CELL_SIZE / 2,
        CELL_SIZE * col + CELL_SIZE / 2,
        CELL_SIZE / 3,
        0,
        Math.PI * 2
      );
      ctx.stroke();
      ctx.closePath();
    };
  },
  false
);
