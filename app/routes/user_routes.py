from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from app.models.user import User
from app.models.role import Role  # <--- Импорт ролей
from app.forms.user_forms import UserForm
from app import db

user_bp = Blueprint('user', __name__, url_prefix='/user')
base_bp = Blueprint('base', __name__)


class DeleteForm(FlaskForm):
    pass

@base_bp.route('/')
@user_bp.route('/')
@login_required
def index():
    users = User.query.all()
    form = DeleteForm()
    return render_template('index.html', users=users, form=form)


@user_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_user():
    form = UserForm()
    form.role_id.choices = [(role.id, role.name) for role in Role.query.all()]
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            middle_name=form.middle_name.data,
            role_id=form.role_id.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Пользователь успешно создан')
        return redirect(url_for('user.index'))
    return render_template('user_form.html', form=form)


@user_bp.route('/<int:user_id>', methods=['GET'])
@login_required
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_view.html', user=user)


@user_bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    form.role_id.choices = [(role.id, role.name) for role in Role.query.all()]

    if form.validate_on_submit():
        user.username = form.username.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.middle_name = form.middle_name.data
        user.role_id = form.role_id.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash('Данные пользователя обновлены')
        return redirect(url_for('user.index'))
    return render_template('user_form.html', form=form, user=user)


@user_bp.route('/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Пользователь удалён')
    return redirect(url_for('user.index'))
