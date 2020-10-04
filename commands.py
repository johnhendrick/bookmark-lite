import sys

from database import DatabaseManager
from datetime import datetime


#create object instance as db
db = DatabaseManager('bookmarks.db')

class CreateBookmarksTableCommand:

    def execute(self):
        db.create_table('bookmarks', 
        {
            'id' : 'integer primary key autoincrement',
            'title' : 'text not null',
            'url': 'text not null',
            'notes' : 'text', 
            'date_added' : 'text not null'
        }
        )

#to add bookmark, pass data from presenetation layer to persistence layer

class AddBookmarkCommand:

    def execute(self, data):
        data['date_added'] = datetime.utcnow().isoformat() 
        print(f'passing data : {data}')
        db.add('bookmarks', data)  
        return 'Bookmark added!'  


class ListBookmarksCommand:

    def __init__(self, order_by = 'date_added' ):
        self.order_by = order_by
    
    def execute(self):
        return db.select('bookmarks', order_by = self.order_by).fetchall()

class DeleteBookmarkCommand:

    def execute(self, data): 
        db.delete('bookmarks', {'id': data})
        return 'Bookmark deleted'

class QuitCommand:

    def execute(self):
        sys.exit()
