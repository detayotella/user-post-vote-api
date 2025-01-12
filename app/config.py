from pydantic_settings import BaseSettings, SettingsConfigDict 

class Settings(BaseSettings): 
    db_host: str 
    db_name: str 
    db_user: str
    db_port: str
    db_password: str 
    secret_key: str
    algorithm: str 
    access_token_expire_minutes: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()