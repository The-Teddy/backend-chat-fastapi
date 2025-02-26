NAME_REGEX      = r"^[a-zA-ZÀ-ÖØ-öø-ÿ\s]{3,30}$"
USERNAME_REGEX  = r"^[a-zA-Z0-9._]{3,25}$"
EMAIL_REGEX     = r"^[a-zA-Z0-9._-]{3,70}@[a-zA-Z0-9.-]{3,50}\.[a-zA-Z]{2,20}$"
PASSWORD_REGEX  = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%&*()=;?]){8,30}"