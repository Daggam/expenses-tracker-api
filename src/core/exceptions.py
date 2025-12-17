class BaseAPIException(Exception):
    def __init__(self,
                 message:str,
                 error_code:str='standar_error',
                 status_code:int=400
                 ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(message)


class ExpenseCategoryNotFoundError(BaseAPIException):
    def __init__(self,category:str):
        super().__init__(message=f"Expense Category {category} not found.",
                        error_code="expense_category_not_found",
                        status_code=404)

class ExpenseNotFoundError(BaseAPIException):
    def __init__(self,
                 expense_id:int):
        super().__init__(message=f"Expense {expense_id} not found.",
                        error_code="expense_not_found",
                        status_code=404)

class InvalidModelError(BaseAPIException):
    def __init__(self):
        super().__init__(message="The model is invalid.",
                         error_code="invalid_model",
                         status_code=422)

class UserNotFoundError(BaseAPIException):
    def __init__(self):
        super().__init__(message="The user not found.",
                         error_code="user_not_found",
                         status_code=404)