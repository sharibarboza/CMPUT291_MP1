from utils import *
from queries import *
##here are functions in lists' home

def answer_check(prompt):
    while True:
        answer = input(prompt)
        if answer.lower() in ['y','yes']:
            return 1
        elif answer.lower() in ['n','no']:
            return 0;
        else:
            answer = input(prompt)

def member_exists(curs, lname, member):

    curs.execute("select * from includes where lname like '%%' || :1 || '%%' "
                 "and member=:2", [lname, member])
    return curs.fetchone() is not None

def has_list(curs, owner):
    
    curs.execute("select * from lists where owner like '%%' || :1 || '%%'", [owner])
    return curs.fetchone() is not None

def get_members(curs, username, lname):
    curs.execute("select member from includes, lists where lists.lname =includes.lname and "
        "lists.owner =:1 and lists.lname like '%%' || :1 ||'%%'", [username,lname])
        

#############################################
#  input user name
#  output user's list
#############################################
def get_users_l(username, curs, con):
    width = BORDER_LEN
    has_lists = False

    if has_list(curs, username):
        has_lists = True
        print_border(length=width, thick=False)
        curs.execute("select lname from lists where owner=:1",[username])
        rows = curs.fetchall()
        print_string("YOUR LISTS:", length=width)
        print_border(length=width, thick=False, sign='|')
        for row in rows:
            print_string(row[0], length=width)
        print_border(length=width, thick=False)
    else:
        print("You do not have any lists.")

    return has_lists



#############################################
#  input user name
#  output lists contains user
#############################################
def get_lhas_user(session, username, curs):
    curs.execute("select lists.owner, users.name, lists.lname from lists,includes,users where  users.usr = lists.owner and lists.lname=includes.lname and includes.member =:1",[username])
    rows = curs.fetchall()

    if len(rows) == 0:
        print("You are not on any lists.")
        return

    cols = curs.description
    owner_header = cols[0][0]
    name_header = cols[1][0]
    lname_header = "LIST NAME"
    headers = "%-5s | %-20s | %-12s" % (owner_header, name_header, lname_header)
    BORD_LEN = 45

    print_border(BORD_LEN, False)
    print_string(headers, length=BORD_LEN)
    print_border(BORD_LEN, False, sign='|')

    for i, row in enumerate(rows):
        owner = row[0]
        name = row[1]
        lname = row[2]
        row_str = "%-5s | %-20s | %-12s" % (owner, name, lname)
        print_string(row_str, length=BORD_LEN)
        if i == len(rows) - 1:
            print_border(BORD_LEN, False)
        else: 
            print_border(BORD_LEN, False, sign='|')

    press_enter(session)
    return

#############################################
#  input user name
#  output
#############################################
def create_l(session, username, curs, con, manage_lists) :
    prompt = "Enter your list name (less than 12 char): "
    lname = validate_str(prompt,session, menu_func=manage_lists, length=12)
    while ( list_exists(curs,lname,username)):
        prompt = "That list exists, please enter other name: "
        lname = validate_str(prompt, session, menu_func=manage_lists, length=12)
    prompt = "You want to create list name as "+lname+"? y/n: "
    if answer_check(prompt) :
    ##create table
        curs.execute('insert into lists values(:1,:2)',[lname,username])
        con.commit()
        print("List %s created." % (lname))
        press_enter(session)
    return


def add_lmember(session, username, curs, con, manage_lists):
    if not get_users_l(username,curs,con):
        return
    prompt = "Enter the list name: "
    lname = validate_str(prompt, session, menu_func=manage_lists, length=12)
    if ( not list_exists(curs,lname,username)):
        print ("That list does not exist!")
        press_enter(session)
        add_lmember(session, username, curs, con, manage_lists)
    else:
        prompt = "Enter the member you want to add: "
        member = validate_num(prompt, session, menu_func=manage_lists)
        if (member_exists(curs,lname,member) or not user_exists(curs,member)):
            print("The user already exists in this list or the user does not exist!")
            press_enter(session)
        else:
            prompt = "You want to add member "+str(member)+"? y/n: "
            if answer_check(prompt) :
                curs.execute('insert into includes values(:1,:2)',[lname,member])
                con.commit()
                print("Added %s to list %s." % (member, lname))
                press_enter(session)
    return


def delete_lmember(session, username, curs, con, manage_lists):
    if not get_users_l(username,curs,con):
        return
    prompt = "Enter the list name: "
    lname = validate_str(prompt, session, menu_func=manage_lists, length=12)
    if ( not list_exists(curs,lname,username)):
        print ("That list does not exist!")
        press_enter(session)
        delete_lmember(session, username, curs, con, manage_lists)
    else:
        get_members(curs, username, lname)
        rows = curs.fetchall()   

        if len(rows) == 0:
            print("No members to delete.")
            return 

        list_members(curs, lname, rows)
        prompt = "Enter the member you want to delete: "
        member = validate_num(prompt, session, menu_func=manage_lists)
        if (not member_exists(curs,lname,member) or not user_exists(curs,member)):
            print("The user does not exist in this list or the user does not exist! ")
            press_enter(session)
        else:
            prompt = "You want to delete member "+str(member)+"? y/n: "
            if answer_check(prompt) :
                curs.execute("delete from includes where lname like '%%' || :1 ||'%%' and member=:2",[lname,member])
                con.commit()
                print("%s deleted from %s." % (member, lname))
                press_enter(session)
    return

def list_members(curs, lname, rows):
    print_border(thick=False)
    columns = "%-5s | %-20s" % ("USER", "NAME")
    print_string(columns)
    print_border(thick=False)

    for row in rows:
        user = row[0]
        name = get_name(curs, user)

        row_str = "%-5s | %-20s" % (user, name)
        print_string(row_str)
    print_border(thick=False)
