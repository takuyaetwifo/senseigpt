from flask import Blueprint, render_template, request, redirect, url_for
from models import db, User
from flask_login import login_required




@app.route("/admin/edit_profile/<int:user_id>", methods=["GET", "POST"])
@login_required
def admin_edit_profile(user_id):
    # ★ここで管理者判定（必要なら）
    if session.get("role") != "admin":
        return "権限がありません", 403

    user = User.query.get(user_id)
    if not user:
        return "ユーザーが見つかりません", 404

    
    if request.method == "POST":
        user.birthday = request.form["birthday"] or None
        user.background = request.form["background"]
        user.profile = request.form["profile"]
        user.hobbies = request.form["hobbies"]
        user.family_status = request.form["family_status"]
        db.session.commit()
        return redirect(url_for("admin_edit_profile", user_id=user_id))
    return render_template("admin_edit_profile.html", user=user)

