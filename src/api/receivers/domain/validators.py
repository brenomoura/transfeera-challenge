import re


def validate_pix(pix_key: str, pix_key_type: str) -> None:
    validators_funcs = {
        "CPF": validate_cpf,
        "CNPJ": validate_cnpj,
        "EMAIL": validate_email,
        "TELEFONE": validate_phone,
        "CHAVE_ALEATORIA": validate_random_key,
    }
    validators_funcs[pix_key_type](pix_key)


def validate_email(value: str) -> str:
    pattern = r"^[A-Z0-9+_.-]+@[A-Z0-9.-]+$"
    match = re.match(pattern, value)
    if not match:
        raise ValueError("Formato de E-mail inválido")
    return value


def validate_cpf(value: str) -> str:
    pattern = r"^[0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2}$"

    match = re.match(pattern, value)
    if not match:
        raise ValueError("Formato de CPF inválido")
    return value


def validate_cnpj(value: str) -> str:
    # check here
    pattern = r"^[0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2}$"

    match = re.match(pattern, value)
    if not match:
        raise ValueError("Formato de CNPJ inválido")
    return value


def validate_phone(value: str) -> str:
    pattern = r"^((?:\+?55)?)([1-9][0-9])(9[0-9]{8})$"

    match = re.match(pattern, value)
    if not match:
        raise ValueError("Formato de telefone inválido")
    return value


def validate_random_key(value: str) -> str:
    pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"

    match = re.match(pattern, value, flags=re.IGNORECASE)
    if not match:
        raise ValueError("Formato de telefone inválido")
    return value


def validate_cpf_cnpj(value: str) -> str:
    if len(value) in [11, 14]:
        try:
            return validate_cpf(value)
        except ValueError:
            pass

    if len(value) in [14, 18]:
        try:
            return validate_cnpj(value)
        except ValueError:
            pass

    raise ValueError(f"Formato de CPF ou CNPJ inválido")
