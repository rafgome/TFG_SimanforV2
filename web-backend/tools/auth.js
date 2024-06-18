const mongo = require('./mongo.js');
const common = require('./common.js');

const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

const SALT = 10;

const {ObjectID} = require('mongodb');

const _getUser = async (user, password) => {
    return new Promise(async (resolve, reject) => {
        console.log('[_getUser]: Start');
        const profiles = await mongo.find('user', {
            user
        });

        const [foundProfile] = profiles;

        if (!foundProfile || foundProfile.status === 'REQUESTED' || foundProfile.status === 'REFUSED') return reject();

        bcrypt.compare(password, foundProfile.password, (err, result) => {
            if (result === true) {
                console.log('[_getUser]: End');

                resolve(foundProfile);
            } else {
                console.log('[_getUser]: End with errors');

                reject();
            }
        });
    });
};

const _createUser = async (user, password, role, info) => {
    return new Promise(resolve => {
        console.log('[_createUser]: Start');

        bcrypt.hash(password, SALT, async (err, encrypted) => {
            const result = await mongo.insert('user', {
                user,
                password: encrypted,
                role,
                ...info
            });
            console.log('[_createUser]: End');

            resolve(result.ops[0]);
        });
    });
};

const _cleanSecurityData = users => {
    console.log('[_cleanSecurityData]: Start');

    if (Array.isArray(users)) {
        return users.map(user => {
            delete user.password;
            delete user.token;
            console.log('[_cleanSecurityData]: End');

            return user;
        });
    } else {
        delete users.password;
        delete users.token;
        console.log('[_cleanSecurityData]: End');

        return users;
    }
};

const PUBLIC_PATHS = [
    `POST:${process.env.SERVER_PATH}/login`,
    `POST:${process.env.SERVER_PATH}/register`
];

