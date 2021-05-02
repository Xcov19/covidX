package(default_visibility = ["//visibility:public"])

load("@rules_python//python:defs.bzl", "py_binary")
#load("@com_github_bazelbuild_buildtools//buildifier:def.bzl", "buildifier")
load("@rules_python//python:defs.bzl", "py_runtime_pair")
load("@my_deps//:requirements.bzl", "requirement")

# TODO(@codecakes): run after fix:
# https://github.com/bazelbuild/buildtools/issues/909
#buildifier(
#    name = "buildifier",
#)

REQS = [
    "django",
    "python-dotenv",
    "social-auth-app-django",
    "social-auth-core",
    "django-extensions",
    "django-cors-headers",
    "psycopg2-binary",
    "werkzeug",
    ]

DEPS = [
    "//covidX:settings",
    "//covidX:urls",
    "//covidX:asgi",
    "//covidX:wsgi",
] + [requirement(r) for r in REQS]

py_library(
    name = "__init__",
    srcs = ["__init__.py"],
)

py_binary(
    name = "manage",
    srcs=["manage.py"],
    main="manage.py",
    python_version="PY3",
    stamp=0,
    visibility=["//visibility:public"],
    deps = DEPS,
    data = [":envs"],
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
    data = [":envs"],
)

filegroup(
    name = "envs",
    srcs = [
        ".env",
        ],
)

filegroup(
    name = "static",
    srcs = glob([
        "static/**",
    ]),
    visibility = ["//covidX:__subpackages__"],
)
