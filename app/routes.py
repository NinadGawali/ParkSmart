# from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
# from werkzeug.security import generate_password_hash, check_password_hash
# from .models import db, User
# from datetime import timedelta

# bp = Blueprint("main", __name__)

# @bp.route("/")
# def index():
#     user = None
#     if session.get("user_id"):
#         user = User.query.get(session["user_id"])
#     return render_template("index.html", user=user)

# @bp.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         username = request.form.get("username", "").strip()
#         email = request.form.get("email", "").strip()
#         password = request.form.get("password", "")
#         if not username or not password:
#             flash("Username and password are required.", "error")
#             return redirect(url_for("main.register"))
#         if User.query.filter_by(username=username).first():
#             flash("Username already taken.", "error")
#             return redirect(url_for("main.register"))
#         pw_hash = generate_password_hash(password)  # PBKDF2 (werkzeug)
#         user = User(username=username, email=email, password_hash=pw_hash)
#         db.session.add(user)
#         db.session.commit()
#         flash("Account created. Please log in.", "success")
#         return redirect(url_for("main.login"))
#     return render_template("register.html")

# @bp.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form.get("username", "").strip()
#         password = request.form.get("password", "")
#         user = User.query.filter_by(username=username).first()
#         if not user or not check_password_hash(user.password_hash, password):
#             flash("Invalid username or password.", "error")
#             return redirect(url_for("main.login"))
#         # login: store user id in session
#         session.clear()
#         session["user_id"] = user.id
#         # optional: set session lifetime
#         session.permanent = True
#         current_app.permanent_session_lifetime = timedelta(hours=4)
#         flash("Logged in successfully.", "success")
#         return redirect(url_for("main.dashboard"))
#     return render_template("login.html")

# @bp.route("/logout")
# def logout():
#     session.clear()
#     flash("Logged out.", "info")
#     return redirect(url_for("main.index"))

# @bp.route("/dashboard")
# def dashboard():
#     if not session.get("user_id"):
#         return redirect(url_for("main.login"))
#     user = User.query.get(session["user_id"])
#     return render_template("dashboard.html", user=user)

# @bp.route("/search")
# def search():
#     # placeholder for parking search page
#     if not session.get("user_id"):
#         return redirect(url_for("main.login"))
#     return render_template("search.html")


from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, ParkingSpace, Booking
from datetime import timedelta, datetime
from decimal import Decimal
from .utils import send_email  # relative import


bp = Blueprint("main", __name__)

# -------------------------
# Helper: current user
# -------------------------
def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)

# -------------------------
# Public pages / auth
# -------------------------
@bp.route("/")
def index():
    user = get_current_user()
    return render_template("index.html", user=user)

@bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            flash("Username and password required", "error")
            return redirect(url_for("main.register"))
        if User.query.filter_by(username=username).first():
            flash("Username already taken", "error")
            return redirect(url_for("main.register"))
        pw_hash = generate_password_hash(password)
        user = User(username=username, email=email, password_hash=pw_hash)
        db.session.add(user)
        db.session.commit()
        flash("Account created. Please log in.", "success")
        return redirect(url_for("main.login"))
    return render_template("register.html")

@bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid username or password.", "error")
            return redirect(url_for("main.login"))
        session.clear()
        session["user_id"] = user.id
        session.permanent = True
        current_app.permanent_session_lifetime = timedelta(hours=4)
        flash("Logged in successfully.", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("login.html")

@bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("main.index"))

@bp.route("/dashboard")
def dashboard():
    user = get_current_user()
    if not user:
        return redirect(url_for("main.login"))
    # show user's posted parking and bookings
    my_parking = ParkingSpace.query.filter_by(owner_id=user.id).all()
    my_bookings = Booking.query.filter_by(user_id=user.id).all()
    return render_template("dashboard.html", user=user, my_parking=my_parking, my_bookings=my_bookings)

