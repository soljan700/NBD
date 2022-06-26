printjson(db.people.updateMany( 
    {
                "location.city": "Moscow"
        },
        // update
        {
                $set: { "location.city" : "Moskwa" }
        }
))

