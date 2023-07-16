# System libraries
import os
from time import sleep
import sys 

# External dependencies
from colorama import Fore, Back, Style

# The screen clear function
def screen_clear():
    # for mac and linux(here, os.name is 'posix')
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        # for windows platfrom
        _ = os.system('cls')


def menu(ts):
    screen_clear()

    if len(ts.clients) < 1:
        print("No clients connected.")
        exit()

    options = {
        "1": ts.show_active_client,
        "2": ts.change_active_client,
        "3": ts.add_client,
        "4": ts.update_profile_picture,
        "5": ts.get_all_groups,
        "6": ts.save_groups,
        "7": ts.show_groups,
        "8": ts.show_group_info,
        "9": ts.clone_group,
        "10": ts.all_clients_join_group,
        "11": ts.all_clients_to_admin_group,
        "12": ts.get_members_from_group,
        "13": ts.show_members,
        "14": ts.import_members_to_group,
        "15": ts.spam_members,
        "16": ts.redirect_msg,
        "17": ts.start_listening_events,
    }
 
    print(Fore.LIGHTBLACK_EX + "\n-------------------------------------------------------------")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.WHITE + "                          CLIENTS                          " + Fore.LIGHTBLACK_EX + "|")
    print(Fore.LIGHTBLACK_EX + "-------------------------------------------------------------")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 1-" + Fore.YELLOW + "  Show active client " + Fore.LIGHTBLACK_EX + "                                   |")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 2-" + Fore.YELLOW + "  Change active client " + Fore.LIGHTBLACK_EX + "                                 |")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 3-" + Fore.YELLOW + "  Add new client " + Fore.LIGHTBLACK_EX + "                                       |")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 4-" + Fore.YELLOW + "  Update profile picture " + Fore.LIGHTBLACK_EX + " (person who doesn't exist)    |")
    print(Fore.LIGHTBLACK_EX + "-------------------------------------------------------------")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.WHITE + "                           GROUPS                          " + Fore.LIGHTBLACK_EX + "|")
    print(Fore.LIGHTBLACK_EX + "-------------------------------------------------------------")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 5-" + Fore.YELLOW + "  Get all your active client Groups                     " + Fore.LIGHTBLACK_EX + "|")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 6-" + Fore.YELLOW + "  Save groups at groups_list.csv                        " + Fore.LIGHTBLACK_EX + "|")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 7-" + Fore.YELLOW + "  Show all groups loaded                                " + Fore.LIGHTBLACK_EX + "|")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 8-" + Fore.YELLOW + "  Show detailed information of a Group                  " + Fore.LIGHTBLACK_EX + "|")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 9-" + Fore.YELLOW + "  Clone Group " + Fore.LIGHTBLACK_EX + " (To a new group or an existing one)      |")
    print(Fore.LIGHTBLACK_EX + "-------------------------------------------------------------")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.WHITE + "                           ACTIONS                         " + Fore.LIGHTBLACK_EX + "|")
    print(Fore.LIGHTBLACK_EX + "-------------------------------------------------------------")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 10-" + Fore.YELLOW + " ALL clients join to a group                           " + Fore.LIGHTBLACK_EX + "|")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 11-" + Fore.YELLOW + " Invite ALL clients to a group and make them Admins    " + Fore.LIGHTBLACK_EX + "|")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 12-" + Fore.YELLOW + " Extract ALL members from a group                      " + Fore.LIGHTBLACK_EX + "|")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 13-" + Fore.YELLOW + " Show all extracted members                            " + Fore.LIGHTBLACK_EX + "|")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 14-" + Fore.YELLOW + " Import all extracted members to a group               " + Fore.LIGHTBLACK_EX + "|")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 15-" + Fore.YELLOW + " Send a random private message to all members (SPAM)   " + Fore.LIGHTBLACK_EX + "|")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 16-" + Fore.YELLOW + " Manage FORWARDING groups messages (sub-menu)          " + Fore.LIGHTBLACK_EX + "|")
    print(Fore.LIGHTBLACK_EX + "-------------------------------------------------------------")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.WHITE + "                           EVENTS                          " + Fore.LIGHTBLACK_EX + "|")
    print(Fore.LIGHTBLACK_EX + "-------------------------------------------------------------")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 17-" + Fore.YELLOW + " START EVENT LISTENING MODE                            " + Fore.LIGHTBLACK_EX + "|")
    print(Fore.LIGHTBLACK_EX + "-------------------------------------------------------------")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.WHITE + "                            EXIT                           " + Fore.LIGHTBLACK_EX + "|")
    print(Fore.LIGHTBLACK_EX + "-------------------------------------------------------------")
    print(Fore.LIGHTBLACK_EX + "|" + Fore.GREEN + " 18-" + Fore.YELLOW + " EXIT                                                  " + Fore.LIGHTBLACK_EX + "|")
    print(Fore.LIGHTBLACK_EX + "-------------------------------------------------------------" + Style.RESET_ALL)
    opt = input("Select option: " + Fore.MAGENTA)

    if opt=="18":
        ts.finish()
        screen_clear()
        print( Fore.BLUE + "¡SEE YOU SOON!" + Style.RESET_ALL)
        sys.exit()

    print(Style.RESET_ALL)
    
    try:
        options[ opt ]()
    except Exception as e:
        print(Fore.RED + "\nThe selected option is not available." + Style.RESET_ALL)

    sleep(1)
    menu(ts)


