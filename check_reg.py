import re

def get_unit(unit_str):
    unit = ''
    razdel = ''
    podrazdel = ''
    try:
        unit = re.search(r'Измеритель:(.*?)\Z', unit_str).group(1)
    except Exception as e:
        return unit, razdel, podrazdel

    try:
        razdel = re.search(r'((Раздел\s{0,2}\d*)((.*?)(\n))*)Подраздел', unit_str, re.IGNORECASE).group(1)
        podrazdel = re.search(r'Подраздел(.*?)\n', unit_str, re.IGNORECASE).group(1)
    except AttributeError as e:
        return unit, razdel, podrazdel

    return unit, razdel, podrazdel

