printjson(
db.people.aggregate([
    { $group: { _id: "$nationality", 
        avgBmi: { 
            $avg: { $divide: [ "$weight", { $multiply: [ "$height", "$height", 0.01, 0.01 ] } ] }
        },
        maxBmi: { 
            $max: { $divide: [ "$weight", { $multiply: [ "$height", "$height", 0.01, 0.01 ] } ] }
        },
        minBmi: { 
            $min: { $divide: [ "$weight", { $multiply: [ "$height", "$height", 0.01, 0.01] } ] }
        }
    } }
])
.toArray())
