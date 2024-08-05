

class InsufficientFunds(Exception) :

    def __init__(self,amount,balance,wallet) :
        self.amount = amount
        self.balance = balance
        self.wallet = wallet

    def __str__(self) :
        return "Your {} balance is too low to perform this transaction. You need an extra #{} to proceed.".format(
            self.wallet,
            self.amount - self.balance

        )    


class IncompleteProcess(Exception) :

    def __init__(self,error="Please try again") :
        self.error = error

    def __str__(self) :
        return "The current process was not completed, {}".format(self.error)


class IncorrectPinError(Exception) :

    def __str__(self) :
        return "The entered pin is incorrect, please crosscheck."