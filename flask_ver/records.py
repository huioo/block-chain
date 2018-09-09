from collections import UserList


class Transaction(UserList):
    pass


a = Transaction([1,2,3]).data
print(a)

