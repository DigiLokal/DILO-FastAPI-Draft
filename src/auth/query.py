def check_username_exist_query(
        username:str
) -> str:
    QUERY = f"""
    SELECT  COUNT(*)
    FROM    public.user
    WHERE   username = '{username}'
    """

    return QUERY

def get_umkm_count_query() -> str:
    QUERY = """
    SELECT  jumlah
    FROM    public.user_count
    WHERE   tipe = 'UMKM'
    """

    return QUERY

def update_umkm_count_query() -> str:
    QUERY = """
    UPDATE public.user_count
    SET jumlah = jumlah + 1
    WHERE tipe = 'UMKM'
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
        email: str,
        umkm_count: int
) -> str:
    QUERY = f"""
    INSERT INTO public.user 
    (id, username, email, password, tipe, count) 
    VALUES 
    ('{user_id}', '{username}', '{email}', '{password}', 'UMKM', {umkm_count})
    """

    return QUERY