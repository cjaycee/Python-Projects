catalog = {
    "chair": 60,
    "table": 100,
    "mirror": 20,
}
shopping_cart = {}
cart_total = 0 
print(f"Welcome to Jiacheng's furniture store!\nHere is the catalog:\n{catalog}")
while True:
    order = input("What do you want to order: ")
    if order=="checkout":
        print("Checking out now")
        break
    ordersplitup = [x.strip() for x in order.split(",")]    
    for item in ordersplitup:
#        if item not in catalog:
#            print("One of the items you've entered is invalid, please retry!")
        if item in catalog:
            quantity = int(input(f"How many {item}s do u want: "))
            shopping_cart.update({item: quantity})
            cart_total += catalog.get(item)*shopping_cart.get(item)
    confirmation = input("Is that all for your order? ")
    if confirmation.lower()=="yes":
        print("Checking out now")
        break
#    if confirmation=="no" or confirmation=="No"
print(f"This is the summary of your shopping cart:\n{shopping_cart}")  
print(f"The total for your cart is: {cart_total}")
print("Pls proceed to checkout")


