printjson(db.people.aggregate([{
    $group: {_id: null, uniqueJobs: {$addToSet: "$job"}}
}]).toArray())

