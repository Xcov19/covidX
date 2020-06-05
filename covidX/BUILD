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
)

py_library(
    name = "settings",
    srcs = ["settings.py"],
    deps = [
        ":schema",
    ],
)

py_library(
    name = "urls",
    srcs = ["urls.py"],
    deps = [
        requirement("django"),
        requirement("graphene-django"),
        "//apps/apihealth:apps",
        "//apps/apihealth:urls",
    ],
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
)

py_library(
    name = "wsgi",
    srcs = ["wsgi.py"],
    deps = [requirement("django")],
)
