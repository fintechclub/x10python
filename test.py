from X10ExchangeAccounts import AccountCreator

creator = AccountCreator()
acc = creator.getAccount("usd_p1")

print(acc.getCommonAccountInfo())