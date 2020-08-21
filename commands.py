import sys

from database import DatabaseManager



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
from datetime import datetime

class AddBookmarkCommand:

    def __init__(self, content):
        time_now = datetime.utcnow().isoformat()
        content['date_added'] = time_now
        db.add('bokmarks', content)
        return 'Bookmark added!!'

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
