user_input = 'random'
data = []

def show_menu():
    print('Menu:')
    print('1. Add an item')
    print('2. Mark as done')
    print('3. View items')
    print('4. Exit')

while user_input != '4':

    show_menu()
    user_input = input('Enter your choice >>> ')

    if user_input == '1':
        item = input("Add an item: ")
        print('Added an item:', item)
        data.append(item)
    elif user_input == '2':
        item = input('Enter item to be marked as done: ')
        if item in data:
            data.remove(item)
            print('Removed item: ', item)
        else:
            print('Item does not exist in the list')

    elif user_input == '3':
        for item in data:
            print(item)

    elif user_input == '4':
        print('Goodbye')
    else:
        print('Please enter one of 1, 2, 3, or 4')
