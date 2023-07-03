import mysql.connector
from datetime import datetime, date
from datetime import datetime, date, timedelta

conn=mysql.connector.connect(host='localhost',username='root',password='#Shruti_DBMS4',database='BazaarLane')
my_cursor=conn.cursor()
conn.connect()

#start defining all functions here

def extractID(n, val):  ## to extract the ID of the customer and update it

    val_ini = val[:n]
    val_fi = val[n:]
    l = len(val_fi)

    int_val = int(val_fi)
    int_val += 1

    new_str = str(int_val).zfill(l)

    new_str = val_ini + new_str
    return new_str

####################################################################

def enterChoice():  ## user can enter as one of the following

    print("Enter one of the options")
    print("1. Enter as Admin")
    print("2. Enter as Customer")
    print("3. Enter as Delivery Person")
    print("4. Exit the application")

####################################################################

def addProduct(new_str, table_name, productID):  ##fuction to add a product

    prodName = input("Enter the product name ")
    prodQuantity = input("Enter the product Quantity ")
    prodPrice = int(input("Enter product price "))
    prodStock = int(input("Enter the stock of the product "))

    new_prod = f"""insert into %s 
    (ProductID, CategoryID, ProductName, ProductQuantity, ProductPrice, ProductStock) 
    values ('{productID}', '{new_str}', '{prodName}', '{prodQuantity}', {prodPrice}, {prodStock});
    """%(table_name)
    
    my_cursor.execute(new_prod)
    conn.commit()

####################################################################

def aunthenticateAdmin():  ##admin authentication ##hardcoded

    ID_admin = 'admin'
    pw_admin = 'admin123'

    admin_ID = input("Please enter admin ID ")
    admin_pw = input("Please enter admin password ")
    print()

    if(admin_ID == ID_admin and pw_admin == admin_pw):
        print("Welcome Admin!! ")
        print()
    
    else:
        print("Incorrect ID or password!! Please enter correct details to proceed")
        op = input("Press 'e' to exit or press 'c' to continue ")
        if(op == 'c'):
            aunthenticateAdmin()
        else:
            exit() 

def enterAdminChoice():  ##options available to the admin
    
    print("Please choose one of the following options ")
    print("1. Add a category")
    print("2. Add a product")
    print("3. Delete a category")
    print("4. Delete a product") 
    print("5. Change price of product")
    print("6. Update product Stock")
    print("7. Add Coupon")
    print("8. Delete Coupon")
    print("9. Update Coupon Discount") 
    print("10. Update MinValue of Coupon")
    print("11. Update Expiry Date of coupon ")
    print("12. Show grants")  
    print("13. Exit")  
    print()

