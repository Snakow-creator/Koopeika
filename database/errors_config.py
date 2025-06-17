# делаем свои классы ошибок


class BadUserIdError(Exception):
    def __init__(self):
        message = "Ошибка, айди транзакции не найдено, или оно было удалено."
        super().__init__(message)


class BadMessageText(TypeError):
    def __init__(self):
        message = "Ошибка в получении сообщения, скорее всего вы ввели неприемлемый тип сообщения."
        super().__init__(message)


class ManyTransactionsError(Exception):
    def __init__(self):
        message = "У вас слишком много активов и трат(50), удалите лишнюю и добавьте другую"
        super().__init__(message)


class BigNumError(ValueError):
    def __init__(self):
        message = "Вы ввели слишком много активов, введите число поменьше."
        super().__init__(message)
