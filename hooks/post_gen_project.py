import shutil
from pathlib import Path

# https://github.com/cookiecutter/cookiecutter/issues/824
#   our workaround is to include these utility functions in the CCDS package
from ccds.hook_utils.custom_config import write_custom_config
from ccds.hook_utils.dependencies import write_dependencies

#
#  TEMPLATIZED VARIABLES FILLED IN BY COOKIECUTTER
#
packages = [
    "black",
    "flake8",
    "isort",
    "pip",
    "setuptools",
    "wheel",
]

# {% if cookiecutter.dataset_storage.s3 %}
packages += ["awscli"]
# {% endif %} #

# {% if cookiecutter.include_code_scaffold == "Yes" %}
packages += [
    "typer",
    "python-dotenv",
    "loguru",
]
# {% endif %}

# {% if cookiecutter.pydata_packages == "basic" %}
packages += [
    "ipython",
    "jupyter",
    "matplotlib",
    "numpy",
    "pandas",
    "scikit-learn",
]
# {% endif %}

# track packages that are not available through conda
pip_only_packages = [
    "awscli",
    "python-dotenv",
]

docs_path = Path("{{ cookiecutter.project_name }} ") / "docs"
# {% if cookiecutter.docs == "sphinx" %}
packages += ["sphinx"]
shutil.rmtree(docs_path / "mkdocs")
shutil.move(docs_path / "sphinx", docs_path)
# {% elif cookiecutter.docs == "mkdocs" %}
packages += ["mkdocs"]
pip_only_packages += ["mkdocs"]
# {% else %}
shutil.rmtree(docs_path / "mkdocs")
shutil.rmtree(docs_path / "sphinx")
# {% endif %}

#
#  POST-GENERATION FUNCTIONS
#
write_dependencies(
    "{{ cookiecutter.dependency_file }}",
    packages,
    pip_only_packages,
    repo_name="{{ cookiecutter.repo_name }}",
    module_name="{{ cookiecutter.module_name }}",
    python_version="{{ cookiecutter.python_version_number }}",
)

write_custom_config("{{ cookiecutter.custom_config }}")


# {% if cookiecutter.include_code_scaffold == "No" %}
# remove everything except __init__.py so result is an empty package
for generated_path in Path("{{ cookiecutter.module_name }}").iterdir():
    if generated_path.is_dir():
        shutil.rmtree(generated_path)
    elif generated_path.name != "__init__.py":
        generated_path.unlink()
# {% endif %}
