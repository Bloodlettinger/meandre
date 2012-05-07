SETTINGS
========

Add the following into project's settings::

  CUSTOM_USER_MODEL = 'users.CustomUser'
  AUTHENTICATION_BACKENDS = (
      'users.auth_backend.Backend',
      'django.contrib.auth.backends.ModelBackend',
  )
