height = float(input("What is your height in metres?"))
weight = float(input("What is your weight in kilograms?"))
bmi = float(round(weight/(height*height),2))
print(bmi)