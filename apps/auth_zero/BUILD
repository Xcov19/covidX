package(default_visibility = ["//visibility:public"])

load("@my_deps//:requirements.bzl", "requirement")

py_library(
    name = "__init__",
    srcs = ["__init__.py"],
)

py_library(
    name = "apps",
    srcs = ["apps.py"],
    deps = [
      ":auth0backend"
    ],
)

py_library(
  name = "auth0backend",
  srcs = ["auth0backend.py"],
  deps = [
    requirement("django"),
    requirement("python-jose"),
    requirement("social-auth-core"),
  ],
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
    deps = [
      requirement("django"),
      ],
    data = [":auth_zero_tmpl"],
)

filegroup(
    name = "auth_zero_tmpl",
    srcs = glob([
        "templates/**",
    ]),
)
