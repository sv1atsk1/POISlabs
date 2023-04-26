
from kivy.config import Config
Config.set("graphics", "width", 1820)
Config.set("graphics", "height", 980)
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.anchorlayout import MDAnchorLayout
#from main import *
import json 
import os.path


KV = '''
Screen:

    MDNavigationLayout:

        ScreenManager:

            Screen:

                MDBoxLayout:
                    orientation: 'horizontal'

                    MDTopAppBar:
                        title: "Банковские аккаунты"
                        elevation: 4
                        pos_hint: {"top": 1}
                        md_bg_color: "#00870e"
                        specific_text_color: "#ffffff"
                        left_action_items:
                            [['menu', lambda x: nav_drawer.set_state("open")]]


        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)
 
            ContentNavigationDrawer:
                ScrollView:
                    MDList:
                        OneLineListItem:
                            text:"Добавление кард-аккаунта"
                            on_release:app.show_string_adding_dialog()
                            

                        OneLineListItem:
                            text:"Удаление последнего кард-аккаунта"
                            on_release:app.show_string_removing_dialog()
            
                        OneLineListItem:
                            text:"Поиск кард-аккаунта"
                            on_release:app.show_string_filtering_dialog()

                        OneLineListItem:
                            text:"Считывание/Сохранение из/в файл(а)"
                            on_release:app.show_reading_writing_file_dialog()
                        
                        OneLineListItem:
                            text:"Снятие денег с карты"
                            on_release:app.card_paying_dialog()
                        
                        OneLineListItem:
                            text:"Пополнение баланса телефона"
                            on_release:app.phone_paying_dialog()
'''

class ContentNavigationDrawer(BoxLayout):
    pass

