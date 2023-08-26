
create_birthday_table = 'create table birthday (id text primary key, day numeric, month numeric, year NUMERIC )'

delete_birthday_table = 'drop table if exists birthday'

create_birthday = "insert into birthday (id, day, month, year ) values (%s, %s, %s, %s)"

update_birthday = "update birthday set month = %s, day = %s, year = %s  where id = '%s'"

delete_birthday = "delete from birthday where id = '%s'"

get_birthday_all = "select * from birthday"

get_birthday_one = "select * from birthday where id = '%s'"
