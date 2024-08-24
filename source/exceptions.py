from fastapi import HTTPException

PasswordUpperCaseException = HTTPException(
    status_code=400,
    detail='Пароль должен содержать минимум одну букву верхнего регистра [Eng]'
)

PasswordLowerCaseException = HTTPException(
    status_code=400,
    detail='Пароль должен содержать минимум одну букву нижнего регистра [Eng]'
)

PasswordNumException = HTTPException(
    status_code=400,
    detail='Пароль должен содержать минимум одну цифру'
)

PasswordCharException = HTTPException(
    status_code=400,
    detail='Пароль должен содержать минимум один спец символ'
)

PasswordLengthException = HTTPException(
    status_code=400,
    detail='Пароль должен быть не менее 12 и не более 30 символов'
)

PasswordNotAsciiException = HTTPException(
    status_code=400,
    detail='Пароль должен содержать только печатаемые символы'
)

OldPasswordIncorrectException = HTTPException(
    status_code=400,
    detail='Старый пароль неверен'
)

PasswordsMatchException = HTTPException(
    status_code=400,
    detail='Старый и новый пароль должны отличаться'
)


IncorrectJWTException = HTTPException(
    status_code=401,
    detail='Токен невалиден'
)

ExpireJWTException = HTTPException(
    status_code=401,
    detail='Токен истёк'
)

JWTNotFound = HTTPException(
    status_code=401,
    detail='Токен не найден'
)

EmailAlreadyException = HTTPException(
    status_code=409,
    detail='Почта уже зарегистрирована'
)

EmailOrPasswordIncorrectException = HTTPException(
    status_code=401,
    detail='Неверная почта или пароль'
)

NotFoundException = HTTPException(
    status_code=404,
    detail='Not Found'
)

MusicAlreadyExistException = HTTPException(
    status_code=409,
    detail='Данная музыка уже находиться в базе'
)

RollbackException = HTTPException(
    status_code=500,
    detail='Произошла ошибка, попробуйте снова'
)

GenreNotFoundException = HTTPException(
    status_code=404,
    detail='Такого жанра нет в сервисе'
)

FileNotEndswithException = HTTPException(
    status_code=400,
    detail='Файл не имеет расширения'
)

FileNotSupportedException = HTTPException(
    status_code=400,
    detail='Расширение таких файлов не поддерживаеться'
)

EmailNotFoundException = HTTPException(
    status_code=404,
    detail='Почта не зарегистрирована'
)

UserNotFoundException = HTTPException(
    status_code=404,
    detail='Пользователь удалён'
)

UserAlreadyAuthException = HTTPException(
    status_code=400,
    detail='Выйдите из аккаунта для продолжения действий'
)