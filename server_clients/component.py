import sqlite3


def select(data, opp):
    con = sqlite3.connect('../Hotel.db')
    cur = con.cursor()
    if opp == 'select':
        try:
            sel = con.execute(f'{data}').fetchall()
            return sel
        except sqlite3.Error as error:
            sel = f"An Error occurred : {error}"
            return sel
    else:
        try:
            cur.execute(f'{data}')
            con.commit()
            result = 'Operation done'
            return result
        except sqlite3.Error as error:
            result = f"An Error occurred : {error}"
            print(result)
            return result


def selectView(data):
    con = sqlite3.connect('../Hotel.db')
    try:
        sel = con.execute(f'{data}').fetchall()
        return sel
    except sqlite3.Error as error:
        result = f"An Error occurred : {error}"
        print(result)
        return result


def divView1(c1,c2):
    client1=0
    client2 =0
    for i in c1:
        client1 += i
    for i in c2:
        client2 += i

    if client1 > client2:
        return "<<view1 for client2(Room Service G2)>>\n<<view2 for client1(Room Service G1)>>"
    else:
        return "<<view1 for client1(Room Service G1)>>\n<<view2 for client2(Room Service G2)>>"


def divView2(c1, c2):
    client1 = len(c1)
    client2 = len(c2)
    if client1 > client2:
        return " view2 for client1(Room Service G1)\n view1 for client2(Room Service G2)"
    elif client1 < client2:
        return " view2 for client1(Room Service G1)\n view1 for client2(Room Service G2)"
    else:
        return " view1 for client1(Room Service G1)\n view2 for client2(Room Service G2)"
