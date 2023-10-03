import pandas as pd

df = pd.read_csv("hotels.csv", dtype={'id': str})
df_card = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_card_authenticate = pd.read_csv("card_security.csv", dtype=str)


class Hotel:

    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df['id'] == self.hotel_id, 'name'].squeeze()

    def book(self):
        """book the hotel by changing availability no"""
        df.loc[df['id'] == self.hotel_id, 'available'] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """checks if the hotel is available"""
        availability = df.loc[df['id'] == self.hotel_id, 'available'].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class SpaHotel(Hotel):
    def book_spa_package(self):
        pass


class ReservaionTicket:

    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for reservation!
        Your details are following
        Name: {self.customer_name}
        Hotel_name: {self.hotel.name}
        
        Have a good day!
        """
        return content


class CreditCard:

    def __init__(self, number):
        self.number = number

    def validate(self, expiration, cvc, holder):
        card_data = {"number": self.number, "expiration": expiration, "cvc": cvc, "holder": holder}
        if card_data in df_card:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):

    def authenticates(self, given_password):
        password = df_card_authenticate.loc[df_card_authenticate['number'] == self.number, 'password'].squeeze()
        if password == given_password:
            return True
        else:
            return False


class Spa:

    def __init__(self, customer_name, hotel_object):
        self.hotel = hotel_object
        self.customer_name = customer_name
        self.hotel_object = hotel_object

    def generate(self):
        content = f"""
        Thank you for spa reservation!
        Followings are the spa details:
        Name:{self.customer_name}
        Hotel name = {self.hotel.name}
        """
        return content


print(df)
hotel_ID = input("Enter the id of the hotel: ")
hotel = SpaHotel(hotel_ID)
if hotel.available():
    creditcard = SecureCreditCard(number="1234")
    if creditcard.validate(expiration="12/26", cvc="123", holder="JOHN SMITH"):
        if creditcard.authenticates(given_password="mypass"):
            hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservaionTicket(name, hotel)
            print(reservation_ticket.generate())
            choice = input("Do you want to book a spa package?: ")
            if choice == "yes":
                hotel.book_spa_package()
                spa = Spa(name, hotel)
                print(spa.generate())
            else:
                print("Thank you!")
        else:
            print("Your authentication has been failed!")
    else:
        print("There was a problem with your payment!")
else:
    print("Hotel not available")
