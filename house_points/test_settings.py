from .settings import * 

DATABASE = {
    "default" : {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

EMAIL_BAKCEND = 'django.core.mail.backends.locmem.EmailBackend'