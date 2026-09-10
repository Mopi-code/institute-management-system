# Institute Management System

A desktop app for managing a small institute/school, built with **Python (PySide6/Qt)** and **MySQL**. Students can register, log in, browse available classes, enroll or unenroll, and view teacher information.

## Features

- Student registration and login (email + password)
- Browse available classes with teacher, schedule, and live capacity (X booked / capacity)
- Enroll in a class (blocks duplicate enrollment and enforces capacity limits)
- View and manage "My Classes" — unenroll with a confirmation prompt
- View all teachers and their subjects/emails in a separate dialog
- Styled UI using `qt-material` (dark blue theme by default)

## Tech Stack

- **GUI:** PySide6 (Qt for Python) + qt-material
- **Database:** MySQL
- **Connector:** mysql-connector-python

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up the database

Run the SQL script in `sql/institute.sql` against your MySQL server. This creates the `institute` database along with the `teachers`, `students`, `classes`, and `enrollments` tables, plus some sample data:

```bash
mysql -u root -p < sql/institute.sql
```

### 3. Configure your database credentials

Copy `.env.example` to `.env` and fill in your own MySQL credentials:

```bash
cp .env.example .env
```

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=institute
```

The `.env` file is git-ignored, so your real credentials never get committed.

### 4. Run the app

Run this from the project root (not from inside `app/`) so `.env` is found correctly:

```bash
python app/institute.py
```

This launches the login window first. Use one of the sample accounts seeded in `institute.sql`, or register a new one:

| Email | Password |
|---|---|
| john.doe@example.com | password123 |
| jane.smith@example.com | securepass1 |
| alex.turner@example.com | mypassword1 |

## Project Structure

```
institute-management-system/
├── .env                  # your real DB credentials (git-ignored, not included)
├── .env.example           # template for required environment variables
├── .gitignore
├── README.md
├── requirements.txt
├── app/
│   ├── institute.py        # main window: browse/enroll classes, view teachers
│   ├── login.py             # login window
│   └── register.py          # registration window
└── sql/
    └── institute.sql        # database schema + sample data
```

The three `.py` files must stay together in `app/` — they import each other directly by filename (e.g. `from login import Login`). The `.env` file must stay in the project root, and the app should be run from the root (`python app/institute.py`) so it can find it.

## Known Limitations

- Passwords are currently stored and checked as plain text in the `students` table. This is fine for local learning/demo purposes, but should not be used as-is for anything handling real user data — a hashing library like `bcrypt` would be a good next step.

## License

MIT
