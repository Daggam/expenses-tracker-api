from typing import Annotated

from fastapi import Depends


#Por ahora lo vamos a dejar así
def get_current_user() -> int:
    return 1

CurrentUser = Annotated[int,Depends(get_current_user)]