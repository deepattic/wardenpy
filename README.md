## First iteration 
thinking that only one user would use the tool

[] - Fix the autentication logic

[] - add migration logic to main inti logic
[] - fix todo and warning notations
[] - fix funtions return type to optimize the thing
[] - add colors for all the funtions

<!-- markdownlint-configure-file {
  "MD013": {
    "code_blocks": false,
    "tables": false
  },
  "MD033": false,
  "MD041": false
} -->

<div align="center">
<hr />

# WardenPy

[![crates.io][crates.io-badge]][crates.io]
[![Downloads][downloads-badge]][releases]
[![Built with Nix][builtwithnix-badge]][builtwithnix]

wardenpy is a **cli-password manager**, inspired by bitwarden and 1pass.

It uses the most modern and up-to-date hashing algorithms, such as argon 2, and encryption techniques, such as ChaCha20-Poly1305.

| [Getting started](#getting-started) •
[Installation](#installation) |

</div>

## Getting started

![Tutorial][tutorial]

Run With python :
```sh
wardenpy init [username]        # Set up a SQLite database and create a new user named {username}.
wardenpy -u [username]          # Login with your username
wardenpy -u [*] -p [password]   # Login with your username and password.

wardenpy ..               # cd one level up
z -                # cd into previous directory

```
**- [] write new implementations**
## Installation

wardenpy can be installed in these easy steps:

1. **Manual Installation**

   wardenpy runs on most major platforms.

   <details>
   <summary>Linux / WSL</summary>

   > Just clone the repo and install the requirements:
   >
   > ```sh
   > git clone --depth=1 https://www.github.com/deepattic/wardenpy
   > cd wardenpy
   > pip install -r requirements.txt
   > ```
   </details>

   <details>
   <summary>macOS</summary>

   > I just dont have an apple device if you have one plz consider putting a pull request :)

   </details>

   <details>
   <summary>Windows</summary>

   > And i also dont have a windows pc if you have one plz consider putting a pull request :/
   </details>



[tutorial]: contrib/tutorial.webp