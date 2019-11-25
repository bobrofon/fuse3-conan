from conans import ConanFile, tools, Meson


class LibfuseConan(ConanFile):
    name = "fuse3"
    version = "3.7.0"
    license = "LGPLv2"
    author = "bobrofon@gmail.com"
    url = "https://github.com/bobrofon/fuse3"
    description = "Linux FUSE (Filesystem in Userspace) interface"
    topics = ("fuse", "fs")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "disable_mtab": [True, False],
               "examples": [True, False],
               "udevrulesdir": "ANY",
               "useroot": [True, False],
               "utils": [True, False]}
    default_options = {"shared": False,
                       "disable_mtab": False,
                       "examples": False,
                       "udevrulesdir": "/etc/udev/rules.d",
                       "useroot": True,
                       "utils": True}
    generators = "pkg_config"
    build_requires = "meson_installer/0.51.0@bincrafters/stable"

    def source(self):
        git = tools.Git(folder="fuse")
        git.clone("https://github.com/libfuse/libfuse.git", "fuse-3.7.0")

    def build(self):
        meson = Meson(self)
        meson.configure(source_folder="fuse", build_folder="build",
                        args=["-D", "disable-mtab={}".format("true" if self.options.disable_mtab else "false"),
                              "-D", "examples={}".format("true" if self.options.examples else "false"),
                              "-D", "udevrulesdir={}".format(self.options.udevrulesdir),
                              "-D", "useroot={}".format("true" if self.options.useroot else "false"),
                              "-D", "utils={}".format("true" if self.options.utils else "false")])
        meson.build()

    def package(self):
        self.copy("*.h", dst="include", src="fuse/include")
        self.copy("*fuse3.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*fuse3.pc", dst="", keep_path=False)
        self.copy("*fusermount3", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["fuse3", "dl", "pthread"]
        self.cpp_info.defines = ["_FILE_OFFSET_BITS=64"]
