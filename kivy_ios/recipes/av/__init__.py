from kivy_ios.toolchain import CythonRecipe
from os.path import join


class PyAVRecipe(CythonRecipe):

    name = "av"
    library = "av.a"
    version = "10.0.0"
    url = "https://github.com/PyAV-Org/PyAV/archive/v{version}.zip"

    depends = ["python3", "cython", "ffmpeg"]
    opt_depends = ["openssl"]
    pre_build_ext = True

    def get_recipe_env(self, arch, with_flags_in_cc=True):
        env = super().get_recipe_env(arch)

        build_dir = join(self.ctx.dist_dir, "include", arch.arch, "ffmpeg")
        self.setup_extra_args = ["--ffmpeg-dir={}".format(build_dir)]

        return env


recipe = PyAVRecipe()
