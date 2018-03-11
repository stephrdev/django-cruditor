import django_tables2 as tables


class RecordTable(tables.Table):
    name = tables.Column(orderable=False)
    comment = tables.Column(orderable=False)
