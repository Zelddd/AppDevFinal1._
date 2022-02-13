import uuid


class Information():
    def __init__(self, product_name, product_price, product_weight, product_image, product_details, product_category):
        self.__product_id = str(uuid.uuid4())
        self.__product_name = product_name
        self.__product_price = product_price
        self.__product_weight = product_weight
        self.__product_image = product_image
        self.__product_details = product_details
        self.__product_category = product_category

    def get_id(self):
        return self.__product_id
    
    def get_name(self):
        return self.__product_name

    def get_price(self):
        return self.__product_price
    
    def get_weight(self):
        return self.__product_weight

    def get_image(self):
        return self.__product_image

    def get_details(self):
        return self.__product_details
    
    def get_category(self):
        return self.__product_category

    
    def set_id(self, product_id):
        self.__product_id = product_id
    
    def set_name(self, name):
        self.__product_name = name

    def set_price(self, product_price):
        self.__product_price = product_price
    
    def set_weight(self, product_weight):
        self.__product_weight = product_weight
    
    def set_image(self, product_image):
        self.__product_image = product_image

    def set_details(self, product_details):
        self.__product_details = product_details
    
    def set_category(self, product_category):
        self.__product_category = product_category