
# Client side requests
class User:

    def __init__(self, name):
        self.name = name


class AddOrganRequest(User):
    
    def __init__(self, dealer_name, organ_type, organ_price, organ_expiration_date):
        super().__init__(dealer_name)
        self.organ_type = organ_type
        self.organ_price = organ_price
        self.organ_expiration_date = organ_expiration_date


class BuyOrganRequest(User):

    def __init__(self, buyer_name, organ_id):
        super().__init__(buyer_name)
        self.organ_id = organ_id

# Server side responses

class SuccessResponse:
    pass


class ErrorResponse:
    pass


class Balance(SuccessResponse):
    
    def __init__(self, balance):
        self.balance = balance


class BuyOrganResponse(SuccessResponse):
    
    def __init__(self, organ_dealer_name, organ_type, organ_price, organ_expiration_date):
        self.organ_dealer_name = organ_dealer_name
        self.organ_type = organ_type
        self.organ_price = organ_price
        self.organ_expiration_date = organ_expiration_date