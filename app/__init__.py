from flask import Flask



app = Flask(__name__)

#import routernya ke app
from app.controller import routersdetailPinjaman
from app.controller import routers
from app.controller import routersautentication
from app.controller import routersbuktipeminjam
from app.controller import routersAccPinjamanWait
