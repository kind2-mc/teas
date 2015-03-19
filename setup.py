#!/usr/bin/env python

from distutils.core import setup
import os
import shutil
from src.stdout import info, warning, error, new_line

readme_md = "README.md"
readme_target = "README"
should_rm_readme_target = False

new_line()

# Copy `readme_md` to `readme_target` if the former exists but the
# former does not.
if os.path.isfile(readme_md) :

    if not os.path.isfile(readme_target) :
        info(
            "copying \"" + readme_md + "\" to \"" + readme_target + \
            "\" for distutils."
        )
        shutil.copyfile( readme_md, readme_target )
        should_rm_readme_target = True

    else : warning(
        "distutils readme file \"" + readme_target + \
        "\" detected, not copying \"" + readme_md + \
        "\"."
    )

else : warning( "readme file \"" + readme_md + "\" not found." )

new_line()

# Setup things.
try: setup(
    name='testeas',
    version='0.0',
    description='Test Execution and Analysis System',
    license='Apache 2.0',
    author='Adrien Champion',
    author_email='adrien.champion@email.com',
    url='https://github.com/kind2-mc/testeas',
    package_dir={'testeas': 'src'},
    packages=['testeas'],
)

finally :
    new_line()

    # Whatever happens during setup, remove target readme if necessary.
    if should_rm_readme_target:
        info("deleting distutils readme file \"" + readme_target + "\".")
        os.remove( readme_target )

    new_line()