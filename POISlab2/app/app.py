
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
                        title: "Таблица поездов"
                        elevation: 4
                        pos_hint: {"top": 1}
                        md_bg_color: "#e7e4c0"
                        specific_text_color: "#4a4939"
                        left_action_items:
                            [['menu', lambda x: nav_drawer.set_state("open")]]


        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)
 
            ContentNavigationDrawer:
                ScrollView:
                    MDList:
                        OneLineListItem:
                            text:"Добавление строки"
                            on_release:app.show_string_adding_dialog()
                            

                        OneLineListItem:
                            text:"Удаление строки"
                            on_release:app.show_string_removing_dialog()
            
                        OneLineListItem:
                            text:"Поиск строки"
                            on_release:app.show_string_filtering_dialog()

                        OneLineListItem:
                            text:"Считывание/Сохранение из/в файл(а)"
                            on_release:app.show_reading_writing_file_dialog()
'''

class ContentNavigationDrawer(BoxLayout):
    pass


class POISlab2(MDApp):
    dialog_for_adding = None
    dialog_for_filtering = None
    dialog_for_removing = None
    dialog_for_writing_reading_file = None
    info,info1,error_dialog = None,None,None

    def on_button_press(self, instance_button: MDRaisedButton):
        try:
            {
                "Чтение": self.read_file,
                "Запись": self.write_file,
                "Отмена": self.close_string_adding_dialog,
                "Отмена.": self.close_string_removing_dialog,
                ".Отмена": self.close_string_filtering_dialog,
                ".Отмена.": self.close_reading_writing_file_dialog,
                "Добавить": self.add_row,
                "Попробовать заново": self.close_error_dialog,
                "Поиск": self.search_and_output_rows,
                "Удалить.": self.remove_row,
                "Удалить": self.search_and_delete_rows,
                "Закрыть": self.close_info_dialog,
            }[instance_button.text]()
        except KeyError:
            pass

    def get_rows(self):
        data_temp = self.table.row_data
        data = {}
        data["items"] = []
        for item in data_temp:
            data["items"].append({
                "number": 0 if item[0] == "" else int(item[0]),
                "departure_station": item[1],
                "arrival_station": item[2],
                "date_and_time_of_departure":item[3],
                "date_and_time_of_arrival": item[4],
                "time_in_travel":item[5]
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
                self.table.add_row((item["number"], item["departure_station"],
                                          item["arrival_station"], item["date_and_time_of_departure"],
                                          item["date_and_time_of_arrival"],item["time_in_travel"]))
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
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.on_button_press,
                ),
            ],
        )
        self.error_dialog.open()

    def write_file(self):
        file_name = self.get_for_writing_reading_file_dialog_data()
        with open(file_name["File Name"].text, "w+") as outfile:
            json.dump(self.get_rows(), outfile)
        self.dialog_for_writing_reading_file.dismiss()

    

    def search_and_output_rows(self):
        data = self.get_rows()
        filled_fields = self.get_filtering_dialog_data()
        section_for_search = field_for_search = None
        counter = 0
        self.new_data = []
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
                    ("Номер поезда", dp(90)),
                    ("Станция отправления", dp(45)),
                    ("Станция прибытия", dp(60)),
                    ("Дата и время отправления", dp(60)),
                    ("Дата и время прибытия", dp(60)),
                    ("Время в пути",dp(60)),
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
            height="800dp",
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
            self.table.add_row((item["number"], item["departure_station"],
                                      item["arrival_station"], item["date_and_time_of_departure"], item["date_and_time_of_arrival"],item["time_in_travel"]))
        self.close_string_filtering_dialog()
        self.info_about_deleted_rows(counter)

    def info_about_deleted_rows(self, counter):
        self.info = MDDialog(
            text="Count Of Deleted Rows: " + str(counter),
            buttons=[
                MDFlatButton(
                    text="Закрыть",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.on_button_press,
                ),
            ],
        )
        self.info.open()


    def close_error_dialog(self):
        self.error_dialog.dismiss()

    def close_info_dialog(self):
        self.info.dismiss()

    def close_string_adding_dialog(self):
        self.dialog_for_adding.dismiss()

    def close_string_removing_dialog(self):
        self.dialog_for_removing.dismiss()

    def close_string_filtering_dialog(self):
        self.dialog_for_filtering.dismiss()
    
    def close_reading_writing_file_dialog(self):
        self.dialog_for_writing_reading_file.dismiss()


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
                    ("Номер поезда", dp(90)),
                    ("Станция отправления", dp(45)),
                    ("Станция прибытия", dp(60)),
                    ("Дата и время отправления", dp(60)),
                    ("Дата и время прибытия",dp(60)),
                    ("Время в пути", dp(60)),
                ],
                
            
            )
        screen.add_widget(self.table)
        screen.add_widget(Builder.load_string(KV))

        return screen
    
    def add_row(self):
        item = self.get_adding_dialog_data()
        self.table.add_row((item["number"].text, item["departure_station"].text,
                                  item["arrival_station"].text, item["date_and_time_of_departure"].text,
                                  item["date_and_time_of_arrival"].text,item["time_in_travel"].text))
        self.dialog_for_adding.dismiss()

    def get_adding_dialog_data(self):
        return self.dialog_for_adding.content_cls.ids
    
    def get_filtering_dialog_data(self):
        return self.dialog_for_filtering.content_cls.ids

    def get_for_writing_reading_file_dialog_data(self):
        return self.dialog_for_writing_reading_file.content_cls.ids
    
    def remove_row(self):
        if len(self.table.row_data) > 0:
            self.table.remove_row(self.table.row_data[-1])

    
    def show_string_adding_dialog(self):

        if not self.dialog_for_adding:
            self.dialog_for_adding = MDDialog(
                 title = 'Новая запись',
        type = 'custom',
        content_cls = MDBoxLayout(
            MDTextField(
                id = 'number',
                hint_text="Номер поезда",
                font_size='20',
                max_text_length = 10,
            ),
            MDTextField(
                id = 'departure_station',
                hint_text="Станция отправления",
                font_size='20',
                max_text_length = 50,
            ),
            MDTextField(
                id = 'arrival_station',
                hint_text="Станция прибытия",
                font_size='20',
                max_text_length = 50,
            ),
            MDTextField(
                id = 'date_and_time_of_departure',
                hint_text="Дата и время отправления",
                font_size='20',
                max_text_length = 50,
            ),
            MDTextField(
                id = 'date_and_time_of_arrival',
                hint_text="Дата и время прибытия",
                font_size='20',
                max_text_length = 50,
            ),
            MDTextField(
                id = 'time_in_travel',
                hint_text="Время в пути",
                font_size='20',
                max_text_length = 50,
                helper_text= "Поле должно содержать минимум одну строку",
                helper_text_mode= "on_error"
            ),
            orientation="vertical",
            spacing="15dp",
            size_hint_y=None,
            height="470dp"
        ),
        buttons=[
            MDFlatButton(
                text="Отмена",
                font_style = 'Button',
                font_size='17',
                on_release = self.on_button_press,
            ),
            MDRaisedButton(
                text="Добавить",
                font_size='17',
                md_bg_color = 'gray',
                font_style = 'Button',
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
                    text="Отмена.",
                    font_style = 'Button',
                    font_size='17',
                    on_release = self.on_button_press
                ),
                MDRaisedButton(
                    text="Удалить.",
                    font_size='17',
                    md_bg_color = 'gray',
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
                id = 'number',
                hint_text="Номер поезда",
                font_size='20',
                max_text_length = 10,
                helper_text= "Поле должно содержать минимум одну цифру",
                helper_text_mode= "on_error"
            ),
            MDTextField(
                id = 'departure_station',
                hint_text="Станция отправления",
                font_size='20',
                max_text_length = 50,
                helper_text= "Поле должно содержать хотя бы одну строку",
                helper_text_mode= "on_error"
            ),
            MDTextField(
                id = 'arrival_station',
                hint_text="Станция прибытия",
                font_size='20',
                max_text_length = 50,
                helper_text= "Поле должно содержать хотя бы одну строку",
                helper_text_mode= "on_error"
            ),
            MDTextField(
                id = 'date_and_time_of_departure',
                hint_text="Дата и время отправления",
                font_size='20',
                max_text_length = 50,
                helper_text= "Поле должно содержать минимум одну дату",
                helper_text_mode= "on_error"
            ),
            MDTextField(
                id = 'date_and_time_of_arrival',
                hint_text="Дата и время прибытия",
                font_size='20',
                max_text_length = 50,
                helper_text= "Поле должно содержать минимум одну дату",
                helper_text_mode= "on_error"
            ),
            MDTextField(
                id = 'time_in_travel',
                hint_text="Время в пути",
                font_size='20',
                max_text_length = 50,
                helper_text= "Поле должно содержать минимум одну строку",
                helper_text_mode= "on_error"
            ),
            orientation="vertical",
            spacing="15dp",
            size_hint_y=None,
            height="470dp"
        ),
            buttons=[
                MDFlatButton(
                    text=".Отмена",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.on_button_press,
                ),
                MDFlatButton(
                    text="Поиск",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.on_button_press,
                ),
                MDFlatButton(
                    text="Удалить",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.on_button_press,
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
                    text=".Отмена.",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.on_button_press,
                ),
                MDFlatButton(
                    text="Чтение",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.on_button_press,
                ),
                MDFlatButton(
                    text="Запись",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.on_button_press,
                )
            ],
        )
        self.dialog_for_writing_reading_file.open()


a = POISlab2()
a.run()
