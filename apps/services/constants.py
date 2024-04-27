###############################################################################
#                           Модель Collect
###############################################################################
# Максимальная длинна title карточки сбора.
COLLECT_TITLE_LENGTH = 100

# Кол-во символов в choices карточки сбора.
COLLECT_CHOICES_LEN = 10

# Максимальная длинна description карточки сбора.
COLLECT_DESC_LENGTH = 2000

# Максимальная длина slug карточки сбора.
COLLECT_SLUG_MAX_LEN = 100

# Максимальная длинна occasion карточки сбора.
COLLECT_OCASSION_LENGTH = 100

# Пагинация сборов.
COLLECT_PAGINATE_COUNT = 3

###############################################################################
#                            Модель Payment
###############################################################################
# Максимльное число знаков в платеже.
PAIMENT_MAX_DIGITS = 10

# Максимльное число знаков после запятой в платеже.
PAIMENT_DECIMAL_PLACES = 2

# Максимальное число знаков комментария.
PAIMENT_COMMENT_MAX_LEN = 250

# Кол-во символов в choices платежа.
PAIMENT_CHOICES_LEN = 15

# Пагинация сборов.
PAIMENT_PAGINATE_COUNT = 3


###############################################################################
#                            Модель DonationsUser
###############################################################################
# Максимальное кол-во знаков описания профиля.
BIO_MAX_LENGTH = 400

# Максимальное кол-во знаков отчества.
PATERNAL_NAME_LEN = 30


###############################################################################
#                                   Прочее
###############################################################################
# Help text для заполнения target_amount исходя из ограничений.
MAX_PAYMENT_VALUE = (f'Сумма в рублях, максимальное занчение: '
                     f'{'9' * (PAIMENT_MAX_DIGITS - PAIMENT_DECIMAL_PLACES)}.'
                     f'{'9' * PAIMENT_DECIMAL_PLACES}')
