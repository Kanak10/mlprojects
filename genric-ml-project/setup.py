from setuptools import find_packages, setup
from typing import List
import ast


def _get_pyproject_dependencies(file_path: str) -> List[str]:
    try:
        import tomllib
    except ModuleNotFoundError:
        try:
            import tomli as tomllib
        except ModuleNotFoundError:
            tomllib = None

    if tomllib is not None:
        with open(file_path, "rb") as file_obj:
            pyproject_data = tomllib.load(file_obj)
        return pyproject_data.get("project", {}).get("dependencies", [])

    with open(file_path, encoding="utf-8") as file_obj:
        lines = file_obj.readlines()

    in_project_section = False
    for index, line in enumerate(lines):
        stripped_line = line.strip()

        if stripped_line.startswith("[") and stripped_line.endswith("]"):
            in_project_section = stripped_line == "[project]"
            continue

        if in_project_section and stripped_line.startswith("dependencies"):
            _, _, dependencies_block = line.partition("=")
            cursor = index + 1

            while dependencies_block.count("[") > dependencies_block.count("]"):
                dependencies_block += lines[cursor]
                cursor += 1

            return list(ast.literal_eval(dependencies_block.strip()))

    return []


def get_requirements(file_path: str) -> List[str]:
    '''
    this function will return the list of requiremennts
    '''
    if file_path.endswith(".toml"):
        return _get_pyproject_dependencies(file_path)

    with open(file_path, encoding="utf-8") as file_obj:
        requirements = file_obj.readlines()

    return [
        requirement.strip()
        for requirement in requirements
        if requirement.strip() and requirement.strip() != "-e ."
    ]

setup(
    name="generic-ml-project",
    version="0.0.1",
    author="Kanak",
    author_email="kanakgupta814@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("pyproject.toml")
)
