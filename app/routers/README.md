# Routes

Each route serves a unique purpose; some are necessary for the functioning of others. The main idea is to have two types of routes: public ones and those that require authentication to access. To authenticate users, it’s necessary to register them and grant them access to those routes. This is done through the **/register** route, which creates the user in the database, primarily storing the username, email, and password.
