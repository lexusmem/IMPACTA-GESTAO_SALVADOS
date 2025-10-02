from datetime import datetime


# Função que recebe uma data e um formato, retornando a data formatada
def strftime_filter(value, format_string):
    if value and isinstance(value, (datetime, str)):
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                return value
        return value.strftime(format_string)
    return ''


def currency_filter(value):
    if value is None or value == '':
        return ''
    try:
        value = float(value)
        return f"R$ {value:,.2f}".replace('.', '#').replace(',', '.').replace('#', ',')
    except (ValueError, TypeError):
        return value
