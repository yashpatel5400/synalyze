"""
__authors__	 = Yash, Will, Peter
__description__ = Cleans up DB, largely for the case of maintenance or
simply debugging before deployment. DO NOT EXECUTE ON SERVER
__name__ = clean.py
"""

import settings as s
import sqlite3

cur = sqlite3.connect(s.DB_NAME)
cur.execute("DROP TABLE {}".format(s.USERS_TABLE))
cur.execute("DROP TABLE {}".format(s.REPORTS_TABLE))
cur.execute("DROP TABLE {}".format(s.USER_REPORTS_TABLE))
cur.commit()