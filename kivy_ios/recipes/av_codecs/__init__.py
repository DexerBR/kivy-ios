from kivy_ios.toolchain import Recipe


class PyAVCodecsRecipe(Recipe):
    depends = ["libx264", "libshine", "libvpx"]

    def build_arch(self, arch):
        pass


recipe = PyAVCodecsRecipe()
