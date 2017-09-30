"""
API client generator.
"""
import os

import yaml


class Settings(object):
    """
    Settings.
    """

    @property
    def acg_dir(self):
        return os.path.dirname(os.path.realpath(__file__))

    @property
    def call_acg_dir(self):
        return os.getcwd()

    @property
    def acg_directory(self):
        return self.acg_dir

    @property
    def configurations_yml(self):
        return self.call_acg_dir + '/.acg.yml'

    @property
    def package_directory(self):
        return self.call_acg_dir + '/' + Configurations().package_name

    @property
    def package_file_path(self):
        return self.package_directory + '/' + Configurations().package_name + '/' + Configurations().package_file_name


class Configurations(object):
    """
    Configurations.
    """

    @staticmethod
    def parse_endpoints(endpoints):

        _endpoints = {}

        for endpoint in endpoints.split(', '):
            method_name, http_method = endpoint.split(':')
            _endpoints[method_name] = http_method

        return _endpoints

    @staticmethod
    def parse_service(services):
        return services.split('.')

    @property
    def pypi(self):
        return self._get_configurations()['pypi']

    @property
    def get_api_url(self):
        return self._get_configurations()['acg']['api']

    @property
    def package_name(self):
        return self._get_configurations()['acg']['name']

    @property
    def package_version(self):
        return self._get_configurations()['acg']['version']

    @property
    def package_author(self):
        return self._get_configurations()['pypi']['username']

    @property
    def package_author_password(self):
        return self._get_configurations()['pypi']['password']

    @property
    def package_file_name(self):
        return self._get_configurations()['acg']['name'] + '.py'

    @property
    def package_api_client_name(self):
        return self._get_configurations()['acg']['name'] + '_client'

    @property
    def services(self):
        return self._get_configurations()['acg']['services']

    @property
    def api_client_class(self):
        return self.package_name.capitalize() + '_client'

    @property
    def api_client_object(self):
        return self.package_api_client_name + ' = ' + self.api_client_class

    @staticmethod
    def _get_configurations():
        with open(Settings().configurations_yml, 'r') as configurations:
            try:
                return yaml.load(configurations)
            except yaml.YAMLError:
                print('No configurations file called `.acg.yml`')  # pylint: disable=superfluous-parens


class ConfigurationsMixin(Configurations):
    """
    Provide configurations points to needed parts of core logic.
    """


class SettingsMixin(Settings):
    """
    Provide configurations points to needed parts of core logic.
    """


class TemplatesSourceFiles:
    """
    Source files of needed templates handler.
    """

    def __init__(self, templates_directory):
        """
        Init.
        """
        self.templates_directory = templates_directory

    @property
    def imports_(self):
        return self.templates_directory + 'client/imports.txt'

    @property
    def class_(self):
        return self.templates_directory + 'client/class.txt'

    @property
    def property_(self):
        return self.templates_directory + 'client/property.txt'

    @property
    def request_(self):
        return self.templates_directory + 'client/request.txt'

    @property
    def api_client(self):
        return self.templates_directory + 'client/api_client.txt'

    @property
    def init_(self):
        return self.templates_directory + 'package/init.txt'

    @property
    def setup_(self):
        return self.templates_directory + 'package/setup.txt'

    @property
    def licence_(self):
        return self.templates_directory + 'package/license.txt'

    @property
    def requirements_(self):
        return self.templates_directory + 'package/requirements.txt'

    @property
    def pypirc_(self):
        return self.templates_directory + 'pypi/pypirc.txt'


class TemplatesManager(SettingsMixin):
    """
    Template manager.
    """

    def __init__(self):
        """
        Init.
        """
        self.templates_directory = self.acg_directory + '/templates/'

    @staticmethod
    def get_template_content(template, substitutes=None):

        with open(template, 'r') as template_file:
            template_content = ''.join(template_file.readlines())

            if substitutes:
                return template_content.format(**substitutes)

            return template_content

    @staticmethod
    def write_content(file, content):  # pylint: disable=redefined-builtin
        file.write(content)

    @property
    def templates(self):
        return TemplatesSourceFiles(self.templates_directory)


class PackageBone(ConfigurationsMixin, SettingsMixin):
    """
    Handle package bone points.
    """

    def __init__(self):
        """
        Init.
        """
        self.templates_manager = TemplatesManager()

    def build(self):

        self.create_package_directory()
        self.create_init_file()
        self.create_setup_file()
        self.create_license_file()
        self.create_requirements_file()

    def create_package_directory(self):
        if not os.path.exists(self.package_directory):
            os.makedirs(self.package_directory)
            os.makedirs(self.package_directory + '/' + self.package_name)

    def create_package_file(self, file_name, substitutes, template):
        with open(self.package_directory + '/' + file_name, 'w+') as file:
            template_content = self.templates_manager.get_template_content(template, substitutes)
            self.templates_manager.write_content(file, template_content)

    def create_init_file(self):
        substitutes = {
            'package_name': self.package_name,
            'api_client': self.package_api_client_name
        }

        self.create_package_file(
            self.package_name + '/__init__.py', substitutes, self.templates_manager.templates.init_
        )

    def create_setup_file(self):

        substitutes = {
            'author': self.package_author,
            'package_name': self.package_name,
            'version': self.package_version
        }

        self.create_package_file('setup.py', substitutes, self.templates_manager.templates.setup_)

    def create_license_file(self):
        substitutes = {
            'author': self.package_author,
        }

        self.create_package_file('LICENSE', substitutes, self.templates_manager.templates.licence_)

    def create_requirements_file(self):
        self.create_package_file('requirements.txt', {}, self.templates_manager.templates.requirements_)


