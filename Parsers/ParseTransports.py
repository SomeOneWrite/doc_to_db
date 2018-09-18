from Helpers import to_float, without_whitespace


class ParseTransports:
    def __init__(self, query):
        self.query = query

    def create_or_update(self, table_name, dict, where_dict):
        select_sql = 'select * from ' + table_name + ' where ' + \
                     ', '.join(["%s = %s" % (column, data) for column, data in dict.items()]) + \
                     ' where ' + \
                     ', '.join(["%s = %s" % (column, data) for column, data in where_dict.items()])
        res = self.query.execute(select_sql)
        return

    def run(self, table):
        rows = table.rows
        prefix = 'ТССЦпг' + without_whitespace(rows[0].cells[0].text)
        if len(rows[0].cells) == 4:
            for row in range(1, len(rows)):
                id = prefix + '-01' + without_whitespace(rows[row].cells[0].text)
                id_2 = prefix + '-02' + without_whitespace(rows[row].cells[0].text)
                price_1 = to_float(rows[row].cells[2].text)
                price_2 = without_whitespace(rows[row].cells[3].text)
                if price_2 == '-':
                    price_2 = price_1
                else:
                    price_2 = to_float(rows[row].cells[3].text)
                res = self.query.execute('update transports set price = ? where id = ?', [price_1, id]).fetchone()

                res = self.query.execute('update transports set price = ? where id = ?', [price_2, id_2]).fetchone()

        if (len(rows[0].cells) == 6):
            for row in range(1, len(rows)):
                if without_whitespace(rows[row].cells[0].text) == '':
                    continue
                id = prefix + '-01' + without_whitespace(rows[row].cells[0].text)
                id_2 = prefix + '-02' + without_whitespace(rows[row].cells[0].text)
                id_3 = prefix + '-03' + without_whitespace(rows[row].cells[0].text)
                id_4 = prefix + '-04' + without_whitespace(rows[row].cells[0].text)
                lst_ids = [id_2, id_3, id_4]
                price_1 = without_whitespace(rows[row].cells[2].text)
                price_2 = without_whitespace(rows[row].cells[3].text)
                price_3 = without_whitespace(rows[row].cells[4].text)
                price_4 = without_whitespace(rows[row].cells[5].text)
                lst = [price_2, price_3, price_4]
                for price in range(0, len(lst)):
                    if lst[price] == '-':
                        lst[price] = price_1
                    lst[price] = to_float(lst[price])
                    res = self.query.execute('update transports set price = ? where id = ?',
                                             [lst[price], lst_ids[price]]).fetchone()

                price_1 = to_float(price_1)
                res = self.query.execute('update transports set price = ? where id = ?',
                                         [price_1, id]).fetchone()
        # if len(rows[0].cells) == 3:
        #     continue
        # for row in range(1, len(rows)):
        #     id = prefix
        #     price_1 = to_float(rows[row].cells[2].text)
        #
        #     res = self.query.execute('update transports set price = ? where id = ?', [price_1, id]).fetchone()
