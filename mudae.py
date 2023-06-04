def processMudae(content,fromUser,connection):
    cursor = connection.cursor()
    cursor.nextset()
    cursor.execute("USE notaweeb")
    if content[:2] == "r ":
        username = content[2:]
        query = f"""
            SELECT id
            FROM player
            WHERE name = '{username}'
        """
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return "id是别人的了", "text"
        if "lmz" in username or "李明之" in username:
            return "差不多得了😅", "text"
        if len(username)>16:
            return "……你这名字是不是有点长了","text"
        else:
            insert_player_query = f"INSERT INTO player (name,wechat_user) VALUES ('{username}','{fromUser}')"
            cursor.execute(insert_player_query)
            connection.commit()
            return f"{username}你好","text"
    query = f"""
        SELECT *
        FROM player
        WHERE wechat_user = '{fromUser}'
    """
    cursor.execute(query)
    result = cursor.fetchone()

    if not result:
        return "玩之前要先注册辣，\n注册格式是：$r 君の名", "text"
    else:
        userid, username, wechat_id, hanging = result
    if content[:3] == "im ":
        return im(connection,content[3:])
    elif content[0] == 'w':
        return w(connection,userid)
    elif content[:7] == "divorce":
        return divorce(connection,userid,content[8:])
    elif content[:2] == "mm":
        return mm(connection,userid)
    elif content[:5] == "claim":
        return claim(connection,userid)
    else:
        return "前面的功能以后再来探索吧","text"

def im(connection,content):
    cursor = connection.cursor()
    cursor.nextset()
    cursor.execute("USE notaweeb")
    if content.split()[-1].isdigit():
        name = ' '.join(content.split()[:-1])
        print(name)
        index = content.split()[-1]
        query = f"""
            SELECT image_id
            FROM image
            WHERE owner_id = (
                SELECT id
                FROM waifu
                WHERE name = '{name}'
            )
            LIMIT 1
            OFFSET {index}
        """
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            return "Not Found", "text"
        else:
            return result[0], "image"
    else:
        name = content
        query = f"""
            SELECT *
            FROM waifu
            WHERE name = '{name}'
        """
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            return "Not Found", "text"
        id, name, series, marry = result
        if marry:
            marry_query = f"""
                SELECT name
                FROM player
                WHERE id = {marry}
            """
            cursor.execute(marry_query)
            married_by = cursor.fetchone()[0]
            return f"{name}\nfrom {series}\nMarried by {married_by}", "text"
        else:
            return f"{name}\nfrom {series}", "text"

def w(connection,roller):
    cursor = connection.cursor()
    cursor.nextset()
    cursor.execute("USE notaweeb")
    waifu_query = """
        SELECT * FROM waifu ORDER BY RAND() LIMIT 1
    """
    cursor.execute(waifu_query)
    waifu_id, waifu_name, _, owner = cursor.fetchone()
    update_query = f"""
        UPDATE player
        SET curr_roll = {waifu_id}
        WHERE id = {roller}
    """
    cursor.execute(update_query)
    connection.commit()

    image_query = f"""
        SELECT image_id
        FROM image
        WHERE owner_id = {waifu_id}
        ORDER BY RAND()
        LIMIT 1
    """
    cursor.execute(image_query)
    result = cursor.fetchone()[0]
    return result, "image"

def claim(connection, userid):
    cursor = connection.cursor()
    cursor.nextset()
    cursor.execute("USE notaweeb")
    user_query = f"""
        SELECT name, curr_roll
        FROM player
        WHERE id = {userid}
    """
    cursor.execute(user_query)
    username, curr_roll = cursor.fetchone()
    if curr_roll == 0:
        return "你还没roll捏","text"
    waifu_query = f"""
        SELECT id, name, married_by
        FROM waifu
        WHERE id = {curr_roll}
    """
    cursor.execute(waifu_query)
    result = cursor.fetchone()
    waifu_id, waifu_name, waifu_marry = result
    print(result)
    if waifu_marry:
        marry_query = f"""
            SELECT name
            FROM player
            WHERE id = {waifu_marry}
        """
        cursor.execute(marry_query)
        ntr = cursor.fetchone()
        if ntr==username:
            return "已经是你的人辣","text"
        else:
            return f"已经是{ntr}的人辣","text"
    else:
        marry_query = f"""
            UPDATE waifu
            SET married_by = {userid}
            WHERE id = {waifu_id}
        """
        cursor.execute(marry_query)
        marry_query = f"""
            UPDATE player
            SET curr_roll = NULL
            WHERE id = {userid}
        """
        cursor.execute(marry_query)
        connection.commit()
        return f"{username} and {waifu_name} are married!","text"

def divorce(connection,userid,name):
    cursor = connection.cursor()
    cursor.nextset()
    cursor.execute("USE notaweeb")
    waifu_query = f"""
        SELECT id, name, married_by
        FROM waifu
        WHERE name = '{name}'
    """
    cursor.execute(waifu_query)
    result = cursor.fetchone()
    if not result:
        return "❌", "text"
    waifu_id, waifu_name, waifu_marry = result
    if waifu_marry!=userid:
        return "❌", "text"
    else:
        div_query = f"""
            UPDATE waifu
            SET married_by = NULL
            WHERE id = {waifu_id}
        """
        cursor.execute(div_query)
        connection.commit()
        return "✔","text"

def mm(connection, userid):
    cursor = connection.cursor()
    cursor.nextset()
    cursor.execute("USE notaweeb")
    harem_query = f"""
        SELECT name
        FROM waifu
        WHERE married_by = {userid}
    """
    cursor.execute(harem_query)
    waifu_names = cursor.fetchall()
    if not waifu_names:
        return "空的","text"
    name_list = []
    for waifu_name in waifu_names:
        name_list.append(waifu_name[0])
    return '\n'.join(name_list),"text"