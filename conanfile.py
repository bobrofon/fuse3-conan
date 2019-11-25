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
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "pkg_config"
    build_requires = "meson_installer/0.51.0@bincrafters/stable"

    def source(self):
        git = tools.Git(folder="fuse")
        git.clone("https://github.com/libfuse/libfuse.git", "fuse-3.7.0")

    def build(self):
        meson = Meson(self)
        meson.configure(source_folder="fuse", build_folder="build",
                        args=["-D", "udevrulesdir=/etc/udev/rules.d"])
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
