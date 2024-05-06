def calculation(data_dict:dict):
    if data_dict['fill_depth'] == 18:
        price_pine = (data_dict['fill_length']/100) * (data_dict['fill_width']/100) * 7000 + data_dict['fill_underframe'][1]
        price_larch = (data_dict['fill_length']/100) * (data_dict['fill_width']/100) * 9000 + data_dict['fill_underframe'][1]
        return price_pine,price_larch
    if data_dict['fill_depth'] == 40:
        price_pine = (data_dict['fill_length']/100) * (data_dict['fill_width']/100) * 11000 + data_dict['fill_underframe'][1]
        price_larch = (data_dict['fill_length']/100) * (data_dict['fill_width']/100) * 15000 + data_dict['fill_underframe'][1]
        return price_pine,price_larch

def check_number(phone:str):
    number_phone = [i for i in phone]
    result = all(map(lambda x: True if x.isdigit() and len(number_phone)==11 and number_phone[0] == '7' else False, number_phone))
    return result