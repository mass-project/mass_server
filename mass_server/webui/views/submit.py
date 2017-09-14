from flask import url_for, render_template, redirect, flash

from mass_server.core.models import Sample
from mass_server.webui.config import webui_blueprint
from mass_server.webui.forms import SampleSubmitForm


@webui_blueprint.route('/submit/', methods=['GET', 'POST'])
def submit():
    form = SampleSubmitForm()
    if form.validate_on_submit():
        unique_features = {}
        if form.data['file']:
            unique_features['file'] = form.data['file']
        if form.data['ipv4']:
            unique_features['ipv4'] = form.data['ipv4']
        if form.data['ipv6']:
            unique_features['ipv6'] = form.data['ipv6']
        if form.data['port']:
            unique_features['port'] = form.data['port']
        if form.data['domain']:
            unique_features['domain'] = form.data['domain']
        if form.data['uri']:
            unique_features['uri'] = form.data['uri']
        sample = Sample.create_or_update(unique_features=unique_features, tlp_level=form.data['tlp_level'])
        flash('Your sample has been submitted', 'success')
        return redirect(url_for('webui.sample_detail', sample_id=sample.id))
    return render_template('submit.html', form=form)
