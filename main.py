
import commands
import os


def clear_screen():
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)

def print_options(options):
    for shortcut, option in options.items():
        print(f'({shortcut}) {option}')
    print()

def option_choice_is_valid(choice, options):
    return choice in options or choice.upper() in options

def get_option_choice(options):
    choice = input('Choose an option: ')
    while not option_choice_is_valid(choice, options):
        print('Invalid choice')
        choice = input('Choose an option: ')

    return options[choice.upper()]

# repeating prompt
def get_user_input(label, required = True):
    value = input(f'{label}: ') or None
    while required and not value:
        value  = input(f'{label}: ') or None
    return value

def get_github_import_options():
    return {
        'github_username': get_user_input('GitHub username'),
        'preserve_timestamps':
        get_user_input(
            'Preserve timestamps [Y/n]',
            required=False
        ) in {'Y', 'y', None},
    }

#get information of new bookmark
def get_new_bookmark_data():
    return{
        'title': get_user_input('Title'),
        'url': get_user_input('URL'),
        'notes': get_user_input('Notes', required= False),
    }

#get information to delete
def get_bookmark_id_for_deletion():
    return get_user_input('Enter bookmark ID to delete')


def print_bookmarks(bookmarks):
    for bookmark in bookmarks:
        print('\t'.join(
            str(field) if field else ''
            for field in bookmark
        ))

# github API extension: get github username, import stars
# option to preserve timestamps of original stars
# trigger a corresponding command


class Option:
    '''
    print key for user to enter to choose opiton
    print option text
    check if user input matches an option, choose option'''

    def __init__(self, name, command, prep_call = None):
        self.name = name
        self.command = command
        self.prep_call = prep_call  #optional prep step before executing command

    def _handle_message(self, message):
        if isinstance(message, list):
            print_bookmarks(message)
        else:
            print(message)
            
    def choose(self):
        data = self.prep_call() if self.prep_call else None
        print(f'passing data : {data}')
        message = self.command.execute(data) if data else self.command.execute()
        self._handle_message(message)

    def __str__(self):
        return self.name

def loop():

    
    options = {
        'A':Option('Add a bookmark', commands.AddBookmarkCommand(), prep_call = get_new_bookmark_data ),
        'B':Option('List bookmarks by date', commands.ListBookmarksCommand()),
        'T':Option('List bookmarks by title', commands.ListBookmarksCommand(order_by = 'title')),
        'D':Option('Delete a bookmark', commands.DeleteBookmarkCommand(), prep_call= get_bookmark_id_for_deletion),
        'G':Option('Import Github stars', commands.getGSCommand() , prep_call =  get_github_import_options ),
        'Q':Option('Quit', commands.QuitCommand()),
    }

    clear_screen()
    print('Welcome to Bark!')

    print_options(options)

    chosen_option = get_option_choice(options)
    
    clear_screen()
    chosen_option.choose()   # <- ?????


    _ =  input('Press ENTER to return to menu')


if __name__ == '__main__':

    commands.CreateBookmarksTableCommand().execute()

    while True:
        loop()
