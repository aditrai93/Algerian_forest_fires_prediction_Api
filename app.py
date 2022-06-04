import pickle
from flask import Flask, request,app,jsonify,render_template
import numpy as np
import logging
logging.basicConfig(filename = 'logfile1.log', level = logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
import mysql.connector as conn
import pandas as pd

app = Flask(__name__)
model1=pickle.load(open('class_model1.pkl','rb'))
model2=pickle.load(open('reg_model.pkl','rb'))

@app.route('/')
def home():
    #return 'Hello World'
    return render_template('home.html')

@app.route('/new_api',methods=['POST'])
def new_api():
    try:
        data=request.json['data1']
        print(data)
        new_value=[list(data.values())]
        output=model1.predict(new_value)[0]
        logging.info("prediction %s", str(output))
        return jsonify(output)
    except Exception as e:
        logging.exception("Exception is " + str(e))


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = [float(x) for x in request.form.values()]
        final_features = [np.array(data)]
        print(data)

        output = model1.predict(final_features)[0]
        print(output)
        logging.info("prediction %s", str(output))
        # output = round(prediction[0], 2)
        return render_template('home.html', prediction_text="Forest fire prediction is  {}".format(output))
    except Exception as e:
        logging.exception("Exception is " + str(e))

@app.route('/predict_temp', methods=['POST'])
def predict_temp():
    try:
        data = [float(x) for x in request.form.values()]
        final_features = [np.array(data)]
        print(data)

        output = model2.predict(final_features)[0]
        print(output)
        logging.info("prediction %s", str(output))
        # output = round(prediction[0], 2)
        return render_template('home.html', prediction_text2="Temperature prediction is  {}".format(output))
    except Exception as e:
        logging.exception("Exception is " + str(e))

@app.route('/pred_temp_batch', methods=['POST'])
def pred_temp_batch():
    try:
        data = [str(x) for x in request.form.values()]
        mydb = conn.connect(host='localhost', user=data[0], passwd=data[1],database=data[2])
        print(mydb)
        my_cursor = mydb.cursor()
        my_cursor.execute('Use '+data[2])
        my_cursor.execute("SELECT * from " + data[3])
        sql_data = pd.DataFrame(my_cursor.fetchall())
        sql_data.columns = my_cursor.column_names
        sql_data.drop('index', axis=1, inplace=True)    #if you have index col
        output=model2.predict(sql_data)
        print(output)
        logging.info("prediction %s", str(output))
        return render_template('home.html', prediction_text3="Temperature prediction are  {}".format(output))

    except Exception as e:
        logging.exception("Exception is " + str(e))


@app.route('/pred_fire_batch', methods=['POST'])
def pred_fire_batch():
    try:
        data = [str(x) for x in request.form.values()]
        mydb = conn.connect(host='localhost', user=data[0], passwd=data[1],database=data[2])
        print(mydb)
        my_cursor = mydb.cursor()
        my_cursor.execute('Use '+data[2])
        my_cursor.execute("SELECT * from " + data[3])
        sql_data = pd.DataFrame(my_cursor.fetchall())
        sql_data.columns = my_cursor.column_names
        sql_data.drop('index', axis=1, inplace=True)    #if you have index col
        output=model1.predict(sql_data)
        print(output)
        logging.info("prediction %s", str(output))
        return render_template('home.html', prediction_text3="Forest Fire prediction are  {}".format(output))

    except Exception as e:
        logging.exception("Exception is " + str(e))




if __name__=="__main__":
    app.run(debug=True)