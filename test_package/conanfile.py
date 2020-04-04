from conans import ConanFile, CMake


class LibfuseTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    build_requires = 'cmake/3.17.0'

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        pass
