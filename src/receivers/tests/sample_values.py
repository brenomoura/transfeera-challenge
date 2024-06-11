VALID_CPF_LIST = [
    "70641242034",
    "97009322147",
    "012.355.010-60",
    "052.518.511-97",
]
INVALID_CPF_LIST = [
    "123.456.789-0",
    "123.456.789-012",
    "123.456.78A-90",
    "123.456.78#-90",
    "123. 456.789-10",
    # some below should be invalid?
    # "111.111.111-11",
    # "000.000.000-00",
    # "123.456.789-10",
    # "987.654.321-00",
    # "123.456.789-09"
]
VALID_CNPJ_LIST = ["33.429.016/0001-73", "88103318000149"]
INVALID_CNPJ_LIST = [
    "12.345.678/0001-9",
    "12.345.678/0001-234",
    "12.345.678/000A-90",
    "12.345.678/000*-90",
    "12. 345.678/0001-10",
    # some below should be invalid?
    # "00.000.000/0000-00",
    # "12.345.678/0001-10",
    # "98.765.432/0001-00",
    # "12.345.678/0001-09"
]

VALID_EMAIL_LIST = [
    "TEST@EXAMPLE.COM",
    "USER+TEST@DOMAIN-TEST.COM",
    "MY_EMAIL123@DOMAIN123.COM",
    "USER.NAME@DOMAIN.COM",
    "NAME_WITH.DOTS@SUB-DOMAIN.EXAMPLE.COM",
    "TEST_USER@EXAMPLE-ORG.COM",
    "TEST-USER@DOMAIN-CO.UK",
    "USER123@DOMAIN.EDU",
    "USER123+TEST@DOMAIN.AC.UK",
    "TEST123@SUB-DOMAIN.TEST.COM",
]

INVALID_EMAIL_LIST = [
    "TEST@EXAMPLE,COM",
    "USER@DOMAIN.COM,BR",
    "USER@",
    "@DOMAIN.COM",
    "USER@DOMAIN!COM",
    "USER NAME@DOMAIN.COM",
    "USER@DOMA IN.COM",
    "USER@DOMAIN@EXAMPLE.COM",
    # some below should be invalid?
    # "USER@DOMAIN.COM.",
    # ".USER@DOMAIN.COM",
    # "USER@.DOMAIN.COM",
    # "USER@DOMAIN..COM",
    # "USER@DOMAIN.COM..BR",
    # "USER@DOMAIN",
    # "USER@-DOMAIN.COM",
    # "USER@DOMAIN-.COM",
    # "USER@DOMAIN.COM.1",
]

VALID_PHONE_LIST = [
    "+5511998765432",
    "+5561987654321",
    "+5571998765432",
    "+5581987654321",
    "+5521998765432",
    "+5562998765432",
    "+5574998765432",
    "+5566998765432",
    "+5541998765432",
    "+5531998765432",
    "11998765432",
    "61998765432",
    "71998765432",
    "81998765432",
    "21998765432",
    "62998765432",
    "74998765432",
    "66998765432",
    "41998765432",
    "31998765432",
]

INVALID_PHONE_LIST = [
    "+5501998765432",
    "+551199876543",
    "+55119987654321",
    "+55A11998765432",
    "551198765432",
    "01998765432",
    "1198765432",
    "+55 11 998765432",
    "+55-11998765432",
    "1199876543",
    "119987654321",
    "+55998765432",
    "++5511998765432",
    "1199876 5432",
    "1A998765432",
    "55+11998765432",
    "+55110098765432",
    "+55-11-998765432",
    "+55(11)998765432",
    "+55.11.998765432",
]

VALID_PIX_RANDOM_KEY_LIST = [
    "123e4567-e89b-12d3-a456-426614174000",
    "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
    "f47ac10b-58cc-4372-a567-0e02b2c3d479",
]

INVALID_PIX_RANDOM_KEY_LIST = [
    "123e4567-e89b-12d3-a456-42661417400",  # Menos dígitos no final
    "123e4567-e89b-12d3-a456-4266141740000",  # Mais dígitos no final
    "123e4567e89b12d3a456426614174000",  # Sem hífens
    "123e4567-e89b-12d3-a456-42661417400g",  # Caractere inválido 'g'
    "123e4567-e89b-12d3-a456-426614174",  # Final muito curto
    "123e4567-e89b-12d3-a456-426614174000-",  # Hífen extra no final
    "123e4567-e89b-12d3-a456-426614-174000",  # Hífen extra no meio
    "g23e4567-e89b-12d3-a456-426614174000",  # Caractere inválido 'g' no início
    "123e4567-e89b-12d3-a456-42661417-4000",  # Hífen incorreto na última parte
    "123e4567-e89b-12d3-a456-426614174000-1",  # Hífen extra e dígito extra no final
    "123e4567-e89b-12d3-a456-42661417400$",  # Símbolo inválido '$'
    "123e4567-e89b-12d3-a456-42661417!000",  # Símbolo inválido '!'
    "123e4567-e89b-12d3-a456-42661417400 ",  # Espaço no final
    " 123e4567-e89b-12d3-a456-426614174000",  # Espaço no início
    "123e4567-e89b-12d3-a456-42661417400\n",  # Nova linha no final
    "123e4567-e89b-12d3a-456-426614174000",  # Hífen no lugar errado
    "123e4567-e89b-12d3-a456-4266:4174000",  # Dois pontos em vez de hífen
    "123e4567-e89b-12d3-a456-4266141_4000",  # Underscore em vez de hífen
    "123e4567-e89b-12d3-a456-4266141740",  # Muito curto no final
    "123e4567-e89b-12d3-a456-4266141740000a",  # Dígito extra no final
    "123e4567-e89b-12d3-a456-42661417400000",  # 12 caracteres finais em vez de 13
    "123e4567-e89b-12d3-a456-42661417",  # Incompleto no final
    "123e4567-e89b-12d3-a456-42661417400-",  # Hífen extra no final
    "-123e4567-e89b-12d3-a456-426614174000",  # Hífen extra no início
    "123e4567-e89b-12d3a-456-426614174000",  # Hífen no lugar errado
    "123e4567e-89b-12d3-a456-426614174000",  # Hífen no lugar errado
]

PIX_AND_VALID_VALUES = [
    ("CPF", VALID_CPF_LIST),
    ("CNPJ", VALID_CNPJ_LIST),
    ("EMAIL", VALID_EMAIL_LIST),
    ("TELEFONE", VALID_PHONE_LIST),
    ("CHAVE_ALEATORIA", VALID_PIX_RANDOM_KEY_LIST),
]

PIX_AND_INVALID_VALUES = [
    ("CPF", INVALID_CPF_LIST),
    ("CNPJ", INVALID_CNPJ_LIST),
    ("EMAIL", INVALID_EMAIL_LIST),
    ("TELEFONE", INVALID_PHONE_LIST),
    ("CHAVE_ALEATORIA", INVALID_PIX_RANDOM_KEY_LIST),
]
