import os
import glob

from conans import ConanFile, tools, Meson

import tools.meson as meson_tools

from tools import append_value
from tools.meson import with_fake_compiler


class LibfuseConan(ConanFile):
    name = 'fuse3'
    version = '3.9.1'
    license = 'LGPLv2'
    author = 'bobrofon@gmail.com'
    url = 'https://github.com/bobrofon/fuse3-conan'
    description = 'Linux FUSE (Filesystem in Userspace) interface'
    topics = ('fuse', 'fs')
    settings = ('os', 'compiler', 'build_type', 'arch')
    options = {'shared': [True, False],
               'disable_mtab': [True, False],
               'examples': [True, False],
               'useroot': [True, False],
               'utils': [True, False]}
    default_options = {'shared': False,
                       'disable_mtab': False,
                       'examples': False,
                       'useroot': False,
                       'utils': True}
    generators = 'pkg_config'
    build_requires = 'meson/0.54.0'

    patches = 'patches/*.patch'
    exports = 'tools/*.py', patches
    src_repo_folder = 'fuse'

    cross_file_name = 'cross_file.txt'

    meson = None

    def source(self):
        git_tag = 'fuse-' + self.version

        git = tools.Git(folder=self.src_repo_folder)
        git.clone('https://github.com/libfuse/libfuse.git', git_tag)

    @classmethod
    def apply_patches(cls):
        for patch in sorted(glob.glob(cls.patches)):
            print('Apply patch {}'.format(patch))
            tools.patch(base_path=cls.src_repo_folder, patch_file=patch)

    def build(self):
        self.apply_patches()

        args = ['-D', 'disable-mtab=' + str(self.options.disable_mtab).lower(),
                '-D', 'examples=' + str(self.options.examples).lower(),
                '-D', 'useroot=' + str(self.options.useroot).lower(),
                '-D', 'utils=' + str(self.options.utils).lower()]

        if tools.cross_building(self.settings):
            meson_tools.write_cross_file(self.cross_file_name, self)
            args += ['--cross-file', 'cross_file.txt']

        defs = meson_tools.common_flags(self.settings)
        if not self.options.shared:
            append_value(defs, 'c_link_args', '-static')

        # there is no usage of native compiler but we had to trick
        # meson's sanity check somehow
        meson_env = (with_fake_compiler()
                     if tools.cross_building(self.settings)
                     else tools.no_op())
        self.meson = Meson(self)
        with meson_env:
            self.meson.configure(source_folder=self.src_repo_folder,
                                 build_folder='build',
                                 args=args,
                                 defs=defs)
        self.meson.build()

    def package(self):
        self.meson.install()

    def package_info(self):
        self.cpp_info.libs = ['fuse3', 'dl', 'pthread']
        self.cpp_info.defines = ['_FILE_OFFSET_BITS=64']
        self.cpp_info.includedirs.append(os.path.join('include', 'fuse3'))
