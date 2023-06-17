def reset(connection):
    cursor = connection.cursor()
    cursor.nextset()
    cursor.execute("USE notaweeb")
    query = """
        UPDATE player
        SET curr_roll=NULL, roll_count=0, claimed=NULL
    """
    cursor.execute(query)
    connection.commit()


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
        userid, username, wechat_id, curr_roll, roll_count, claimed = result
    if content == "h":
        return "非常感谢你使用此公众号！教程文档在：https://www.bilibili.com/read/readlist/rl717702", "text"
    elif content[:3] == "im ":
        return im(connection,content[3:],userid)
    elif content[:4] == "ima ":
        return ima(connection,content[4:],userid)
    elif content == "imr":
        if not curr_roll:
            return "还没roll捏","text"
        return imr(connection,curr_roll,userid)
    elif content == 'w':
        if not roll_count or roll_count<12:
            return w(connection,userid)
        return "（每小时10次，下个小时再来吧）","text"
    elif content[:8] == "divorce ":
        return divorce(connection,userid,content[8:])
    elif content == "mm":
        return mm(connection,userid)
    elif content == "claim":
        if claimed:
            return "（已经claim过了，下个小时再来吧）","text"
        return claim(connection,userid)
    elif content[:3] == "top":
        return top(connection, content)
    elif content[:2] == "d ":
        return ban(connection,content[2:], userid)
    elif content[:2] == "dl":
        return banlist(connection, userid)
    elif content[:3] == "ad ":
        return antiban(connection,content[3:], userid)
    else:
        return "前面的功能以后再来探索吧","text"

def im(connection,content,user_id):
    cursor = connection.cursor()
    cursor.nextset()
    cursor.execute("USE notaweeb")
    harem_query = f"""
        SELECT id
        FROM waifu
        WHERE id IN (SELECT waifu_id FROM marry WHERE user_id = {user_id})
    """
    cursor.execute(harem_query)
    result = cursor.fetchall()
    waifu_list = []
    for waifu_id in result:
        waifu_list.append(waifu_id[0])
    if content.split()[-1][0] == '$':
        name = ' '.join(content.split()[:-1])
        index = int(content.split()[-1][1:])-1
        if index<0:
            return "Not Found", "text"
        query = f"""
            SELECT image_id
            FROM image
            WHERE owner_id IN (
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
        result = cursor.fetchall()
        if not result:
            return "Not Found", "text"
        resultList = []
        for row in result:
            id, name, series = row
            marry_query = f"""
                SELECT count(*)
                FROM marry
                WHERE waifu_id = {id}
            """
            cursor.execute(marry_query)
            married_by = cursor.fetchone()[0]
            if id in waifu_list:
                resultList.append(f"{name}❤ \nfrom {series}\nClaim#：{married_by}")
            elif married_by:
                resultList.append(f"{name}\nfrom {series}\nClaim#：{married_by}")
            else:
                resultList.append(f"{name}\nfrom {series}")
        return "\n\n".join(resultList), "text"

def ima(connection, content,user_id):
    cursor = connection.cursor()
    cursor.nextset()
    cursor.execute("USE notaweeb")
    harem_query = f"""
        SELECT name
        FROM waifu
        WHERE id IN (SELECT waifu_id FROM marry WHERE user_id = {user_id})
    """
    cursor.execute(harem_query)
    result = cursor.fetchall()
    waifu_list = []
    for waifu_name in result:
        waifu_list.append(waifu_name[0])
    if content.split()[-1][0] == '$':
        name = ' '.join(content.split()[:-1])
        index = (int(content.split()[-1][1:])-1)*10
        query = f"""
            SELECT name
            FROM waifu
            WHERE series = '{name}'
            LIMIT 11
            OFFSET {index}
        """
        cursor.execute(query)
        result = cursor.fetchall()
        if not result:
            return "Not found", "text"
        name_list = []
        for waifu_name in result:
            if waifu_name[0] in waifu_list:
                name_list.append(waifu_name[0] + "❤ ")
            else:
                name_list.append(waifu_name[0])

        if len(name_list) > 10:
            return '\n'.join(name_list[:10]), "text"
        else:
            return '\n'.join(name_list), "text"
    else:
        query = f"""
            SELECT name
            FROM waifu
            WHERE series = '{content}'
            LIMIT 11
        """
        cursor.execute(query)
        result = cursor.fetchall()
        if not result:
            return "Not found", "text"
        name_list = []
        for waifu_name in result:
            if waifu_name[0] in waifu_list:
                name_list.append(waifu_name[0]+"❤ ")
            else:
                name_list.append(waifu_name[0])
        if len(name_list)>10:
            return '\n'.join(name_list[:10])+"\n……", "text"
        else:
            return '\n'.join(name_list), "text"

def imr(connection, curr_roll,user_id):
    cursor = connection.cursor()
    cursor.nextset()
    cursor.execute("USE notaweeb")
    harem_query = f"""
        SELECT name
        FROM waifu
        WHERE id IN (SELECT waifu_id FROM marry WHERE user_id = {user_id})
    """
    cursor.execute(harem_query)
    result = cursor.fetchall()
    waifu_list = []
    for waifu_name in result:
        waifu_list.append(waifu_name[0])
    query = f"""
        SELECT *
        FROM waifu
        WHERE id = '{curr_roll}'
    """
    cursor.execute(query)
    result = cursor.fetchone()
    if not result:

        return "Not Found", "text"
    id, name, series = result
    marry_query = f"""
        SELECT count(*)
        FROM marry
        WHERE waifu_id = {id}
    """
    cursor.execute(marry_query)
    married_by = cursor.fetchone()[0]

    if name in waifu_list:
        return f"{name}❤ \nfrom {series}\nClaim#：{married_by}", "text"
    elif married_by:
        return f"{name}\nfrom {series}\nClaim#：{married_by}", "text"
    else:
        return f"{name}\nfrom {series}", "text"

def w(connection,user_id):
    cursor = connection.cursor()
    cursor.nextset()
    cursor.execute("USE notaweeb")
    waifu_query = f"""
        SELECT *
        FROM waifu
        WHERE series NOT IN (
            SELECT series
            FROM ban
            WHERE user_id = {user_id}
        )
        ORDER BY RAND()
        LIMIT 1
    """
    cursor.execute(waifu_query)
    waifu_id, _, waifu_series = cursor.fetchone()
    update_query = f"""
        UPDATE player
        SET curr_roll={waifu_id}, roll_count=roll_count+1
        WHERE id = {user_id}
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
    if not curr_roll:
        return "你还没roll捏","text"
    waifu_query = f"""
        SELECT id, name
        FROM waifu
        WHERE id = {curr_roll}
    """
    cursor.execute(waifu_query)
    result = cursor.fetchone()
    waifu_id, waifu_name = result
    marry_query = f"""
        SELECT *
        FROM marry
        WHERE user_id={userid} AND waifu_id={waifu_id}
    """
    cursor.execute(marry_query)
    result = cursor.fetchone()
    if result:
        return "已经是你的辣","text"
    marry_query = f"""
        INSERT INTO marry (user_id, waifu_id)
        VALUES ({userid},{waifu_id})
    """
    cursor.execute(marry_query)
    claim_query = f"""
        UPDATE player
        SET claimed = {waifu_id}
        WHERE id = {userid}
    """
    cursor.execute(claim_query)
    connection.commit()

    return f"{username} and {waifu_name} are married!","text"

