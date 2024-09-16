import csv
import os


# 1. The second line of the csv should be in correct format which is taken as a referenceline by default
# 2. To change the refference line use refferenceline parameter in fixbyremoval() to set your preferred refference line
# Note:- chosen refferenceline should be free of errors to get optimal output
# 3. code check weather the number of element in the refferenceline is equal to all other lines -
# 4. and type of each element in each line corresponding  to the element in the refferenceline -
# if 3 or 4 fails then that line is skipped
# tested in linux(Ubuntu) only

def fixbyremoval(src=None, refferenceline=2):
    def typeidentification(item):
        try:
            return type(int(item))
        except:
            pass
        try:
            return type(float(item))
        except:
            pass
        try:
            return type(bool(item))
        except:
            pass
        return type(item)
    
    if src is None:
        src = input("enter your source file as name or in (path)\n")
    skippedlines = []
    typecheck = []
    with open(src, 'r') as r:
        f = csv.reader(r)
        csv2list = list(f)
        csvlenchecker = len(csv2list[refferenceline])
        for i in csv2list[refferenceline]:
            typecheck.append(typeidentification(i))
        new = ''
        if '/' in src[::-1]:
            for i in src[::-1]:
                if i == '/':
                    new = new[::-1]
                    break
                else:
                    new += i
            tempfile = f'{new[:-4]}_temp.csv'
        else:
            tempfile = f'{src[:-4]}_temp.csv'
        with open(tempfile, 'w') as w:
            write = csv.writer(w)
            line = 0
            for i in csv2list:
                line += 1
                if len(i) == csvlenchecker:
                    typeflag = True
                    inc = 0
                    for j in i:
                        temp = typeidentification(j)
                        if temp == typecheck[inc]:
                            inc += 1
                        else:
                            typeflag = False
                            skippedlines.append(f'{line}->format mismatch')
                            break
                    if typeflag:
                        write.writerow(i)
                else:
                    skippedlines.append(f'{line}->length mismatch')
    
    print(f"skipped lines are {skippedlines}")
    # headding line added
    with open(src, 'r') as r:
        newfile = f'{tempfile[:-8]}updated.csv'
        with open(newfile, 'w') as w:
            reader = csv.reader(r)
            writer = csv.writer(w)
            first_row = next(reader)
            writer.writerow(first_row)
    with open(tempfile, 'r') as r:
        with open(newfile, 'a') as a:
            reader = csv.reader(r)
            writer = csv.writer(a)
            writer.writerows(reader)
    
    print(f'new file is created on {os.getcwd()} by name {newfile}')
    if os.path.exists(tempfile):
        os.remove(tempfile)
    else:
        print(f'fail to delete temporary file - {tempfile}')

# fixbyremoval(refferenceline=3)