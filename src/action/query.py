def add_order_query(
        id: str,
        username: str,
        service_id: str
) -> str:
    QUERY = f"""
    INSERT INTO public.orders
    (id, username, "order", status)
    VALUES
    ('{id}', '{username}', '{service_id}', '5efa3a56-d2a5-46ce-bdae-792a89bc23cb')
    """
    return QUERY

def add_like_query(
        username: str,
        likes_user: str
) -> str:
    QUERY = f"""
    INSERT INTO public.user_likes
    ("user", likes)
    VALUES
    ('{username}', '{likes_user}')
    """
    return QUERY

def get_order_query(
        username: str
) -> str:
    QUERY = f"""
    SELECT  orders.username AS ordered_by
            , ic.nama
            , ic.detail
            , ic.harga
            , ct.content
            , ct.social_media
            , os.status
    FROM    orders
    LEFT JOIN   influencer_card ic
    ON  orders."order" = ic.id
    LEFT JOIN   order_status os
    ON  orders.status = os.id
    LEFT JOIN   content_type ct
    ON  ic.content_type_id = ct.id
    WHERE   orders.username = '{username}';
    """
    return QUERY

def get_likes_query(
        username: str
) -> str:
    QUERY = f"""
    WITH
        user_liked AS (
            SELECT  likes
            FROM    user_likes
            WHERE   "user" = '{username}'
        )

        , user_have_instagram AS (
            SELECT  user_id
            FROM    socmed_account
            WHERE   social_media = 'Instagram'
        )

        , user_have_twitter AS (
            SELECT  user_id
            FROM    socmed_account
            WHERE   social_media = 'Twitter'
        )

        , user_have_tiktok AS (
            SELECT  user_id
            FROM    socmed_account
            WHERE   social_media = 'Tiktok'
        )

    SELECT  "user".id AS user_id
            , "user".username AS user_name
            , "user".email AS user_email
            , city.city AS user_city
            , field_area.type AS user_field_area
            , CASE
                WHEN "user".id IN (SELECT user_id FROM user_have_instagram)
                THEN (  SELECT  followers
                        FROM    socmed_account
                        WHERE   user_id = "user".id
                                AND social_media = 'Instagram')
                ELSE 0
            END AS num_followers_instagram
            , CASE
                WHEN "user".id IN (SELECT user_id FROM user_have_twitter)
                THEN (  SELECT  followers
                        FROM    socmed_account
                        WHERE   user_id = "user".id
                                AND social_media = 'Twitter')
                ELSE 0
            END AS num_followers_twitter
            , CASE
                WHEN "user".id IN (SELECT user_id FROM user_have_tiktok)
                THEN (  SELECT  followers
                        FROM    socmed_account
                        WHERE   user_id = "user".id
                                AND social_media = 'Tiktok')
                ELSE 0
            END AS num_followers_tiktok
    FROM    "user"
    LEFT JOIN   city
    ON  "user".city_id = city.id
    LEFT JOIN   field_area
    ON  "user".field_area_id = field_area.id
    WHERE   "user".tipe = 'Influencer'
            AND "user".username IN (SELECT likes FROM user_liked);
    """
    return QUERY
