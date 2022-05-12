import os

class Config:
  SQLALCHEMY_DATABASE_URI= "sqlite:///Blog.db"
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SECRET_KEY = '9ab803b32301726f09247060e35175'
  
  # To add configuration to environment
  # type the following on the terminal
  
  # export SECRET_KEY='9ab803b32301726f09247060e35175'
  # SQLALCHEMY_DATABASE_URI="sqlite:///music.db"
  
  # THEN WRITE IT HERE AS 
  # SQLALCHEMY_DATABASE_URI= os.environ.get(SQLALCHEMY_DATABASE_URI)
  # SECRET_KEY = os.environ.get(SECRET_KEY)