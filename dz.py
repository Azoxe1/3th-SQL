import psycopg2

conn = psycopg2.connect(database = 'clients', user = 'postgres', password = '3543')

with conn.cursor()as cur:
    cur.execute("""
                DROP TABLE phone;
                DROP TABLE client;
                """)
    
    cur.execute("""
                CREATE TABLE IF NOT EXISTS client(
                    ID SERIAL PRIMARY KEY,
                    name VARCHAR (60),
                    surname VARCHAR (60),
                    email VARCHAR (100)
                )
                """)
    cur.execute("""
                CREATE TABLE IF NOT EXISTS phone(
                    ID SERIAL PRIMARY KEY,
                    client_id INTEGER NOT NULL REFERENCES client(id),
                    number VARCHAR (60)
                )
                """)
    conn.commit()
    
    def add_client (cursore, name, surname, email):
        cursore.execute("""
                        INSERT INTO client(name, surname, email) VALUES (%s, %s, %s) RETURNING id, name, surname, email;
                        """, (name, surname, email))
        return cur.fetchall()

    def add_phone (cursore, client_id, number):
        cursore.execute("""
                        INSERT INTO phone(client_id, number) VALUES (%s, %s) RETURNING id, client_id, number;
                        """, (client_id, number))
        return cur.fetchall()
    
    def change_info(cursore, id, name, surname, email):
        cursore.execute("""
                        update client SET name =%s, surname=%s, email=%s WHERE id =%s RETURNING id, name, surname, email;
                        """, (name, surname, email, id))
        return cur.fetchall()
    
    def del_phone(cursore, client_id):
        cursore.execute("""
                        DELETE FROM phone WHERE client_id =%s;
                        """, (client_id, ))
        cursore.execute("""
                SELECT * FROM phone;
                """)
        return cur.fetchall()
    
    def del_client (cursore, id):
        cursore.execute("""
                        DELETE FROM phone WHERE client_id=%s;
                        """, (id, ))
        cursore.execute("""
                        DELETE FROM client WHERE id =%s;
                        """, (id, ))
        cursore.execute("""
                SELECT * FROM client;
                """)
        return cur.fetchall()
    
    def coop(cursore):
        cursore.execute("""
                SELECT DISTINCT c.name, c.surname, c.email, p.number from phone p
                join client c on c.id = p.client_id;
                """)
        return cur.fetchall()
        
    def find_client(cursor, info):
        for i in coop(cursor):
            for y in i:
                if y == info:
                    return i
    
    
    add_client(cur,'qwe', 'rty', 'qwe@qwe')
    add_client(cur,'iop', 'yui', 'vbnnmnmb@12e') #добавление клиентов
    add_client(cur,'bnm', 'zxc', 'q1q2q3@000')        
        
    add_phone(cur, 1, '456-1231')
    add_phone(cur, 1, '456456-1231')
    add_phone(cur, 2, '456sdfad-1231') #добавление номеров клиентов
    add_phone(cur, 2, '123-123')
    add_phone(cur, 3, '098-098')
            
    change_info(cur, 1, 'cvb', 'bnm', 'uio@ryt') #изменение инфо о клиенте по айди
    
    del_phone(cur, 'указать айди клиента') #удаление номера\номеров клиента по айди
    
    del_client(cur, 'указать айди клиента') #удаление инфо о клиенте по айди
    
    print(find_client(cur, 'rty')) #поиск всей инфо клиента по любым данным
    
conn.close()
