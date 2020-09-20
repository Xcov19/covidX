workspace(name = "covidx")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

#http_archive(
#    name = "com_github_ali5h_rules_pip",
#    strip_prefix = "rules_pip-3.0.0",
#    sha256 = "630a7cab43a87927353efca116d20201df88fb443962bf01c7383245c7f3a623",
#    urls = ["https://github.com/ali5h/rules_pip/archive/3.0.0.tar.gz"],
#)
#load("@com_github_ali5h_rules_pip//:defs.bzl", "pip_import")

http_archive(
    name = "rules_python",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.0.3/rules_python-0.0.3.tar.gz",
    sha256 = "e46612e9bb0dae8745de6a0643be69e8665a03f63163ac6610c210e80d14c3e4",
)

load("@rules_python//python:repositories.bzl",
    "py_repositories",
    )
py_repositories()
# Only needed if using the packaging rules.

load("@rules_python//python:pip.bzl", "pip3_import", "pip_repositories")
pip_repositories()

# Create a central repo that knows about the dependencies needed for
# requirements.txt.
pip3_import(
   name = "my_deps",
   requirements = "//:requirements.txt",
)

# Load the central repo's install function from its `//:requirements.bzl` file,
# and call it.
load("@my_deps//:requirements.bzl", "pip_install")
pip_install()
