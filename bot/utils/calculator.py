from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.orm import AsyncOrm

def check_number(phone:str):
    number_phone = [i for i in phone]
    result = all(map(lambda x: True if x.isdigit() and len(number_phone)==11 and number_phone[0] == '7' else False, number_phone))
    return result


async def calculate_price(data: dict, session: AsyncSession):
    length = data['fill_length']
    width = data['fill_width']
    materials = await AsyncOrm.get_all_materials(session=session)
    if int(data['fill_underframe']) != 0:
        result = await AsyncOrm.get_underframe(session=session, underframe_id=data['fill_underframe'])
        underframe = result.price
    else:
        underframe = 0


    price_pine = (length/100) * (width/100) * materials[0].price + underframe
    price_larch = (length/100) * (width/100) * materials[1].price + underframe

    return price_pine, price_larch
    
