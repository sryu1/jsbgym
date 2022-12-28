from setuptools import setup, find_packages


setup(name='jsbgym',
      version='0.1',
      description='A package of reinforcement learning environments for flight '
                  'control using the JSBSim flight dynamics model.',
      url='https://github.com/sryu1/jsbgym',
      author='sryu1',
      license='MIT',
      install_requires=[
          'numpy',
          'gymnasium',
          'matplotlib',
      ],
      packages=find_packages(),
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Science/Research',
          'Programming Language :: Python :: 3.7',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
      ],
      python_requires='>=3.7',
      include_package_data=True,
      zip_safe=False)
