const fs = require('fs');
const mongo = require('../tools/mongo.js');
const common = require('../tools/common.js');
const ssh = require('../tools/ssh.js');
const jsonTemplate = require('./scenario-template.json')

const {ObjectID} = require('mongodb');

const _regexEscape = (str) => {
    return str.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&')
}

const _stepsToScenarioJSON = (steps, context) => {
    const {inventory, scenario} = context;
    const json = JSON.parse(JSON.stringify(jsonTemplate));

    json.operations[`operation_1`].model_path = context.modelPath;
    json.operations[`operation_1`].model_class = context.modelClass;

    steps.forEach(step => {
        json.operations[`operation_${Object.keys(json.operations).length}`] = {
            name: step.name,
            description: step.description,
            model_path: step.model.modelPath,
            model_class: step.model.modelClass,
            operation: step.model.operation,
            variables: step.variables
        };
    });

    let stringJSON = JSON.stringify(json, null, 2);

    const regex1 = new RegExp(`${_regexEscape('$OUTPUT_DIR')}`, 'g');
    const regex2 = new RegExp(`${_regexEscape('$INPUT_DIR')}`, 'g');
    const regex3 = new RegExp(`${_regexEscape('$INVENTORY_FILE')}`, 'g');

    stringJSON = stringJSON.replace(regex1, `${process.env.SCRATCH_PATH}${process.env.OUTPUT_SCRATCH_PATH}/${scenario._id}_`);
    stringJSON = stringJSON.replace(regex2, `${process.env.SCRATCH_PATH}${process.env.INPUT_SCRATCH_PATH}`);
    stringJSON = stringJSON.replace(regex3, `${inventory.fileUrl}`);

console.info(stringJSON);

    return stringJSON;
};

