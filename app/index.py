from flask import render_template, request, redirect
# sau khi đã refactor qua bên init
from app import app, dao, login
# import admin vào
from flask_login import login_user , logout_user
import cloudinary.uploader


# __name__ nó sẽ tự hieu là tên của package python
@app.route('/')  # @saleapp nếu như saleapp = Flask(...)
def index():
    # return  'hello the anh'
    cate_id = request.args.get('category_id')
    # Sau khi viết cate_id thì qua bên dao.py truyền vào load_product
    # Sau khi thêm bên kia sẽ thêm kw vao để truyền

    # Lấy name ='keyword' bên name='keyword' của index.html
    kw = request.args.get('keyword')
    products = dao.load_products(cate_id=cate_id, kw=kw)
    return render_template('index.html', products=products)  # nó sẽ tự động tìm trong templates


# categories red là biến dùng ngoài templates -> nghĩa là trên index nó dùng ,  còn màu trắng là biến = dao.load_categories

# Thêm phương thức ở đây để có thể truyền lên trên thanh của web
# Phải có dấu / đầu  và product_id phải parse về số nguyên .
@app.route('/product/<int:product_id>')
def detail(product_id):
    # Khi đã cài bên dao thì qua đùng cài cái này để truyền lên templates
    p = dao.get_product_by_id(product_id)
    return render_template('detail.html', product=p)


# Sau khi đã sửa bên index.html của admin thêm dòng này vào
@app.route('/login-admin', methods=['post'])
def admin_login():
    username = request.form['username']
    password = request.form['password']
    user = dao.auth_user(username=username, password=password)

    if user:
        login_user(user=user)
    # Chuyển trang -> cụ thể là chuyển về trang chủ
    return redirect('/admin')


# KHi qua trang khác sẽ hiện toàn bộ thanh navbar chứ không cần phải truyền  vào render_template categories
# chỉ cần có phương thức dưới thì những thằng nào có render_template đều sẽ có navbar hiên full categories
@app.context_processor
def common_attr():
    categories = dao.load_categories()
    return {
        'categories': categories
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_id(user_id)


# Sau khi thêm qua bên index.html của admin thêm method="post"


# Đăng ký

# get trong cái này dùng để lấy đường dãn tới trang đăng ký còn post để lấy thông tin kiểm tra người dùng
@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            # upload

            # 2 dòng này debug
            # import pdb
            # pdb.set_trace()
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']
            # save_user
            try:
                dao.register(name=request.form['name'],
                             username=request.form['username'],
                             password=password, avatar=avatar)
                return redirect('/login')
            except:
                err_msg = " Hệ thống đang có lỗi! Vui lòng quay lại sau!"
        # pip install cloudinary
        else:
            err_msg = 'Mật khẩu không khớp'

    # nếu không phải post thì nó đi tới trang này ->
    return render_template('register.html', err_msg=err_msg)


@app.route('/login', methods=['get','post'])
def login_my_user():
    # POST phải viết hoa
    if request.method.__eq__('POST'):
        # Lấy username của người dùng so sanh với của request ( hãy người dùng nhập)
        username = request.form['username']
        password = request.form['password']
        # Truyền hàm chứng thực người dùng vào
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            #  về trang chủ
            return redirect('/')

    # get vào trang
    return render_template('login.html')
# Xoá trạng thái đặng nhập khỏi session
@app.route('/logout')
def logout_my_user():
    logout_user()
    # đằng xuất là về login
    return redirect('login')


if __name__ == '__main__':
    app.run(debug=True)  # port này thêm vào để làm port của /
