const canvas = document.getElementById("gameCanvas");

const ctx = canvas.getContext("2d");

const CELL_SIZE = canvas.width / 7;

canvas.height = CELL_SIZE * 6;

var done = false;

function draw_board() {
  ctx.lineWidth = 1;
  for (var i = 0; i < 7; i++) {
    ctx.beginPath();
    ctx.moveTo(CELL_SIZE * i, 0);
    ctx.lineTo(CELL_SIZE * i, canvas.height);
    ctx.stroke();
    ctx.closePath();
  }

  for (var j = 0; j < 6; j++) {
    ctx.beginPath();
    ctx.moveTo(0, CELL_SIZE * j);
    ctx.lineTo(canvas.width, CELL_SIZE * j);
    ctx.stroke();
    ctx.closePath();
  }
}

draw_board();

document.getElementById("newGame").addEventListener("click", (event) => {

  done = false;

  const Http = new XMLHttpRequest();
  var url = `../connectfour`;
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

    var col;

    for (var j = 0; j < 7; j++) {
      if (
        CELL_SIZE * j <= x &&
        CELL_SIZE * j + CELL_SIZE >= x
      ) {
        col = j;
      }
    }

    const Http = new XMLHttpRequest();
    var url = `../connectfour/board/set/${col}`;
    Http.open("GET", url);
    Http.send();

    Http.onreadystatechange = (e) => {
      var res = JSON.parse(Http.responseText);

      if (res.success == false) return;

      ctx.beginPath();
      ctx.fillStyle = "Red";
      ctx.lineWidth = 1;
      ctx.arc(
        CELL_SIZE * res.col + CELL_SIZE / 2,
        CELL_SIZE * res.row + CELL_SIZE / 2,
        CELL_SIZE / 3,
        0,
        Math.PI * 2
      );
      ctx.fill();
      ctx.stroke();
      ctx.closePath();

      ctx.beginPath();
      ctx.fillStyle = "Blue";
      ctx.arc(
        CELL_SIZE * col + CELL_SIZE / 2,
        CELL_SIZE * res.player_row + CELL_SIZE / 2,
        CELL_SIZE / 3,
        0,
        Math.PI * 2
      );
      ctx.fill();
      ctx.stroke();
      ctx.closePath();

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
