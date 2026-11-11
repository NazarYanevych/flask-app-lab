from datetime import datetime
from pathlib import Path
from uuid import uuid4

from flask import render_template, abort, redirect, url_for, flash
from tinydb import Query

from . import products_bp
from .database import products_table
from .forms import ProductForm, DeleteProductForm


@products_bp.route("/")
def product_list():
    products = products_table.all()
    return render_template("products/products.html", products=products)


@products_bp.route("/<int:id>")
def product_detail(id):
    product = products_table.get(Query().id == id)

    if product is None:
        abort(404)

    delete_form = DeleteProductForm()

    return render_template(
        "products/detail_product.html",
        product=product,
        delete_form=delete_form
    )

@products_bp.route("/add", methods=["GET", "POST"])
def add_product():
    form = ProductForm()

    if form.validate_on_submit():
        image_path = ""

        if form.image.data:
            file = form.image.data
            extension = Path(file.filename).suffix.lower()
            filename = f"{uuid4().hex}{extension}"

            upload_dir = Path(__file__).resolve().parent / "static" / "uploads"
            upload_dir.mkdir(parents=True, exist_ok=True)

            file.save(str(upload_dir / filename))
            image_path = f"uploads/{filename}"

        product = {
            "name": form.name.data,
            "content": form.content.data,
            "price": float(form.price.data),
            "category": form.category.data,
            "quantity": form.quantity.data,
            "image": image_path,
            "created_at": datetime.now().isoformat()
        }

        product_id = products_table.insert(product)
        products_table.update({"id": product_id}, doc_ids=[product_id])

        flash("Товар успішно додано!", "success")
        return redirect(url_for("products.product_list"))

    return render_template("products/add_product.html", form=form)


@products_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit_product(id):
    product = products_table.get(Query().id == id)

    if product is None:
        abort(404)

    form = ProductForm(data=product)

    if form.validate_on_submit():
        image_path = product.get("image", "")

        if form.image.data:
            file = form.image.data
            extension = Path(file.filename).suffix.lower()
            filename = f"{uuid4().hex}{extension}"

            upload_dir = Path(__file__).resolve().parent / "static" / "uploads"
            upload_dir.mkdir(parents=True, exist_ok=True)

            file.save(str(upload_dir / filename))
            image_path = f"uploads/{filename}"

        products_table.update({
            "name": form.name.data,
            "content": form.content.data,
            "price": float(form.price.data),
            "category": form.category.data,
            "quantity": form.quantity.data,
            "image": image_path
        }, Query().id == id)

        flash("Товар успішно оновлено!", "success")
        return redirect(url_for("products.product_detail", id=id))

    return render_template("products/edit_product.html", form=form, product=product)



@products_bp.route("/<int:id>/delete", methods=["POST"])
def delete_product(id):
    product = products_table.get(Query().id == id)

    if product is None:
        abort(404)

    form = DeleteProductForm()

    if not form.validate_on_submit():
        abort(400)

    products_table.remove(Query().id == id)

    flash("Товар успішно видалено!", "success")
    return redirect(url_for("products.product_list"))
