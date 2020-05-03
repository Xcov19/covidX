workspace(name = "covidx")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

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

# bazel-skylib 0.8.0 released 2019.03.20 (https://github.com/bazelbuild/bazel-skylib/releases/tag/0.8.0)
skylib_version = "0.8.0"
http_archive(
    name = "bazel_skylib",
    type = "tar.gz",
    url = "https://github.com/bazelbuild/bazel-skylib/releases/download/{}/bazel-skylib.{}.tar.gz".format (skylib_version, skylib_version),
    sha256 = "2ef429f5d7ce7111263289644d233707dba35e39696377ebab8b0bc701f7818e",
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


#Setup Docker

# Download the rules_docker repository at release v0.14.1
http_archive(
    name = "io_bazel_rules_docker",
    sha256 = "dc97fccceacd4c6be14e800b2a00693d5e8d07f69ee187babfd04a80a9f8e250",
    strip_prefix = "rules_docker-0.14.1",
    urls = ["https://github.com/bazelbuild/rules_docker/releases/download/v0.14.1/rules_docker-v0.14.1.tar.gz"],
)
load(
    "@io_bazel_rules_docker//repositories:repositories.bzl",
    container_repositories = "repositories",
)
container_repositories()

#Use Python3 image
load(
    "@io_bazel_rules_docker//repositories:repositories.bzl",
    container_repositories = "repositories",
)

container_repositories()
# To use py3_image. See: https://github.com/bazelbuild/rules_docker#py3_image
load(
    "@io_bazel_rules_docker//python3:image.bzl",
    _py_image_repos = "repositories",
)

_py_image_repos()


#Setup K8

# This requires rules_docker to be fully instantiated before
# it is pulled in.
# Download the rules_k8s repository at release v0.4
http_archive(
    name = "io_bazel_rules_k8s",
    sha256 = "d91aeb17bbc619e649f8d32b65d9a8327e5404f451be196990e13f5b7e2d17bb",
    strip_prefix = "rules_k8s-0.4",
    urls = ["https://github.com/bazelbuild/rules_k8s/releases/download/v0.4/rules_k8s-v0.4.tar.gz"],
)

load("@io_bazel_rules_k8s//k8s:k8s.bzl", "k8s_repositories")

k8s_repositories()

load("@io_bazel_rules_k8s//k8s:k8s_go_deps.bzl", k8s_go_deps = "deps")

k8s_go_deps()

#register_toolchains("//:my_toolchain")
