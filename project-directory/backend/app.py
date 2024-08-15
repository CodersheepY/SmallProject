from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'product_management'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'product_management'

mysql = MySQL(app)

# 在这里添加你的 Flask 路由
# 比如获取产品信息、更新销售、更新库存、删除产品等路由

if __name__ == '__main__':
    app.run(debug=True)
