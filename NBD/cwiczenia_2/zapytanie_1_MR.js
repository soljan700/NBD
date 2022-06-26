db.people.mapReduce(
	function() {
		let key = this.sex;
		let value = { 
			height: parseFloat(this.height),
			weight: parseFloat(this.weight),
			count: 1
		};
	emit(key, value);
	}, 
	
	function(key, values) {
		let reduce = { 
			height: 0,
			weight: 0,
			count: 0
		};
	values.forEach(function(value){
		reduce.height += value.height,
		reduce.weight += value.weight,
		reduce.count += value.count;
	});
		return reduce;
	},
	
	{ 
	out: 'averages',
	finalize: function(key, reduce) 
		{
		reduce.height = reduce.height / reduce.count;
		reduce.weight = reduce.weight / reduce.count;
		return reduce;
		},
	}
)

printjson(db.averages.find().toArray())
