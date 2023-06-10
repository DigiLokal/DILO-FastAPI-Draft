def ml_model_data_query() -> str:
    QUERY = """
    WITH
        user_have_instagram AS (
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

    SELECT  "user".count AS "User ID"
            , city.city AS "City"
            , field_area.type AS "Field"
            , CASE
                WHEN "user".id IN (SELECT user_id FROM user_have_instagram)
                THEN 1
                ELSE 0
            END AS is_have_instagram
            , CASE
                WHEN "user".id IN (SELECT user_id FROM user_have_twitter)
                THEN 1
                ELSE 0
            END AS is_have_twitter
            , CASE
                WHEN "user".id IN (SELECT user_id FROM user_have_tiktok)
                THEN 1
                ELSE 0
            END AS is_have_tiktok
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
    """
    return QUERY

def ml_recommendation_data_query(
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

    SELECT  "user".count AS "User ID"
            , city.city AS "City"
            , field_area.type AS "Field"
            , CASE
                WHEN "user".id IN (SELECT user_id FROM user_have_instagram)
                THEN 1
                ELSE 0
            END AS is_have_instagram
            , CASE
                WHEN "user".id IN (SELECT user_id FROM user_have_twitter)
                THEN 1
                ELSE 0
            END AS is_have_twitter
            , CASE
                WHEN "user".id IN (SELECT user_id FROM user_have_tiktok)
                THEN 1
                ELSE 0
            END AS is_have_tiktok
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

def get_list_of_recommendations(
        user_ids: list
) -> str:
    QUERY = f"""
    WITH
        user_have_instagram AS (
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
            AND "user".count IN {user_ids};
    """
    return QUERY

def check_user_has_liked(
        username:str
) -> str:
    QUERY = f"""
    SELECT  COUNT(*)
    FROM    public.user_likes
    WHERE   "user" = '{username}'
    """

    return QUERY