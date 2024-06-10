import pytest

from receivers.domain.validators import validate_cpf, validate_cnpj, validate_cpf_cnpj, validate_email, validate_phone, \
    validate_pix_random_key, validate_pix
from receivers.tests.sample_values import VALID_PHONE_LIST, INVALID_EMAIL_LIST, VALID_EMAIL_LIST, INVALID_CNPJ_LIST, \
    INVALID_CPF_LIST, VALID_CNPJ_LIST, VALID_CPF_LIST, INVALID_PHONE_LIST, VALID_PIX_RANDOM_KEY_LIST, \
    INVALID_PIX_RANDOM_KEY_LIST


@pytest.mark.parametrize("cpf", VALID_CPF_LIST)
def test_validate_valid_cpf(cpf):
    validate_cpf(cpf)


@pytest.mark.parametrize(
    "cpf", INVALID_CPF_LIST
)
def test_validate_valid_cpf(cpf):
    with pytest.raises(ValueError) as error:
        validate_cpf(cpf)
    assert str(error.value) == "Formato de CPF inválido"


@pytest.mark.parametrize("cnpj", VALID_CNPJ_LIST)
def test_validate_valid_cnpj(cnpj):
    validate_cnpj(cnpj)


@pytest.mark.parametrize("cnpj", INVALID_CNPJ_LIST)
def test_validate_invalid_cnpj(cnpj):
    with pytest.raises(ValueError) as error:
        validate_cnpj(cnpj)
    assert str(error.value) == "Formato de CNPJ inválido"


@pytest.mark.parametrize("cpf_cnpj", VALID_CNPJ_LIST + VALID_CPF_LIST)
def test_validate_valid_cpf_cnpj(cpf_cnpj):
    validate_cpf_cnpj(cpf_cnpj)


@pytest.mark.parametrize("cpf_cnpj", INVALID_CNPJ_LIST + INVALID_CPF_LIST)
def test_validate_invalid_cpf_cnpj(cpf_cnpj):
    with pytest.raises(ValueError) as error:
        validate_cpf_cnpj(cpf_cnpj)
    assert str(error.value) == "Formato de CPF ou CNPJ inválido"


@pytest.mark.parametrize(
    "email",
    VALID_EMAIL_LIST
)
def test_validate_valid_email(email):
    validate_email(email)


@pytest.mark.parametrize(
    "email",
    INVALID_EMAIL_LIST

)
def test_validate_invalid_email(email):
    with pytest.raises(ValueError) as error:
        validate_email(email)
    assert str(error.value) == "Formato de E-mail inválido"


@pytest.mark.parametrize(
    "phone",
    VALID_PHONE_LIST
)
def test_validate_valid_phone(phone):
    validate_phone(phone)


@pytest.mark.parametrize(
    "phone",
    INVALID_PHONE_LIST
)
def test_validate_invalid_phone(phone):
    with pytest.raises(ValueError) as error:
        validate_phone(phone)
    assert str(error.value) == "Formato de telefone inválido"


@pytest.mark.parametrize(
    "pix_random_key", VALID_PIX_RANDOM_KEY_LIST)
def test_validate_valid_pix_random_key(pix_random_key):
    validate_pix_random_key(pix_random_key)


@pytest.mark.parametrize(
    "pix_random_key", INVALID_PIX_RANDOM_KEY_LIST)
def test_validate_valid_pix_random_key(pix_random_key):
    with pytest.raises(ValueError) as error:
        validate_pix_random_key(pix_random_key)
    assert str(error.value) == "Formato de Chave Aleatória inválido"


@pytest.mark.parametrize(
    "pix",
    [
        ("CPF", VALID_CPF_LIST),
        ("CNPJ", VALID_CNPJ_LIST),
        ("EMAIL", VALID_EMAIL_LIST),
        ("TELEFONE", VALID_PHONE_LIST),
        ("CHAVE_ALEATORIA", VALID_PIX_RANDOM_KEY_LIST),
    ]
)
def test_validate_valid_pix(pix):
    pix_key_type, valid_pix_key_values = pix
    for valid_pix in valid_pix_key_values:
        validate_pix(valid_pix, pix_key_type)


@pytest.mark.parametrize(
    "pix",
    [
        ("CPF", INVALID_CPF_LIST),
        ("CNPJ", INVALID_CNPJ_LIST),
        ("EMAIL", INVALID_EMAIL_LIST),
        ("TELEFONE", INVALID_PHONE_LIST),
        ("CHAVE_ALEATORIA", INVALID_PIX_RANDOM_KEY_LIST),
    ]
)
def test_validate_invalid_pix_key_values(pix):
    pix_key_type, valid_pix_key_values = pix
    for valid_pix in valid_pix_key_values:
        with pytest.raises(ValueError):
            validate_pix(valid_pix, pix_key_type)


def test_validate_invalid_pix_key_type():
    with pytest.raises(ValueError) as error:
        validate_pix("RANDOM_KEY_VALUE", "NON_EXISTING_KEY")
    assert str(error.value) == "Tipo de Chave Pix inválido"
