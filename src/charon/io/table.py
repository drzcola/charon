from rich.table import Table


def build_table(*columns: str) -> Table:
    table = Table(border_style="#34ebc3", header_style="#4a9eff bold")
    for column in columns:
        table.add_column(column)
    return table
