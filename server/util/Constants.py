from operator import lt, le, eq, ne, ge, gt, and_, or_
class Constants(list):

    logical_operators = {'and': and_, 'or': or_}
    mathematical_operators = {'>': gt, '=': eq, '<':lt, '>=': ge, '<=': le,'!=': ne}

