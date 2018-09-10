import re


def format_str(string):
    string = ''.join(string.strip())
    string = string.replace('\n', '')
    return string


def get_table_name(unit_str):
    result = re.search(r'(Таблица \d\d-\d\d-\d\d\d(.*?)\n)', unit_str, re.IGNORECASE)
    if result:
        return ''.join(result.group(1).strip())
    return None


def get_otdel(unit_str):
    result = re.search(r'(Отдел(.*?)\n)', unit_str, re.IGNORECASE)
    if result:
        return ''.join(result.group(1).strip())
    return None


def get_razdel(unit_str):
    unit_str = format_str(unit_str)
    result = re.search(r'(Раздел\s{0,2}\d{1,2}(.*?)\n*)Таблица', unit_str, re.IGNORECASE)
    if result:
        return ''.join(result.group(1).strip())
    return None


def get_podrazdel(unit_str):
    result = re.search(r'(Подраздел(.*?)\n)', unit_str, re.IGNORECASE)
    if result:
        return ''.join(result.group(1).strip())
    return None


def get_unit(unit_str):
    result = re.search(r'Измеритель:(.*?)\Z', unit_str)
    if result:
        return ''.join(result.group(1).strip())
    return None


def check_id(str):
    str = ''.join(str.strip())
    result = re.match(r'\d\d-\d\d-\d\d\d-\d\d', str)
    if result:
        return True
    else:
        return False
