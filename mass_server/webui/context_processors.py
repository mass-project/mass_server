from flask import current_app, render_template, url_for
from markupsafe import Markup

from mass_server.core.models import FileSample, IPSample, DomainSample, URISample, ExecutableBinarySample, UserLevel
from mass_server.webui.config import webui_blueprint


@webui_blueprint.context_processor
def sample_processors():
    def sample_icon(sample):
        if isinstance(sample, FileSample):
            return Markup('<i class="fa fa-file"></i>')
        elif isinstance(sample, IPSample):
            return Markup('<i class="fa fa-desktop"></i>')
        elif isinstance(sample, DomainSample):
            return Markup('<i class="fa fa-globe"></i>')
        elif isinstance(sample, URISample):
            return Markup('<i class="fa fa-at"></i>')
        else:
            return Markup('<i class="fa fa-question"></i>')

    def is_file_sample(sample):
        return isinstance(sample, FileSample)

    def is_executable_binary_sample(sample):
        return isinstance(sample, ExecutableBinarySample)

    def tag_search_link(tag):
        kwargs = {
            'common-tags': tag,
            'submit': 'Submit'
        }
        return url_for('.sample_search', **kwargs)

    return dict(
        sample_icon=sample_icon,
        is_file_sample=is_file_sample,
        is_executable_binary_sample=is_executable_binary_sample,
        tag_search_link=tag_search_link
    )


@webui_blueprint.context_processor
def user_processors():
    def user_level(user):
        if user.user_level == UserLevel.USER_LEVEL_ADMIN:
            return 'Administrator'
        elif user.user_level == UserLevel.USER_LEVEL_MANAGER:
            return 'Manager'
        elif user.user_level == UserLevel.USER_LEVEL_PRIVILEGED:
            return 'Privileged user'
        elif user.user_level == UserLevel.USER_LEVEL_USER:
            return 'Normal user'
        elif user.user_level == UserLevel.USER_LEVEL_ANONYMOUS:
            return 'Guest user'
        else:
            return 'Unknown user level'

    return dict(
        user_level=user_level
    )


@webui_blueprint.context_processor
def generic_processors():
    def mass_version():
        return current_app.version

    def pagination(paginator):
        return Markup(render_template('pagination.html', paginator=paginator))

    return dict(
        mass_version=mass_version,
        pagination=pagination
    )
