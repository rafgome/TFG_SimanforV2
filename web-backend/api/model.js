const fs = require('fs');
const mongo = require('../tools/mongo.js');
const common = require('../tools/common.js');

const {ObjectID} = require('mongodb');

module.exports = app => {
    app.get(`${process.env.SERVER_PATH}/model`, async (req, res) => {

        console.log('[GET][/model]: Start');
        let result;

        if (req.query['type'] === 'projection' || req.query['type'] === 'cutting') {
            console.log('[GET][/model]: Querying model with type ' + req.query['type']);
            result = await mongo.find('model', {'type': req.query['type']});
        } else {
            if (req.authdata.role.toLowerCase() === 'basic') {
                console.log('[GET][/model]: Querying model with type proyection for basic user');
                result = await mongo.find('model', {'type': 'projection'});
            } else {
                console.log('[GET][/model]: Querying model without query for admin user');
                result = await mongo.find('model', {});
            }
        }

        console.log('[GET][/model]: Models found');
        console.log('[GET][/model]: End');

        common.returnSuccess(res, 200, result);
    });

    app.post(`${process.env.SERVER_PATH}/model`, async (req, res) => {
        console.log('[POST][/model]: Start');

        if (req.authdata.role !== 'admin') {
            console.log('[POST][/model]: Invalid role.');

            return common.returnError(res, 403, 'Invalid role.', 'invalid_role');
        }

        req.body = req.body || {};
        const {
            name,
            description,
            type,
            docs,
            status,
            modelPath,
            modelClass,
            operation,
            specie,
            applicationArea,
            executionPeriod,
            operatingDimensions
        } = req.body;

        if (!common.requiredParamsExist(
            name,
            description,
            type,
            docs,
            status,
            modelPath,
            modelClass,
            operation,
            specie,
            applicationArea,
            executionPeriod,
            operatingDimensions
        )) {
            console.log('[POST][/model]: Required params not found');
            return common.returnError(res, 400, 'Required params not found.', 'required_params');
        }

        const {authdata} = req;

        const mongoResult = await mongo.insert('model', {
            name,
            description,
            type,
            docs,
            status,
            modelPath,
            modelClass,
            creatorId: authdata.id.trim(),
            operation,
            specie,
            applicationArea,
            executionPeriod,
            operatingDimensions
        });
        console.log('[POST][/model]: End');

        common.returnSuccess(res, 201, mongoResult.ops[0]);
    });

    app.post(`${process.env.SERVER_PATH}/model/:id`, async (req, res) => {

        req.body = req.body || {};

        if (req.authdata.role !== 'admin') {
            console.log('[POST][/model]: Invalid role.');

            return common.returnError(res, 403, 'Invalid role.', 'invalid_role');
        }

        const {
            name,
            description,
            type,
            docs,
            status,
            modelPath,
            modelClass,
            operation,
            specie,
            applicationArea,
            executionPeriod,
            operatingDimensions
        } = req.body;
        const {id} = req.params;
        console.log('[POST][/model' + id + ']: Start');

        try {
            const [result] = await mongo.find('model', {_id: new ObjectID(id)});
            if (!result) {
                console.log('[POST][/model' + id + ']: Model item not found');

                return common.returnError(res, 404, 'Model item not found.', 'not_found');
            }

            if (name) result.name = name;
            if (description) result.description = description;
            if (type) result.type = type;
            if (docs) result.docs = docs;
            if (status) result.status = status;
            if (modelPath) result.modelPath = modelPath;
            if (modelClass) result.modelClass = modelClass;
            if (operation) result.operation = operation;
            if (specie) result.specie = specie;
            if (applicationArea) result.applicationArea = applicationArea;
            if (executionPeriod) result.executionPeriod = executionPeriod;
            if (operatingDimensions) result.operatingDimensions = operatingDimensions;

            const updated = await mongo.update('model', {_id: new ObjectID(id)}, result)
            console.log('[POST][/model' + id + ']: Model updated');
            console.log('[POST][/model' + id + ']: End');

            common.returnSuccess(res, 200, result);
        } catch (err) {
            console.log('[POST][/model' + id + ']: Model item not found');

            common.returnError(res, 404, 'Model item not found.', 'not_found');
        }

    });

    app.get(`${process.env.SERVER_PATH}/model/:id`, async (req, res) => {
        const {id} = req.params;
        console.log('[GET][/model' + id + ']: Start');

        try {
            const [result] = await mongo.find('model', {_id: new ObjectID(id)});
            console.log('[GET][/model' + id + ']: Model found');

            if (!result) {
                console.log('[GET][/model' + id + ']: Model item not found');

                return common.returnError(res, 404, 'Model item not found.', 'not_found');
            }
            console.log('[GET][/model' + id + ']: End');

            common.returnSuccess(res, 200, result);
        } catch (err) {
            console.log('[GET][/model' + id + ']: Model item not found');

            common.returnError(res, 404, 'Model item not found.', 'not_found');
        }
    });

    app.delete(`${process.env.SERVER_PATH}/model/:id`, async (req, res) => {
        const {id} = req.params;
        console.log('[DELETE][/model' + id + ']: Start');
        if (req.authdata.role !== 'admin') {
            console.log('[DELETE][/model]: Invalid role.');

            return common.returnError(res, 403, 'Invalid role.', 'invalid_role');
        }
        try {
            const [result] = await mongo.find('model', {_id: new ObjectID(id)});

            if (!result) {
                console.log('[DELETE][/model' + id + ']: Model item not found');

                return common.returnError(res, 404, 'Model item not found.', 'not_found');
            }

            await mongo.remove('model', {_id: new ObjectID(id)});
            console.log('[DELETE][/model' + id + ']: Model found');
            console.log('[DELETE][/model' + id + ']: End');

            common.returnSuccess(res, 204);
        } catch (err) {
            console.log('[DELETE][/model' + id + ']: Model item not found');

            common.returnError(res, 404, 'Model item not found.', 'not_found');
        }
    });
};
