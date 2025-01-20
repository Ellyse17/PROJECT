
class Config:
    DEBUG =False
    TESTING =False
    SECRET_KEY ='secret_key'
    
class DevelopmentConfig(Config):
        DEBUG =True
    

class TestingConfig(Config):
        TESTING =True


class ProductionConfig(Config):
 pass