def adminChoice(k):  ##admin functionality function

    while(k<13):

        if(k==1):  ##add a category 
            
            print("Please enter the following details to add a category")
            catName = input("Please enter the name of the category ")

            val = """select CategoryID from Category
            ORDER BY CategoryID DESC LIMIT 1;"""

            my_cursor.execute(val)
            db = my_cursor.fetchall()
            
            new_str = extractID(3, db[0][0])

            input_customer = f"""insert into Category (CategoryID, CategoryName) values ('{new_str}', '{catName}');"""
            my_cursor.execute(input_customer)
            conn.commit()

            print("Category Successfully Added!!")
            print("Category ID is ", new_str)

            table_name = input("Enter the name of the product table ")

            prod_table = f"""create table %s(
                ProductID varchar(255) PRIMARY KEY,
                CategoryID varchar(255),
                ProductName varchar(255) NOT NULL,
                ProductQuantity varchar(255) NOT NULL,
                ProductPrice float NOT NULL,
                ProductStock int NOT NULL,
                FOREIGN KEY(CategoryID) REFERENCES Category(CategoryID) ON DELETE SET NULL
                );"""%(table_name)
            
            my_cursor.execute(prod_table)
            conn.commit()

            print("Please enter a product in the category added ")
            productID = input("Enter the product ID ")
            addProduct(new_str, table_name, productID)

            print("Category Added Successfully ")

        elif(k==2): ##add a product ##done

            print("Please enter the following details to add a product ") 
            catID = input("Enter the categoryID you would to add the product in ")

            catName = f"""select CategoryName from Category
            where CategoryID = '{catID}';"""

            my_cursor.execute(catName)
            table_name = my_cursor.fetchall()

            old_prodID = """select ProductID from %s
            ORDER BY ProductID DESC LIMIT 1;"""%(table_name[0][0])

            my_cursor.execute(old_prodID)
            db = my_cursor.fetchall()
            
            productID = extractID(2, db[0][0])

            addProduct(catID, table_name[0][0], productID)

            print("Product Added Successfully ")
                
        elif(k==3): ##delete a category ##done

            print("Please enter the following details to delete a category ")
            catID = input("Enter the category ID you would like to delete ")
            del_Cat = f"""delete from Category WHERE CategoryID = '{catID}';"""

            my_cursor.execute(del_Cat)
            conn.commit()

            print("Category Deleted Successfully ")

        elif(k==4): ##delete a product ##done

            print("Please enter the following details to delete a product ")
            catID = input("Enter the categoryID whose product you would like to delete ")
            prodID = input("Enter the product ID you would like to delete ")

            catName = f"""select CategoryName from Category
            where CategoryID = '{catID}';"""

            my_cursor.execute(catName)
            table_name = my_cursor.fetchall()

            del_Prod = f"""delete from %s WHERE ProductID = '{prodID}';"""%(table_name[0][0])
            
            my_cursor.execute(del_Prod)
            conn.commit()

            print("Product Deleted Successfully ")

        elif(k==5): ##change price of product ##done

            print("Please enter the following details to change the price of a product ")
            prodID = input("Enter the product ID whose price you would like to update ")
            catID = input("Enter the categoryID of the product ")

            catName = f"""select CategoryName from Category
            where CategoryID = '{catID}';"""

            my_cursor.execute(catName)
            table_name = my_cursor.fetchall()
            
            new_price = int(input("Enter the new price of the product "))

            update_price =f"""UPDATE %s
                SET ProductPrice = {new_price}
                WHERE ProductID = '{prodID}';"""%(table_name[0][0])
            
            my_cursor.execute(update_price)
            conn.commit()

            print("Price updated successfully")
        
        elif(k==6): ##update stock of product ##done

            print("Please enter the following details to update the stock of a product ")
            prodID = input("Enter the product ID whose stock you would like to update ")
            catID = input("Enter the categoryID of the product ")

            catName = f"""select CategoryName from Category
            where CategoryID = '{catID}';"""

            my_cursor.execute(catName)
            table_name = my_cursor.fetchall()

            stock = int(input("Enter the stock you would like to add "))

            update_stock = f"""UPDATE %s
                SET ProductStock = ProductStock + {stock}
                WHERE ProductID = '{prodID}';"""%(table_name[0][0])
            
            my_cursor.execute(update_stock)

            conn.commit()

            print("Stock updated successfully")

        elif(k==7): ##add a coupon ##done

            print("Please enter the following details to add a coupon ") 
            cpn_Name = input("Enter coupon Name ")
            cpn_dis = int(input("Enter coupon discount "))
            cpn_minVal = int(input("Enter minimum Value of coupon "))
            cpn_expiry = input("Enter expiryDate of coupon ")

            val = """select CouponID from Coupon
            ORDER BY CouponID DESC LIMIT 1;"""

            my_cursor.execute(val)
            db = my_cursor.fetchall()
            
            cpn_ID = extractID(6, db[0][0])

            coupon_new = f"""insert into Coupon (CouponID, CouponName, Discount, MinValue, ExpiryDate) 
            values ('{cpn_ID}', '{cpn_Name}', {cpn_dis}, {cpn_minVal}, '{cpn_expiry}');"""

            my_cursor.execute(coupon_new)
            conn.commit()

            print("Coupon Added Successfully ")

        elif(k==8): ##delete a coupon ##done

            print("Please enter the following details to delete a coupon") 
            cpn_ID = input("Enter the coupon ID you would like to delete ")

            del_Coupon = f"""delete from Coupon WHERE CouponID = '{cpn_ID}';"""

            my_cursor.execute(del_Coupon)
            conn.commit()

            print("Coupon Deleted Successfully ")
        
        elif(k==9): ##change the discount of a coupon ##done

            print("Please enter the following details to change the discount of a coupon ")
            couponID = input("Enter the coupon ID of the coupon whose discount you would like to update ")
            dis = int(input("Enter the new discount"))

            update_disount = f"""UPDATE Coupon
                SET Discount = {dis}
                WHERE CouponID = '{couponID}';"""
            
            my_cursor.execute(update_disount)
            conn.commit()

            print("Discount updated successfully")

        elif(k==10): ##change the minimum Value of a coupon ##done

            print("Please enter the following details to change the minimum value of a coupon ")
            couponID = input("Enter the coupon ID of the coupon whose minimum value you would like to update ")
            minVal = int(input("Enter the new minimum value"))

            update_minVal = f"""UPDATE Coupon
                SET MinValue = {minVal}
                WHERE CouponID = '{couponID}';"""
            
            my_cursor.execute(update_minVal)
            conn.commit()

            print("Minimum Value updated successfully")

        elif(k==11): ##change expiry date of coupon ##done

            print("Please enter the following details to change the expiry date of a coupon ")
            couponID = input("Enter the coupon ID of the coupon whose expiry date you would like to update ")
            expDate = input("Enter the new expiry date")

            update_expDate = f"""UPDATE Coupon
                SET ExpiryDate = '{expDate}'
                WHERE CouponID = '{couponID}';"""
            
            my_cursor.execute(update_expDate)
            conn.commit()

            print("Expiry Date updated successfully")

        elif(k==12): ##change expiry date of coupon ##done

            print("To show grants ")

            grants = f"""SHOW GRANTS FOR root@localhost;;"""
            
            my_cursor.execute(grants)
            db = my_cursor.fetchall()

            for i in db:
                print(i)
                print()
        
        else:
            exit()
            
        print()
        enterAdminChoice()
        k = int(input())
    
    print("You have logged out of admin ")
    print()

