from x10project import BitfinexLogic
from x10project import BittrexLogic

class AccountCreator:
    def __init__(self):
        self.accounts={'usd_p1': BitfinexLogic('Bitfinex USD', 
                                                 'vpSFVZbAyllcTKiCNOMi5hMKJgUusqAZV2LUoQ6wohR',             'aU5vcSwaNdpBchIPWuACUvx4mntghvQB3zBcj8KLV9d'),
                      'rustam':  BitfinexLogic('Аккаунт Рустама', 
                                                 'ldRMGd9EJSBFBsqiY3PAOJQFhfajnqh7O8ONmY8wmPf', 
                                                 'CQQsGPr0APN8owGKjtB1KthukKQu6M5lqVZoIuPwft2'),
                      'arsen':  BitfinexLogic('Арсений Мск', 
                                                 'TuWsoRu4vvrNrQBYQgDMSrMMv0tAAKIKjFSOefLNJg8', 
                                                 'tS4woU82QpuKnBNORId8XbCWN6ZhOklHWSyckJvPO46'),
                      'pokrov': BittrexLogic('Покровский', 
                                                'a1ab591819dd4789a6f0bc4e762caa9d',	
                                                'ecf2d128ed614816b0ab4abbb6ce80e9'),
                      'igor': BittrexLogic('Игорь', 
                                                '64fa097eb78c40338301fd1cd8df61ed',	
                                                '574d13a6749749ad90ee94621084f6a0')}
        
        
    def getAccount(self, code):
        return self.accounts[code] if code in self.accounts else None
        
        
    def getAvailiableAccounts(self):
        return [x for x in self.accounts.keys()]
    
