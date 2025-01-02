from config import *

login_bp = Blueprint("login_bp", __name__, template_folder="templates")


@login_bp.route("/", methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
       
        usuario = request.form.get('usuario')
        
        print(f"--------{usuario}---------")
        
        return redirect(url_for('login_bp.load', usuario=usuario))
    
    return render_template("login.html")


@login_bp.route('/load')
def load():
    usuario = request.args.get('usuario', None)  # Obtém o valor de 'usuario' da URL
    return render_template("load.html", usuario=usuario)