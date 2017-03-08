
from utils import *
from f_lists import get_users_l, get_lhas_user, create_l, add_lmember,delete_lmember



################################
## input: session(with username,conncetion)
##
## purpose: create a list_home, user can do following things: 1 print out all lists' name
##                                                            2 print out all list user is on and owner's name
##                                                            3 create a list
##                                                            4/5 add/delete a member's name
##                                                            6 back to main home
##                                                            7 quit
##
## return none
#################################

def manage_lists(session) :
    username = session.get_username()
    curs = session.get_curs()
    con  = session.get_conn()
    while True:
        chooses= ["Show your lists", "Show lists you are on", "Create a list","Add a member to a list","Delete a member from a list","Back to home","Log out"]
        display_selections(chooses, "Manage Lists")
        num_choose = validate_num(SELECT, session, size = len(chooses))
        if num_choose == 1:
            get_users_l(username,curs,con)
        elif num_choose == 2:
            get_lhas_user(username,curs)
        elif num_choose == 3:
            create_l(session, username,curs,con)
        elif num_choose == 4:
            add_lmember(session, username,curs,con)
        elif num_choose == 5:
            delete_lmember(session, username,curs,con)
        elif num_choose == 6:
            session.home()
        else:
            session.logout()
    return





        
