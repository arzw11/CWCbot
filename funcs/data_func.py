import sqlite3

connection = sqlite3.connect('cwc_database.db')
cursor = connection.cursor()

def get_data(value:str):
    cursor.execute(f'SELECT * FROM {value}')
    result = cursor.fetchall()
    return result

class CWCdata:
    def __init__(self,value_data):
        self.value_data = value_data

    def get_data(self):
        cursor.execute(f'SELECT * FROM {self.value_data}')
        result = cursor.fetchall()
        return result
class CWCorders(CWCdata):
    def __init__(self,value_data,page_number,photo_text,name_text,material_text,cover_text,color_text):
        super().__init__(value_data)
        self.page_number = page_number
        self.photo_text = photo_text
        self.name_text = name_text
        self.material_text = material_text
        self.cover_text = cover_text
        self.color_text = color_text
    def get_data(self):
        super().get_data()
    def get_color_wood(self):
        cursor.execute(f"SELECT {self.photo_text} FROM {self.value_data} WHERE page= {self.page_number}")
        result = cursor.fetchone()
        return result[0]
    def get_photo_prev_orders(self):
        cursor.execute(f"SELECT {self.photo_text} FROM {self.value_data} WHERE page= {self.page_number}")
        result = cursor.fetchone()
        return result[0]
    def get_caption_prev_orders(self):
        cursor.execute(f"SELECT {self.name_text},{self.material_text},{self.cover_text},{self.color_text} FROM {self.value_data} WHERE page = {self.page_number}")
        name,material,cover,color = cursor.fetchone()
        result = f"{name}\n\n▪Столешница: {material}\n▪Покрытие: {cover}\n▪Цвет: {color}\n\n📷Фотографии заказчика."
        return result
class CWCcolors(CWCdata):
    def __init__(self,value_data,page_number,photo_text):
        super().__init__(value_data)
        self.page_number = page_number
        self.photo_text = photo_text

    def get_data(self):
        super().get_data()
    def get_color_wood(self):
        cursor.execute(f"SELECT {self.photo_text} FROM {self.value_data} WHERE page= {self.page_number}")
        result = cursor.fetchone()
        return result[0]
class CWCunderframePhoto(CWCdata):
    def __init__(self, value_data):
        super().__init__(value_data)
    def get_underframe_photo(self):
        cursor.execute(f'SELECT * FROM {self.value_data}')
        result = cursor.fetchone()
        return result[0]
    def get_underframe_caption(self):
        result = 'Выберите подстолье или пропустите этот шаг, нажав кнопку «Без подстолья»'
        return result