class POISlab2(MDApp):
    dialog_for_adding = None
    dialog_for_filtering = None
    dialog_for_removing = None
    dialog_for_writing_reading_file = None
    info,info1,error_dialog = None,None,None
    dialog_for_paying_phone = None
    dialog_for_withdrawal_by_card = None

    def on_button_press(self, instance_button: MDFlatButton):
        try:
            {
                "Чтение": self.read_file,
                "Запись": self.write_file,
                "Закрыть окно добавления": self.close_string_adding_dialog,
                "Закрыть окно удаления": self.close_string_removing_dialog,
                "Закрыть окно фильтрации": self.close_string_filtering_dialog,
                "Закрыть окно чтения/записи": self.close_reading_writing_file_dialog,
                "Добавить": self.add_row,
                "Попробовать заново": self.close_error_dialog,
                "Поиск": self.search_and_output_rows,
                "Удалить последнюю строку": self.remove_row,
                "Удалить найденную строку": self.search_and_delete_rows,
                "Закрыть": self.close_info_dialog,
                "Закрыть окно.": self.close_phone_paying_dialog,
                "Пополнить баланс телефона": self.phone_paying_function,
                "Закрыть окно": self.close_card_withdrawal_dialog,
                "Снять деньги с карты": self.card_withdraw_function,
            }[instance_button.text]()
        except KeyError:
            pass

    def get_rows(self):
        data_temp = self.table.row_data
        data = {}
        data["items"] = []
        for item in data_temp:
            data["items"].append({
                "FIO": item[0],
                "card_number": item[1],
                "card_expiry_date": item[2],
                "PIN":item[3],
                "CVV": item[4],
                "phone_balance": 0 if item[5] == "" else int(item[5]),
                "card_balance": 0 if item[6] == "" else int(item[6])
            })
        return data
    
    def clear_data_base(self):
        while len(self.table.row_data) > 0:
            self.table.remove_row(self.table.row_data[-1])

    def read_file(self):
        self.clear_data_base() 
        file_name = self.get_for_writing_reading_file_dialog_data()
        if os.path.isfile(file_name["File Name"].text):
            json_file = open(file_name["File Name"].text, "r")
            data_base = json.load(json_file)
            for item in data_base["items"]:
                self.table.add_row((item["FIO"], item["card_number"],
                                          item["card_expiry_date"], item["PIN"],
                                          item["CVV"],item["phone_balance"],item["card_balance"]))
            json_file.close()
            self.dialog_for_writing_reading_file.dismiss()
        else:
            self.error_file_dialog()


    def error_file_dialog(self):
        self.error_dialog = MDDialog(
            text="The File Does Not Exist!",
            buttons=[
                MDFlatButton(
                    text="Попробовать заново",
                    font_style = 'Button',
                    font_size='17',
                    on_release = self.on_button_press,
                ),
            ],
        )
        self.error_dialog.open()

    def write_file(self):
        file_name = self.get_for_writing_reading_file_dialog_data()
        with open(file_name["File Name"].text, "w+") as outfile:
            json.dump(self.get_rows(), outfile,indent='\t')
        self.dialog_for_writing_reading_file.dismiss()

    def phone_paying_dialog(self):
        
        self.dialog_for_paying_phone = MDDialog(
                 title = 'Выберите аккаунт,на котором хотите пополнить телефон и сумму оплаты',
        type = 'custom',
        content_cls = MDBoxLayout(
            MDTextField(
                id = 'number_of_account',
                hint_text="Номер аккаунта",
                font_size='20',
                max_text_length = 5,
            ),
            MDTextField(
                id = 'sum_of_phone_payment',
                hint_text="Сумма оплаты телефона",
                font_size='20',
                max_text_length = 10,
            ),
            orientation="vertical",
                spacing="10dp",
                size_hint_y=None,
                height="130dp",
                width="200dp"
       ),
        buttons=[
            MDFlatButton(
                text="Закрыть окно.",
                font_style = 'Button',
                font_size='12',
                on_release = self.on_button_press,
            ),
            MDFlatButton(
                text="Пополнить баланс телефона",
                font_style = 'Button',
                font_size='12',
                on_release = self.on_button_press,
            ),
        ],
            )
        self.dialog_for_paying_phone.open()



    def card_paying_dialog(self):
        
        self.dialog_for_withdrawal_by_card = MDDialog(
                 title = 'Выберите аккаунт,с которого хотите снять деньги  и сумму',
        type = 'custom',
        content_cls = MDBoxLayout(
            MDTextField(
                id = 'number_of_card_account',
                hint_text="Номер аккаунта",
                font_size='20',
                max_text_length = 5,
            ),
            MDTextField(
                id = 'sum_of_card_withdrawal',
                hint_text="Сумма снятия",
                font_size='20',
                max_text_length = 10,
            ),
            orientation="vertical",
                spacing="10dp",
                size_hint_y=None,
                height="130dp",
                width="200dp"
       ),
        buttons=[
            MDFlatButton(
                text="Закрыть окно",
                font_style = 'Button',
                font_size='12',
                on_release = self.on_button_press,
            ),
            MDFlatButton(
                text="Снять деньги с карты",
                font_style = 'Button',
                font_size='12',
                on_release = self.on_button_press,
            ),
        ],
            )
        self.dialog_for_withdrawal_by_card.open()


    def card_withdraw_function(self):
        data = self.get_rows()
        answers = self.get_card_withdrawal_dialog_data()
        counter = -1
        self.result_data = []
        for field in answers:
            if answers[field].text:
                if field == "number_of_card_account":
                    number_of_account = int(answers[field].text)
                
                elif field == "sum_of_card_withdrawal":
                    sum_of_withdraw = int(answers[field].text)

        for item in data["items"]:
            counter +=1
            for section in item:
                if section == "card_balance" and counter == number_of_account:
                    item[section] = int(item[section] - sum_of_withdraw)
                    self.table.add_row((item["FIO"], item["card_number"],
                                    item["card_expiry_date"], item["PIN"], item["CVV"],item["phone_balance"],item["card_balance"]))
                    self.table.remove_row(self.table.row_data[number_of_account])
                    break
                else:
                    pass

    def phone_paying_function(self):
        data = self.get_rows()
        answers = self.get_phone_paying_dialog_data()
        counter = -1
        self.result_data = []
        for field in answers:
            if answers[field].text:
                if field == "number_of_account":
                    number_of_account = int(answers[field].text)
                
                elif field == "sum_of_phone_payment":
                    sum_of_payment = int(answers[field].text)

        for item in data["items"]:
            counter +=1
            for section in item:
                if section == "phone_balance" and counter == number_of_account:
                    item[section] = int(item[section] + sum_of_payment)
                    self.table.add_row((item["FIO"], item["card_number"],
                                    item["card_expiry_date"], item["PIN"], item["CVV"],item["phone_balance"],item["card_balance"]))
                    self.table.remove_row(self.table.row_data[number_of_account])
                    break
                else:
                    pass
                
    
    def search_and_output_rows(self):
        data = self.get_rows()
        filled_fields = self.get_filtering_dialog_data()
        section_for_search = field_for_search = None
        counter = 0
        self.new_data = []
        for field in filled_fields:
            if filled_fields[field].text:
                section_for_search = field
                if section_for_search == "PIN" or section_for_search == "CVV" or section_for_search == "phone_balance" or section_for_search == "card_balance":
                    field_for_search = int(filled_fields[field].text)
                else:
                    field_for_search = filled_fields[field].text
                break
        for item in data["items"]:
            for section in item:
                if section == section_for_search:
                    if item[section] == field_for_search:
                        self.new_data.append(item)
                        counter += 1
                    else:
                        continue
        self.new_data = [list(i.values()) for i in self.new_data]
        self.counter = counter
        self.close_string_filtering_dialog()
        self.info_about_searched_rows()


    def returned_table(self,new_data):
        return MDAnchorLayout(
            MDDataTable(
                size_hint=(1, 1),
                use_pagination=True,
                rows_num=5,
                width="1600dp",
                height="1000dp",
                column_data=[
                    ("ФИО", dp(70)),
                    ("Номер карты", dp(70)),
                    ("Срок действия карты", dp(50)),
                    ("PIN", dp(30)),
                    ("CVV",dp(30)),
                    ("Баланс телефона",dp(60)),
                    ("Баланс на карте", dp(60)),
                ],
                row_data = new_data
            )
        )
    
    def info_about_searched_rows(self):
        self.info1 = MDDialog(
            title="Result: " + str(self.counter) + " rows found",
            type="custom",
            size_hint_x=None,
            size_hint_y=None,
            height="1000dp",
            width="1800dp",
            content_cls=MDBoxLayout(
                self.returned_table(self.new_data),
                orientation="vertical",
                spacing="15dp",
                size_hint_y=None,
                height="500dp",
                width="1000dp"
            ),
        )
        self.info1.open()

    

    def search_and_delete_rows(self):
        data = self.get_rows()
        filled_fields = self.get_filtering_dialog_data()
        section_for_search = field_for_search = None
        counter = 0
        new_data = {}
        new_data["items"] = []
        for field in filled_fields:
            if filled_fields[field].text:
                section_for_search = field
                if section_for_search == "number":
                    field_for_search = int(filled_fields[field].text)
                else:
                    field_for_search = filled_fields[field].text
                break
        for item in data["items"]:
            for section in item:
                if section == section_for_search:
                    if item[section] == field_for_search:
                        counter += 1
                        continue
                    else:
                        new_data["items"].append(item)
        self.clear_data_base()
        for item in new_data["items"]:
            self.table.add_row((item["FIO"], item["card_number"],
                                      item["card_expiry_date"], item["PIN"], item["CVV"],item["phone_balance"],item["card_balance"]))
        self.close_string_filtering_dialog()
        self.info_about_deleted_rows(counter)

    def info_about_deleted_rows(self, counter):
        self.info = MDDialog(
            text="Count Of Deleted Rows: " + str(counter),
            buttons=[
                MDFlatButton(
                    text="Закрыть",
                    font_style = 'Button',
                    font_size='17',
                    on_release = self.on_button_press,
                ),
            ],
        )
        self.info.open()


    def close_error_dialog(self):
        self.error_dialog.dismiss()

    def close_info_dialog(self):
        self.info.dismiss()

    def close_phone_paying_dialog(self):
        self.dialog_for_paying_phone.dismiss()

    def close_string_adding_dialog(self):
        self.dialog_for_adding.dismiss()

    def close_string_removing_dialog(self):
        self.dialog_for_removing.dismiss()

    def close_string_filtering_dialog(self):
        self.dialog_for_filtering.dismiss()
    
    def close_reading_writing_file_dialog(self):
        self.dialog_for_writing_reading_file.dismiss()

    def close_card_withdrawal_dialog(self):
        self.dialog_for_withdrawal_by_card.dismiss()

    def build(self):
        screen = Screen()
        
        self.theme_cls.theme_style = "Dark"
        self.table = MDDataTable(
                size_hint=(1, 0.95),
                use_pagination=True,
                check = True,
                rows_num = 10,
                pagination_menu_height = 300,
                column_data=[
                    ("ФИО", dp(70)),
                    ("Номер карты", dp(70)),
                    ("Срок действия карты", dp(50)),
                    ("PIN", dp(30)),
                    ("CVV",dp(30)),
                    ("Баланс телефона",dp(60)),
                    ("Баланс на карте", dp(60)),
                ],
                
            )
        screen.add_widget(self.table)
        screen.add_widget(Builder.load_string(KV))

        return screen
    
    def add_row(self):
        item = self.get_adding_dialog_data()
        self.table.add_row((item["FIO"].text, 
                            item["card_number"].text,
                            item["card_expiry_date"].text, 
                            int(item["PIN"].text),
                            int(item["CVV"].text),
                            int(item["phone_balance"].text),
                            int(item["card_balance"].text)))
        self.dialog_for_adding.dismiss()

    def get_adding_dialog_data(self):
        return self.dialog_for_adding.content_cls.ids
    
    def get_phone_paying_dialog_data(self):
        return self.dialog_for_paying_phone.content_cls.ids
    
    def get_card_withdrawal_dialog_data(self):
        return self.dialog_for_withdrawal_by_card.content_cls.ids
    
    def get_filtering_dialog_data(self):
        return self.dialog_for_filtering.content_cls.ids

    def get_for_writing_reading_file_dialog_data(self):
        return self.dialog_for_writing_reading_file.content_cls.ids
    
    def remove_row(self):
        if len(self.table.row_data) > 0:
            self.table.remove_row(self.table.row_data[-1])
            self.dialog_for_removing.dismiss()

    
    def show_string_adding_dialog(self):
        if not self.dialog_for_adding:
            self.dialog_for_adding = MDDialog(
                 title = 'Новая запись',
        type = 'custom',
        content_cls = MDBoxLayout(
            MDTextField(
                id = 'FIO',
                hint_text="ФИО",
                font_size='20',
                max_text_length = 50,
            ),
            MDTextField(
                id = 'card_number',
                hint_text="Номер карты",
                font_size='20',
                max_text_length = 50,
            ),
            MDTextField(
                id = 'card_expiry_date',
                hint_text="Срок действия карты",
                font_size='20',
                max_text_length = 5,
            ),
            MDTextField(
                id = 'PIN',
                hint_text="PIN",
                font_size='20',
                max_text_length = 4,
            ),
            MDTextField(
                id = 'CVV',
                hint_text="CVV",
                font_size='20',
                max_text_length = 3,
            ),
            MDTextField(
                id = 'phone_balance',
                hint_text="Баланс телефона",
                font_size='20',
                max_text_length = 20,
            ),
            MDTextField(
                id = 'card_balance',
                hint_text="Баланс на карте",
                font_size='20',
                max_text_length = 20,
                helper_text= "Поле должно содержать минимум одну строку",
                helper_text_mode= "on_error"
            ),
            orientation="vertical",
            spacing="15dp",
            size_hint_y=None,
            height="570dp"
        ),
        buttons=[
            MDFlatButton(
                text="Закрыть окно добавления",
                font_style = 'Button',
                font_size='17',
                on_release = self.on_button_press,
            ),
            MDFlatButton(
                text="Добавить",
                font_style = 'Button',
                font_size='17',
                on_release = self.on_button_press,
            ),
        ],
            )
        self.dialog_for_adding.open()

    def show_string_removing_dialog(self):
        if not self.dialog_for_removing:
            self.dialog_for_removing = MDDialog(
                title = f'Удалить последнюю запись?',
                buttons=[
                MDFlatButton(
                    text="Закрыть окно удаления",
                    font_style = 'Button',
                    font_size='17',
                    on_release = self.on_button_press,
                ),
                MDFlatButton(
                    text="Удалить последнюю строку",
                    font_size='17',
                    font_style = 'Button',
                    on_release = self.on_button_press,
                ),
            ],
        )
        self.dialog_for_removing.open()

    def show_string_filtering_dialog(self):
        self.dialog_for_filtering = MDDialog(
            title="Заполните одно из полей:",
            type="custom",
            content_cls=MDBoxLayout(
                MDTextField(
                id = 'FIO',
                hint_text="ФИО",
                font_size='20',
                max_text_length = 50,
                helper_text= "Поле должно содержать корректное ФИО пользователя",
                helper_text_mode= "on_error"
            ),
            MDTextField(
                id = 'card_number',
                hint_text="Номер карты",
                font_size='20',
                max_text_length = 50,
                helper_text= "Поле должно содержать корректный номер карты пользователя",
                helper_text_mode= "on_error"
            ),
            MDTextField(
                id = 'card_expiry_date',
                hint_text="Срок действия карты",
                font_size='20',
                max_text_length = 5,
                helper_text= "Поле должно содержать корректный срок действия карты пользователя",
                helper_text_mode= "on_error"
            ),
            MDTextField(
                id = 'PIN',
                hint_text="PIN",
                font_size='20',
                max_text_length = 4,
                helper_text= "Поле должно содержать корректный PIN пользователя",
                helper_text_mode= "on_error"
            ),
            MDTextField(
                id = 'CVV',
                hint_text="CVV",
                font_size='20',
                max_text_length = 3,
                helper_text= "Поле должно содержать корректный CVV пользователя",
                helper_text_mode= "on_error"
            ),
            MDTextField(
                id = 'phone_balance',
                hint_text="Баланс телефона",
                font_size='20',
                max_text_length = 20,
                helper_text= "Поле должно содержать корректный баланс телефона пользователя",
                helper_text_mode= "on_error"
            ),
            MDTextField(
                id = 'card_balance',
                hint_text="Баланс на карте",
                font_size='20',
                max_text_length = 20,
                helper_text= "Поле должно содержать корректный баланс карты пользователя",
                helper_text_mode= "on_error"
            ),
            orientation="vertical",
            spacing="10dp",
            size_hint_y=None,
            height="520dp"
        ),
            buttons=[
                MDFlatButton(
                    text="Закрыть окно фильтрации",
                    font_style = 'Button',
                    font_size='17',
                    on_release = self.on_button_press,
                ),
                MDFlatButton(
                    text="Поиск",
                    font_style = 'Button',
                    font_size='17',
                    on_release = self.on_button_press,
                ),
                MDFlatButton(
                    text="Удалить найденную строку",
                    font_style = 'Button',
                    font_size='17',
                    on_release = self.on_button_press,
                ),
            ],
        )
        self.dialog_for_filtering.open()

    def show_reading_writing_file_dialog(self):
        self.dialog_for_writing_reading_file = MDDialog(
            title="Enter File Name:",
            type="custom",
            content_cls=MDBoxLayout(
                MDTextField(
                    id="File Name",
                    hint_text="File Name",
                ),
                orientation="vertical",
                spacing="8dp",
                size_hint_y=None,
                height="60dp",
            ),
            buttons=[
                MDFlatButton(
                    text="Закрыть окно чтения/записи",
                    font_style = 'Button',
                    font_size='17',
                    on_release = self.on_button_press,
                ),
                MDFlatButton(
                    text="Чтение",
                    font_style = 'Button',
                    font_size='17',
                    on_release = self.on_button_press,
                ),
                MDFlatButton(
                    text="Запись",
                    font_style = 'Button',
                    font_size='17',
                    on_release = self.on_button_press,
                )
            ],
        )
        self.dialog_for_writing_reading_file.open()

a = POISlab2()
a.run()

#if __name__ == "__main__":
    #print("Выберите вариант работы:\n"
          #"1 - Консоль\n"
          #"2 - GUI\n")
    #choice = int(input())
    #if choice == 1:
        #autorization()
    #elif choice == 2:      
    #a = POISlab2()
    #a.run()