class APIClient(ConfigurationsMixin, SettingsMixin):
    """
    Handle API client points.
    """

    def __init__(self):
        """
        Init.
        """
        self.templates_manager = TemplatesManager()

    def build(self):

        with open(self.package_file_path, 'w+') as package_file:
            self.package_file = package_file  # pylint: disable=attribute-defined-outside-init

            self.create_imports()
            self.create_services()
            self.create_classes_properties()
            self.create_endpoints_requests()
            self.create_api_client()
            self.create_api_client_endpoints()
            self.create_api_object()

    def create_imports(self):

        imports_template_content = self.templates_manager.get_template_content(
            self.templates_manager.templates.imports_
        )

        self.templates_manager.write_content(self.package_file, imports_template_content)

    def create_services(self):

        temp_classes = []

        for service in self.services.keys():
            services = self.parse_service(service)

            for sub_service in services:
                substitutes = {
                    'class': sub_service.capitalize()
                }

                class_template_content = self.templates_manager.get_template_content(
                    self.templates_manager.templates.class_,
                    substitutes
                )

                if sub_service not in temp_classes:
                    self.templates_manager.write_content(self.package_file, class_template_content)
                    temp_classes.append(sub_service)

    def create_classes_properties(self):

        for service in self.services.keys():
            services = self.parse_service(service)

            for index, sub_service in enumerate(services):

                if index == len(services) - 1:
                    break

                substitutes = {
                    'class': sub_service.capitalize(),
                    'property': services[index + 1],
                    'class_second': services[index + 1].capitalize()
                }

                property_template_content = self.templates_manager.get_template_content(
                    self.templates_manager.templates.property_,
                    substitutes
                )

                self.templates_manager.write_content(self.package_file, property_template_content)

    def create_endpoints_requests(self):

        for service in self.services.keys():
            endpoints = self.parse_endpoints(self.services[service]['endpoints'])
            url = self.services[service]['url']
            last_service = self.parse_service(service)[-1]

            for endpoint, http_method in endpoints.items():

                substitutes = {
                    'class': last_service.capitalize(),
                    'endpoint': endpoint,
                    'http_method': http_method,
                    'url': self.get_api_url + url,
                }

                request_template_content = self.templates_manager.get_template_content(
                    self.templates_manager.templates.request_,
                    substitutes
                )

                self.templates_manager.write_content(self.package_file, request_template_content)

    def create_api_client(self):

        substitutes = {
            'class': self.api_client_class,
        }

        class_template_content = self.templates_manager.get_template_content(
            self.templates_manager.templates.class_,
            substitutes
        )

        self.templates_manager.write_content(self.package_file, class_template_content)

    def create_api_client_endpoints(self):

        for service in self.services.keys():
            first_service = self.parse_service(service)[0]

            substitutes = {
                'class': self.api_client_class,
                'property': first_service,
                'class_second': first_service.capitalize(),
            }

            property_template_content = self.templates_manager.get_template_content(
                self.templates_manager.templates.property_,
                substitutes
            )

            self.templates_manager.write_content(self.package_file, property_template_content)

    def create_api_object(self):

        substitutes = {
            'api_object': self.package_name,
            'api_class': self.api_client_class,
        }

        api_client_template_content = self.templates_manager.get_template_content(
            self.templates_manager.templates.api_client,
            substitutes
        )

        self.templates_manager.write_content(self.package_file, api_client_template_content)


class Pypi(ConfigurationsMixin, SettingsMixin):
    """
    PYPI handler.
    """

    def __init__(self):
        """
        Init.
        """
        self.templates_manager = TemplatesManager()

    def create_pypirc(self):
        pypirc_template_content = self.templates_manager.templates.pypirc_

        substitutes = {
            'username': self.package_author,
            'password': self.package_author_password,
        }

        with open(os.path.expanduser('~') + '/.pypirc', 'w+') as pypirc_file:
            pypirc_content = self.templates_manager.get_template_content(pypirc_template_content, substitutes)
            pypirc_file.write(pypirc_content)

    def build(self):
        self.create_pypirc()

        os.system('pip install twine')
        os.chdir(self.package_directory)
        os.system('python setup.py sdist')
        os.system('python setup.py bdist_wheel')
        os.system('twine upload dist/*')


def acg():
    """
    Run API client builders.
    """
    PackageBone().build()
    APIClient().build()
    Pypi().build()


if __name__ == '__main__':
    acg()
