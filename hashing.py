import bcrypt

def hashing(plain_text_password):
  return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())

def check_hashing(plain_text_password, hashed_password):
  return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)
