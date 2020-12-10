import setuptools
import setuptools.command.develop
import setuptools.command.install


class WithCompile:
	def run(self):
		super().run()


class InstallWithCompile(WithCompile, setuptools.command.install.install):
	pass


class DevelopWithCompile(WithCompile, setuptools.command.develop.develop):
	pass


class SDistWithCompile(WithCompile, setuptools.command.sdist.sdist):
	pass


setuptools.setup(
	cmdclass={
		"install": InstallWithCompile,
		"develop": DevelopWithCompile,
		"sdist": SDistWithCompile,
	}
)
