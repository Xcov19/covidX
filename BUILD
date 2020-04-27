package(default_visibility = ["//visibility:public"])
load("@my_deps//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "app",
    srcs=["manage.py"],
    main="manage.py",
    python_version="PY3",
    stamp=0,
    visibility=["//visibility:public"],
    deps = [
        "//covidX:settings",
        "//covidX:urls",
        "//covidX:wsgi",
        requirement("django"),
        requirement("python-dotenv"),
    ]
)