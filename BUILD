package(default_visibility = ["//visibility:public"])

load("@my_deps//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary")


_REQ = [
        "asgiref",
        "django==3.0.7",             # via -r requirements.in (line 1)
        "gevent",             # via gunicorn
        "greenlet",          # via gevent
        # Gunicorn
        "gunicorn",  # via -r requirements.in (line 2)
        "python-dotenv",     # via -r requirements.in (line 3)
        "pytz",             # via django
        "sqlparse",           # via django
        "psycopg2-binary",
        "psycopg2",
        "pyopenssl",
        "Werkzeug",
        #Misc
        'django_extensions',
        # Django related packages
        "django-model-utils",
        "django-phonenumber-field",
        "phonenumbers",
        "social-auth-app-django",

        # Tests and Fixtures
        "factory-boy",
        "snapshottest",

        # Misc
        "pycountry",
        "openpyxl",
        "xlrd",
        "ipdb",

        # API
        "graphene-django",
        "django-filter",
        "django-cors-headers",

        # GAE related libraries
        "google-cloud==0.34.0",
        "google-api-core[grpc]==1.22.2",  # via google-cloud-secret-manager
        "google-auth==1.21.2",       # via google-api-core
        "google-cloud-secret-manager==2.0.0",  # via -r requirements.txt
        "googleapis-common-protos[grpc]==1.52.0",  # via google-api-core, grpc-google-iam-v1
        "graphene-django==2.13.0",   # via -r requirements.txt
        "graphene-file-upload==1.2.2",  # via -r requirements.txt
        "graphene==2.1.8",           # via graphene-django
        "graphql-core==2.3.2",       # via graphene, graphene-django, graphql-relay
        "graphql-relay==2.0.1",      # via graphene
    ]

py_binary(
    name = "manage",
    srcs=["manage.py"],
    main="manage.py",
    python_version="PY3",
    stamp=0,
    visibility=["//visibility:public"],
    deps = [
        "//covidX:settings",
        "//covidX:urls",
        "//covidX:asgi",
    ] + [requirement(pkg) for pkg in _REQ],
)

py_binary(
    name = "main",
    srcs=["main.py"],
    main="main.py",
    deps = [
        "//:manage",
    ],
    python_version="PY3",
    stamp=0,
    visibility=["//visibility:public"],
)
