def edit_profile_query(username: str, nama: str, detail: str) -> str:
    QUERY = f"""
    UPDATE  "user"
    SET     nama = '{nama}', detail = '{detail}'
    WHERE   username = '{username}';
    """

    return QUERY

def get_profile_query(username: str) -> str:
    QUERY = f"""
    SELECT  username
            , email
            , nama
            , detail
            , tipe
            , field_area.type
    FROM    "user"
    LEFT JOIN   field_area
    ON  "user".field_area_id = field_area.id
    WHERE   username = '{username}'   
    """

    return QUERY