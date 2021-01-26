import os
import glob

from conans import ConanFile, tools
from conans.errors import ConanInvalidConfiguration
from conan.tools.meson import MesonToolchain, Meson


required_conan_version = ">=1.33.0"


class LibfuseConan(ConanFile):
    name = 'fuse3'
    version = '3.10.1'
    license = ' LGPL-2.1-only'
    author = 'bobrofon@gmail.com'
    url = 'https://github.com/bobrofon/fuse3-conan'
    homepage = 'https://github.com/libfuse/libfuse'
    description = 'Linux FUSE (Filesystem in Userspace) interface'
    topics = ('conan', 'libfuse', 'fuse', 'fs', 'filesystems', 'C')
    settings = ('os', 'compiler', 'build_type', 'arch')
    options = {
        'shared': [True, False],
        'fPIC': [True, False],
    }
    default_options = {
        'shared': False,
        'fPIC': True,
    }
    _patches = 'patches/*.patch'
    exports = 'tools/*.py', _patches
    _source_subfolder = 'source_subfolder'
    _build_subfolder = 'build_subfolder'
    _meson = None

    def validate(self):
        if self.settings.os != "Linux":
            raise ConanInvalidConfiguration("Only Linux supported")

    def configure(self):
        if self.options.shared:
            del self.options.fPIC
        del self.settings.compiler.cppstd
        del self.settings.compiler.libcxx

    def build_requirements(self):
        self.build_requires('meson/0.56.2')

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("fuse-" + self.version, self._source_subfolder)

    def _apply_patches(self):
        for patch in sorted(glob.glob(self._patches)):
            self.output.info('Apply patch {}'.format(patch))
            tools.patch(base_path=self._source_subfolder, patch_file=patch)

    def _configure_meson(self):
        if self._meson:
            return self._meson

        env = os.environ.copy()
        # meson will autodetect linker
        del env['LD']
        tc = MesonToolchain(self, env=env)
        tc.definitions['disable-mtab'] = False
        tc.definitions['examples'] = False
        tc.definitions['useroot'] = False
        tc.definitions['utils'] = False
        tc.generate()

        self._meson = Meson(self, build_folder=self._build_subfolder)
        self._meson.configure(source_folder=self._source_subfolder)
        return self._meson

    def build(self):
        self._apply_patches()
        meson = self._configure_meson()
        meson.build()

    def package(self):
        meson = self._configure_meson()
        meson.install()
        self.copy(pattern="LGPL2.txt", dst="licenses", src=self._source_subfolder)
        if os.path.exists(os.path.join(self.package_folder, "lib64")):
            os.rename(os.path.join(self.package_folder, "lib64"),
                      os.path.join(self.package_folder, "lib"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        self.cpp_info.libs.append('fuse3')
        self.cpp_info.defines.append('_FILE_OFFSET_BITS=64')
        self.cpp_info.includedirs.append(os.path.join('include', 'fuse3'))
        self.cpp_info.system_libs.extend(('dl', 'pthread', 'rt'))
