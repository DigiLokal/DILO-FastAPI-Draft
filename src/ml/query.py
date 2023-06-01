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

    SELECT  "user".id
            , city.city
            , field_area.type
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
    ON  "user".field_area_id = field_area.id;
    """
    return QUERY