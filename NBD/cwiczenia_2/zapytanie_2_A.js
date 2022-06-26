

db.people.find().forEach(function(data) {
    db.people.update({
        _id: data._id,
    }, {
        $set: {
            credit: data.credit.map(function(credit) {
                return {
                    type: credit.type,
                    number: credit.number,
                    currency: credit.currency,
                    balance: parseFloat(credit.balance)
                };
            })
        }
    });
})


printjson(
    db.people.aggregate([
        {
            $unwind: "$credit"
        },
        {
            $group: {
                _id: "$credit.currency",
                value: { $sum: "$credit.balance" }
            }
        }
    ]).toArray()
)
