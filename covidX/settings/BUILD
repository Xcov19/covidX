package(default_visibility = ["//visibility:public"])
load("@my_deps//:requirements.bzl", "requirement")

py_library(
    name = "__init__",
    srcs = ["__init__.py"],
)

py_library(
    name = "base",
    srcs = ["base.py"],
    deps = [
        requirement("django-extensions"),
        requirement("social-auth-core"),
        requirement("social-auth-app-django"),
        requirement("graphene-django"),
        requirement("django-guardian"),
        requirement("djangorestframework"),
        requirement("drf-jwt"),
        requirement("django-debug-toolbar"),
        "//covidX:gae_settings",
        "//covidX:schema",
        "//covidX:utils",
        "//apps/apihealth:__init__",
        "//apps/apihealth:apps",
        "//apps/hrm:__init__",
        "//apps/hrm:apps",
        "//apps/hrm:models",
        "//apps/auth_zero:__init__",
        "//apps/auth_zero:apps",
        "//apps/auth_zero:models",
        "//apps/auth_zero:auth0backend",
        "//:__init__",
    ],
    srcs_version="PY3",
    data = ["//:static",],
    visibility=["//visibility:public"],
)

py_library(
    name = "dev",
    srcs = ["dev.py"],
    deps = [
        ":base",
    ],
    srcs_version="PY3",
    visibility=["//visibility:public"],
)
