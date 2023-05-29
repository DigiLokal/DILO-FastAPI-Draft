def check_username_exist(
        username:str
) -> str:
    QUERY = f"""
    SELECT  COUNT(*)
    FROM    public.user
    WHERE   username = '{username}'
    """

    return QUERY

def login_query(
        username: str,
        password: str
) -> str:
    QUERY = f"""
    SELECT  COUNT(*)
    FROM    public.user
    WHERE   password = '{password}'
            AND username = '{username}'
    """

    return QUERY

def register_query(
        user_id: str,
        username: str,
        password: str,
        email: str
) -> str:
    QUERY = f"""
    INSERT INTO public.user 
    (id, username, email, password) 
    VALUES 
    ('{user_id}', '{username}', '{email}', '{password}')
    """

    return QUERY