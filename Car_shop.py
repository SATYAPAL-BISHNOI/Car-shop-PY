import pickle
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Car:
    def __init__(self ,holder_name,car_number,car_name,booking_date ,email):
        self.booking_number = None
        self.email = email
        self.holder_name = holder_name
        self.car_number = car_number
        self.car_name = car_name
        self.booking_date = booking_date
        self.delevery_date = None
        self.service_reminder_date = None
    
    def set_delivery_date(self, delivery_date):
        self.delivery_date = delivery_date

    def set_service_reminder_date(self, service_reminder_date):
        self.service_reminder_date = service_reminder_date

    def get_booking_number(self, booking_number =100):
        booking_number +=1
        self.booking_number = booking_number
        return self.booking_number

    def calculate_service_charge( self, gst):
        service_charge = input('Service charge(first charge is 1000rupess) : ') 
        gst_amount = (service_charge*gst)/service_charge
        total_amount = service_charge+gst_amount
        return total_amount
    
class Carshop:
    def __init__(self):
        self.cars = []

    def add_car(self, car):
        self.cars.append(car)

    def display_all(self):
        for idx, car in enumerate(self.cars, start=1):
            print(f"Car {idx}:")
            print(f"Booking Number: {car.get_booking_number()}")
            print(f"Email: { car.email}")
            print(f"Holder Name: {car.holder_name}")
            print(f"Car Number: {car.car_number}")
            print(f"Car Name: {car.car_name}")
            print(f"Booking Date: {car.booking_date}")
            print(f"Delivery Date: {car.delivery_date}")
            if car.service_reminder_date:
                print(f"Service Reminder Date: {car.service_reminder_date}")
            else:
                print(f"Service Reminder Date: not due to service reminder")
            print()
        
    
    def delete_from_file(self, filename,car_idx):
        if car_idx < 0 or car_idx >= len(self.cars):
            print("invalid car index")
            return
        try:
            with open (filename,'rb') as file:
                self.cars = pickle.load(file)
            
        except FileNotFoundError:
            print(" Not found this file :" + filename)
            return
        
        del self.cars[car_idx]
        print("car deleted successfully from :" + filename)

        with open (filename,'wb') as file:
            pickle.dump(self.cars,file)
            print("save all reminder data to file :" + filename)

    def set_service_reminder(self, car_idx):
        car = self.cars[car_idx]
        reminder_date = datetime.datetime.now() + datetime.timedelta(minutes=2)
        car.set_service_reminder_date(reminder_date)
        print("Reminder Date set successfully")

    def delete_data(self):
        curruntime = datetime.datetime.now()
        for car in self.cars:
            if car.booking_date + datetime.timedelta(minutes=10)< curruntime:
                self.cars.remove(car)
        print("Data deleted successfully")


    def calulate_service_charges(self,car_idx,gst_rate):
        car = self.cars[car_idx]
        total_charge = car.calculate_service_charge(gst_rate)
        print(f"service charge(including{gst_rate}%GST):${total_charge: .2f}")
    def save_to_file(self,filename):
        with open(filename,'wb') as file:
            pickle.dump(self.cars,file)
        print("Data saved successfully")

    def load_from_file(self,filename):
        try:
            with open(filename,'rb') as file:
                self.cars = pickle.load(file)
                print("Data loaded successfully")
        except FileNotFoundError:
            print("File not found")

    def send_service_reminder_email(self, car):
        sender_email = "xyzxyz6547@gmail.com"
        receiver_email = car.email
        password = "Satish@000"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Service Reminder"

        body = f"Dear {car.holder_name},\n\n"
        body += f"Your service reminder for {car.car_name} is due on {car.service_reminder_date}.\n\n"
        body += f"Regards,\nSatyapal Bishnoi"
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        # server.ehlo()
        server.starttls()
        # server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully")

def main():
    car_shop = Carshop()

    while True:
        print("1. Add Car")
        print("2. Display All Cars")
        print("3. Set Service Reminder")
        print("4. Delete Data")
        print("5. Calculate Service Charge")
        print("6. Save to File")
        print("7. Load from File")
        # print("8. Send Service Reminder Email")
        print("9. delete from file(faster::::::: delete)")
        print("10. Exit")
        choice = int(input("Enter your choice: "))


        if choice == 1:
            holder_name = input("Enter holder name: ")
            email = input("Enter email: ")
            car_number = input("Enter car number: ")
            car_name = input("Enter car name: ")
            booking_date = datetime.datetime.now()
            delivery_date = input("Enter delivery date (yyyy-mm-dd): ")
            delivery_date = datetime.datetime.strptime(delivery_date, '%Y-%m-%d')
            car = Car(holder_name,car_number,car_name,booking_date,email)
            car.set_delivery_date(delivery_date)
            car_shop.add_car(car)
            print("Car added successfully")


        elif choice == 2:
            car_shop.display_all()

        
        elif choice == 3:
            car_idx = int(input("Enter car index: ")) -1
            car_shop.set_service_reminder(car_idx)

        elif choice == 4:
            car_shop.delete_data()

        elif choice == 5:
            car_idx = int(input("Enter car index: ")) -1
            gst_rate = int(input("Enter gst rate: "))
            car_shop.calulate_service_charges(car_idx,gst_rate)
        
        elif choice == 6:
            filename = input("Enter filename: ")
            car_shop.save_to_file(filename)

        elif choice == 7:
            filename = input("Enter filename: ")
            car_shop.load_from_file(filename)

        elif choice == 8:
            car_idx = int(input("Enter car index: ")) -1
            car_shop.send_service_reminder_email(car_shop.cars[car_idx])


        elif choice == 9:
            car_idx = int(input("Enter car index: ")) -1
            filename = input("Enter filename: ")
            car_shop.delete_from_file( filename,car_idx)

        elif choice == 10:
            print("exit............")
            break

        else:
            print("Invalid choice")
        
if __name__ == "__main__":
    main()