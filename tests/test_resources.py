"""
    Test the resources.py file.
"""

import os
from pathlib import Path

import validators


def test_resources_class():
    from pytia_property_manager.resources import Resources

    resource = Resources()


def test_settings():
    from pytia_property_manager.resources import resource

    assert isinstance(resource.settings.title, str)
    assert len(resource.settings.title) > 0
    assert isinstance(resource.settings.debug, bool)
    assert isinstance(resource.settings.demo, bool)
    assert isinstance(resource.settings.revision, int)
    assert isinstance(resource.settings.link_material, bool)
    assert (
        isinstance(resource.settings.min_brightness, int)
        or resource.settings.min_brightness is None
    )

    assert isinstance(resource.settings.restrictions.allow_all_users, bool)
    assert isinstance(resource.settings.restrictions.allow_all_editors, bool)
    assert isinstance(resource.settings.restrictions.allow_unsaved, bool)
    assert isinstance(resource.settings.restrictions.allow_outside_workspace, bool)
    assert isinstance(resource.settings.restrictions.strict_project, bool)
    assert isinstance(resource.settings.restrictions.strict_product, bool)
    assert isinstance(resource.settings.restrictions.enable_information, bool)

    assert isinstance(resource.settings.separators.bought, str)
    assert isinstance(resource.settings.separators.metadata, str)

    assert isinstance(resource.settings.nomenclature.made, str)
    assert isinstance(resource.settings.nomenclature.bought, str)

    assert isinstance(resource.settings.processes.first, int)
    assert resource.settings.processes.first in [0, 1]
    assert isinstance(resource.settings.processes.min, int)
    assert isinstance(resource.settings.processes.max, int)

    assert isinstance(resource.settings.tolerances, list)
    assert isinstance(resource.settings.tolerances[0], str)

    assert isinstance(resource.settings.spare_part_level, list)
    assert isinstance(resource.settings.spare_part_level[0], str)

    assert isinstance(resource.settings.paths.catia, Path)
    assert isinstance(resource.settings.paths.material, Path)
    assert isinstance(resource.settings.paths.release, Path)

    assert isinstance(resource.settings.files.app, str)
    assert isinstance(resource.settings.files.launcher, str)
    assert isinstance(resource.settings.files.bounding_box_launcher, str)
    assert isinstance(resource.settings.files.material, str)
    assert isinstance(resource.settings.files.workspace, str)

    if resource.settings.urls.help:
        assert validators.url(resource.settings.urls.help)  # type: ignore
    assert validators.email(resource.settings.mails.admin)  # type: ignore


def test_properties():
    from pytia_property_manager.resources import resource

    assert "project" in resource.props.infra.keys
    assert "product" in resource.props.infra.keys
    assert "material" in resource.props.infra.keys
    assert "base_size" in resource.props.infra.keys
    assert "base_size_preset" in resource.props.infra.keys
    assert "mass" in resource.props.infra.keys
    assert "manufacturer" in resource.props.infra.keys
    assert "supplier" in resource.props.infra.keys
    assert "tolerance" in resource.props.infra.keys
    assert "spare_part_level" in resource.props.infra.keys
    assert "creator" in resource.props.infra.keys
    assert "modifier" in resource.props.infra.keys

    assert "general" in resource.props.notes.keys
    assert "material" in resource.props.notes.keys
    assert "base_size" in resource.props.notes.keys
    assert "supplier" in resource.props.notes.keys
    assert "production" in resource.props.notes.keys

    assert "process_n" in resource.props.production.keys
    assert "note_process_n" in resource.props.production.keys


def test_users():
    from pytia_property_manager.resources import resource

    logon_list = []

    for user in resource.users:
        assert isinstance(user.logon, str)
        assert isinstance(user.id, str)
        assert isinstance(user.name, str)
        assert isinstance(user.mail, str)
        assert user.logon not in logon_list

        logon_list.append(user.logon)


def test_release_folder():
    from pytia_property_manager.resources import resource

    assert os.path.isdir(resource.settings.paths.release)


def test_debug_mode():
    from pytia_property_manager.resources import resource

    assert resource.settings.debug == False
