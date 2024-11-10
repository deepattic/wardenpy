import os
import argparse
import newapp
from db import db

authenticated = None

def init_store(args) -> None:
    #WARNING: remove this if statement block
    db.execute('SELECT username FROM users;') 
    username = args.username
    if ((username,) not in db.fetchall()):
        print("create a strong and memorable password\nguide: https://anonymousplanet.org/guide.html#appendix-a2-guidelines-for-passwords-and-passphrases\n")
        password = password = input("Enter Master Password: ")
        newapp.register_user(username, password)
        args.username = None
        global authenticated
        authenticated = True
    else:
    #TODO: remove this when complete
        args.username = None
        print("Username exit")

def main() -> None:
    global authenticated
    args = parse_arguments()
    if ((args.password != None and args.username != None)):
        password = args.password
        newapp.authenticate_user(args.username, password)
    elif (args.username != None and args.password == None):
        password = input("Enter Master Password: ")

    authenticated = True

    if authenticated:
        banner = r"""
__        __            _            ______   __
\ \      / /_ _ _ __ __| | ___ _ __ |  _ \ \ / /
 \ \ /\ / / _` | '__/ _` |/ _ \ '_ \| |_) \ V / 
  \ V  V / (_| | | | (_| |  __/ | | |  __/ | |  
   \_/\_/ \__,_|_|  \__,_|\___|_| |_|_|    |_|  
                            -- created by supun
type .help for help and x or .exit to exit.

   1.) Add a Password       [A]
   2.) Search Site Password [S]
   3.) List Passwords       [L]
        """
        print(banner)
        while True:
            user_input = input('> ')
            if user_input.upper() == '.CLEAR':
                os.system('clear')
            if user_input == '?' or user_input.upper() == '.HELP':
                print(help_msg)
            if user_input == '1' or user_input.upper() == 'A' or user_input.upper() == '.ADD':
                site = input(".add website_url > ")
                site_pass = input(".add password (leave this blank for random password) > ")
                if not site_pass:
                    site_pass = newapp.generate_password()
                newapp.add_password(
                    args.username, args.password, site, site_pass
                )
            if user_input == '2' or user_input.upper() == 'S' or user_input.upper() == '.SEARCH':
                site = input(".search > ")
                newapp.get_password(args.username, args.password, site)

            if user_input == '3' or user_input.upper() == 'L' or user_input.upper() == '.LIST':
                newapp.list_passwords(
                    args.username, args.password
                )
            if user_input.upper() == 'X' or user_input.upper() == '.EXIT':
                break

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(
        title='Commands',
    )
    parser.add_argument("-u", "--username", help="use the username given here")
    parser.add_argument("-p", "--password", help="use the password given here")
    parser.add_argument("-a", "--add", help="add password")

    init_parser = subparser.add_parser("init",aliases="i", help="Inizialize password repo")
    init_parser.add_argument('username', help='username for initialize the password store')
    init_parser.set_defaults(func=init_store)
    subparser.add_parser("new", help="Inizialize new password repo").set_defaults(func=init_store)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    return args

help_msg ="""
.help, ?        Show this menu
.clear          Clear the screen
.add, A|a       Add a password to the vault
.search, S|s    Search a site/password in the vault
.list, L|l      List all passwords in the vault
.exit, X|x      Exit and lock the vault
"""


if __name__ == "__main__":
    main()
