    thCheck = threading.Thread(target=check, args=(updateCounter, data))
    thCheck.start()