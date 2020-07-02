let grid = [];
const maxNumber = Math.pow(10,1000);
function create(game) {
    var temp = [];
    for (var row = 0; row < 24; row++){
        var colVal = [];
        for(var col = 0; col < 24; col++){
            dot = {
                x: col,
                y: row,
                color: getRandomColor(),
                selected: false,
            }
            colVal.push(dot);
        }
        temp.push(colVal);
    }
grid = temp;
}

function getRandomColor(){
    var rand = Math.floor(Math.random() * (Object.keys(Color).length - 4)) + 2;
    var randColorValue = Color[Object.keys(Color)[rand]];
    return randColorValue;
}
// Games last 45 seconds
let timeRemaining = 45;

let interval = setInterval(decreaseTimer, 1000);

let score = 0;
let longestDrome = 0;
let uniqueDrome = 0;

function decreaseTimer() {
  timeRemaining--;
  if (timeRemaining == 0) {
    clearInterval(interval);
  }
}
function update(game) {
    for(row of grid){
        for(dot of row){
            if(!dot.selected){
                game.setDot(dot.x, dot.y, dot.color);
            }else{
                game.setDot(dot.x, dot.y, Color.Gray);
            }
        }
    }
    game.setText(`Score: ${score} -- Longest Pal: ${longestDrome} -- Unique Pal: ${uniqueDrome}`);
    //if (timeRemaining <= 0) {
       //game.setText(`Game over! Final score: ${score}`);
       //game.end();
    //}
}

function isSafe(row, col){
    if(row >= 0 && row < 24 && col >= 0 && col < 24){
        return grid[row][col].selected;
    }else{
        return false;
    }
}

function containsValue(edge, explored){
    for (let item of explored) {
        if (item.row === edge.row && item.col == edge.col){
            return true;
        }
    }
    return false;
}
function DFS(row, col) {
   // Create a Stack and add our initial node in it
   let s = [];
   s.push({"row": row, "col": col});
   let explored = new Set();

   // Mark the first node as explored
   explored.add({"row": row, "col": col});
   let tempIsland = [];

   while (s.length !== 0) {
      let t = s.pop();
       tempIsland.push(t);


       let edges = [{"row": t.row, "col": t.col+1},{"row":t.row, "col": t.col - 1},{"row":t.row + 1, "col": t.col},{"row": t.row - 1, "col": t.col}];
        for(edge of edges){
            if(!containsValue(edge, explored)){
                if(isSafe(edge.row,edge.col)){
                    explored.add(edge);
                    s.push(edge);
                }
            }
        }
   }

    return {first: explored, second: tempIsland};
}

function getIslands(){
    let islands = [];
    let exploredOuter = new Set();
    let tempIsland = [];
    let exploredTemp;
    for(var row = 0; row < 24; row++){
        for(var col = 0; col < 24; col++){
            if(isSafe(row, col) && !containsValue({"row":row, "col":col}, exploredOuter)){
                var values = DFS(row, col);
                exploredTemp = values.first;
                tempIsland = values.second;
                for(node of exploredTemp){
                    exploredOuter.add(node);
                }
                islands.push(tempIsland);
            }
        }
    }

    return islands;
}

function isPalindrome(dots) {
    var colors = [];
    for(var i = 0; i < dots.length; i++){
        row = dots[i].row;
        col = dots[i].col;

        colors.push(grid[row][col].color);
    }
    if(colors.join('') === colors.reverse().join('')){
        return true;
    }else{
        return false;
    }
}

function getPalindromes(islands){
    var palindromes = [];
    for (island of islands){
        if(isPalindrome(island)){
            palindromes.push(island);
        }else{
            for(dot of island){
                grid[dot.row][dot.col].selected = false;
            }
        }
    }
    return palindromes;
}


function hasGrey(){
    for(var row = 0; row < 24; row++){
        for(var col = 0; col < 24; col++){
            if(grid[row][col].selected){
                return true;
            }
        }
    }
    return false;
}

function fillGrey(direction){
    while(hasGrey()){
        if (direction === Direction.Up){
            // start at row 23
            // traverse rows backwards
            for(var row = 23; row >= 0; row--){
                for(var col = 0; col < 24; col++){
                    if(grid[row][col].selected){
                        // edge case
                        if(row === 23){
                            grid[row][col].selected = false;
                            grid[row][col].color = getRandomColor();
                        }else{
                            grid[row][col].selected = false;
                            grid[row][col].color = grid[row+1][col].color;
                            grid[row+1][col].selected = true;
                        }
                    }
                }
            }
        } else if (direction === Direction.Down){
            // start at row 0
            // traverse rows forwards
            for(var row = 0; row < 24; row++){
                for(var col = 0; col < 24; col++){
                    if(grid[row][col].selected){
                        if(row === 0){
                            grid[row][col].selected = false;
                            grid[row][col].color = getRandomColor();
                        }else{
                            grid[row][col].selected = false;
                            grid[row][col].color = grid[row-1][col].color;
                            grid[row-1][col].selected = true;
                        }
                    }
                }
            }
        } else if (direction === Direction.Left){
            // start at col 23
            // traverse cols backwards
            for(var col = 23; col >= 0; col--){
                for(var row = 0; row < 24; row++){
                    if(grid[row][col].selected){
                        if(col === 23){
                            grid[row][col].selected = false;
                            grid[row][col].color = getRandomColor();
                        }else{
                            grid[row][col].selected = false;
                            grid[row][col].color = grid[row][col+1].color;
                            grid[row][col+1].selected = true;
                        }
                    }
                }
            }
        } else if (direction === Direction.Right){
            // start at col 0
            // travers cols forward
            for(var col = 0; col < 24; col++){
                for(var row = 0; row < 24; row++){
                    if(grid[row][col].selected){
                        if(col === 0){
                            grid[row][col].selected = false;
                            grid[row][col].color = getRandomColor();
                        }else{
                            grid[row][col].selected = false;
                            grid[row][col].color = grid[row][col-1].color;
                            grid[row][col-1].selected = true;
                        }
                    }
                }
            }
        }
    }
    // void
}

function updateScore(palindrome){
    score += 1;
    score += palindrome.length;
    if(palindrome.length > longestDrome){
        longestDrome = palindrome.length;
    }
    var uniqueColors = 0;
    var seenColors = new Set();
    for(dot of palindrome){
        seenColors.add(grid[dot.row][dot.col].color);
    }
    console.log(seenColors);
    if(seenColors.size > uniqueDrome){
        uniqueDrome = seenColors.size;
    }
}
function onKeyPress(direction) {
    var islands = getIslands();
    var palindromes = getPalindromes(islands);
    var startRow;

    for(palindrome of palindromes){
        updateScore(palindrome);
    }

    fillGrey(direction);
    // delete selected dots
    // create new random dots in same "column" based on direction
}

function onDotClicked (x, y) {
    grid[y][x].selected = !grid[y][x].selected;
}

let config = {
  create: create,
  update: update,
  onKeyPress: onKeyPress,
  onDotClicked: onDotClicked,
};

let game = new Game(config);
game.run();
