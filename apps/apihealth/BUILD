package(default_visibility = ["//visibility:public"])

load("@my_deps//:requirements.bzl", "requirement")

py_library(
    name = "__init__",
    srcs = ["__init__.py"],
)

py_library(
    name = "admin",
    srcs = ["admin.py"],
    deps = [],
)

py_library(
    name = "apps",
    srcs = ["apps.py"],
)

py_library(
    name = "urls",
    srcs = ["urls.py"],
    deps = [
        requirement("django"),
        ":views",
    ],
)

py_library(
    name = "views",
    srcs = ["views.py"],
    deps = [requirement("django")],
)
