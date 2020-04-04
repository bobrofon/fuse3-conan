import os

from conans import ConanFile, tools, Meson

import tools.meson as meson_tools

from tools import append_value
from tools.meson import with_fake_compiler


class LibfuseConan(ConanFile):
    name = 'fuse3'
    version = '3.7.0'
    license = 'LGPLv2'
    author = 'bobrofon@gmail.com'
    url = 'https://github.com/bobrofon/fuse3-conan'
    description = 'Linux FUSE (Filesystem in Userspace) interface'
    topics = ('fuse', 'fs')
    settings = ('os', 'compiler', 'build_type', 'arch')
    options = {'shared': [True, False],
               'disable_mtab': [True, False],
               'examples': [True, False],
               'udevrulesdir': 'ANY',
               'useroot': [True, False],
               'utils': [True, False]}
    default_options = {'shared': False,
                       'disable_mtab': False,
                       'examples': False,
                       'udevrulesdir': '/etc/udev/rules.d',
                       'useroot': False,
                       'utils': True}
    generators = 'pkg_config'
    build_requires = 'meson/0.54.0'

    exports = 'tools/*.py'

    cross_file_name = 'cross_file.txt'

    meson = None

    def source(self):
        git_tag = 'fuse-' + self.version

        git = tools.Git(folder='fuse')
        git.clone('https://github.com/libfuse/libfuse.git', git_tag)

        # TODO: remove (problems with installation paths within install_helper)
        tools.replace_in_file('fuse/util/meson.build',
"""meson.add_install_script('install_helper.sh',
                         join_paths(get_option('prefix'), get_option('sysconfdir')),
                         join_paths(get_option('prefix'), get_option('bindir')),
                         udevrulesdir,
                         '@0@'.format(get_option('useroot')))""", '')

    def build(self):
        args = ['-D', 'disable-mtab=' + str(self.options.disable_mtab).lower(),
                '-D', 'examples=' + str(self.options.examples).lower(),
                '-D', 'udevrulesdir=' + str(self.options.udevrulesdir),
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
            self.meson.configure(source_folder='fuse',
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
