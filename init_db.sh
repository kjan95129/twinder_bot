#!/bin/bash

if [ -f chat_server.db ] ; then
    rm chat_server.db
fi

sqlite3 chat_server.db < db_script.sql
