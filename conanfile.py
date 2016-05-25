from conans import ConanFile, ConfigureEnvironment
import os
from conans.tools import download, unzip

class XercesCConan(ConanFile):
    name = "xerces-c"
    version = "3.1.3"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    url="https://xerces.apache.org/xerces-c/"
    license="http://www.apache.org/licenses/LICENSE-2.0.html"
    folder_name="xerces-c-3.1.3"

    def source(self):
        zip_name = "xerces-c-3.1.3.zip"
        url = "http://apache.proserve.nl/xerces/c/3/sources/xerces-c-3.1.3.zip"
        download(url, zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
        self.run("cd %s && %s" % (self.folder_name, 'chmod u+x configure'))
        self.run("cd %s/config && %s" % (self.folder_name, 'chmod u+x pretty-make'))
        self.run("cd %s && %s %s" % (self.folder_name, env.command_line, './configure'))
        self.run("cd %s && %s %s" % (self.folder_name, env.command_line, 'make'))
        
        # Copying all executable files to bin
        self.run("mkdir -p bin")
        self.run("find %s/samples/ -type f -executable -exec cp {} bin \;" % (self.folder_name))

    def package(self):
        self.run("mkdir -p include")
        self.copy(pattern="*.hpp", dst="include", src="%s/src/" % (self.folder_name)) 
        self.copy(pattern="*.c", dst="include", src="%s/src/" % (self.folder_name)) 

        # Copying static and dynamic libs
        self.copy(pattern="*.a", dst="lib", src="%s/src/.libs/" % (self.folder_name), keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="%s/src/.libs" % (self.folder_name), keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src="%s/src/.libs" % (self.folder_name), keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src="%s/src/.libs" % (self.folder_name), keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src="%s/src/.libs" % (self.folder_name), keep_path=False)
        self.copy(pattern="*", dst="bin", src="bin", keep_path=False)


    def package_info(self):
        self.cpp_info.libdirs = ['lib']
        self.cpp_info.includedirs = ['include']
        self.cpp_info.bindirs = ['bin']
        if not self.settings.os == "Windows":
            self.cpp_info.libs = ["libxerces-c.a"] if not self.options.shared else ['libxerces-c.so']

