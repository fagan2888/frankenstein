class DefaultConfig():


    epochs = 10  # number of variations to cross validate per model


    class Polynomial():

        START = 2
        STOP = 2


    @classmethod
    def loss(cls, preds, targets):
        return sum([(p-t)**2 for p,t in zip(preds, targets)])
