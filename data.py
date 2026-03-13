BASE_URL = 'https://stellarburgers.education-services.ru'
CREATE_USER_URL =       f'{BASE_URL}/api/auth/register'     
DELETE_USER_URL =       f'{BASE_URL}/api/auth/user'         
LOGIN_USER_URL =        f'{BASE_URL}/api/auth/login'        
UPDATE_USER_DATA_URL =  f'{BASE_URL}/api/auth/user'         
CREATE_ORDER_URL =      f'{BASE_URL}/api/orders'            
GET_ORDER_URL =         f'{BASE_URL}/api/orders'            
GET_INGREDIENTS_URL =   f'{BASE_URL}/api/ingredients'       

 
USER_EXISTS =       "User already exists"               
REQUIRED_FIELDS =   "Email, password and name are required fields"
LOGIN_ERROR =       "email or password are incorrect"
AUTH_REQUIRED =     "You should be authorised"
NO_INGREDIENTS =    "Ingredient ids must be provided"


INVALID_ORDER_DATA = [
    (["invalid_hash_1", "invalid_hash_2"], "two_invalid_hashes"),
    ([""], "empty_string_hash"),
    (["invalid_hash_1", "valid_but_wrong_format"], "mixed_invalid_hashes")
]
