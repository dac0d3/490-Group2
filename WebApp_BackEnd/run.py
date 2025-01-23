from astrocultivators import socket, app

if __name__ == '__main__':
    host = '130.166.24.225'

    # socket.run(app, host=host, port=5000, debug=True)
    socket.run(app, debug=True) # run local
    
    