# -------------------------
# Post parking (owner)
# -------------------------
@bp.route("/post-parking", methods=["GET", "POST"])
def post_parking():
    user = get_current_user()
    if not user:
        flash("Please log in to post parking.", "error")
        return redirect(url_for("main.login"))
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        address = request.form.get("address", "").strip()
        lat = request.form.get("lat")
        lng = request.form.get("lng")
        google_map_url = request.form.get("google_map_url", "").strip()
        price = request.form.get("price_per_hour", "0").strip()
        try:
            lat = float(lat) if lat else None
            lng = float(lng) if lng else None
            price = Decimal(price)
        except Exception:
            flash("Invalid numeric values.", "error")
            return redirect(url_for("main.post_parking"))
        ps = ParkingSpace(
            owner_id=user.id,
            title=title or "Parking space",
            address=address,
            lat=lat,
            lng=lng,
            google_map_url=google_map_url,
            price_per_hour=price,
            is_available=True
        )
        db.session.add(ps)
        db.session.commit()
        flash("Parking space posted.", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("post_parking.html", user=user)

# -------------------------
# Search API (JSON) + UI route uses it
# GET params: q, min_price, max_price, lat, lng, radius_km, available_only
# -------------------------
@bp.route("/api/search-parking", methods=["GET"])
def api_search_parking():
    q = request.args.get("q", type=str)
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    lat = request.args.get("lat", type=float)
    lng = request.args.get("lng", type=float)
    radius_km = request.args.get("radius_km", type=float, default=5.0)
    available_only = request.args.get("available_only", default="1")
    available_only = True if available_only in ("1","true","True") else False

    # Optional desired start + hours (for availability projection)
    desired_start_iso = request.args.get("desired_start")  # ISO8601
    desired_hours = request.args.get("desired_hours", type=float)
    desired_start = None
    if desired_start_iso:
        try:
            desired_start = datetime.fromisoformat(desired_start_iso)
        except Exception:
            desired_start = None
    desired_end = None
    if desired_start and desired_hours and desired_hours > 0:
        desired_end = desired_start + timedelta(hours=desired_hours)

    query = ParkingSpace.query
    if q:
        like_q = f"%{q}%"
        query = query.filter(ParkingSpace.title.ilike(like_q) | ParkingSpace.address.ilike(like_q))
    if min_price is not None:
        query = query.filter(ParkingSpace.price_per_hour >= min_price)
    if max_price is not None:
        query = query.filter(ParkingSpace.price_per_hour <= max_price)
    # "is_available" flag still acts as master toggle: False => always unavailable irrespective of bookings.
    if available_only:
        query = query.filter(ParkingSpace.is_available == True)

    # naive bounding box search if lat/lng provided (approx)
    if lat is not None and lng is not None:
        # convert radius km to approximate degree delta (~111 km per degree lat)
        delta = radius_km / 111.0
        query = query.filter(
            ParkingSpace.lat.between(lat - delta, lat + delta),
            ParkingSpace.lng.between(lng - delta, lng + delta)
        )

    results = query.limit(200).all()
    out = []
    for s in results:
        # Determine dynamic availability: space is unavailable iff there exists an overlapping booking.
        now = datetime.utcnow()
        reference_start = desired_start or now
        reference_end = desired_end or reference_start + timedelta(hours=1)
        # Overlap logic: booking with defined window overlaps if starts before ref_end and ends after ref_start.
        overlapping = False
        for b in s.bookings:
            # Indefinite lock if either time_start or time_end is NULL
            if b.time_start is None or b.time_end is None:
                overlapping = True
                break
            if b.time_start < reference_end and b.time_end > reference_start:
                overlapping = True
                break
        dynamic_available = (s.is_available and not overlapping)
        out.append({
            "id": s.id,
            "title": s.title,
            "address": s.address,
            "lat": s.lat,
            "lng": s.lng,
            "google_map_url": s.google_map_url,
            "price_per_hour": str(s.price_per_hour),
            "is_available": bool(dynamic_available),
            "owner_username": s.owner.username if s.owner else None,
            "next_available_estimate": (reference_end.isoformat() if overlapping else reference_start.isoformat())
        })
    return jsonify({"spaces": out})

# -------------------------
# Booking endpoint: checks availability then marks unavailable
# Body: parking_id, time_start (ISO), time_end (ISO)
# -------------------------
@bp.route("/book", methods=["POST"])
def book():
    user = get_current_user()
    if not user:
        return jsonify({"error": "unauthenticated"}), 401

    data = request.get_json() or {}
    parking_id = data.get("parking_id")
    time_start_raw = data.get("time_start")
    time_end_raw = data.get("time_end")
    hours_raw = data.get("hours")  # optional duration input

    if not parking_id:
        return jsonify({"error": "missing parking_id"}), 400
    if not (time_start_raw and (time_end_raw or hours_raw)):
        return jsonify({"error": "missing time window (provide time_start + (time_end or hours))"}), 400

    # parse start
    try:
        ts = datetime.fromisoformat(time_start_raw)
    except Exception:
        return jsonify({"error": "invalid time_start (ISO expected)"}), 400

    # derive end either from provided end or hours
    te = None
    if time_end_raw:
        try:
            te = datetime.fromisoformat(time_end_raw)
        except Exception:
            return jsonify({"error": "invalid time_end (ISO expected)"}), 400
    elif hours_raw:
        try:
            hrs = float(hours_raw)
            if hrs <= 0:
                return jsonify({"error": "hours must be > 0"}), 400
            te = ts + timedelta(hours=hrs)
        except Exception:
            return jsonify({"error": "invalid hours value"}), 400

    if not te:
        return jsonify({"error": "could not determine end time"}), 400
    if te <= ts:
        return jsonify({"error": "end must be after start"}), 400

    # Start a transaction to avoid race conditions
    try:
        ps = ParkingSpace.query.with_for_update().filter_by(id=parking_id).first()
        if not ps:
            return jsonify({"error": "parking not found"}), 404
        if not ps.is_available:
            return jsonify({"error": "parking currently disabled"}), 400

        # Check overlapping bookings (including indefinite locks)
        overlapping = False
        for b in ps.bookings:
            if b.time_start is None or b.time_end is None:
                overlapping = True
                break
            if b.time_start < te and b.time_end > ts:
                overlapping = True
                break
        if overlapping:
            return jsonify({"error": "requested window overlaps existing booking"}), 409

        # compute amount (hours * price) - round up to nearest 0.01
        hours = (te - ts).total_seconds() / 3600.0
        if hours < 0.01:
            hours = 0.01
        total = (Decimal(ps.price_per_hour) * Decimal(hours)).quantize(Decimal('0.01'))

        # create booking
        booking = Booking(
            user_id=user.id,
            parking_id=ps.id,
            time_start=ts,
            time_end=te,
            duration_hours=Decimal(f"{hours:.2f}"),
            total_amount=total
        )
        # Do NOT flip is_available; dynamic logic will surface availability.
        db.session.add(booking)
        db.session.commit()

                # after db.session.commit() -- inside the book() route
        # build receipt data
        try:
            receipt = {
                "booking_id": booking.id,
                "username": user.username,
                "email": user.email,
                "parking_title": ps.title,
                "parking_address": ps.address or "",
                "google_map_url": ps.google_map_url or "",
                "time_start": booking.time_start.isoformat(),
                "time_end": booking.time_end.isoformat(),
                "total_amount": str(booking.total_amount),
                "reference": f"BK-{booking.id}",
                "generated_on": booking.created_at.isoformat()
            }
            subject = f"ParkSmart booking confirmation — #{booking.id}"
            # best-effort send; don't interrupt booking flow if email fails
            sent = send_email(user.email, subject, receipt)
            if not sent:
                current_app.logger.warning("Email not sent for booking %s (user %s)", booking.id, user.id)
        except Exception:
            current_app.logger.exception("Error while attempting to send receipt email")


        return jsonify({"ok": True, "booking_id": booking.id, "total": str(total), "duration_hours": str(booking.duration_hours)})
    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("Booking failed")
        return jsonify({"error": "internal error"}), 500

# -------------------------
# UI: Search page (template)
# -------------------------
@bp.route("/search")
def search():
    user = get_current_user()
    if not user:
        return redirect(url_for("main.login"))
    return render_template("search.html", user=user)
