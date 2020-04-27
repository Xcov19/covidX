workspace(name = "covidx")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
http_archive(
    name = "bazel_federation",
    url = "https://github.com/bazelbuild/bazel-federation/archive/130c84ec6d60f31b711400e8445a8d0d4a2b5de8.zip",
    sha256 = "9d4fdf7cc533af0b50f7dd8e58bea85df3b4454b7ae00056d7090eb98e3515cc",
    strip_prefix = "bazel-federation-130c84ec6d60f31b711400e8445a8d0d4a2b5de8",
    type = "zip",
)

http_archive(
    name = "rules_python",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.0.1/rules_python-0.0.1.tar.gz",
    sha256 = "aa96a691d3a8177f3215b14b0edc9641787abaaa30363a080165d06ab65e1161",
)

load("@bazel_federation//:repositories.bzl",
     "bazel_stardoc",
     "rules_pkg",
     "rules_python_deps",
)

load("@bazel_federation//setup:rules_python.bzl",  "rules_python_setup")
rules_python_setup(use_pip=True)
rules_python_deps()

load("@rules_python//python:repositories.bzl",
    "py_repositories",
    )
py_repositories()
# Only needed if using the packaging rules.

load("@rules_python//python:pip.bzl", "pip_repositories", "pip_import")
pip_repositories()
# Create a central repo that knows about the dependencies needed for
# requirements.txt.
pip_import(
   name = "my_deps",
   requirements = "//:requirements.txt",
)
# Load the central repo's install function from its `//:requirements.bzl` file,
# and call it.
load("@my_deps//:requirements.bzl", "pip_install")
pip_install()




