workspace(name = "covidx")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

http_archive(
    name = "com_github_ali5h_rules_pip",
    strip_prefix = "rules_pip-3.0.0",
    sha256 = "630a7cab43a87927353efca116d20201df88fb443962bf01c7383245c7f3a623",
    urls = ["https://github.com/ali5h/rules_pip/archive/3.0.0.tar.gz"],
)
load("@com_github_ali5h_rules_pip//:defs.bzl", "pip_import")

http_archive(
    name = "bazel_skylib",
    urls = [
        "https://github.com/bazelbuild/bazel-skylib/releases/download/1.0.3/bazel-skylib-1.0.3.tar.gz",
        "https://mirror.bazel.build/github.com/bazelbuild/bazel-skylib/releases/download/1.0.3/bazel-skylib-1.0.3.tar.gz",
    ],
    sha256 = "1c531376ac7e5a180e0237938a2536de0c54d93f5c278634818e0efc952dd56c",
)
# Add skylib common_settings dependency for buildifier
load("@bazel_skylib//:workspace.bzl", "bazel_skylib_workspace")
bazel_skylib_workspace()

# Download the rules_docker repository at release v0.14.4
git_repository(
    name = "io_bazel_rules_docker",
    remote = "https://github.com/bazelbuild/rules_docker.git",
    tag = "v0.14.4",
)

load(
    "@io_bazel_rules_docker//repositories:repositories.bzl",
    container_repositories = "repositories",
)
container_repositories()

load("@io_bazel_rules_docker//repositories:deps.bzl", container_deps = "deps")

container_deps()

load(
    "@io_bazel_rules_docker//container:container.bzl",
    "container_pull",
    "container_image",
)

container_pull(
  name = "python3_image",
  registry = "index.docker.io",
  repository = "codecakes/buster_py",
  # 'tag' is also supported, but digest is encouraged for reproducibility.
  digest = "sha256:c461bf44bafc3b434ec6818075cf499338b8ff934130989a288e5a045b076c16",
)

load("@io_bazel_rules_docker//repositories:pip_repositories.bzl", "pip_deps")

pip_deps()

load(
    "@io_bazel_rules_docker//python3:image.bzl",
    _py3_image_repos = "repositories",
)

_py3_image_repos()

http_archive(
    name = "rules_python",
    url = "https://github.com/bazelbuild/rules_python/archive/master.zip",
)

load("@rules_python//python:repositories.bzl",
    "py_repositories",
    )
py_repositories()
# Only needed if using the packaging rules.

load("@rules_python//python:pip.bzl", "pip_repositories")
pip_repositories()

# Create a central repo that knows about the dependencies needed for
# requirements.txt.
# Load the central repo's install function from its `//:requirements.bzl` file,
# and call it.
rules_python_external_version = "0.1.5"
RULES_PY_COMMIT_SHA = "bc655e6d402915944e014c3b2cad23d0a97b83a66cc22f20db09c9f8da2e2789"
http_archive(
    name = "rules_python_external",
    sha256 = "{COMMIT_SHA}".format(COMMIT_SHA=RULES_PY_COMMIT_SHA), # Fill in with correct sha256 of your COMMIT_SHA version
    strip_prefix = "rules_python_external-{version}".format(version = rules_python_external_version),
    url = "https://github.com/dillon-giacoppo/rules_python_external/archive/v{version}.zip".format(version = rules_python_external_version),
)
# Install the rule dependencies
load("@rules_python_external//:repositories.bzl", "rules_python_external_dependencies")
rules_python_external_dependencies()

# See why: https://github.com/dillon-giacoppo/rules_python_external
# load("@rules_python_external//:defs.bzl", "pip_install")
load("@rules_python//python:pip.bzl", "pip_install")
pip_install(
    # Uses the default repository name "pip"
    name = "my_deps",
    requirements = "//:requirements.txt",
)


# Invoke buildifier via the Bazel rule
# buildifier is written in Go and hence needs rules_go to be built.
# See https://github.com/bazelbuild/rules_go for the up to date setup instructions.
http_archive(
    name = "io_bazel_rules_go",
    sha256 = "9fb16af4d4836c8222142e54c9efa0bb5fc562ffc893ce2abeac3e25daead144",
    urls = [
        "https://storage.googleapis.com/bazel-mirror/github.com/bazelbuild/rules_go/releases/download/0.19.0/rules_go-0.19.0.tar.gz",
        "https://github.com/bazelbuild/rules_go/releases/download/0.19.0/rules_go-0.19.0.tar.gz",
    ],
)

load("@io_bazel_rules_go//go:deps.bzl", "go_register_toolchains", "go_rules_dependencies")

go_rules_dependencies()

go_register_toolchains()

http_archive(
    name = "bazel_gazelle",
    sha256 = "be9296bfd64882e3c08e3283c58fcb461fa6dd3c171764fcc4cf322f60615a9b",
    urls = [
        "https://storage.googleapis.com/bazel-mirror/github.com/bazelbuild/bazel-gazelle/releases/download/0.18.1/bazel-gazelle-0.18.1.tar.gz",
        "https://github.com/bazelbuild/bazel-gazelle/releases/download/0.18.1/bazel-gazelle-0.18.1.tar.gz",
    ],
)

load("@bazel_gazelle//:deps.bzl", "gazelle_dependencies")

gazelle_dependencies()

http_archive(
    name = "com_google_protobuf",
    strip_prefix = "protobuf-master",
    urls = ["https://github.com/protocolbuffers/protobuf/archive/master.zip"],
)

load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps")

protobuf_deps()

http_archive(
    name = "com_github_bazelbuild_buildtools",
    strip_prefix = "buildtools-master",
    url = "https://github.com/bazelbuild/buildtools/archive/master.zip",
)