####################################################################

def customerOptions(): ##customer initial option
    print("1. Login")
    print("2. SignUP")
    print("3. Exit")

def aunthenticationCustomer():  ##customer authentication

    customer_ID = input("Please enter Customer ID ")
    
    check_ID = f"""SELECT COUNT(CustomerID) FROM Customer
    WHERE EXISTS(
    SELECT * FROM Customer WHERE CustomerID = '{customer_ID}');"""
    
    my_cursor.execute(check_ID)
    db = my_cursor.fetchall()

    if(db[0][0] == 0):
        print("CustomerID does not exist please enter a valid customerID")
        op = input("Press 'e' to exit or press 'c' to continue ")
        if(op == 'c'):
            aunthenticationCustomer()
        else:
            exit()
    else:
        cus_pw = customer_ID + '_123'
        customer_pw = input("Please enter Customer Password ")
        if(cus_pw == customer_pw):
            print()
            print("Welcome Customer! ")
        else:
            print("CustomerPW is not correct please enter the correct password ")
            op = input("Press 'e' to exit or press 'c' to continue ")
            if(op == 'c'):
                aunthenticationCustomer()
            else:
                exit()


def customerInit(x):  ##initial customer functionality

    if(x==1):
        print("Hey please login")
        aunthenticationCustomer()
        enterCustomerChoice()
        k = int(input())
        customerChoice(k)

    elif(x==2): 

        print("Please Enter the following details ")
        firstName = input("Please enter the first name ")
        middleName = input("Please enter the middle name(NULL if none) ")
        lastName = input("Please enter the last name ")
        email = input("Please enter email ID ")
        age = int(input("Please enter the age "))
        sex = input("Enter Male, Female, or Prefer not say ")
        addr = input("Enter address ")
        phNum = input("Enter phone number ")

        val = """select CustomerID from Customer
            ORDER BY CustomerID DESC LIMIT 1;"""

        my_cursor.execute(val)
        db = my_cursor.fetchall()
        
        cus_ID = extractID(3, db[0][0])

        input_customer = f"""insert into Customer (CustomerID, FirstName, MiddleName, LastName, 
        Email, Age, Sex, Address, PhoneNumber) values ('{cus_ID}', '{firstName}', '{middleName}', '{lastName}', 
        '{email}', {age}, '{sex}', '{addr}', '{phNum}');"""

        my_cursor.execute(input_customer)

        print("Your Customer ID is ", cus_ID)
        cus_pw = cus_ID + '_123'
        print("Your password is ", cus_pw)

        customerInit(1)
    
    else:
        print("You have logged out of customer ")
        print()
        return

