from kivy_ios.toolchain import CythonRecipe, shprint
import sh


class PyAVRecipe(CythonRecipe):

    name = "av"
    version = "10.0.0"
    url = "https://github.com/PyAV-Org/PyAV/archive/v{version}.zip"

    depends = ["python3", "ffmpeg"]
    opt_depends = ["openssl"]
    hostpython_prerequisites = ["Cython"]

    cythonize = True
    pre_build_ext = True

    def build_arch(self, arch):
        hostpython3 = sh.Command(self.ctx.hostpython)
        ffmpeg_dir = self.get_recipe("ffmpeg", self.ctx).get_build_dir(
            arch.arch
        )
        shprint(
            hostpython3,
            "setup.py",
            "build",
            "--ffmpeg-dir={}".format(ffmpeg_dir),
        )
        self.biglink()


recipe = PyAVRecipe()
