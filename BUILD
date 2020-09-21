package(default_visibility = ["//visibility:public"])

load("@my_deps//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary")
load("@com_github_bazelbuild_buildtools//buildifier:def.bzl", "buildifier")

# TODO(@codecakes): run after fix:
# https://github.com/bazelbuild/buildtools/issues/909
buildifier(
    name = "buildifier",
)

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
    ] + [requirement("python-dotenv")],
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
