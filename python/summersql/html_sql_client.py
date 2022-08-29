import socket
from tcp_by_size import send_with_size, recv_by_size
import os
import pickle
from protocol import User, AddOrganRequest, BuyOrganRequest, SuccessResponse, ErrorResponse, Balance, BuyOrganResponse
os.system("")  # enables ansi escape characters in terminal

class Client:
    BUY = 1
    ADD = 2
    GET_BALANCE = 3
    QUIT = 4

    def __init__(self):
        
        self.name = input("Please enter your name (John, Paul, George, Ringo): ")
        
        self.sock = socket.socket()
        self.sock.connect(('127.0.0.1', 2000))
        Client.intro()
        self.run()

    def run(self) -> None:
        while True:
            cli_action = Client.menu()
            match cli_action:
                case Client.QUIT:
                    print('Goodbye!')
                    break
                case Client.ADD:
                    organ_type = input('Enter organ type: ')
                    organ_price = int(input('Enter organ price: '))
                    organ_expiration_date = input('Enter organ expiration date (MM-YYYY): ')
                    self.sock.send(pickle.dumps(AddOrganRequest(self.name, organ_type, organ_price, organ_expiration_date)))
                    response = pickle.loads(self.sock.recv(1024))
                    if isinstance(response, SuccessResponse):
                        print(f"Added {self.name}, {organ_type}, {organ_price}, {organ_expiration_date}")
                    else:
                        print(f"Couldn't complete action")
                case Client.BUY:
                    organ_id = int(input('Enter organ id: '))
                    self.sock.send(pickle.dumps(BuyOrganRequest(self.name, organ_id)))
                    response = pickle.loads(self.sock.recv(1024))
                    if isinstance(response, BuyOrganResponse):
                        print(f"Bought organ successfully")
                        print(f"Organ id: {organ_id}")
                        print(f"Organ dealer name: {response.organ_dealer_name}")
                        print(f"Organ type: {response.organ_type}")
                        print(f"Organ price: {response.organ_price}")
                        print(f"Organ expiration date: {response.organ_expiration_date}")
                    else:
                        print(f"Couldn't complete action")
                case Client.GET_BALANCE:
                    self.sock.send(pickle.dumps(User(self.name)))
                    response = pickle.loads(self.sock.recv(1024))
                    if isinstance(response, Balance):
                        print(f"Your balance is {response.balance}")
                    else:
                        print(f"Couldn't complete action")
                case _:
                    print('Invalid choice. Please enter a valid instruction.')

    @staticmethod
    def intro() -> None:
        print("""                                                                                                                       
[38;5;10m                            @/&@                                    
                            .#////                                  
                            @#@////                                 
                         #@%#&(@%#@%                                
                        ,(@%@@@@@&%@                                
        /%@#@/*,(@      *@@&#@@&///%/*,                             
       (@@(/***@*@     @@@&&%*////##@&@.                            
           *@#%//@   ,@@@/&@@@@/@@&#**@@                            
             &///#@ @@&/@*@(/@#@@///@/%///           [38;5;255mWelcome to The Silk Road.
[38;5;10m             @/#///#(//////*/@@//@/////////%         [38;5;255mEnjoy your stay!
[38;5;10m              @@/%/#////@(***//@(@/////*%@@@                        
             @  @*@@///@@/@@@//@*@////*/@@@@                        
                    //@*@@@@/%@/@@#//#/@@@@@                        
                     (/@  @@@     @//&% #@*@                        
                     ,/@  @&(      ///   @%/                        
                      //  @*.      //*    @/                        
                      //# @&%       **     @,                       
                      (&   /        /@%    (*@                      
                       @   #@       *@      @@                      
                       /    /      @@       @@                      
                      (/,  @/@    #@  @@@@@@@%@&@@*                 
                    #//@@&@*@@@@@/#@@@@@@@@@*/@@@                   
                             (/@(/@(         *                                  
[38;5;255m""")

    @staticmethod
    def menu() -> int:
        print("""
        1. Buy Organ
        2. Add Organ
        3. Get Balance
        4. Exit
        """)
        return int(input("Enter Instruction Number: "))


if __name__ == '__main__':
    Client()
