from flet import *
from datetime import datetime
import csv

current_pointer = 0
data = []
edit_stage = 'edit'
def writeAll_csv(data):
    with open('flash_cards.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
        print('written complete')
        data = read_csv()

def append_to_csv(vocab, definition):
    global current_pointer
    try:
        with open('flash_cards.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if (not vocab) or (not definition):
                print("Vocabulary or definition is empty, skipping write.")
                return
            else :
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([vocab, definition, ts])
                current_pointer += 1
                

    except Exception as e:
        print(f"Error appending to CSV: {e}")

def read_csv():
    global current_pointer, data
    try:
        with open('flash_cards.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Skip header if it exists
            data = [row for row in reader if row and not (row[0] == "Vocabulary" and row[1] == "Definition")]
            if data:
                current_pointer = len(data) - 1
                return data
            else:
                return []
    except FileNotFoundError:
        return []
    except UnicodeDecodeError:
        print("Encoding error - trying alternative approach")
        # Try reading with different encoding if UTF-8 fails
        with open('flash_cards.csv', mode='r', encoding='latin-1') as file:
            reader = csv.reader(file)
            data = [row for row in reader if row and not (row[0] == "Vocabulary" and row[1] == "Definition")]
            return data

def init_csv():
    try:
        with open('flash_cards.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Vocabulary", "Definition", "Timestamp"])
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow(["dog", r"หมา", ts])
            writer.writerow(["cat", r"แมว", ts])
            writer.writerow(["bird", r"นก", ts])
    except Exception as e:
        print(f"Error initializing CSV: {e}")

def main(page: Page):
    global current_pointer 
    global data
    global edit_stage
    current_pointer = 0

    def update_page():
        global data
        data = read_csv()
        current_pointer = len(data)-1
        display.value = data[current_pointer][0] +' = ' + data[current_pointer][1]
        page.update()

    def edit_click(e):
        global data
        global current_pointer
        global edit_stage
        if edit_stage == 'edit':
            edit_stage = 'save'
            btn_edit_save.icon = Icons.SAVE
            vocab.value = data[current_pointer][0]
            definition.value = data[current_pointer][1]
            # print([vocab.value, definition.value,edit_stage, current_pointer])
        elif edit_stage == 'save' :
            edit_stage = 'edit'
            btn_edit_save.icon = Icons.EDIT
            data[current_pointer][0] = vocab.value
            data[current_pointer][1] = definition.value
            # print([vocab.value, definition.value,edit_stage, current_pointer])
            writeAll_csv(data)
            current_pointer = len(data)-1
            update_page()
        else :
            print("the stage not allow check")
            pass
        page.update()

    btn_edit_save = IconButton(icon=Icons.EDIT, on_click=edit_click, width=150)

    def add_card(e):
        data = read_csv()
        esixting_vocab = [row[0].upper() for row in data]
        if vocab.value.upper() not in esixting_vocab:
            append_to_csv(vocab.value.strip(), definition.value.strip())
            vocab.value, definition.value = "", ""
            data = read_csv()
            display.value = data[current_pointer][0] + " : " + data[current_pointer][1]
            page.update()
            return
        else :
            return
    def next_card(e):
        global current_pointer
        if current_pointer + 1 < len(data):
            current_pointer += 1
            display.value = data[current_pointer][0] + " : " + data[current_pointer][1]
            page.update()

    def prev_card(e):
        global current_pointer
        if current_pointer > 0:
            current_pointer -= 1
            display.value = data[current_pointer][0] + " : " + data[current_pointer][1]
            page.update()

    # Initialize only if file doesn't exist
    try:
        with open('flash_cards.csv', 'r', encoding='utf-8'):
            pass
    except FileNotFoundError:
        init_csv()
    except UnicodeDecodeError:
        # If existing file has encoding issues, overwrite it
        init_csv()

    page.title = "Flashcard App"
    page.bgcolor = Colors.BLUE_GREY_50
    page.window.width = 400
    page.window.height = 400
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.CENTER
    data = read_csv()
    display = Text(size=30, width=300)
    display.value = data[current_pointer][0] + " : " + data[current_pointer][1] if data else "No cards available"
    vocab = TextField(label="Enter Vocabulary", autofocus=True, width=300)
    definition = TextField(label="Enter Definition",width=300)
    add_button = ElevatedButton("Add", on_click=add_card, width=150)
    next_button = ElevatedButton("Next", on_click=next_card, width=150)
    prev_button = ElevatedButton("Previous", on_click=prev_card, width=150)

    row1 = Row(spacing=2,controls=[add_button, btn_edit_save],alignment=MainAxisAlignment.CENTER)
    row2 = Row(spacing=2, controls=[prev_button, next_button],alignment=MainAxisAlignment.CENTER)
    page.add(display,vocab, definition, row1, row2 )
    page.update()

app(target=main)
