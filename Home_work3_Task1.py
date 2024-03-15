import re
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value    

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Birthday(Field):
    def __init__(self, value: str) -> None:
        if self.__is_valid_date(value):
            super().__init__(value)
        else:
            raise ValueError("Date must be in format dd.mm.yyyy")

    def __is_valid_date(self, value) -> bool:
        pattern = r'^\d{2}\.\d{2}\.\d{4}$'
        if re.match(pattern, value):
            return True
        return False

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) < 10 or len(value) > 13:
            raise ValueError("Phone number must be a 10-digit number.")
        super().__init__(value)
        
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday: Birthday = None    
        
    def add_phone(self, phone):
        self.phones.append(Phone(phone))    
        
    def delete_phone(self, phone):
        temp_list=[]
        for i in self.phones:
            if i.value != phone:
                temp_list.append(i.value)
        self.phones=temp_list
        print("phone -",phone,"is deleted in contact -", self.name)
    
    def change_phone(self, phone_old, phone_new):
        self.delete_phone(phone_old)
        self.add_phone(phone_new)
        print("phone changed in contact -", self.name)    
    
    def find_phone(self, phone):
        for i in self.phones:
            if i.value == phone:
                return i
        return None    

    def add_birthday(self, birthday_n):
        self.birthday=(Birthday(birthday_n))


    def __str__(self):
        phone_s='; '.join(str(p) for p in self.phones)
        birthday_s=f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phone_s}{birthday_s}"



class AddressBook:
    def __init__(self):
        self.data = {}    
    
    def add_record(self, record):
        self.data[record.name.value] = record    

    def delete(self, name):
        if name in self.data:
            del self.data[name]    
    
    def find(self, name):
        return self.data.get(name)    
    
    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

    def get_birthdays_per_week(self):
        today = datetime.today().date()
        current_day = today.weekday()
        birthdays = {i: [] for i in range(7)}
        for record in self.data.values():
            if record.birthday:
                birthday = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
                birthday_this_year = birthday.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                delta_days = (birthday_this_year - today).days
                birthday_weekday = (today + timedelta(days=delta_days)).weekday()
                if delta_days <= current_day:
                    birthday_weekday = (birthday_weekday + 1) % 7
                birthdays[birthday_weekday].append(record.name.value)

        for day, names in birthdays.items():
            day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][day]
            if names:
                print(f"{day_name}: {', '.join(names)}")


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func): #декоратор для перевірки помилок в командах
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Enter actual key"
        except IndexError:
            return "Do not have user on this position"
    return inner

@input_error
def add_contact(args, contacts):
    name, phone = args
    record=Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return "Contact added."

@input_error #зстосування декоратора для перевірки правильності введення даних
def change_username_phone(args, contacts):
    name, phone_new = args
    record = contacts.find(name)
    if record:
        record.add_phone(phone_new)
    return "Contact changed."

def add_birthday(args, contacts):
    name, birthday=args
    record=contacts.find(name)
    if record:
        record.add_birthday(birthday)
        return "birthday added for name"
    else: return "Contact not found"

def show_birthday(args, contacts):
    name=args[0]
    record=contacts.find(name)
    if record and record.birthday:
        return f"{name} have birthday on {record.birthday}"
    elif record:
        return f"{name} does not have a birthday set"
    else: return f"Contact {name} not found"

def get_birthdays_per_week(contacts):
    contacts.get_birthdays_per_week()
    return ""


def main():
    contacts = {}
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_username_phone(args, book))
        elif command == "all": #потрібно ще попрацювати над цим в залежності, що буде відображати
            print(book)
        elif command == "phone":
            for name in args:
                print(name, ":", contacts.get(name))
        elif command == "add-birthday":
            print(add_birthday(args,book))
        elif command=="show-birthday":
            print (show_birthday(args, book))
        elif command=="birthdays":
            print (get_birthdays_per_week(book))
        elif command == "commands":
            print("all commands: hello - hello\n, add - add new contact to Adress book\n, change, all, phone, commands")
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

