package(default_visibility = ["//visibility:public"])

load("@my_deps//:requirements.bzl", "requirement")

py_library(
    name = "__init__",
    srcs = ["__init__.py"],
    deps = [
      ":apps",
    ],
)

py_library(
    name = "apps",
    srcs = ["apps.py"],
    deps = [],
)

py_library(
  name = "auth0backend",
  srcs = ["auth0backend.py"],
  deps = [
    requirement("requests"),
    requirement("django"),
    requirement("python-jose"),
    requirement("social-auth-core"),
    requirement("social-auth-app-django"),
    ":apps",
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
        requirement("djangorestframework"),
        requirement("drf-jwt"),
      ],
    data = [":auth_zero_tmpl",],
)

py_library(
    name = "models",
    srcs = ["models.py"],
    deps = [
        requirement("django"),
    ],
    data = [":migrations",],
)

py_library(
    name = "admin",
    srcs = ["admin.py"],
    deps = [
        requirement("django"),
        requirement("django-guardian"),
        ":models",
    ],
)

py_test(
    name = "test",
    srcs = [
        "tests.py",
    ],
    # TODO(codecakes): include common in deps module once moved to apps/
    deps = [
        requirement("django"),
    ],
    # TODO(codecakes): include data to include data folder
    #  that has config/test_config.ini
    data = [],
    main = "tests.py",
    srcs_version = "PY3"
)

filegroup(
    name = "auth_zero_tmpl",
    srcs = glob([
        "templates/**",
    ]),
)

filegroup(
    name = "migrations",
    srcs = glob([
        "migrations/**",
    ]),
)
