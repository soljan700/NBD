db.people.find().forEach(function(data) {     db.people.update({         
"_id": data._id,         "weight": data.weight   ,         "height": 
data.height   }, {         "$set": {             "weight": 
parseInt(data.weight)  , "height": parseInt(data.height)    }     }) }) 
printjson(db.people.aggregate(    [      {        $group:          {            
_id: "$sex",            avgWeight: { $avg: "$weight" }   ,avgHight: { 
$avg: "$height" }                   }      }    ] ).toArray())
