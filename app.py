from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Koneksi ke database MongoDB
client = MongoClient('mongodb+srv://michaelraphael710:Ykoxx859v9U3ghYB@clustertraining.plgnk.mongodb.net/')
db = client['marketplace']
collection = db['products']


# Route untuk halaman utama
@app.route('/')
def index():
    # Ambil semua produk dari MongoDB
    products = collection.find()
    return render_template('index.html', products=products)


# Route untuk menambahkan produk baru
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        # Tambahkan produk ke MongoDB dan simpan ID produk yang baru saja ditambahkan
        result = collection.insert_one({'name': name, 'price': price, 'description': description})
        # Redirect ke halaman view_product
        return redirect(url_for('view_product', id=result.inserted_id))
    return render_template('add_product.html')



# Route untuk menghapus produk
@app.route('/delete_product/<id>')
def delete_product(id):
    # Hapus produk berdasarkan ID
    collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))


# Route untuk mengedit produk
@app.route('/edit_product/<id>', methods=['GET', 'POST'])
def edit_product(id):
    product = collection.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        # Perbarui produk berdasarkan ID
        collection.update_one({'_id': ObjectId(id)}, {'$set': {'name': name, 'price': price, 'description': description}})
        return redirect(url_for('index'))
    return render_template('edit_product.html', product=product)

@app.route('/view_product/<id>')
def view_product(id):
    # Cari produk berdasarkan ID
    product = collection.find_one({'_id': ObjectId(id)})
    return render_template('view_product.html', product=product)



if __name__ == '__main__':
    app.run(debug=True)