def divorce(connection,userid,name):
    cursor = connection.cursor()
    cursor.nextset()
    cursor.execute("USE notaweeb")
    waifu_query = f"""
        SELECT id, name
        FROM waifu
        WHERE name = '{name}'
    """
    cursor.execute(waifu_query)
    result = cursor.fetchone()
    if not result:
        return "❌", "text"
    waifu_id, waifu_name = result
    div_query = f"""
        DELETE FROM marry
        WHERE waifu_id={waifu_id} AND user_id={userid}
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
        WHERE id IN (SELECT waifu_id FROM marry WHERE user_id = {userid})
    """
    cursor.execute(harem_query)
    waifu_names = cursor.fetchall()
    if not waifu_names:
        return "空的","text"
    name_list = []
    for waifu_name in waifu_names:
        name_list.append(waifu_name[0])
    return '\n'.join(name_list),"text"

def top(connection, content):
    cursor = connection.cursor()
    cursor.nextset()
    cursor.execute("USE notaweeb")
    if content.split()[-1][0] == '$':
        index = int(content.split()[-1][1:])
    else:
        index = 10
    if index<0:
        return "❌","text"
    query = f"""
        SELECT w.name, w.series, COUNT(*) as c
        FROM waifu w JOIN marry m ON w.id=m.waifu_id
        GROUP BY w.name, w.series
        ORDER BY c DESC
        LIMIT {index}
    """
    cursor.execute(query)
    result = cursor.fetchall()
    if not result:
        return "Not found", "text"
    name_list = []
    index = 1
    for waifu_name, series, c in result:
        name_list.append(str(index)+'. '+waifu_name)
        index += 1
    return '\n'.join(name_list), "text"

def ban(connection, content, user_id):
    cursor = connection.cursor()
    cursor.nextset()
    cursor.execute("USE notaweeb")
    series_query = f"""
        SELECT series
        FROM waifu
        WHERE series = '{content}'
    """
    cursor.execute(series_query)
    result = cursor.fetchone()
    if not result:
        return "该系列不存在","text"
    else:
        series = result[0]
    ban_query = f"""
        SELECT series
        FROM ban
        WHERE user_id = '{user_id}'
    """
    cursor.execute(ban_query)
    result = cursor.fetchall()
    if len(result)>=2:
        return "超出禁用上限","text"
    for row in result:
        if row[0]==series:
            return "✔","text"
    insert_ban = f"""
        INSERT INTO ban (user_id, series)
        VALUES ({user_id}, '{series}')
    """
    print(insert_ban)
    cursor.execute(insert_ban)
    connection.commit()
    return "✔","text"

def banlist(connection, userid):
    cursor = connection.cursor()
    cursor.nextset()
    cursor.execute("USE notaweeb")
    ban_query = f"""
        SELECT series
        FROM ban
        WHERE user_id = {userid}
    """
    cursor.execute(ban_query)
    result = cursor.fetchall()
    if not result:
        return "空的","text"
    name_list = []
    for row in result:
        name_list.append(row[0])
    return '\n'.join(name_list), "text"

def antiban(connection, content, userid):
    cursor = connection.cursor()
    cursor.nextset()
    cursor.execute("USE notaweeb")
    ban_query = f"""
        SELECT id
        FROM ban
        WHERE user_id={userid} AND series='{content}'
    """
    cursor.execute(ban_query)
    result = cursor.fetchone()
    if not result:
        return "❌","text"
    ban_delete = f"""
        DELETE FROM ban
        WHERE user_id={userid} AND series='{content}'
    """
    cursor.execute(ban_delete)
    connection.commit()
    return "✔","text"


