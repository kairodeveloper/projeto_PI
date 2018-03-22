SECRET_KEY = '4v79p)lu=+#vq2t1!^z9=8h=u8oo5mcizw#bgnjaci&=j*w9+1'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'banco_de_dados_aemtkd',
        # 'NAME': os.path.join(BASE_DIR, 'mydb'),
        'USER': 'user_bd_tkd',
        'PASSWORD': 'gn2ps2AME4' ,
        'HOST': '127.0.0.1',
        'PORT': '', # 8000 is default
    }
}