def enterCustomerChoice(): ##options avaialble to customer
    print("Please choose one of the following options ")
    print("1. Add product to cart")
    print("2. Remove product from cart")
    print("3. View product catalog")  
    print("4. Check all coupons")
    print("5. Check available coupons") #left
    print("6. View Previous Orders")
    print("7. Checkout")
    print("8. Cancel Order")
    print("9. Add money to wallet")
    print("10. Update email")
    print("11. Update Address")
    print("12. Update Phone number")
    print("13. exit")

def customerChoice(k): ##customer functionality function
        
    while(k<13):

        if(k==1): ##add product to cart
            print("Please neter the following details to add a product in the cart")
            catID = input("Enter the category ID of the product you would like to add to cart ")
            prodID = input("Enter the product ID of the product you would like to add to cart ")

            catName = f"""select CategoryName from Category
            where CategoryID = '{catID}';"""

            my_cursor.execute(catName)
            table_name = my_cursor.fetchall()

            prod_name = f"""select ProductName from %s
            where ProductID = '{prodID}'; """ %(table_name[0][0])

            my_cursor.execute(prod_name)
            product_name = my_cursor.fetchall()

            prod_price = f"""select ProductPrice from %s
            where ProductID = '{prodID}'; """ %(table_name[0][0])

            my_cursor.execute(prod_price)
            unit_price = my_cursor.fetchall()

            quantity = int(input("Please enter the quantity you would like to add "))

            stock = f"""select ProductStock from %s
            where ProductID = '{prodID}'; """ %(table_name[0][0])

            my_cursor.execute(stock)
            available_stock = my_cursor.fetchall()
          
            if(quantity > available_stock[0][0]):
                print("Not enough stock ")
            
            else:
                total = quantity * unit_price[0][0]
                addTOCart = f"""insert into Cart 
                (ProductID, ProductName, CategoryName, UnitPrice, Quantity, Total) 
                values ('{prodID}', '{product_name[0][0]}', '{table_name[0][0]}', {unit_price[0][0]}, {quantity}, {total});"""

                my_cursor.execute(addTOCart)
                conn.commit()
                
                print()
                print("Product successfully added!! ")
                print()

        elif(k==2): ##remove product from cart

            print("Please enter the following details to delete a product from cart")
            prodID = input("Please enter the product ID you would like to remove from cart ")

            delFromCart = f"""delete from Cart WHERE ProductID = '{prodID}';"""

            my_cursor.execute(delFromCart)
            conn.commit()

            print("Product Deleted from Cart Successfully ")

        elif(k==3): ##product catalogue
            print("The product catalog is ")
            my_cursor.execute("SELECT * FROM Inventory;")
            showinventory = my_cursor.fetchall()
            for i in showinventory:
                print(i)
        
        elif(k==4): ##all coupons
            print("The coupons available in the application are ")
            all_Coupon = """select * from Coupon;"""

            my_cursor.execute(all_Coupon)
            details = my_cursor.fetchall()

            for i in details:
                print(i)

        elif(k==5): ##available coupons for customer
            print("Available coupons are ")

            total = f"""select SUM(Total) from Cart; """

            my_cursor.execute(total)
            cart_total = my_cursor.fetchall()

            query = f"""select * from Coupon 
            where MinValue < {cart_total[0][0]};
            """
            my_cursor.execute(query)
            available_coupon = my_cursor.fetchall()

            for i in available_coupon:
                print(i)

        elif(k==6): ##details of previos order

            print("Details of previous orders are ")

            all_Orders = """select * from Orders;"""

            my_cursor.execute(all_Orders)
            details = my_cursor.fetchall()

            for i in details:
                print(i)

        elif(k==7): ##checkout order

            print("Please enter the following details")

            orderDate = date.today()
            formatted_date = orderDate.strftime('%Y-%m-%d')

            Address = input("Enter Address: ")
            paymentMethod = input("Enter Payment Method: ")

            val = """select OrderID from Orders
                        ORDER BY OrderID DESC LIMIT 1;"""

            my_cursor.execute(val)
            db = my_cursor.fetchall()
                        
            ord_ID = extractID(3, db[0][0])

            total = f"""select SUM(Total) from Cart; """

            my_cursor.execute(total)
            cart_total = my_cursor.fetchall()

            order_new = f"""insert into Orders (OrderID, OrderStatus, OrderDate, Address, TotalAmount, PaymentMethod, ShipperID) 
                        values ('{ord_ID}', 'Confirmed', '{formatted_date}', '{Address}', '{cart_total[0][0]}', '{paymentMethod}', 'S0029');"""

            my_cursor.execute(order_new)
            conn.commit()

            print("Checkout successful ")
        
        elif(k==8): ##cancel order ##check karna hai

            print("Please enter the following details to cancel your order ")
            orderID = input("Enter the Order ID of the Order which you would like to cancel ")

            update_ordStatus = f"""UPDATE Orders
                SET OrderStatus = 'Cancelled'
                WHERE OrderID = '{orderID}';"""
            
            my_cursor.execute(update_ordStatus)
            conn.commit()

            print("Your Order is Cancelled.")

        elif(k==9): ##add money to wallet

            print("Please enter the following details to add money to the wallet")
            cusID = input("Enter the customer ID linked to the wallet ")
            money = int(input("Enter the amount you would like to add to your wallet "))

            update_wallet = f"""UPDATE Customer
                SET Wallet = Wallet + {money}
                WHERE CustomerID = '{prodID}';"""
            
            my_cursor.execute(update_wallet)
            conn.commit()

            print("Money successfully added to wallet")

        elif(k==10): ##update customer email

            print("Please enter the following details to update the email ")
            cusID = input("Enter the customer ID of the customer whose email you would like to update ")
            email = input("Enter the new email")

            update_email = f"""UPDATE Customer
                SET Email = '{email}'
                WHERE CustomerID = '{cusID}';"""
            
            my_cursor.execute(update_email)
            conn.commit()

            print("Email updated successfully")
        
        elif(k==11): ##update customer address

            print("Please enter the following details to update the address ")
            cusID = input("Enter the customer ID of the customer whose address you would like to update ")
            address = input("Enter the new address")

            update_address = f"""UPDATE Customer
                SET Address = '{address}'
                WHERE CustomerID = '{cusID}';"""
            
            my_cursor.execute(update_address)
            conn.commit()

            print("Address updated successfully")

        elif(k==12): ##update customer phone number

            print("Please enter the following details to update the phone Number ")
            cusID = input("Enter the customer ID of the customer whose phone Number you would like to update ")
            phNum = input("Enter the new phone Number")

            update_phNum = f"""UPDATE Customer
                SET PhoneNumber = '{phNum}'
                WHERE CustomerID = '{cusID}';"""
            
            my_cursor.execute(update_phNum)
            conn.commit()

            print("Phone number updated successfully")
        
        else:
            return
        
        enterCustomerChoice()
        k = int(input())
    
    print()
    print("You have logged out of customer")

