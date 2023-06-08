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
    ON  influencer_card.user_id = "user".id;
    """
    
    return QUERY

def get_all_influencers_query() -> str:
    QUERY = """
    SELECT  "user".id AS user_id
            , "user".username AS user_name
            , "user".email AS user_email
            , city.city AS user_city
            , field_area.type AS user_field_area
    FROM    "user"
    LEFT JOIN   city
    ON  "user".city_id = city.id
    LEFT JOIN   field_area
    ON  "user".field_area_id = field_area.id
    WHERE   "user".tipe = 'Influencer';
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