SQLite DB tables:

- Users (users)
- Reports (reports)
- User Reports (userreports)

# Users
"users" (users.db) table organized as follows:

Column Names: | userid | name | email | 

- User ID (userid): ID associated with the account (internally stored)
- Name (name): Full name of the user
- Email (email): Email address associated with user account

# User Reports
"userreports" (userreports.db) table organized as follows:

Column Names: | userid | reportid |

- Session ID (userid): ID associated with the user (from "users" table)
- Report ID (reportid): ID associated with the produced report 
(from "reports" table)
