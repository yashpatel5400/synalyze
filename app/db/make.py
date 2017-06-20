"""
__authors__	 = Yash, Will, Peter
__description__ = Creates DB file to start - only execute after a clean for
development. DO NOT EXECUTE ON SERVER
__name__ = clean.py
"""

import settings as s
import sqlite3

cur = sqlite3.connect(s.DB_NAME)
cur.execute("""CREATE TABLE {}
	   (userid text, reportid text)""".format(s.TABLE_NAME))
cur.commit()