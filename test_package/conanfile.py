from conans import ConanFile, CMake


class LibfuseTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = ("cmake", "pkg_config")
    build_requires = 'cmake_installer/3.16.3@conan/stable'

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        pass
