# Максимальная длинна title карточки сбора.
COLLECT_TITLE_LENGTH: int = 100

# Кол-во символов в choices карточки сбора.
COLLECT_CHOICES_LEN: int = 10

# Максимальная длинна description карточки сбора.
COLLECT_DESC_LENGTH: int = 2000

# Максимальная длина slug карточки сбора.
COLLECT_SLUG_MAX_LEN: int = 100

# Максимальная длинна occasion карточки сбора.
COLLECT_OCASSION_LENGTH: int = 100

# Пагинация сборов.
COLLECT_PAGINATE_COUNT: int = 3

# Максимльное число знаков в платеже.
PAIMENT_MAX_DIGITS: int = 10

# Максимльное число знаков после запятой в платеже.
PAIMENT_DECIMAL_PLACES: int = 2

# Максимальное число знаков комментария.
PAIMENT_COMMENT_MAX_LEN: int = 250

# Кол-во символов в choices платежа.
PAIMENT_CHOICES_LEN: int = 15

# Пагинация сборов.
PAIMENT_PAGINATE_COUNT: int = 3


# Help text для заполнения target_amount исходя из ограничений.
MAX_PAYMENT_VALUE: str = (
    f'Сумма в рублях, максимальное занчение: '
    f'{"9" * (PAIMENT_MAX_DIGITS - PAIMENT_DECIMAL_PLACES)}.'
    f'{"9" * PAIMENT_DECIMAL_PLACES}'
)
