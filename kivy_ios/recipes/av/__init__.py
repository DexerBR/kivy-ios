from kivy_ios.toolchain import CythonRecipe, shprint
import sh


class PyAVRecipe(CythonRecipe):

    name = "av"
    library = "av.a"
    version = "10.0.0"
    url = "https://github.com/PyAV-Org/PyAV/archive/v{version}.zip"

    depends = ["python3", "ffmpeg"]
    opt_depends = ["openssl"]
    hostpython_prerequisites = ["Cython", "pkg-config"]
    cythonize = False
    # pre_build_ext = True

    def get_recipe_env(self, arch, with_flags_in_cc=True):
        env = super().get_recipe_env(arch)
        return env

    def build_arch(self, arch):
        build_env = self.get_recipe_env(arch)
        hostpython3 = sh.Command(self.ctx.hostpython)
        build_dir = self.get_recipe('ffmpeg', self.ctx).get_build_dir(
            arch.arch
        )
        setup_extra_args = ["--ffmpeg-dir={}".format(build_dir)]
        shprint(
            hostpython3,
            "setup.py",
            "build_ext",
            setup_extra_args,
            _env=build_env,
        )
        self.biglink()


recipe = PyAVRecipe()
