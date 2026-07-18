# create errors


class BadUserIdError(BaseException):
    def __init__(self):
        message = "Ошибка, айди транзакции не найдено, или оно было удалено."
        super().__init__(message)


class ValueNotFoundError(BaseException):
    def __init__(self):
        message = "Криптовалюта не была найдена. Пожалуйста, укажите валюту в формате: <b>BTC</b> или <b>ETH</b>"
        super().__init__(message)


class BadMessageText(TypeError):
    def __init__(self):
        message = "Ошибка в получении сообщения, скорее всего вы ввели неприемлемый тип сообщения."
        super().__init__(message)


class ManyTransactionsError(BaseException):
    def __init__(self):
        message = "У вас слишком много активов и трат(50), удалите лишнюю и добавьте другую"
        super().__init__(message)


class BigNumError(BaseException):
    def __init__(self):
        message = "Вы ввели слишком много активов, введите число поменьше."
        super().__init__(message)


class BigCommentError(BaseException):
    def __init__(self):
        message = "Вы ввели слишком длинный комментарий, введите его поменьше."
        super().__init__(message)


class PageError(BaseException):
    def __init__(self):
        message = "Такой страницы не существует."
        super().__init__(message)


class ProfileExpiredError(BaseException):
    def __init__(self):
        message = "Похоже, вы давно не пользовались ботом, перейдите в главное меню, чтобы начать заново."
        super().__init__(message)