module.exports = app => {
    app.use((req, res, next) => {
        if (PUBLIC_PATHS.includes(`${req.method}:${req.url}`)) return next();

        const token = req.headers['authorization'];
        if (token) {
            jwt.verify(token, process.env.JWT_MASTER_TOKEN, (err, decoded) => {
                if (err) {

                    common.returnError(res, 401, 'Invalid authorization header.', 'not_authorized');
                } else {

                    req.authdata = decoded;
                    next();
                }
            });
        } else {

            common.returnError(res, 401, 'Invalid authorization header.', 'not_authorized');
        }
    });

    app.post(`${process.env.SERVER_PATH}/login`, async (req, res) => {
        const {user, password} = req.body;
        console.log('[GET][/login]: Start');

        if (!common.requiredParamsExist(user, password)) return common.returnError(res, 400, 'Required params not found.', 'required_params');

        let profile;

        try {
            profile = await _getUser(user, password);
        } catch (err) {
            console.log('[GET][/login]: User not found or password invalid.');

            return common.returnError(res, 401, 'User not found or password invalid.', 'incorrect_credentials');
        }

        const payload = {
            id: profile._id,
            user: profile.user,
            role: profile.role
        };

        const role = profile.role
        const token = jwt.sign(payload, process.env.JWT_MASTER_TOKEN, {
            expiresIn: '24h'
        });
        console.log('[GET][/login]: End');

        common.returnSuccess(res, 200, {
            token,
            role
        });
    });

    app.post(`${process.env.SERVER_PATH}/register`, async (req, res) => {
        console.log('[POST][/register]: Start');

        const {
            user,
            password,
            name,
            surname,
            center,
            department,
            email,
            phone,
            role
        } = req.body;

        if (!common.requiredParamsExist(
            user,
            password,
            name,
            surname,
            center,
            department,
            email,
            phone,
            role
        )) {
            console.log('[POST][/register]: Required params not found');

            return common.returnError(res, 400, 'Required params not found.','required_params');
        }

        const profiles = await mongo.find('user', {
            user,
            status: { $ne: 'REFUSED' }
        });
        console.log('[POST][/register]: User found');


        const [existProfile] = profiles;

        if (existProfile) {
            console.log('[POST][/register]: User already exists');

            return common.returnError(res, 409, 'User already exists.', 'user_already_exists');
        }

        const emails = await mongo.find('user', {
            email,
            status: { $ne: 'REFUSED' }
        });
        console.log('[POST][/register]: Email found');


        const [existEmail] = emails;

        if (existEmail) {
            console.log('[POST][/register]: Email already exists');

            return common.returnError(res, 409, 'Email already exists.', 'email_already_exists');
        }

        const status = "REQUESTED";

        const result = await _createUser(user, password, role, {
            name,
            surname,
            status,
            center,
            department,
            email,
            phone
        });
        console.log('[POST][/register]: End');

        common.returnSuccess(res, 201, _cleanSecurityData(result));
    });

    app.post(`${process.env.SERVER_PATH}/user/:id`, async (req, res) => {

        const {id} = req.params;
        console.log('[POST][/user/' + id + ']: Start');

        const {authdata} = req;
        if (authdata.role !== 'admin') {
            console.log('[POST][/register]: Invalid role.');

            return common.returnError(res, 403, 'Invalid role.', 'invalid_role');
        }

        const {status} = req.body;
        console.log('[POST][/user/' + id + ']: status: ' + status);

        try {
            const query = { _id: new ObjectID(id) };
            const [result] = await mongo.find("user", query);
            console.log('[POST][/user/' + id + ']: User found');

            if (!result) {
                console.log('[POST][/user/' + id + ']: User not found');
                return common.returnError(res, 404, 'User item not found.', 'not_found');
            }

            if(status === 'REQUESTED'){
                result.status = 'ACCEPTED';
            } else {
                result.status = status;
            }

            const updated = await mongo.update('user', {_id: new ObjectID(id)}, result)
            console.log('[POST][/user/' + id + ']: User updated');
            console.log('[POST][/user/' + id + ']: End');
            
            common.returnSuccess(res, 200, updated);
        } catch (err) {
            console.error(err);
            console.log('[POST][/user/' + id + ']: User item not found');

            common.returnError(res, 404, 'User item not found.', 'not_found');
        }
    });

    app.get(`${process.env.SERVER_PATH}/user`, async (req, res) => {
        console.log('[GET][/user]: Start');

        const {authdata} = req;
        if (authdata.role !== 'admin') {
            console.log('[GET][/user]: Invalid role.');

            return common.returnError(res, 403, 'Invalid role.', 'invalid_role');
        }

        const users = await mongo.find('user', { status: { $nin: ['REQUESTED', 'REFUSED'] } });
        console.log('[GET][/user]: End');

        common.returnSuccess(res, 200, _cleanSecurityData(users));
    });

    app.get(`${process.env.SERVER_PATH}/requested`, async (req, res) => {
        console.log('[GET][/requested]: Start');

        const {authdata} = req;
        if (authdata.role !== 'admin') {
            console.log('[GET][/requested]: Invalid role.');

            return common.returnError(res, 403, 'Invalid role.', 'invalid_role');
        }

        const users = await mongo.find('user', { status: 'REQUESTED' });
        console.log('[GET][/requested]: End');

        common.returnSuccess(res, 200, _cleanSecurityData(users));
    });

    app.delete(`${process.env.SERVER_PATH}/user/:id`, async (req, res) => {
        console.log('[DELETE][/user]: Start');

        const {authdata} = req;
        if (authdata.role !== 'admin') {
            console.log('[DELETE][/user]: Invalid role');

            return common.returnError(res, 403, 'Invalid role.', 'invalid_role');
        }

        const {id} = req.params;

        if(await mongo.find('inventory', {creatorId: id})) {
            await mongo.remove('inventory', {creatorId: id});
        }
        if(await mongo.find('actions', {creatorId: id})) {
            await mongo.remove('actions', {creatorId: id});
        }
        if(await mongo.find('model', {creatorId: id})) {
            await mongo.remove('model', {creatorId: id});
        }
        if(await mongo.find('scenario', {creatorId: id})) {
            await mongo.remove('scenario', {creatorId: id});
        }
        if(await mongo.find('user', {creatorId: id})) {
            await mongo.remove('user', {_id: new ObjectID(id)});
        }

        console.log('[DELETE][/user]: End');

        common.returnSuccess(res, 204);
    });

    app.get(`${process.env.SERVER_PATH}/me`, async (req, res) => {
        console.log('[GET][/me]: Start');

        const {authdata} = req;

        const {id} = authdata;

        const profiles = await mongo.find('user', {_id: new ObjectID(id)});

        const [existProfile] = profiles;

        if (!existProfile) {
            console.log('[GET][/me]: User not found');

            return common.returnError(res, 404, 'User not found.', 'not_found');
        }
        console.log('[GET][/me]: End');

        common.returnSuccess(res, 200, _cleanSecurityData(existProfile));
    });

    app.post(`${process.env.SERVER_PATH}/me/changepassword`, async (req, res) => {
        console.log('[POST][/me/changepassword]: Start');

        const {authdata} = req;
        const {user} = authdata;
        const {oldPassword, newPassword} = req.body;

        if (!common.requiredParamsExist(oldPassword, newPassword))  {
            console.log('[POST][/me/changepassword]: Required params not found');
            return common.returnError(res, 400, 'Required params not found.', 'required_params');
        }

        let currentUser;

        try {
            currentUser = await _getUser(user, oldPassword);
        } catch (err) {
            console.log('[POST][/me/changepassword]: Invalid old password');

            return common.returnError(res, 400, 'Invalid old password.', 'invalid_old_password');
        }

        bcrypt.hash(newPassword, SALT, async (err, encrypted) => {
            await mongo.update('user', {_id: new ObjectID(currentUser._id)}, {password: encrypted});
            console.log('[POST][/me/changepassword]: End');

            common.returnSuccess(res, 204);
        });
    });
};
