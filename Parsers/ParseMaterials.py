import re
from colorama import Fore, Style


class ParseMaterials:

    def __init__(self, query):
        self.query = query

    def get_material_price(self, cells):
        result = None
        for i in range(1, 6):
            if len(cells) - 1 < i:
                break
            result = cells[i].text
            result = ''.join(result.split())
            result = result.replace(',', '.')
            try:
                result = float(result)
                result_2 = cells[i + 1].text
                result_2 = ''.join(result_2.split())
                result_2 = result_2.replace(',', '.')
                result_2 = float(result_2)
                return result, result_2
            except Exception as e:
                result = None
                continue
            break
        return result

    def check_material_key(self, cells):
        cell = cells[0]
        result = re.search(r'(\d\d\d-\d\d\d\d)', cell.text)
        if result:
            return result.group(1)
        return None

    def run(self, row):
        result = self.check_material_key(row.cells)
        if not result: return
        db_result = self.query.execute("select * from materials where materials.id = ?", [result]).fetchone()
        if db_result:
            price, price_2 = self.get_material_price(row.cells)
            if re.match("^\d+?\.\d+?$", str(price)) is None:
                pass
            if not price:
                print('error update materials with id {}'.format(db_result[0]))
                return
            result = self.query.execute('update materials set price_vacantion = ? where materials.id = ?',
                                        (price, db_result[0]))
            if not result:
                print('error update materials with id {}'.format(db_result[0]))
            return
        return
