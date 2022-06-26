from riak import RiakClient

client = RiakClient(pb_port=8087)
bucket = client.bucket('s26342')

# wrzucenie dokumentu
doc_0 = {"id": 6790,  "Name": "Gladiator", "isUsed": 1, "Type": "digital"}
key_0 = 'program_0'
bucket.new(key_0, data=doc_0).store()

doc_1 = {"id": 274,  "Name": "Transformers", "isUsed": 0, "Type": "digital"}
key_1 = 'program_1'
bucket.new(key_1, data=doc_1).store()

# pobranie i wypisanie
doc_0 = bucket.get(key_0)
print(f'Dodany dokument:\n{doc_0.data}\n\n')

doc_1 = bucket.get(key_1)
print(f'Dodany dokument:\n{doc_1.data}\n\n')

# modyfikacja, pobranie i wypisanie
doc_0.data["Type"] = "CD"
doc_0.store()
doc_0 = bucket.get(key_0)
print(f'Zmodyfikowany dokument:\n{doc_0.data}\n\n')

# usunięcie i próba pobrania
doc_0.delete()
doc_0 = bucket.get(key_0)
print(f'Czy w bazie zmodyfikowany doc_0 :\n{doc_0.data}')

doc_1 = bucket.get(key_1)
print(f'Czy w bazie doc_1:\n{doc_1.data}')
