# Bricklink CSV Part Solver
import csv

'''
Bricklink CSV format: ItemType, ItemId*, Color*, MaxPrice, MinQty*, Condition, Notify
Stud.io CSV export: BLItemNo, ElementId, LdrawId*, PartName, BLColorId*, LDrawColorId, ColorName, ColorCategory, Qty*, Weight
'''

def subtractParts(haveFile, wantFile):
    h = open(haveFile)
    w = open(wantFile)
    out = open("res.csv", mode = "w", newline = "")

    csv_have = csv.reader(h, delimiter = "\t")
    csv_want = csv.reader(w, delimiter = "\t")
    csv_res = csv.writer(out, delimiter = ",")

    nameIdx = 3
    colorIdx = 6
    qtyIdx = 8

    partIdIdx = 2
    colorIdIdx = 5


    res = [["Part", "Color", "Quantity"]]
    # Go through wanted items
    for row in csv_want:
        temp = row
        toAdd = True

        wantName = row[nameIdx]
        wantColor = row[colorIdx]
        wantQuantity = row[qtyIdx]

        for row2 in csv_have:
                haveName = row2[nameIdx]
                haveColor = row2[colorIdx]
                haveQuantity = row2[qtyIdx]
                
                if wantName == haveName and wantColor == haveColor: # If the parts are a match
                    if not wantQuantity.isnumeric(): # Header or empty
                        toAdd = False
                        break
                    elif int(wantQuantity) <= int(haveQuantity): # If wanted quantity is less or equal to have quantity
                        temp[qtyIdx] = 0
                    else:
                        needed = str(int(wantQuantity) - int(haveQuantity))
                        temp[qtyIdx] = needed
                    break # Found the part so we can exit here

        # Reset the file heading to keep reading the CSV
        h.seek(0)

        # Append to the array
        #res.append(temp)
        if toAdd:
            res.append([temp[partIdIdx], temp[colorIdIdx], temp[qtyIdx]])       

    for row in res:
        csv_res.writerow(row)

    return 

def main():
    subtractParts("StrikerOriginal.csv", "Reaper.csv")

if __name__ == "__main__":
    main()
