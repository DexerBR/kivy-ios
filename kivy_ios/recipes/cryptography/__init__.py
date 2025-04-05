from kivy_ios.toolchain import CythonRecipe
from os.path import join
import os
import glob
import shutil

class CryptographyRecipe(CythonRecipe):
    version = '42.0.1'
    url = 'https://github.com/pyca/cryptography/archive/refs/tags/{version}.tar.gz'
    library = 'libcryptography.a'
    depends = ['openssl', 'python', 'setuptools', 'cffi']
    
    RUST_ARCH_CODES = {
        "arm64": "aarch64-apple-ios",
        "x86_64": "x86_64-apple-ios",
        "arm64-sim": "aarch64-apple-ios-sim",
    }
    
    def check_host_deps(self):
        import sh
        try:
            sh.rustup("--version")
        except Exception:
            print("Error: `rustup` was not found on your system.")
            print("Please install it using: `curl https://sh.rustup.rs -sSf | sh`")
            exit(1)
    
    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        
        build_target = self.RUST_ARCH_CODES.get(arch.arch)
        if not build_target:
            print(f"Error: Unsupported architecture: {arch.arch}")
            exit(1)
        
        openssl_recipe = self.ctx.recipe_build("openssl")
        openssl_build_dir = openssl_recipe.get_build_dir(arch.arch)
        
        env["CARGO_BUILD_TARGET"] = build_target
        
        env["OPENSSL_DIR"] = openssl_build_dir
        env["OPENSSL_INCLUDE_DIR"] = join(openssl_build_dir, 'include')
        env["OPENSSL_LIB_DIR"] = join(openssl_build_dir, 'lib')
        
        target_upper = build_target.upper().replace("-", "_")
        env[f"{target_upper}_OPENSSL_INCLUDE_DIR"] = join(openssl_build_dir, 'include')
        env[f"{target_upper}_OPENSSL_LIB_DIR"] = join(openssl_build_dir, 'lib')
        
        env["RUSTFLAGS"] = f"-Clink-args=-L{openssl_build_dir}/lib"
        
        import sh
        print("Ensuring rust build toolchain")
        sh.rustup("target", "add", build_target)
        
        return env
    
    def build_arch(self, arch):
        self.check_host_deps()
        
        build_dir = self.get_build_dir(arch.arch)
        
        env = self.get_recipe_env(arch)
        
        self.set_python_path(arch)
        
        cmd = ['build_ext', '--inplace']
        self.call_hostpython_via_targetpython(cmd, build_dir, env=env)
        
        self.install_python_package(arch)
        
        dylib_dir = join(self.ctx.dist_dir, 'root', 'python3', 'lib', 'python3.9', 'site-packages', 'cryptography')
        so_files = glob.glob(join(build_dir, "**", "*.so"), recursive=True)
        for so_file in so_files:
            shutil.copy(so_file, dylib_dir)


recipe = CryptographyRecipe()