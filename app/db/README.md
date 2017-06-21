SQLite DB files:

- Users (users.db)
- Reports (reports.db)
- User Reports (userreports.db)

# Users
"users" (users.db) table organized as follows:

| User ID | Report ID |

- Session ID: ID associated with the user logged in
- Report ID: ID associated with the produced report - used in all analytics 
files as well

# Reports
"reports" (reports.db) table organized as follows:

| User ID | Report ID |

- Session ID: ID associated with the user logged in
- Report ID: ID associated with the produced report - used in all analytics 
files as well


# User Reports
"userreports" (userreports.db) table organized as follows:

| User ID | Report ID |

- Session ID: ID associated with the user logged in
- Report ID: ID associated with the produced report - used in all analytics 
files as well
