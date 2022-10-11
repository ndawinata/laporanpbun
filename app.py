from flask import Flask, render_template, request, make_response, session, redirect, url_for, flash, abort, jsonify, send_file
import os
from sys import prefix
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, false, insert, text, Table, Column, Integer, String, Float, MetaData, true
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

app.secret_key = '5eb1d440a0ea8d97df5bf481faa7b117479de6cd4c99510f688497d165c589ca'

# upload gambar
app.config['UPLOAD_FOLDER'] = 'static'

engine = create_engine('mysql+pymysql://bmkgpang_nanda:bmkgpanglaporan@localhost/bmkgpang_laporan_shift')

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    qpg = 'SELECT * FROM petugas'
    pg = pd.read_sql(qpg, con=engine)
    
    qpagi = 'SELECT * FROM pagi'
    pagi = pd.read_sql(qpagi, con=engine)
    
    qsiang = 'SELECT * FROM siang'
    siang = pd.read_sql(qsiang, con=engine)
    
    qmalam = 'SELECT * FROM malam'
    malam = pd.read_sql(qmalam, con=engine)
    
    qshift = 'SELECT * FROM shift'
    shift = pd.read_sql(qshift, con=engine)
    
    qData = 'SELECT tgl, petugas, shift, jobdesk FROM laporan ORDER BY tgl DESC LIMIT 15'
    laporan = pd.read_sql(qData, con=engine)
    laporan['tanggal'] = laporan['tgl'].dt.strftime('%d-%m-%Y %H:%M:%S')
    lapor = laporan[['tanggal','petugas','shift','jobdesk']].sort_values(by=['tanggal'],ascending=False)
    
    arrPegawai = pg['nama'].to_numpy()
    arrPagi = pagi['keterangan'].to_numpy()
    arrSiang = siang['keterangan'].to_numpy()
    arrMalam = malam['keterangan'].to_numpy()
    arrShift = shift['keterangan'].to_numpy()
    arrLaporan = lapor.iloc[:].to_numpy()
    # arrLaporan = laporan.iloc[:]
    # print(arrLaporan)
    
    data = {
        'pegawai':arrPegawai.tolist(),
        'pagi':arrPagi.tolist(),
        'siang':arrSiang.tolist(),
        'malam':arrMalam.tolist(),
        'shift':arrShift.tolist(),
        'laporan':arrLaporan.tolist()
    }
    
    return render_template('dashboard.html', data=data)

@app.route('/laporan', methods=['GET', 'POST'])
def postData():
    if request.method == 'POST':
        req = request.json
        
        metadata_obj = MetaData()
        laporan_table = Table(
                "laporan",
                metadata_obj,
                Column('id', Integer, primary_key=True),
                Column('tgl', String),
                Column('shift', String),
                Column('jobdesk', String),
                Column('petugas', String),
            )

            

        stmt = insert(laporan_table).values(
            tgl=req['tgl'], 
            shift=req['shift'], 
            jobdesk=req['job'], 
            petugas=req['petugas'], 
        )

        compiled = stmt.compile()

        with engine.connect() as conn:
            result = conn.execute(stmt)
                
        return result
        
    
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    # socketio.run(app)
    # app.run(host='0.0.0.0', debug=True, port=80)
    app.run(host='0.0.0.0', debug=True, port=5000)
# serve(app, host='0.0.0.0', port=5000)
