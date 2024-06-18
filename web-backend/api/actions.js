const fs = require('fs');
const mongo = require('../tools/mongo.js');
const common = require('../tools/common.js');
const smartelo = require('../tools/smartelo.js');
const inventoryCheck = require('../tools/inventory-check.js');
const Ajv = require("ajv");
const ajv = new Ajv();
const jsonTemplate = require('./actions-template.json');
const XLSX = require("xlsx");


const {ObjectID} = require('mongodb');

module.exports = app => {
    app.get(`${process.env.SERVER_PATH}/actions`, async (req, res) => {
        console.log('[GET][/actions]: Start');

        const result = (req.authdata.role === 'admin') ?
            await mongo.find('actions', {}) :
            await mongo.find('actions', {'creatorId': req.authdata.id});

        console.log('[GET][/actions]: Actions found');
        console.log('[GET][/actions]: End');
        common.returnSuccess(res, 200, result);
    });

    app.post(`${process.env.SERVER_PATH}/actions`, async (req, res) => {
        console.log('[POST][/actions]: Start');

        req.body = req.body || {};
          
        const validate = ajv.compile(jsonTemplate)
        const valid = validate(req.body);
        if (!valid){
            console.log('[POST][/actions]: Invalid JSON schema format');
            console.log(validate.errors);
            return common.returnError(res, 400, 'Invalid JSON schema format.', 'bad_request');
        }

        const {inventory, actions} = req.body;
        
        const [inventoryItem] = await mongo.find('inventory', {$and: [{inventoryId: inventory}, {$or:[{public: true}, {'creatorId': req.authdata.id}]}]});

        if (!inventoryItem) {
            console.log('[POST][/actions]: Inventory not found');

            return common.returnError(res, 404, 'Inventory item not found.', 'not_found');
        }

        const {authdata} = req;

        const timestamp = new Date().getTime();
        
        try {
            const mongoResult = await mongo.insert('actions', {
                inventoryKey: inventoryItem._id,
                inventoryId: inventory,
                creator: authdata.user,
                creatorId: authdata.id.trim(),
                creationDate: timestamp,
                actions,
                smarteloFile: false
            });
            console.log('[POST][/actions]: Actions inserted');
            console.log('[POST][/actions]: End');

            common.returnSuccess(res, 201, mongoResult.ops[0]);
        } catch (err) {
            console.log(err)
            console.log('[POST][/actions]: Actions item insert failed');
            common.returnError(res, 404, 'Actions item insert failed', 'not_found');
        }
    });
    app.post(`${process.env.SERVER_PATH}/actions/:id/generateSmartelo`, async (req, res) => {
        
        const {id} = req.params;
        const inventoryPath = `${__dirname}/../input/inventory/`;
        const smarteloPath = `${__dirname}/../output/actions/smartelo_`;
        
        console.log('[POST][/actions/'  + id + '/generateSmartelo]: Start');
          
        const [actions] = (req.authdata.role === 'admin') ?
            await mongo.find('actions', {_id: new ObjectID(id)}) :
            await mongo.find('actions', {$and: [{_id: new ObjectID(id)}, {'creatorId': req.authdata.id}]});

        if (!actions) {
            console.log('[POST][/actions/'  + id + '/generateSmartelo]: Actions item not found');
            return common.returnError(res, 404, 'Actions item not found.', 'not_found');
        }

        if (actions.smarteloFile){
            console.log('[POST][/actions/'  + id + '/generateSmartelo]: Found existent Smartelo file')  
            res.download(`${smarteloPath}${id}.xlsm`);
            console.log('[POST][/actions/'  + id + '/generateSmartelo]: End');
        }

        const [inventory] = await mongo.find('inventory', {_id: actions.inventoryKey});

        if (!inventory){
            console.log('[POST][/actions/'  + id + '/generateSmartelo]: Inventory not found');
            return common.returnError(res, 404, 'Inventory file not found.', 'not_found');
        }

        if (!inventory.fileUrl){
            console.log('[POST][/actions/'  + id + '/generateSmartelo]: Inventory file not found');
            return common.returnError(res, 404, 'Inventory file not found.', 'not_found');
        }

        let parcelasJson, piesMayoresJson;

        if (inventory.type === 'xlsx'){
            const workbookInventory = XLSX.readFile(`${inventoryPath}${inventory.fileUrl}`, {cellStyles: true});
            parcelasJson = XLSX.utils.sheet_to_json(workbookInventory.Sheets['Parcelas'], { header: 1 });
            piesMayoresJson = XLSX.utils.sheet_to_json(workbookInventory.Sheets['PiesMayores'], { header: 1 });
            parcelasJson.shift();
            piesMayoresJson.shift();
        } else {
            parcelasJson = fs.readFileSync(`${inventoryPath}${inventory.fileUrl}`, "utf8");
            piesMayoresJson = fs.readFileSync(`${inventoryPath}${inventory.fileUrl2}`, "utf8");
            parcelasJson = inventoryCheck.parseCsv(parcelasJson);  
            piesMayoresJson = inventoryCheck.parseCsv(piesMayoresJson);  
        }

        const workbookTemplate = await smartelo.readTemplate();

        smartelo.insertInicio(parcelasJson[0], workbookTemplate.sheet('Inicio'));
        smartelo.insertCoordenadas(piesMayoresJson, workbookTemplate.sheet('Coordenadas'));
        smartelo.insertArboles(piesMayoresJson, workbookTemplate.sheet('Árboles'));
        smartelo.insertEquipos(req.authdata.user, actions.actions, workbookTemplate.sheet('Equipos'));
        smartelo.insertIndustrias(piesMayoresJson, workbookTemplate.sheet('Industrias'));
        smartelo.insertBiomasa(piesMayoresJson, workbookTemplate.sheet('Biomasa'));
        
        workbookTemplate.toFileAsync(`${smarteloPath}${id}.xlsm`)
            .then(() => {
                mongo.update('actions', { _id: new ObjectID(id) }, { smarteloFile: true });
                res.download(`${smarteloPath}${id}.xlsm`);
                console.log('[POST][/actions/'  + id + '/generateSmartelo]: End');
              })
              .catch(err => {
                console.error('[POST][/actions/'  + id + '/generateSmartelo]:' + err);
                return common.returnError(res, 404, 'Smartelo file not available', 'not_found');
              });
    });

    app.get(`${process.env.SERVER_PATH}/actions/:id`, async (req, res) => {

        const {id} = req.params;

        console.log('[GET][/actions/' + id + ']: Start');

        try {
            const [result] = (req.authdata.role === 'admin') ?
                await mongo.find('actions', {_id: new ObjectID(id)}) :
                await mongo.find('actions', {$and: [{_id: new ObjectID(id)}, {'creatorId': req.authdata.id}]});

            if (!result) {
                console.log('[GET][/actions/' + id + ']: Actions item not found');

                return common.returnError(res, 404, 'Actions item not found.', 'not_found');
            }
            console.log('[GET][/actions/' + id + ']: Actions item found');
            console.log('[GET][/actions/' + id + ']: End');

            common.returnSuccess(res, 200, result);
        } catch (err) {
            console.log('[GET][/actions/' + id + ']: Actions item not found');
            common.returnError(res, 404, 'Actions item not found', 'not_found');
        }
    });

    app.delete(`${process.env.SERVER_PATH}/actions/:id`, async (req, res) => {
        const {id} = req.params;
        console.log('[DELETE][/actions/' + id + ']: Start');

        try {
            const [result] = (req.authdata.role === 'admin') ?
                await mongo.find('actions', {_id: new ObjectID(id)}) :
                await mongo.find('actions', {$and: [{_id: new ObjectID(id)}, {'creatorId': req.authdata.id}]});

            if (!result) {
                console.log('[DELETE][/actions/' + id + ']: Action item not found');
                return common.returnError(res, 404, 'Action item not found.', 'not_found');
            }

            if (req.authdata.role !== 'admin') {
                await mongo.remove('actions', {$and: [{_id: new ObjectID(id)}, {'creatorId': req.authdata.id}]});
            } else {
                await mongo.remove('actions', {_id: new ObjectID(id)});
            }

            try {
                fs.unlinkSync(`${__dirname}/../output/actions/smartelo_` + id + `.xlsm`);
            } catch (err) {
                console.log(err);
            }

            console.log('[DELETE][/actions/' + id + ']: Action item deleted');
            console.log('[DELETE][/actions/' + id + ']: End');

            common.returnSuccess(res, 204);
        } catch (err) {
            console.log('[DELETE][/actions/' + id + ']: Action item not found');
            common.returnError(res, 404, 'Action item not found.', 'not_found');
        }
    });
};
