package(default_visibility = ["//visibility:public"])

load("@my_deps//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary")
load("@io_bazel_rules_docker//python3:image.bzl", "py3_image")
("@io_bazel_rules_docker//container:image.bzl",
 "container",
 "image")
load("@io_bazel_rules_docker//python:image.bzl", "py_layer")
load("@io_bazel_rules_k8s//k8s:object.bzl", "k8s_object")

load("@rules_python//python:defs.bzl", "py_runtime_pair")

_REQ = [
        "asgiref",
        "django",             # via -r requirements.in (line 1)
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

        # Django related packages
        "django-model-utils",
        "django-phonenumber-field",
        "phonenumbers",
        "social-auth-app-django",
        "graphene-file-upload",
        "django-extensions",

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
        "//covidX:wsgi",
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

py_runtime(
    name = "py37",
    interpreter_path = "/usr/bin/python3",
    files = [],
)

py_runtime_pair(
    name = "pair",
    py3_runtime = ":py37",
)

toolchain(
    name = "my_toolchain",
#    target_compatible_with = <...>,
    toolchain = ":pair",
    toolchain_type = "@rules_python//python:toolchain_type",
)
#
#py3_image(
#  name='main',
#  srcs=['main.py'],
#  main='main.py',
#  stamp=0,
#  layers=[
#    # This takes the name as specified in requirements.txt
#    "//:manage",
#  ],
#  visibility=['//visibility:public'],
#)
#
#k8s_object(
#    name = "dev",
#    kind="deployment",
#    images = {
#        "covidx:latest": ":main",
#    },
#    template = "//:deployment.yaml",
#)
