import json


class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        with open('stored_data/output.jason', 'w') as f:
            json.dump(self.datas, f)

