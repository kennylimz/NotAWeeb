def processMudae(content,fromUser,connection):
    cursor = connection.cursor()
    cursor.nextset()
    cursor.execute("USE notaweeb")
    if content[:3] == "im ":
        return im(content[3:],cursor)
    elif content[0] == 'w':
        return w(cursor)
    else:
        return "Feature not implemented"

def im(name,cursor):
    query = f"""
        SELECT image_id
        FROM image
        WHERE owner_id = (
            SELECT id
            FROM waifu
            WHERE name = '{name}'
        )
        ORDER BY RAND()
        LIMIT 1
    """
    cursor.execute(query)
    result = cursor.fetchone()[0]
    if not result:
        return "Not Found", "text"
    else:
        return result, "image"

def w(cursor):
    query = """
        SELECT image_id
        FROM image
        WHERE owner_id IN (
            SELECT id, name FROM person ORDER BY RAND() LIMIT 1
        )
        ORDER BY RAND()
        LIMIT 1
    """
    cursor.execute(query)
    result = cursor.fetchone()[0]
    if not result:
        return "Not Found", "text"
    else:
        return result, "image"