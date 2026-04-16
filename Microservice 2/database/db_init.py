from db_create import create_database
from db_setup import create_table

create_database()
create_table("library_users")
create_table("books")
