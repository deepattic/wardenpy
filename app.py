import argparse
import os

from libwardenpy.colors import colored_string, print_colored
from libwardenpy.db import get_connection
from libwardenpy.funtionality import (
    add_password,
    authenticate_user,
    delete_passwod,
    get_password,
    list_passwords,
    register_user,
)
from libwardenpy.migrations import migrate_DB
from libwardenpy.passgen import generate_password

authenticated = False


def init_store(args) -> None:
    migrate_DB()
    USER_NAME_EXIST = False
    with get_connection() as conn:
        cursor = conn.execute("SELECT username FROM users;")
        username = args.username
        if (username,) in cursor.fetchall():
            USER_NAME_EXIST = True
    if not USER_NAME_EXIST:
        tips_text1 = (
            "create a strong and memorable password\n"
            "guide: https://anonymousplanet.org/guide.html#appendix-a2-guidelines-for-passwords-and-passphrases\n"
        )
        print_colored(tips_text1, "red")
        password = input("Create Strong and Memorable Master Password: ")
        register_user(username, password)
    else:
        print("Username exit")
        exit()


def main() -> None:
    global authenticated
    args = parse_arguments()
    if args.password is not None and args.username is not None:
        password = args.password
        if authenticate_user(args.username, password) is not None:
            authenticated = True
    elif args.username is not None and args.password is None:
        password = input("Enter Master Password: ")
        args.password = password
        if authenticate_user(args.username, password) is not None:
            authenticated = True

    if authenticated:
        banner = r"""
__        __            _            ______   __
\ \      / /_ _ _ __ __| | ___ _ __ |  _ \ \ / /
 \ \ /\ / / _` | '__/ _` |/ _ \ '_ \| |_) \ V /
  \ V  V / (_| | | | (_| |  __/ | | |  __/ | |
   \_/\_/ \__,_|_|  \__,_|\___|_| |_|_|    |_|
                            -- created by supun

type .help or ? for help and x or .exit to exit.

   1.) Add a  Entry        [A]
   2.) Search Entry        [S]
   3.) List   Entries      [L]
   4.) Delete Entry        [D]
   4.) Delete Entry        [D]
        """
        print(banner)
        main_logic(args)


def main_logic(args):
    while True:
        user_input = input("> ")
        if user_input.upper() == ".CLEAR":
            os.system("clear")
        if user_input == "?" or user_input.upper() == ".HELP":
            print(help_msg)
        if (
            user_input == "1"
            or user_input.upper() == "A"
            or user_input.upper() == ".ADD"
        ):
            while True:
                site = input(".add website_url > ").strip()
                if not site:
                    print(colored_string("You Must Add a Website .^.", "RED"))
                else:
                    break
            site_pass = input(".add password (leave this blank for random password) > ")
            if not site_pass:
                site_pass = generate_password()
            add_password(args.username, args.password, site, site_pass)
        if (
            user_input == "2"
            or user_input.upper() == "S"
            or user_input.upper() == ".SEARCH"
        ):
            site = input(".search > ")
            get_password(args.username, args.password, site)

        if (
            user_input == "3"
            or user_input.upper() == "L"
            or user_input.upper() == ".LIST"
        ):
            list_passwords(args.username, args.password)
        if user_input.upper() == "D" or user_input.upper() == ".DEL":
            while True:
                site = input(".search entry > ").strip()
                if not site:
                    print(colored_string("You Must Add a Website .^.", "RED"))
                else:
                    break
            get_password(args.username, args.password, site, 1)
            id = input("Give the id of the entry you want to delete > ")
            id = str(id).strip()
            delete_passwod(args.username, args.password, id)
        if user_input.upper() == "X" or user_input.upper() == ".EXIT":
            break


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(
        title="Commands",
    )
    parser.add_argument("-u", "--username", help="use the username given here")
    parser.add_argument("-p", "--password", help="use the password given here")
    parser.add_argument("-a", "--add", help="add password")

    init_parser = subparser.add_parser(
        "init", aliases="i", help="Inizialize password repo"
    )
    init_parser.add_argument(
        "username", help="username for initialize the password store"
    )
    init_parser.set_defaults(func=init_store)
    subparser.add_parser("new", help="Inizialize new password repo").set_defaults(
        func=init_store
    )

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    return args


help_msg = """
.help, ?        Show this menu
.clear          Clear the screen
.add, A|a       Add a entry to the vault
.search, S|s    Search a entry in the vault
.list, L|l      List all the entries in the vault
.del, D|d       Delete a entry in the vault
.exit, X|x      Exit and lock the vault
"""


if __name__ == "__main__":
    main()
