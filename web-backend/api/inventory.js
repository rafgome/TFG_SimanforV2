const fs = require('fs');
const mongo = require('../tools/mongo.js');
const common = require('../tools/common.js');
const inventoryCheck = require('../tools/inventory-check.js');
const XLSX = require("xlsx");

const {ObjectID} = require('mongodb');

module.exports = app => {
    app.get(`${process.env.SERVER_PATH}/inventory`, async (req, res) => {
        console.log('[GET][/inventory]: Start');

        const filter = {};
        
        if (req.query.smartelo) {
            filter['smartelo'] = (req.query.smartelo === 'true');
        }

        if (req.authdata.role !== 'admin'){
            filter['$or'] = [{'creatorId': req.authdata.id}, {'public': true}];
        }

        const result = await mongo.find('inventory', filter);

        console.log('[GET][/inventory]: Inventories found');
        console.log('[GET][/inventory]: End');
        common.returnSuccess(res, 200, result);
    });

    app.post(`${process.env.SERVER_PATH}/inventory`, async (req, res) => {
        console.log('[POST][/inventory]: Start');

        req.body = req.body || {};

        const {name, type, year, public, smartelo} = req.body;

        if (!req.files) {
            console.log('[POST][/inventory]: Required params not found');
            return common.returnError(res, 400, 'Required params not found.', 'required_params');
        }

        const {csvTree, csvPlot, xlsx} = req.files;
        const {authdata} = req;

        if (!common.requiredParamsExist(
            name,
            type,
            year,
            public,
            smartelo
        )) {
            console.log('[POST][/inventory]: Required params not found');
            return common.returnError(res, 400, 'Required params not found.', 'required_params');
        }


        const timestamp = new Date().getTime();
        let fileUrl, fileUrl2, inventoryId, mongoResult;

        switch (type) {
            case 'csv':

                [fileUrl, fileUrl2] = [`plot_${timestamp}.csv`, `tree_${timestamp}.csv`];

                await csvPlot.mv(`${__dirname}/../input/inventory/${fileUrl}`);
                await csvTree.mv(`${__dirname}/../input/inventory/${fileUrl2}`);

                const [csvPlotData, csvTreeData] = await Promise.all([
                    fs.promises.readFile(`${__dirname}/../input/inventory/${fileUrl}`, 'utf8').then(inventoryCheck.parseCsv),
                    fs.promises.readFile(`${__dirname}/../input/inventory/${fileUrl2}`, 'utf8').then(inventoryCheck.parseCsv)
                  ]);
                
                if (smartelo  === 'true' && !inventoryCheck.validateCsv(csvPlotData, csvTreeData)){
                    console.log('[POST][/inventory]: Invalid CSV schema format');
                    return common.returnError(res, 400, 'CSV schema format.', 'bad_request');
                }
                
                inventoryId = smartelo  === 'true' ? Object.values(csvTreeData[0])[0] : '-';
                break;
            case 'xlsx':
                fileUrl = `inventory_${timestamp}.xlsx`;
                await xlsx.mv(`${__dirname}/../input/inventory/${fileUrl}`);
                const workbook = XLSX.read(xlsx.data);

                if (smartelo  === 'true' && !inventoryCheck.validateXlsx(workbook)){
                    console.log('[POST][/inventory]: Invalid XLSX schema format');
                    return common.returnError(res, 400, 'XLSX schema format.', 'bad_request');
                }

                inventoryId = smartelo  === 'true' ? workbook.Sheets[workbook.SheetNames[0]]['A2'].v : '-';
                break;
            default:
                console.log('[POST][/inventory]: Type not found');
                return common.returnError(res, 404, 'Type not found.', 'type_not_found');
        }
        
        const [existentInventory] = await mongo.find('inventory', { $and: [{ inventoryId }, { $or: [{ public: true }, { creatorId: authdata.id }] }] });
        if (smartelo === 'true' && existentInventory) {
          console.log('[POST][/inventory]: Inventory already exists');
          return common.returnError(res, 409, 'Inventory already exists.', 'inventory_already_exists');
        }

        const inventoryData = {
            inventoryId,
            name,
            year,
            creator: authdata.user,
            creatorId: authdata.id.trim(),
            creationDate: timestamp,
            public: (public === 'true'),
            smartelo: (smartelo === 'true'),
            fileUrl,
            fileUrl2,
            type
        };

        mongoResult = await mongo.insert('inventory', inventoryData);
        console.log('[POST][/inventory]: Inventory inserted');
        console.log('[POST][/inventory]: End');

        common.returnSuccess(res, 201, mongoResult.ops[0]);
    });

    app.post(`${process.env.SERVER_PATH}/inventory/:id`, async (req, res) => {

        req.body = req.body || {};
        const {name, year, public, smartelo} = req.body;
        const {id} = req.params;
        console.log('[POST][/inventory/' + id + ']: Start');
        try {
            const query = {
                _id: new ObjectID(id),
                ...(req.authdata.role === "admin" ? {} : { creatorId: req.authdata.id }),
              };
            const [result] = await mongo.find("inventory", query);
            console.log('[POST][/inventory/' + id + ']: Inventory found');

            if (!result) {
                console.log('[POST][/inventory/' + id + ']: Inventory not found');
                return common.returnError(res, 404, 'Inventory item not found.', 'invalid_role');
            }

            result.name = name || result.name;
            result.year = year || result.year;
            result.public = public ? (public === "true") : result.public;
            result.smartelo = smartelo ? (smartelo === "true") : result.smartelo;

            if (result.type === 'xlsx'){
                const file = XLSX.readFile(`${__dirname}/../input/inventory/${result.fileUrl}`);
                if (result.smartelo && !inventoryCheck.validateXlsx(file)){
                    console.log('[POST][/inventory]: Invalid XLSX schema format');
                    return common.returnError(res, 400, 'XLSX schema format.', 'bad_request');
                }
                result.inventoryId = result.smartelo ? file.Sheets[file.SheetNames[0]]["A2"].v : result.inventoryId;
            }

            if (result.type === 'csv') {
                const file = fs.readFileSync(`${__dirname}/../input/inventory/${result.fileUrl}`, "utf8");
                const file2 = fs.readFileSync(`${__dirname}/../input/inventory/${result.fileUrl2}`, "utf8");
                const parsedFile = inventoryCheck.parseCsv(file);
                const parsedFile2 = inventoryCheck.parseCsv(file2);
                if (result.smartelo && !inventoryCheck.validateCsv(parsedFile, parsedFile2)){
                    console.log('[POST][/inventory]: Invalid CSV schema format');
                    return common.returnError(res, 400, 'CSV schema format.', 'bad_request');
                }
                result.inventoryId = result.smartelo ? Object.values(parsedFile[0])[0] : result.inventoryId;
            } 

            const updated = await mongo.update('inventory', {_id: new ObjectID(id)}, result)
            console.log('[POST][/inventory/' + id + ']: Inventory updated');
            console.log('[POST][/inventory/' + id + ']: End');

            common.returnSuccess(res, 200, updated);
        } catch (err) {
            console.error(err);
            console.log('[POST][/inventory/' + id + ']: Inventory item not found');

            common.returnError(res, 404, 'Inventory item not found.', 'not_found');
        }
    });

    app.get(`${process.env.SERVER_PATH}/inventory/:id`, async (req, res) => {

        const {id} = req.params;

        console.log('[GET][/inventory/' + id + ']: Start');

        try {
            const [result] = (req.authdata.role === 'admin') ?
                await mongo.find('inventory', {_id: new ObjectID(id)}) :
                await mongo.find('inventory', {$and: [{_id: new ObjectID(id)}, {$or:[{public: true}, {'creatorId': req.authdata.id}]}]});

            if (!result) {
                console.log('[GET][/inventory/' + id + ']: Inventory item not found');

                return common.returnError(res, 404, 'Inventory item not found.', 'not_found');
            }
            console.log('[GET][/inventory/' + id + ']: Inventory found');
            console.log('[GET][/inventory/' + id + ']: End');

            common.returnSuccess(res, 200, result);
        } catch (err) {
            console.log('[GET][/inventory/' + id + ']: Inventory item not found');

            common.returnError(res, 404, 'Inventory item not found.', 'not_found');
        }
    });

    app.delete(`${process.env.SERVER_PATH}/inventory/:id`, async (req, res) => {
        const {id} = req.params;
        console.log('[DELETE][/inventory/' + id + ']: Start');

        try {
            const [result] = (req.authdata.role === 'admin') ?
                await mongo.find('inventory', {_id: new ObjectID(id)}) :
                await mongo.find('inventory', {$and: [{_id: new ObjectID(id)}, {'creatorId': req.authdata.id}]});

            if (!result) {
                console.log('[DELETE][/inventory/' + id + ']: Inventory item not found');

                return common.returnError(res, 404, 'Inventory item not found.', 'not_found');
            }

            // Clean all input files.
            try {
                fs.unlinkSync(`${__dirname}/../input/inventory/${result.fileUrl}`)
            } catch (err) {
                console.log(err)
            }

            if (req.authdata.role !== 'admin') {
                await mongo.remove('inventory', {$and: [{_id: new ObjectID(id)}, {'creatorId': req.authdata.id}]});
            } else {
                await mongo.remove('inventory', {_id: new ObjectID(id)});
            }

            console.log('[DELETE][/inventory/' + id + ']: Inventory item deleted');
            console.log('[DELETE][/inventory/' + id + ']: End');

            common.returnSuccess(res, 204);
        } catch (err) {
            console.log('[DELETE][/inventory/' + id + ']: Inventory item not found');

            common.returnError(res, 404, 'Inventory item not found.', 'not_found');
        }
    });

    app.get(`${process.env.SERVER_PATH}/inventory/:id/download`, async (req, res) => {
        const {id} = req.params;
        try {
            const [result] = (req.authdata.role === 'admin') ?
                await mongo.find('inventory', {_id: new ObjectID(id)}) :
                await mongo.find('inventory', {$and: [{_id: new ObjectID(id)}, {$or:[{public: true}, {'creatorId': req.authdata.id}]}]});

            if (!result) {
                return common.returnError(res, 404, 'Inventory item not found.', 'not_found');
            }

            const {fileUrl} = result;

            res.download(`${__dirname}/../input/inventory/${fileUrl}`);
        } catch (err) {
            console.error(err);
            common.returnError(res, 404, 'Inventory item not found.', 'not_found');
        }
    });
};
