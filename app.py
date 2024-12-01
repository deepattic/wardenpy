import csv
import os
import time
from datetime import datetime
from typing import Annotated

import questionary
import typer
from rich import print
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from rich.table import Table

from libwardenpy.db import get_connection
from libwardenpy.funtionality import (
    AuthenticatedData,
    Entry,
    UnAuthData,
    add_password,
    authenticate_user,
    delete_passwod,
    get_password,
    list_passwords,
    register_user,
)
from libwardenpy.passgen import generate_password

authenticated = False

data: UnAuthData = UnAuthData("", "")
auth_data: AuthenticatedData = AuthenticatedData("", b"")

app = typer.Typer()


@app.command()
def login(
    username: Annotated[
        str,
        typer.Option("--username", "-u"),
    ],
    password: Annotated[
        str,
        typer.Option("--password", "-p", prompt=True, hide_input=True),
    ],
):
    global authenticated, auth_data, data
    data.username = username
    data.master_password = password
    auth_data.username = username
    key = authenticate_user(get_connection(), data)
    if key is not None:
        auth_data.key = key
        authenticated = True
    main()


@app.command()
def create(
    username: str,
    password: Annotated[
        str,
        typer.Option(
            "--password", "-p", prompt=True, confirmation_prompt=True, hide_input=True
        ),
    ],
):
    global data
    data.username, data.master_password = username, password
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT COUNT(*) FROM users WHERE username = ?", (username,)
        )

        if cursor.fetchone()[0] == 0:
            if register_user(get_connection(), data):
                print(f"User {username} registered successfully!")
        else:
            print("Username exists")


@app.command()
def export(
    username: str,
    password: Annotated[
        str,
        typer.Option(
            "--password", "-p", prompt=True, confirmation_prompt=True, hide_input=True
        ),
    ],
):
    global authenticated, auth_data, data
    data.username = username
    data.master_password = password
    auth_data.username = username
    key = authenticate_user(get_connection(), data)
    if key is not None:
        auth_data.key = key
        authenticated = True
    passwords = list_passwords(get_connection(), auth_data)
    if passwords is not None:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Writing data to csv...", total=None)
            time.sleep(1.5)
            with open(
                f"data/export-{datetime.today().date()}.csv", "w", newline=""
            ) as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
                )
                for entry in passwords:
                    writer.writerow(entry)
        print("Done!")


def main() -> None:
    global authenticated
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

   PRESS X TO QUITE
        """
        print(banner)
        main_logic()


def main_logic():
    global auth_data
    while True:
        user_input = Prompt.ask("[bold green]> [/bold green]").upper()

        if user_input == ".CLEAR":
            os.system("clear")

        if user_input in ("?", ".HELP"):
            print(help_msg)

        if user_input in ("1", "A", ".ADD"):
            while True:
                site = input(".add website_url > ").strip()
                if not site:
                    print("[bold red]You Must Add a Website .^.[/bold red]")
                else:
                    break
            site_pass = input(".add password (leave this blank for random password) > ")
            if not site_pass:
                site_pass = generate_password()
            entry: Entry = Entry(site, site_pass)
            add_password(get_connection(), auth_data, entry)

        if user_input in ("2", "S", ".SEARCH"):
            site = input(".search > ")
            a = get_password(get_connection(), auth_data, site)
            print(a)

        if user_input in ("3", "L", ".LIST"):
            passwords = list_passwords(get_connection(), auth_data)
            if passwords is None:
                print(f"No passwords for user {auth_data.username}")
            else:
                table = Table(title="List of Passwords")
                table.add_column("Site/Url", style="blue")
                table.add_column("Password", style="red")
                for item in passwords:
                    table.add_row(item[0], item[1])
                console = Console()
                console.print(table)

        if user_input in ("D", "4", ".DEL"):
            while True:
                site = input(".search entry > ").strip()
                if not site:
                    print("[bold red]You Must Add a Website .^.[bold red]")
                else:
                    break
            list_of_entries = get_password(get_connection(), auth_data, site)

            if list_of_entries is None:
                print(f"no entries have {site}")
            if list_of_entries is not None:
                table = Table(title="List of Entries")
                table.add_column("id", style="bold blue")
                table.add_column("Site/Url", style="green")
                table.add_column("Password", style="red")
                for item in list_of_entries:
                    table.add_row(str(item[0]), item[1], item[2].decode("utf-8"))
                console = Console()
                console.print(table)
                choices = [str(id[0]) for id in list_of_entries]
                id = questionary.select(
                    "Which entry do you want to delet?",
                    choices=choices,
                    qmark="> ",
                    pointer=">",
                ).ask()
                delete_the_entry = Prompt.ask(
                    f"Are You sure You want to delete [bold red]{id}[/bold red] {'[y/N]'} ?",
                    default=False,
                )
                if delete_the_entry:
                    delete_passwod(get_connection(), auth_data, id)

        if user_input in ("X", ".EXIT"):
            break


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
    app()
