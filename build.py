#!/usr/bin/env python3

from cpt.packager import ConanMultiPackager

if __name__ == "__main__":
    arch_build = "x86_64"
    settings = {
        "os": "Linux",
        "os_build": "Linux",
        "arch_build": arch_build,
        "compiler": "gcc",
        "compiler.version": 6,
        "compiler.libcxx": "libstdc++11",
        "compiler.cppstd": 14,
        "build_type": "Release",
        "gcc-toolchain:arch": arch_build,
        "ninja:arch": arch_build,
        "meson:arch": arch_build,
        "cmake_installer:arch": arch_build,
    }
    options = {
        "*:shared": False,
        "*:fPIC": True,
    }
    build_requires = {
        "*": [
            "gcc-toolchain/6.3.0@bobrofon/stable",
            "meson/0.56.2"
        ]
    }

    builder = ConanMultiPackager(
        username="bobrofon",
        channel="testing",
        upload="https://api.bintray.com/conan/bobrofon/sshfs-world",
        build_policy="missing",
    )
    builder.add(settings=settings | {"arch": "armv6"},
                options=options | {"gcc-toolchain:target": "armv6"},
                build_requires=build_requires)
    builder.add(settings=settings | {"arch": "armv8"},
                options=options | {"gcc-toolchain:target": "armv8"},
                build_requires=build_requires)
    builder.add(settings=settings | {"arch": "x86"},
                options=options | {"gcc-toolchain:target": "x86"},
                build_requires=build_requires)
    builder.add(settings=settings | {"arch": "x86_64"},
                options=options | {"gcc-toolchain:target": "x86_64"},
                build_requires=build_requires)
    builder.run()
