package(default_visibility = ["//visibility:public"])

load("@my_deps//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary")
load("@com_github_bazelbuild_buildtools//buildifier:def.bzl", "buildifier")
load("@io_bazel_rules_docker//python3:image.bzl", "py3_image")
load("@io_bazel_rules_docker//container:image.bzl", "container_image")
load("@rules_python//python:defs.bzl", "py_runtime_pair")

# TODO(@codecakes): run after fix:
# https://github.com/bazelbuild/buildtools/issues/909
buildifier(
    name = "buildifier",
)

REQS = [
    "python-dotenv",
    "social-auth-app-django",
    "social-auth-core",
    "django-extensions",
    "django-cors-headers",
    "psycopg2",
    "werkzeug",
    ]

LIBS = [
    "//covidX:settings",
    "//covidX:urls",
    "//covidX:asgi",
    "//covidX:wsgi",
] + [requirement(r) for r in REQS]

py_binary(
    name = "manage",
    srcs=["manage.py"],
    main="manage.py",
    python_version="PY3",
    stamp=0,
    visibility=["//visibility:public"],
    deps = LIBS,
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

py3_image(
    name = "covidx_image",
    srcs=["main.py"],
    main="main.py",
    layers = [
        "//:manage",
        "//covidX:wsgi",
    ],
    stamp=0,
    visibility=["//visibility:public"],
    base = "@python3_image//image",
    srcs_version="PY3",
)

py3_image(
    name = "covidx_manage",
    srcs=["manage.py"],
    main="manage.py",
    stamp=0,
    visibility=["//visibility:public"],
    layers = LIBS,
    base = "@python3_image//image",
    srcs_version="PY3",
)
