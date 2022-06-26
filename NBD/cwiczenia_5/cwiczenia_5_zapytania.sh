 curl http://localhost:8098/buckets/s26342/props \
     -i -v -X PUT \
     --header 'Content-Type: application/json' \
     --data '{"props":{}}'

#1

curl -i -v -X PUT \
    --header 'Content-Type: application/json' \
    --data '{"id": 6790,  "Name": "Gladiator", "isUsed": 1, "Type": "digital"}'\
    http://localhost:8098/buckets/s26342/keys/record1?returnbody=true 
    
curl -i -v -X PUT \
    --header 'Content-Type: application/json' \
    --data '{"id": 87653,  "Name": "Star Wars: The Force awakens", "isUsed": 0, "Type": "digital"}'\
    http://localhost:8098/buckets/s26342/keys/record2?returnbody=true 
    
curl -i -v -X PUT \
    --header 'Content-Type: application/json' \
    --data '{"id": 53,  "Name": "Hobbit", "isUsed": 1, "Type": "CD"}'\
    http://localhost:8098/buckets/s26342/keys/record3?returnbody=true 
    
curl -i -v -X PUT \
    --header 'Content-Type: application/json' \
    --data '{"id": 86543,  "Name": "Queen", "isUsed": 0, "Type": "disc"}'\
    http://localhost:8098/buckets/s26342/keys/record4?returnbody=true 
    
curl -i -v -X PUT \
    --header 'Content-Type: application/json' \
    --data '{"id": 274,  "Name": "Transformers", "isUsed": 0, "Type": "digital"}'\
    http://localhost:8098/buckets/s26342/keys/record5?returnbody=true    

#2

curl -i http://localhost:8098/buckets/s26342/keys/record2?returnbody=true

#3

curl -i -v -X PUT \
    --header 'Content-Type: application/json' \
    --data '{"id": 274,  "Name": "Transformers", "isUsed": 0, "Type": "digital", "DateRelease": 2002}'\
    http://localhost:8098/buckets/s26342/keys/record5?returnbody=true 

#4

curl -i -v -X PUT \
    --header 'Content-Type: application/json' \
    --data '{"id": 86543,  "Name": "Queen", "Type": "disc"}'\
    http://localhost:8098/buckets/s26342/keys/record4?returnbody=true 

#5
 
curl -i -v -X PUT \
    --header 'Content-Type: application/json' \
    --data '{"id": 6790,  "Name": "Gladiator", "isUsed": 1, "Type": "CD"}'\
    http://localhost:8098/buckets/s26342/keys/record1?returnbody=true 

#6

curl -i -v -X DELETE \
    http://localhost:8098/buckets/s26342/keys/record4?returnbody=true

#7

curl -i -v    http://localhost:8098/buckets/s26342/keys/record4?returnbody=true


#8

curl -i -v -X POST     --header 'Content-Type: application/json'     --data '{"Name": "Star Wars"}'     http://localhost:8098/buckets/s26342/keys?returnbody=true 


#9

curl -i http://localhost:8098/buckets/s26342/keys/89nwgRoG3kvvaPbzJZspICDoxfy


#10

curl -i -v -X DELETE  http://localhost:8098/buckets/s26342/keys/89nwgRoG3kvvaPbzJZspICDoxfy

