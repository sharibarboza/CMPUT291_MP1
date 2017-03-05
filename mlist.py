
from utils import validate_num
from constants import BORDER,SELECT
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

def manage_lists(sesssion) :
    while True:
        print(BORDER)
        chooses= ["show your lists", "show lists you are on", "create a list","add a member in a list","delete a member in a list","back to home","log out"]
        num_choose = validate_num(SELECT,len(chooses))
    	if num_choose ==1:
    		get_users_l(sesssion)
    	else if num_choose==2: 
    		get_lhas_user(sesssion)
    	else if num_choose ==3:
    		create_l(sesssion)
    	else if num_choose ==4:
    		add_lmember(sesssion)
    	else if num_choose ==5:
    		delete_lmember(sesssion)
    	else if num_choose ==6:
    		sesssion.home()
    	else
    		sesssion.logout()





        
