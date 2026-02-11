# PasswordManager

## Overview

`PasswordManager` is a small, interactive Python CLI that lets you **store**, **validate**, **update**, **delete**, and **generate** passwords for named programs.

Instead of storing plaintext passwords, it stores a **PBKDF2-HMAC-SHA256 hash** of each password plus a per-entry **random salt** in a local `passwords.txt` file.

> ⚠️ Note: This is a learning/demo-style password utility. It does **not** encrypt the database and does not support retrieving original passwords (only validating them)

---

## Requirements

* Python 3.8+ (stdlib only)

No third-party packages are required.

---

## Run

From the directory containing `PasswordManager.py`:

```bash
python PasswordManager.py
```

You will see:

```
Welcome! To add a password type in add, validate, delete, or generate. Enter q or Q to exit.
```

Then enter one of the supported actions.

---

## Commands

### `add`

Stores a program name and password hash.

Flow:

1. Prompts for **Program Name** and **Enter Password**
2. Generates a random 20-byte salt (`os.urandom(20)` → base64)
3. Hashes password with PBKDF2-HMAC-SHA256 (`iterations = 1000`)
4. Appends to `passwords.txt`

Example stored line format:

```
program: Gmail hash: b'...' salt: <base64-salt>
```

### `validate`

Checks whether an entered password matches the stored hash for a program.

Flow:

1. Prompts for program + password
2. Loads salt + stored hash for that program from `passwords.txt`
3. Recomputes PBKDF2 hash and compares

Outputs either:

* `Passwords match!`
* `Passwords do not match.`

### `delete`

Deletes an entry by removing any line in `passwords.txt` that contains the provided program string.

### `update`

Replaces an entry by:

1. Deleting the program entry
2. Adding the new password for the same program

### `generate`

Generates a random password and stores it.

* The password is produced by generating 20 random bytes and converting them to a large integer string.
* The generated password is printed once:

```
Generated Password: <value>
```

---

## File Storage

All entries are stored in `passwords.txt` in the same directory you run the script from.

Each entry stores:

* Program name
* Password hash bytes (string representation)
* Base64 salt string

---

