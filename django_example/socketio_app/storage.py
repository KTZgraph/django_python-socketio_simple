from cgitb import reset
import collections
from datetime import datetime
from unittest import result

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

CONNECTION_STRING = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false'


def get_db_connector()->pymongo.database.Database:
    client = MongoClient(CONNECTION_STRING)

    # nazwa bazy danych to 'socket_simple'
    db = client.socket_simple
    print(type(db))
    return db

def get_notes_collection()->pymongo.collection.Collection:
    db = get_db_connector()

    # notes to nazwa kolekcji
    print(type(db.notes))
    return db.notes

def find_note_by_id(note_id:str)->pymongo.cursor.Cursor:
    if note_id is None:
        return

    collection = get_notes_collection()
    result = collection.find({"_id": note_id})
    print(result)
        
    return result

def update_note(note:dict)->pymongo.results.UpdateResult:
    collection = get_notes_collection()
    result = collection.update_one(
        {"_id": note['_id']},
        {"$set": {"data": note['data']}}
    )
    print(result)
    print(type(result))
    return result

def save_note(note:dict)->pymongo.results.InsertOneResult:
    collection = get_notes_collection()
    try:
        result = collection.insert_one(note)
        return result
    except pymongo.errors.DuplicateKeyError:
        print(f'Note with id:{note["_id"]} already exists')

def get_or_create_note(note_id):
    if note_id in None:
        return
    
    # note = 

if __name__ == '__main__':
    get_db_connector()
    get_notes_collection()
    # save_note({'_id': 123456, 'data': 'Ala ma kota'})
    # find_note_by_id(123456)
    # update_note({'_id': 123456, 'data': 'Ala ma psa'})
    find_note_by_id(1)