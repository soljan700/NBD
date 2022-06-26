db.people.mapReduce(
    function() {
        var bmi = this.weight / (this.height * this.height * 0.01 * 0.01)
        emit(this.nationality, bmi)
    }, 
    function(keyId, values) {

        var maxBmi = -Infinity
        var minBmi = Infinity

        for (var i=0; i<values.length; i++) {
            if (values[i] > maxBmi) {
                maxBmi = values[i]
            }
            if (values[i] < minBmi) {
                minBmi = values[i]
            }
        }

        return {
            avgBmi: Array.avg(values),
            maxBmi: maxBmi,
            minBmi: minBmi
        }
    },
    { out: "res" }
)

printjson(db.res.find().toArray())
