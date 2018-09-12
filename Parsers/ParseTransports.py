

class ParseTransports:
    def __init__(self, query):
        self.query = query

    def run(self, table):
        rows = table.rows
        prefix = ''.join(rows[0].cells[0].text.strip())
        if len(rows[0].cells) == 4:
            for row in rows:
                for cell in range(0, len(row.cells), 2):

