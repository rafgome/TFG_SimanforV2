const fs = require('fs')

const returnError = (res, code, message, string_code) => {
    res.status(code).send({
        success: false,
        code,
        message,
        string_code
    });
};

const returnSuccess = (res, code, data) => {
    res.status(code).send({
        success: true,
        data
    });  
}

const _regexEscape = (str) => {
    return str.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&')
}

const updateOnFile = async (path, searchItem, value) => {
    return new Promise((resolve, reject) => {
        fs.readFile(path, 'utf8', (err, data) => {
            if (err) {
                console.error(err);
                reject();
                return 
            }

            const regex = new RegExp(`${_regexEscape(searchItem)}`, 'g');
            const result = data.replace(regex, value);

            fs.writeFile(path, result, 'utf8', (err) => {
                if (err) {
                    console.error(err);
                    reject();
                    return 
                }

                resolve();
            });
        });
    });
}

const requiredParamsExist = (...args) => {
    let paramUndefined = false;

    args.forEach(arg => {
        if (!arg) paramUndefined = true;
    });

    return !paramUndefined;
};

module.exports = {
    returnSuccess,
    returnError,
    requiredParamsExist,
    updateOnFile
}