####################################################################

def shipperOptions(): ##shipper initial options
    print("1. Login")
    print("2. SignUP")
    print("3. Exit")

def aunthenticationShipper(): ##shipper aunthetication

    shipper_ID = input("Please enter Shipper ID ")
    
    check_ID = f"""SELECT COUNT(ShipperID) FROM DeliveryPerson
    WHERE EXISTS(
    SELECT * FROM DeliveryPerson WHERE ShipperID = '{shipper_ID}');"""
    
    my_cursor.execute(check_ID)
    db = my_cursor.fetchall()

    if(db[0][0] == 0):
        print("ShipperID does not exist please enter a valid ShipperID")
        op = input("Press 'e' to exit or press 'c' to continue ")
        if(op == 'c'):
            aunthenticationShipper()
        else:
            exit()
    else:
        ship_pw = shipper_ID + '_123'
        shipper_pw = input("Please enter Shipper Password ")
        if(ship_pw == shipper_pw):
            print()
            print("Welcome Shipper! ")
        else:
            print("ShipperPW is not correct please enter the correct password ")
            op = input("Press 'e' to exit or press 'c' to continue ")
            if(op == 'c'):
                aunthenticationShipper()
            else:
                exit()

def shipperInit(x): ##shipper initial functionality

    if(x==1):
        print("Hey please login")
        aunthenticationShipper()
        enterShipperChoice()
        k = int(input())
        shipperChoice(k)

    elif(x==2): 

        print("Please Enter the following details ")
        firstName = input("Please enter the first name ")
        middleName = input("Please enter the middle name(NULL if none) ")
        lastName = input("Please enter the last name ")
        email = input("Please enter email ID ")
        age = int(input("Please enter the age "))
        phNum = input("Enter phone number ")

        val = """select ShipperID from Shipper
            ORDER BY ShipperID DESC LIMIT 1;"""

        my_cursor.execute(val)
        db = my_cursor.fetchall()
        
        ship_ID = extractID(3, db[0][0])

        input_shipper = f"""insert into DeliveryPerson (ShipperID, FirstName, MiddleName, LastName, 
        Email, Age, PhoneNumber) values ('{ship_ID}', '{firstName}', '{middleName}', '{lastName}', 
        '{email}', {age}, '{phNum}');"""

        my_cursor.execute(input_shipper)

        print("Your Shipper ID is ", ship_ID)
        ship_pw = ship_ID + '_123'
        print("Your password is ", ship_pw)

        customerInit(1)
    
    else:
        print("You have logged out of shipper ")
        print()
        return