module.exports = app => {
    app.get(`${process.env.SERVER_PATH}/scenario`, async (req, res) => {
        console.log('[GET][/scenario]: Start');

        const result = (req.authdata.role === 'admin') ?
            await mongo.find('scenario', {}) :
            await mongo.find('scenario', {'creatorId': req.authdata.id})

        console.log('[GET][/scenario]: Scenarios found');
        console.log('[GET][/scenario]: End');

        for (let i = 0; i < result.length; i++) {

            // get inventory data by id
            invId = result[i]['inventoryId'];
            const [inventory] = await mongo.find('inventory', {_id: new ObjectID(invId)});
            if (inventory === undefined) {
                console.log('[GET][/scenario] inventory with id', invId, 'is undefined');
            }
            else {
                result[i]['inventoryName'] = inventory['name'];
            }

            // get creator data by id
            crId = result[i]['creatorId'];
            const [creator] = await mongo.find('user', {_id: new ObjectID(crId)});
            if (creator === undefined) {
                console.log('[GET][/scenario] creator with id', crId, 'is undefined');
            }
            else {
                result[i]['creatorName'] = creator['user'];
            }
        }

        common.returnSuccess(res, 200, result);
    });

    app.post(`${process.env.SERVER_PATH}/scenario`, async (req, res) => {
        console.log('[POST][/scenario]: Start');

        req.body = req.body || {};
        console.log('[POST][/scenario]: Body: ');
        console.log(req.body);

        let {steps, inventoryId, modelClass, modelPath} = req.body;
        steps = JSON.parse(steps);

        if (!steps[0].model) return common.returnError(res, 400, 'At least 1 step is necessary.', 'no_step');

        const [inventory] = await mongo.find('inventory', {_id: new ObjectID(inventoryId)});

        const timestamp = new Date().getTime();

        const jsonFile = `scenario_${timestamp}.json`;

        const {authdata} = req;

        const mongoResult = await mongo.insert('scenario', {
            inventoryId,
            steps,
            jsonFile,
            status: 'NOT_STARTED',
            creatorId: authdata.id.trim(),
            outputFile: null,
            jobId: null,
            modelClass,
            modelPath
        });
        console.log('[POST][/scenario]: Entry inserted');

        const scenario = mongoResult.ops[0];
        const fileContent = _stepsToScenarioJSON(steps, {
            scenario,
            inventory,
            modelClass,
            modelPath
        });

        fs.writeFileSync(`${__dirname}/../input/scenario/${jsonFile}`, fileContent);
        console.log('[POST][/scenario]: End');
        common.returnSuccess(res, 201, mongoResult.ops[0]);
    });

    app.get(`${process.env.SERVER_PATH}/scenario/:id`, async (req, res) => {
        const {id} = req.params;

        console.log('[POST][/scenario/' + id + ']: Start');

        try {

            const [result] = (req.authdata.role === 'admin') ?
                await mongo.find('scenario', {_id: new ObjectID(id)}) :
                await mongo.find('scenario', {$and: [{_id: new ObjectID(id)}, {'creatorId': req.authdata.id}]});

            if (!result) {
                console.log('[POST][/scenario/' + id + ']: Scenario item not found');

                return common.returnError(res, 404, 'Scenario item not found.', 'not_found');
            }
            console.log('[POST][/scenario/' + id + ']: End');

            common.returnSuccess(res, 200, result);
        } catch (err) {
            console.log('[POST][/scenario/' + id + ']: Scenario item not found');

            common.returnError(res, 404, 'Scenario item not found.', 'not_found');
        }
    });

    app.delete(`${process.env.SERVER_PATH}/scenario/:id`, async (req, res) => {
        const {id} = req.params;
        console.log('[DELETE][/scenario/' + id + ']: Start');

        try {
            const [result] = (req.authdata.role === 'admin') ?
                await mongo.find('scenario', {_id: new ObjectID(id)}) :
                await mongo.find('scenario', {$and: [{_id: new ObjectID(id)}, {'creatorId': req.authdata.id}]});


            if (!result) {
                console.log('[DELETE][/scenario/' + id + ']: Scenario item not found');

                return common.returnError(res, 404, 'Scenario item not found.', 'not_found');
            }

            // Clean all results.
            try {
                fs.unlinkSync(`${__dirname}/../input/scenario/${result.jsonFile}`)
            } catch (err) {
            }
            try {
                fs.unlinkSync(`${__dirname}/../output/${result.outputFile}`)
            } catch (err) {
            }

            (req.authdata.role === 'admin') ?
                await mongo.remove('scenario', {_id: new ObjectID(id)}) :
                await mongo.remove('scenario', {$and: [{_id: new ObjectID(id)}, {'creatorId': req.authdata.id}]});

            console.log('[DELETE][/scenario/' + id + ']: End');

            common.returnSuccess(res, 204);
        } catch (err) {
            console.log('[DELETE][/scenario/' + id + ']: Scenario item not found');

            common.returnError(res, 404, 'Scenario item not found.', 'not_found');
        }
    });

    app.post(`${process.env.SERVER_PATH}/scenario/:id/start`, async (req, res) => {
        const {id} = req.params;
        console.log('[POST][/scenario/' + id + '/start]: Start');

        const [scenario] = (req.authdata.role === 'admin') ?
            await mongo.find('scenario',  {_id: new ObjectID(id)}) :
            await mongo.find('scenario', {$and: [{_id: new ObjectID(id)}, {'creatorId': req.authdata.id}]});

        const [inventory] = (req.authdata.role === 'admin') ?
            await mongo.find('inventory', {_id: new ObjectID(scenario.inventoryId)}) :
            await mongo.find('inventory', {$and: [{_id: new ObjectID(scenario.inventoryId)}, {'creatorId': req.authdata.id}]});

        // Upload inventory files.
        // TODO: Add JSON support.
        await ssh.upload(`inventory/${inventory.fileUrl}`);

        // Upload scenario files.
        await ssh.upload(`scenario/${scenario.jsonFile}`);

        // Launch model
        const jobId = await ssh.initScenario(scenario.jsonFile, scenario._id);

        const mongoResult = await mongo.update('scenario', {_id: new ObjectID(id)}, {
            status: 'WAITING',
            jobId
        });
        console.log('[POST][/scenario/' + id + '/start]: Entry updated');

        console.log('[POST][/scenario/' + id + '/start]: End');

        common.returnSuccess(res, 200);
    });

    app.get(`${process.env.SERVER_PATH}/scenario/:id/result`, async (req, res) => {
        const {id} = req.params;
        console.log('[GET][/scenario/' + id + '/result]: Start');

        try {

            const [result] = (req.authdata.role === 'admin') ?
                await mongo.find('scenario', {_id: new ObjectID(id)}) :
                await mongo.find('scenario', {$and: [{_id: new ObjectID(id)}, {'creatorId': req.authdata.id}]});
            console.log('[GET][/scenario/' + id + '/result]: Scenario found');

            if (!result) {
                console.log('[GET][/scenario/' + id + '/result]: Scenario item not found');

                return common.returnError(res, 404, 'Scenario item not found.', 'not_found');
            }

            const {outputFile} = result;

            res.download(`${__dirname}/../output/${outputFile}`);
        } catch (err) {
            console.error(err);
            console.log('[GET][/scenario/' + id + '/result]: Scenario item not found');

            common.returnError(res, 404, 'Scenario item not found.', 'not_found');
        }
    });
};
