package(default_visibility = ["//visibility:public"])
load("@my_deps//:requirements.bzl", "requirement")

py_library(
    name = "__init__",
    srcs = ["__init__.py"],
)

py_library(
    name = "asgi",
    srcs = ["asgi.py"],
    deps = [requirement("django")],
    srcs_version="PY3",
)

py_library(
    name = "settings",
    srcs = [
        "//covidX/settings:base",
        "//covidX/settings:dev",
    ],
    deps = [
        "//:__init__",
    ],
    srcs_version="PY3",
    data = ["//:static",],
)

py_library(
    name = "gae_settings",
    srcs = ["gae_settings.py"],
    deps = [
        requirement("google-cloud-secret-manager"),
    ],
    srcs_version="PY3",
)

py_library(
    name = "utils",
    srcs = ["utils.py"],
    deps = [],
)

py_library(
    name = "urls",
    srcs = ["urls.py"],
    deps = [
        requirement("django"),
        requirement("graphene-django"),
        requirement("djangorestframework"),
        requirement("django-debug-toolbar"),
        ":utils",
        "//apps/apihealth:apps",
        "//apps/apihealth:urls",
        "//apps/auth_zero:apps",
        "//apps/auth_zero:urls",
    ],
    srcs_version="PY3",
)

py_library(
    name = "schema",
    srcs = ["schema.py"],
    deps = [requirement(r) for r in [
            "graphene",
            "graphene-django",
        ]
    ] + [
        "//apps/apihealth:schema",
    ],
    srcs_version="PY3",
)

py_library(
    name = "wsgi",
    srcs = ["wsgi.py"],
    deps = [
        requirement("django"),
        requirement("python-dotenv"),
        "//covidX/settings:dev",
    ],
    srcs_version="PY3",
)
