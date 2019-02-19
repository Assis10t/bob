var PF = require('pathfinding');
const db = require('./db')

module.exports.makeWarehouse = (width,height, shelves) => {
    // create grid
    var walkable_grid = [];
    for (var i = 0; i < height; i++) {
        var to_push = []
        for (var j =0; j <width; j++) {
            to_push.push(0);
        }
        walkable_grid.push(to_push);
    }
   
    

    // add shelves
    for (var s = 0; s < shelves.length; s++) {
        var shelf = shelves[s];
        // TODO: verify shelf
        var startx = shelf[0];
        var starty = shelf[1];
        var len = shelf[2];
        for (var i = startx; i < startx + len; i++) {
            walkable_grid[starty][i] = 1;
        }
    }
    console.log("grid: " + walkable_grid);
    return walkable_grid;
}

module.exports.pathfind_to_point = (current_pos,end_pos, warehouse_grid) => {
    var pf_grid = new PF.Grid(warehouse_grid);
    var finder = new PF.BiAStarFinder();
    var path = finder.findPath(current_pos[0],current_pos[1], end_pos[0], end_pos[1], pf_grid);
    path = PF.Util.compressPath(path);
    console.log(path);
}
module.exports.convert_order_to_job = (order,robot) => {
    console.log(order);
    console.log(robot);
    var robot_pos = robot["location"]
    var item_list = order["items"]
    var job = {}
    for (var i = 0; i < item_list; i++) {
        var current_item = item_list[i]["position"];
        var robot_xy = [robot_pos["x"],robot_pos["y"]]
        var item_xy = [current_item["x"],current_item["y"]]
        var path = pathfind_to_point(robot_pos_arr, item_position);
    }
    /*
    var items_to_collect = order["items"];
    var 
    for (var i =0; i < items_to_collect.length; i++) {
        var item_position = items_to_collect[i];
        
    }
    */
    return {}
}