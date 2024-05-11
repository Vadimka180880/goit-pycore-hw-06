def input_error(func):
    
    def wrapper(*args, **kwargs):                                                   # Декоратор для обробки помилок введення користувача
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError):
            return "Invalid command or argument. Please try again."
    return wrapper

@input_error
def parse_input(user_input):
    parts = user_input.split()                                                      # Розбиваємо введений рядок на окремі частини    
    cmd = parts[0].lower()                                                          # Перший елемент - команда, переводимо його в нижній регістр
    args = parts[1:]                                                                # Решта елементів - аргументи команди
    return cmd, args

import re

@input_error
def add_contact(args, contacts):
    # Додає контакт
    if len(args) != 2:
        return "Give me name and phone, please."
    name, phone = args
    if not re.match(r'^\d+$', phone):                                               # Перевірка, чи номер телефону містить лише цифри
        return "Phone number must contain only digits."
    contacts[name] = phone
    return "Contact added."

@input_error
def search_records(args, contacts):                                                 # Шукає контакти за ім'ям або телефоном    
    if len(args) != 1:
        return "Invalid command. Please provide a name or phone number to search for."
    search_term = args[0]
    matching_contacts = [(name, phone) for name, phone in contacts.items() if re.search(search_term, name) or re.search(search_term, phone)]
    if matching_contacts:
        result = "Matching contacts:\n"
        for name, phone in matching_contacts:
            result += f"{name}: {phone}\n"
        return result
    else:
        return "No matching contacts found."

@input_error
def add_record(args, contacts):                                                     # Додає новий запис    
    if len(args) < 2:
        return "Invalid command. Please provide a name and a phone number for the new record."
    name, phone = args[0], args[1]
    if not re.match(r'^\d+$', phone):                                               # Перевірка, чи номер телефону містить лише цифри
        return "Phone number must contain only digits."
    contacts[name] = phone
    return "Record added."



@input_error
def change_contact(args, contacts):    
    if len(args) != 2:                                                             
        return "Invalid command. Please provide both username and new phone number."    
    name, new_value = args                                                             
    if name in contacts:                                                            
        if re.match(r'^\d+$', new_value):                                           # Перевірка, чи нове значення є номером телефону
            contacts[name] = new_value                                                     
            return "Contact updated."
        else:
            return "Invalid phone number. Please provide a valid phone number for the contact."
    else:
        return f"Contact '{name}' not found."

@input_error
def get_phone(args, contacts):    
    if len(args) != 1:                                                              # Перевіряємо, чи передано один аргумент (ім'я контакту)
        return "Invalid command. Please provide username."    
    name = args[0]                                                                  # Отримуємо ім'я контакту з аргументів
    if name in contacts:                                                            # Перевіряємо, чи ім'я контакту є в словнику     
        return f"Phone number for {name}: {contacts[name]}"                         # Повертаємо номер телефону для зазначеного контакту
    else:
        return f"Contact '{name}' not found."
    
@input_error
def update_phone(args, contacts):    
    if len(args) != 2:                                                             
        return "Invalid command. Please provide both username and new phone number."    
    name, new_phone = args                                                             
    if name in contacts:                                                            
        if re.match(r'^\d+$', new_phone):                                           # Перевірка, чи новий номер телефону містить лише цифри
            contacts[name] = new_phone                                                     
            return "Contact updated."
        else:
            return "Invalid phone number. Please provide a valid phone number for the contact."
    else:
        return f"Contact '{name}' not found."
    
def show_all_contacts(contacts):                                                    # Тут додамо функцію виведення усіх контактів які були записані
    if contacts:
        print("All contacts:")
        for name, phone in contacts.items():
            print(f"{name}: {phone}")
    else:
        print("No contacts found.")

@input_error
def get_all_contacts(contacts):    
    if not contacts:                                                                # Перевіряємо, чи словник контактів не є порожнім
        return "No contacts found."    
    result = "Contacts:\n"                                                          # Формуємо рядок з усіма контактами та їх номерами телефонів
    for name, phone in contacts.items():
        result += f"{name}: {phone}\n"
    return result

def show_available_commands():                                                      # Зформуємо список комад
    print("Available commands:")
    print("hello - Greet the bot")
    print("add <name> <phone> - Add a new contact")
    print("change <name> <phone> - Change the phone number of an existing contact")
    print("phone <name> - Get the phone number of a contact")
    print("all_contacts - Show all saved contacts")
    print("close/exit - Close the bot")
    print("search_records - Search contacts")
    print("add_record - Add contacts")

