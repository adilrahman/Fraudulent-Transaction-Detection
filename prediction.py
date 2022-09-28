import pickle
import pandas as pd


class SuspicionDetection:
    def __init__(self,model, standard_scalar) -> None:
        """'
        Inputs:
            model = prediction model object
            standard_scalar = standardScalar object

        Outputs: None
        """
        self.model = model
        self.standard_scalar = standard_scalar

    def prediction(self) -> str:

        ''''
        description:
            it predict the transaction is suspicious or not

        Output : 
            if suspicious: 
                    return 1
            else:
                    return 0
        '''

        data = {
            "Card": 0,
            "Cash Deposit": 0,
            "Cash Withdrawal": 0,
            "Debit Card": 0,
            "Money Order": 0,
            "amount": 0,
            "PrevBalanceSender": 0,
            "CurrentBalanceSender": 0,
            "PrevBalanceReceiver": 0,
            "CurrentBalanceReceiver": 0,
        }

        print(
            "\nTransaction Type \nOptions :- \n\t1. Card\n\t2. Cash Deposit\n\t3. Cash Withdrawal\n\t4. Debit Card\n\t5. Money Order\n"
        )
        tnx_type = int(input("Enter the number : "))
        if tnx_type == 1:
            data["Card"] = 1

        if tnx_type == 2:
            data["Cash Deposit"] = 1
        
        if tnx_type == 3:
            data["Cash Withdrawal"] = 1

        if tnx_type == 4:
            data["Debit Card"] = 1

        if tnx_type == 5:
            data["Money Order"] = 1

        amount = float(input("Enter the amount : "))
        PrevBalanceSender = float(input("Enter the Prev Balance Sender : "))
        CurrentBalanceSender = float(input("Enter the Current Balance Sender : "))
        PrevBalanceReceiver = float(input("Enter the Prev Balance Receiver : "))
        CurrentBalanceReceiver = float(input("Enter the Current Balance Receiver : "))
    

        data["CurrentBalanceReceiver"] = [CurrentBalanceReceiver]
        data["CurrentBalanceSender"]  = [CurrentBalanceSender]
        data["PrevBalanceSender"] = [PrevBalanceSender]
        data["PrevBalanceReceiver"] = [PrevBalanceReceiver]
        data["amount"] = amount
            
        data = pd.DataFrame(data)
        pred = standard_scalar.transform(data)
        pred = pd.DataFrame(columns = data.columns, data = pred)
        pred = model.predict(pred)[0]

        return int(pred)
        


if __name__ == "__main__":

    # model and standard_scalar loaded
    model = pickle.load(open("trained_model/model.pkl", "rb"))
    standard_scalar = pickle.load(open("encoders/standardScaler.pkl", "rb"))

    cls = SuspicionDetection(model=model,standard_scalar =standard_scalar)

    while True:
        pred = cls.prediction()
        print()
        if pred == 1:
            print(f"prediction : it's suspicious")
        else:
            print(f"prediction : it's not suspicious")
