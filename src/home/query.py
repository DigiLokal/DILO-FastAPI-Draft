def get_all_services_query() -> str:
    QUERY = """
    SELECT  influencer_card.id AS service_id
        , influencer_card.user_id AS influencer_id
        , "user".username AS influencer_username
        , influencer_card.nama AS title
        , influencer_card.detail AS description
        , content_type.content AS category
        , influencer_card.harga AS price
        , content_type.social_media AS platform
    FROM    influencer_card
    LEFT JOIN   content_type
    ON  influencer_card.content_type_id = content_type.id
    LEFT JOIN   "user"
    ON  influencer_card.user_id = "user".id
    WHERE   "user".tipe = 'Influencer'
            AND count <= 20;
    """
    
    return QUERY

def get_all_influencers_query() -> str:
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
            AND count <= 20;
    """
    
    return QUERY

def get_influencer_services_query(username: str) -> str:
    QUERY = f"""
    SELECT  influencer_card.id AS service_id
        , influencer_card.user_id AS influencer_id
        , "user".username AS influencer_username
        , influencer_card.nama AS title
        , influencer_card.detail AS description
        , content_type.content AS category
        , influencer_card.harga AS price
        , content_type.social_media AS platform
    FROM    influencer_card
    LEFT JOIN   content_type
    ON  influencer_card.content_type_id = content_type.id
    LEFT JOIN   "user"
    ON  influencer_card.user_id = "user".id
    WHERE   "user".username = '{username}';
    """
    
    return QUERY