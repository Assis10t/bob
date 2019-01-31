def generate_state(row,column,newline=True):
    if (newline):
        return "square_{}_{}\n".format(row,column)
    else:
        return "square_{}_{}".format(row,column)


def generate_link(row1,columm1,row2,column2):
    return "nextto {} {}".format(generate_state(row1,columm1,False), generate_state(row2,column2))

warehouse_floor = []

#pull in warehouse layout
with open("warehouse-layout.csv") as f:
    for line in f:
        warehouse_floor.append((list(map((lambda x: int(x)), line.split(",")))))

output = file("warehouse_world.txt", "w+")
# TODO: make this into one loop
# Assues rectangular layout
# define each square

print("Generating Warehouse States")
for row in range(0,len(warehouse_floor)):
    for column in range(0,len(warehouse_floor[row])):
        if (warehouse_floor[row][column]  > 0):
            output.write(generate_state(row,column))

for row in range(0,len(warehouse_floor)):
    for column in range(0,len(warehouse_floor[row])):
        if (warehouse_floor[row][column] > 0):
            if (row > 0):
                #check above
                if warehouse_floor[row-1][column] == 1:
                    output.write(generate_link(row,column,row-1,column))
            if (row < len(warehouse_floor)-1):
                #check below
                if warehouse_floor[row+1][column] == 1:
                    output.write(generate_link(row,column,row+1,column))
            if (column > 0):
                #check left
                if warehouse_floor[row][column-1] == 1:
                    output.write(generate_link(row,column,row,column-1))
            if (column < len(warehouse_floor[row]) - 1):
                #check left
                if warehouse_floor[row][column+1] == 1:
                    output.write(generate_link(row,column,row,column+1))



print("Done.")

output.close();
