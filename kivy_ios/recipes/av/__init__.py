from kivy_ios.toolchain import CythonRecipe


class PyAVRecipe(CythonRecipe):

    name = "av"
    library = "av.a"
    version = "10.0.0"
    url = "https://github.com/PyAV-Org/PyAV/archive/v{version}.zip"

    depends = ["python3", "hostpython3", "ffmpeg"]
    hostpython_prerequisites = ["Cython", "pkg-config"]
    opt_depends = ["openssl"]
    cythonize = False
    pre_build_ext = True

    def get_recipe_env(self, arch, with_flags_in_cc=True):
        env = super().get_recipe_env(arch)

        build_dir = self.get_recipe('ffmpeg', self.ctx).get_build_dir(
            arch.arch
        )
        self.setup_extra_args = ["--ffmpeg-dir={}".format(build_dir)]

        env[
            "PKG_CONFIG"
        ] = "ios-pkg-config"  # ios-pkg-config does not exists, is needed to disable the pkg-config usage.

        return env


recipe = PyAVRecipe()