def enterShipperChoice(): ##options available to shipper
    print("Please choose one of the following options ")
    print("1. Print deatils of order ")
    print("2. Update email")
    print("3. Update Phone number")
    print("4. exit")

def shipperChoice(k): ##shipper functionality function
        
    while(k<4):

        if(k==1):
            print("Enter the shipper ID of the shipper whose delivery history you would like to view ")
            shipID = input("Enter the shipper ID")
            
            view_orders = f"""SELECT * FROM Orders
            WHERE ShipperID = '{shipID}';"""

            my_cursor.execute(view_orders)
            orderlist = my_cursor.fetchall()
            for i in orderlist:
                print(i)
            conn.commit()

        elif(k==2):
            print("Please enter the following details to update the email ")
            shipID = input("Enter the shipper ID of the shipper whose email you would like to update ")
            email = input("Enter the new email")

            update_email = f"""UPDATE DeliveryPerson
                SET Email = '{email}'
                WHERE ShipperID = '{shipID}';"""
            
            my_cursor.execute(update_email)
            conn.commit()

            print("Email updated successfully")

        elif(k==3):
            print("Please enter the following details to update the phone Number ")
            print("Please enter the following details to update the phone number ")
            shipID = input("Enter the shipper ID of the shipper whose phone number you would like to update ")
            phnum = input("Enter the new phone number")

            update_phnum = f"""UPDATE DeliveryPerson
                SET PhoneNumber = '{phnum}'
                WHERE ShipperID = '{shipID}';"""
            
            my_cursor.execute(update_phnum)
            conn.commit()
        
        else:
            exit()
        
        enterShipperChoice()
        k = int(input())

    print()
    print("You have logged out of shipper ")

####################################################################

##main menu
print("******************************************************************")
print("                     Welcome to Bazaar Lane")
print("               Your trusted online retail store")
print("******************************************************************")

enterChoice()
n = int(input())

while(n<4):

    if(n==1):

        aunthenticateAdmin()
        enterAdminChoice()
        k = int(input())
        adminChoice(k)

    elif(n==2):

        customerOptions()
        x = int(input("Choose one of the above options to procees "))
        customerInit(x)

    elif(n==3):
        
        aunthenticationShipper()
        enterShipperChoice()        
        k = int(input())
        shipperChoice(k)

    else:
        exit()

    enterChoice()
    n = int(input())

print("******************************************************************")
print("           Thank you so much for choosing BazaarLane")
print("******************************************************************")

conn.close()