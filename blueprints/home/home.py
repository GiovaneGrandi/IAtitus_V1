from config import *

home_bp = Blueprint("home_bp", __name__, template_folder="templates")


@home_bp.route("/", methods=['GET', 'POST'])
def index():
    
    return render_template("home.html")