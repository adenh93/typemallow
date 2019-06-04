import os
import setuptools

with open('README.md') as file:
    long_description = file.read()

setuptools.setup(
    name="typemallow",
    version="0.0.2",
    url="https://github.com/adenh93/typemallow",

    author="Aden Herold",
    author_email="aden.herold1@gmail.com",

    description="An elegant and automatic solution for generating/outputting Typescript interfaces from your Marshmallow Schemas.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['Marshmallow', 'Typescript', 'Python', 'Flask', 'Django'],

    packages=['typemallow'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',

    install_requires=[
        'marshmallow'
    ]
)
