from conans import ConanFile, CMake


class LibfuseTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = ("cmake", "pkg_config")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        pass
