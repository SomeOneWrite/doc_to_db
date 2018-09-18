import re


class ParseMachines:
    def __init__(self, query):
        self.query = query

    def check_machines_key(self, cells):
        cell = cells[0]
        result = re.search(r'(\d\d\d\d\d\d)', cell.text)
        if result:
            return result.group(1)
        return None

    def run(self, row):
        result = self.check_machines_key(row.cells)
        if not result: return
        db_result = self.query.execute("select * from machines where machines.id = ?", [result]).fetchone()
        if db_result:
            price, price_driver = self.get_machine_price(row.cells)
            if not price:
                print('error update machines with id {}, error price'.format(db_result[0]))
                return
            result = self.query.execute('update machines set price = ?, price_driver = ? where machines.id = ?',
                                        (price, price_driver, db_result[0]))
            if not result:
                print('error update machines with id {}, error result'.format(db_result[0]))
            return
        return

    def get_machine_price(self, cells):
        result = None
        for i in range(1, 10):
            if len(cells) - 1 < i:
                break
            unit_str = cells[i].text
            result = re.search(r'(\d{1,6},\d{1,2})\D{1,2}((\d{1,6},\d{1,2})|-)', unit_str)
            if result:
                break
        if not result:
            return None, None
        price = ''.join(result.group(1).split())
        price_driver = ''.join(result.group(2).split())
        price = price.replace(',', '.')
        price_driver = price_driver.replace(',', '.')
        if price_driver == '-':
            price_driver = 0
        try:
            price = float(price)
            price_driver = float(price_driver)
        except Exception as e:
            return None, None
        return price, price_driver
