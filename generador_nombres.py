from faker import Faker
fake = Faker('es_ES')

f = open("nombres.txt", "x")
f = open("nombres.txt", "a")

for _ in range(1000000):
	f.write(fake.name() + "\n")

f.close()
