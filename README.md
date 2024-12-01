<div align="center">
<hr />

# WardenPy

[![codecov](https://codecov.io/github/deepattic/wardenpy/graph/badge.svg?token=U6U8SOJUNW)](https://codecov.io/github/deepattic/wardenpy)
[![License](https://img.shields.io/github/license/deepattic/wardenpy)](https://github.com/deepattic/wardenpy/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/deepattic/wardenpy)](https://github.com/deepattic/wardenpy/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/deepattic/wardenpy)](https://github.com/deepattic/wardenpy/issues)
[![GitHub release](https://img.shields.io/github/v/release/deepattic/wardenpy)](https://github.com/deepattic/wardenpy/releases)

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

wardenpy export                 # Export all the entries of a user 

```
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
