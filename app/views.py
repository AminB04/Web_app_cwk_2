from flask import render_template, redirect, url_for, flash, request, jsonify
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import db, User, Kit
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/current-kits')
def current_kits():
    kits = Kit.query.filter_by(kit_type="Current").all()
    return render_template('kits.html', kits=kits, title='Current Kits')

@app.route('/retro-kits')
def retro_kits():
    kits = Kit.query.filter_by(kit_type="Retro").all()
    return render_template('kits.html', kits=kits, title='Retro Kits')

@app.route('/concept-kits')
def concept_kits():
    kits = Kit.query.filter_by(kit_type="Concept").all()
    return render_template('kits.html', kits=kits, title='Concept Kits')

@app.route('/favourites')
def favourites():
    if current_user.is_authenticated:
        favourites = current_user.favourites
    else:
        favourites = []
    return render_template('favourites.html', favourites=favourites)

@app.route('/add_to_favourites/<int:kit_id>', methods=['GET', 'POST'])
@login_required
def add_to_favourites(kit_id):
    if not current_user.is_authenticated:
        flash("You need to log in to add items to your favourites.", "warning")
        return redirect(url_for('login'))
    kit = Kit.query.get_or_404(kit_id)
    current_user.favourites.append(kit)
    db.session.commit()
    flash(f"{kit.name} has been added to your favourites.", "success")
    return redirect(url_for('favourites'))

@app.route('/remove_from_favourites/<int:kit_id>', methods=['POST'])
@login_required
def remove_from_favourites(kit_id):
    kit = Kit.query.get_or_404(kit_id)
    if kit in current_user.favourites:
        current_user.favourites.remove(kit)
        db.session.commit()
        return jsonify({"success": True, "message": "Removed from favourites"})
    return jsonify({"success": False, "message": "Item not found"}), 404

@app.route('/basket')
def basket():
    if current_user.is_authenticated:
        basket_items = current_user.basket_items
    else:
        basket_items = []
    return render_template('basket.html', basket_items=basket_items)

@app.route('/add_to_basket/<int:kit_id>', methods=['GET', 'POST'])
@login_required
def add_to_basket(kit_id):
    if not current_user.is_authenticated:
        flash("You need to log in to add items to your basket.", "warning")
        return redirect(url_for('login'))
    kit = Kit.query.get_or_404(kit_id)
    if kit.stock_level > 0:
        if kit not in current_user.basket_items:
            current_user.basket_items.append(kit)
            kit.stock_level -= 1  # Decrease stock level
            db.session.commit()
            flash(f"{kit.name} has been added to your Basket.", "success")
    else:
        flash('This kit is out of stock.', 'error')
    return redirect(url_for('basket'))

@app.route('/remove_from_basket/<int:kit_id>', methods=['POST'])
@login_required
def remove_from_basket(kit_id):
    kit = Kit.query.get_or_404(kit_id)
    if kit in current_user.basket_items:
        current_user.basket_items.remove(kit)
        kit.stock_level += 1  # Increase stock level
        db.session.commit()
        flash(f"{kit.name} has been removed to your Basket.", "success")
    return redirect(url_for('basket'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=True)
            next_page = request.args.get('next') or url_for('home')
            return redirect(next_page)
        else:
            flash('Invalid username or password', "danger")
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already in use. Please choose another.", "danger")
            return redirect(url_for('register'))
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. You can now log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
