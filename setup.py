import os
import setuptools

setuptools.setup(
    name="typemallow",
    version="0.0.1",
    url="https://github.com/aher93/typemallow",

    author="Aden Herold",
    author_email="aden.herold1@gmail.com",

    description="An elegant and automatic solution for generating/outputting Typescript interfaces from your Marshmallow Schemas.",
    keywords=['Marshmallow', 'Typescript', 'Python', 'Flask', 'Django'],

    packages=['typemallow'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',

    install_requires=[
        'marshmallow'
    ]
)