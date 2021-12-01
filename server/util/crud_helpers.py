import util.constants
from operator import lt, le, eq, ne, ge, gt, and_, or_

def create_conds_lst(lst):
    conditions_lst = []
    conds_lst = []
    conds_index = 0
    sub_lst = []
    operator = ''
    length = len(lst) 
    count = 1
    for i in lst:
        if i in util.constants.logical_operators:
            i_index = lst.index(i)
            conds_lst = lst[conds_index: i_index]
            #print(i)
            operator = i
            #print(conds_lst)
            sub_lst = lst[i_index +1:]
            #print(sub_lst)
            conditions_lst = [conds_lst] + [operator] + create_conds_lst(sub_lst)
            return conditions_lst 
        count = count +1
        if count == length:
            conditions_lst =  [lst]
    return conditions_lst


def evaluate_conditions(lst, record) -> bool:
    result = False
    if type(lst[0]) == list and len(lst) == 1 : 
        lst = lst[0]
        
    if type(lst[0]) != list :
        operation = util.constants.mathematical_operators[lst[1]]
        record_value = record[lst[0]]
        cond_value = lst[2].replace("'", "")
        if type(record_value) != str:
            if cond_value.isnumeric():
                cond_value = float(cond_value)
                
                
        result = operation(record_value,cond_value)
        return result
    
    if type(lst[0]) == list and len(lst) > 1 :   
        
        operation = util.constants.logical_operators[lst[1][0]]
        record_value = lst[0]
        cond_value = lst[2:]
        result = operation(evaluate_conditions(record_value, record), evaluate_conditions(cond_value, record))  
        return result
    
    return result