from setuptools import setup

""" This is used to setup the web application. Be careful when altering """

setup(name='curriculumstandards',
      version='2023.0.dev1',
      description='Curriculum Mapping Library for Computer Science',
      url='https://github.com/Washburn-CIS/curriculum',
      author='Washburn University Computer Information Sciences Department',
      author_email='Joseph.Kendall-Morwick@washburn.edu',
      license='GPL',
      packages=['curriculumstandards'],  
      package_dir={'curriculumstandards': 'curriculumstandards'}, 
      package_data={'curriculumstandards': ['schema/*.xsd', \
                                        'transformations/*.xsl', \
                                        'standards/*.xml']},
      zip_safe=False)
