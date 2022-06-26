printjson(db.people.insert([
{"sex" : "Male",
	"first_name" : "Jann",
	"last_name" : "Solarz",
	"job" : "Data Scientist",
	"email" : "s26342@pjwstk.edu.pl",
	"location" : {
		"city" : "Wroclaw",
		"address" : {
			"streetname" : "eehte",
			"streetnumber" : "24"
		}
	},
	"description" : "lalala lala",
	"height" : "190.09",
	"weight" : "88.39",
	"birth_date" : "1998-03-04T10:27:20Z",
	"nationality" : "Poland",
	"credit" : [
		{
			"type" : "jcb",
			"number" : "0382463462",
			"currency" : "PLN",
			"balance" : "9999.85"
		},
		{
			"type" : "mastercard",
			"number" : "7654345678",
			"currency" : "EUR",
			"balance" : "4597.96"
		},
		{
			"type" : "visa-club-enroute",
			"number" : "23567",
			"currency" : "USD",
			"balance" : "4349.65"
		}
	]}
	]))
