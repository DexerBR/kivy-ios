from kivy_ios.toolchain import PythonRecipe

# import sh
# 6


class PyAVRecipe(PythonRecipe):

    name = "av"
    # library = "av.a"
    version = "10.0.0"
    url = "https://github.com/PyAV-Org/PyAV/archive/v{version}.zip"

    depends = ["python3", "ffmpeg"]
    opt_depends = ["openssl"]
    hostpython_prerequisites = ["Cython"]
    # cythonize = False
    # pre_build_ext = False

    def get_recipe_env(self, arch, with_flags_in_cc=True):
        env = super().get_recipe_env(arch)
        build_dir = self.get_recipe("ffmpeg", self.ctx).get_build_dir(
            arch.arch
        )
        env["--ffmpeg-dir"] = build_dir
        return env

    # def build_arch(self, arch):
    #     hostpython3 = sh.Command(self.ctx.hostpython)
    #     shprint(
    #         hostpython3,
    #         "setup.py",
    #         "build",
    #         "--ffmpeg-dir={}".format(build_dir),
    #         _env=build_env,
    #     )
    #     self.biglink()


recipe = PyAVRecipe()
