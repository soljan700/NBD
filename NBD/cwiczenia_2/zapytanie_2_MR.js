db.people.mapReduce(
  function () {
    this.credit.forEach(creditCard => {
      emit(creditCard.currency, parseFloat(creditCard.balance));
    });
  },
  function (key, values) {
    return Array.sum(values);
  },
  { out: 'balance_sums' }
);

printjson(db.balance_sums.find().toArray())

