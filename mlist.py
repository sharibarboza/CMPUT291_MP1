
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

class ListManager:

    def __init__(self, session):
        self.session = session
        self.username = session.get_username()
        self.con = session.get_conn()
        self.curs = session.get_curs()

    def manage_lists(self):
        while True:
            chooses= [
                "Show your lists", 
                "Show lists you are on",
                "Create a list",
                "Add a member to a list",
                "Delete a member from a list",
                "Back to home","Log out"
            ]
            print_newline()
            display_selections(chooses, "Manage Lists")
            num_choose = validate_num(SELECT, self.session, menu_func=self.session.home, size=len(chooses))

            if num_choose == 1:
                get_users_l(self.username, self.curs, self.con)
            elif num_choose == 2:
                get_lhas_user(self.username, self.curs)
            elif num_choose == 3:
                create_l(self.session, self.username, self.curs, self.con, self.manage_lists)
            elif num_choose == 4:
                add_lmember(self.session, self.username, self.curs, self.con, self.manage_lists)
            elif num_choose == 5:
                delete_lmember(self.session, self.username, self.curs, self.con, self.manage_lists)
            elif num_choose == 6:
                self.session.home()
            else:
                self.session.logout()
        return





        
