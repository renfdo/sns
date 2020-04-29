class Connection:

    host = None
    db = None
    user = None
    password = None

    @staticmethod
    def set_connection(host, db, user, password):

        if any([Connection.host, Connection.db, Connection.user, Connection.password]) is False:
            Connection.host = host
            Connection.db = db
            Connection.user = user
            Connection.password = password

    @staticmethod
    def set_connection_dict(dict_obj):

        if any([Connection.host, Connection.db, Connection.user, Connection.password]) is False:
            Connection.host = dict_obj['host']
            Connection.db = dict_obj['db']
            Connection.user = dict_obj['user']
            Connection.password = dict_obj['password']