def main():    
    address_book = AddressBook()                                                    # Ініціалізуємо адресну книгу
    print("Welcome to the assistant bot!")
    while True:        
        user_input = input("Enter a command: ")                                     # Запитуємо користувача про команду     
        command, args = parse_input(user_input)                                     # Розбираємо введену команду на команду та аргументи
        
        if command in ["close", "exit"]:
            print("Good bye!")                                                      # Обробляємо команди для виходу з програми
            break
        elif command == "hello":                                                    # Привітання
            print("How can I help you?")
        elif command == "add":                                                      # Додаємо новий запис до адресної книги
            print(add_contact(args, contacts))
        elif command == "change":                                                   # Змінюємо номер телефону контакту
            print(change_contact(args, contacts))
        elif command == "phone":                                                    # Отримуємо номер телефону контакту
            print(get_phone(args, contacts))
        elif command == "all_contacts":                                             # Виведемо усі контакти які були записані            
            show_all_contacts(contacts)
        elif command == "help":                                                     # Покажемо доступні всі команди            
            show_available_commands()
        elif command == "search_records":                                           # Пошук контактів за ім'ям             
            print(search_records(args, contacts))
        elif command == "add_record":                                               # Додавання нового запису            
            print(add_record(args, contacts))
        else:            
            print("Invalid command.")                                               # Якщо команда не відома, виведемо повідомлення про невідому команду

if __name__ == "__main__":
    main()

# Завдяки боту-помічнику, ви матимете зручний інструмент для управління нашими контактами. 
# Ми зможете додавати, змінювати та переглядати інформацію про контакти за допомогою простих команд. 
# Це дозволить нам ефективно організувати наш список контактів та швидко знаходити необхідну інформацію.

class Field:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def set_value(self, value):                                                    # Встановлює значення поля       
        self.value = value

    def get_value(self):                                                           # Повертає значення поля
        return self.value


class Name(Field):
    def __init__(self, name):
        super().__init__("Name", name)


class Phone:
    def __init__(self, phone_number):
        self.value = phone_number
        self.validate_phone()

    def validate_phone(self):                                                      # Перевіряє правильність номера телефону   
        if len(self.value) != 10 or not self.value.isdigit():
            raise ValueError("Phone number must be exactly 10 digits.")

    def set_value(self, phone_number):                                             # Встановлює значення поля та перевіряє його на відповідність формату
        self.value = phone_number        
        self.validate_phone()

    def get_value(self):                                                           # Повертає значення поля    
        return self.value

class Record:
    def __init__(self, name):
        self.name = Name(name)                                                     # Зберігаємо об'єкт Name
        self.phones = []                                                           # Зберігаємо список об'єктів Phone

    def add_phone(self, phone_number):                                             # Додає новий номер телефону  
        try:
            phone = Phone(phone_number)
            self.phones.append(phone)
            return "Phone number added."
        except ValueError as e:
            return str(e)

    def remove_phone(self, phone_number):                                           # Видаляє номер телефону   
        for phone in self.phones:
            if phone.get_value() == phone_number:
                self.phones.remove(phone)
                return "Phone number removed."
        return "Phone number not found."

    def edit_phone(self, old_phone_number, new_phone_number):                       # Редагує номер телефону    
        for phone in self.phones:
            if phone.get_value() == old_phone_number:
                try:
                    phone.set_value(new_phone_number)
                    return "Phone number updated."
                except ValueError as e:
                    return str(e)
        return "Phone number not found."

    def find_phone(self, phone_number):                                             # Шукає номер телефону      
        for phone in self.phones:
            if phone.get_value() == phone_number:
                return "Phone number found."
        return "Phone number not found."

class AddressBook:
    def __init__(self):
        self.data = {}                                                              # Словник для зберігання записів

    def add_record(self, name, phone):                                              # Додає новий запис до адресної книги        
        if name in self.data:
            return "Contact with this name already exists."
        self.data[name] = phone
        return "Contact added."

    def find(self, name):                                                           # Знаходить запис за ім'ям    
        if name in self.data:
            return f"Contact found: {name}: {self.data[name]}"
        else:
            return "Contact not found."

    def delete(self, name):                                                         # Видаляє запис за ім'ям      
        if name in self.data:
            del self.data[name]
            return "Contact deleted."
        else:
            return "Contact not found."