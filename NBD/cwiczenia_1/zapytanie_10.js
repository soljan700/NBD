printjson(db.people.remove({"job":"Editor"},{$unset : 'email'}))
