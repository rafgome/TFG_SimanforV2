const Client = require('ssh2').Client;
const scpClient = require('scp2');

const conn = new Client();

let connReady = false;

const waitingActions = [
    /*
        cb(),
        cb(),
        ...
    */
];

const _checkConnectionOkOrWait = (cb) => {
    if (!connReady) {
        _connect();
        return waitingActions.push(cb);
    }

    cb();
};

const _connect = () => {
    conn.connect({
      host: process.env.SSH_HOST,
      port: process.env.SSH_PORT,
      username: process.env.SSH_USERNAME,
      password: process.env.SSH_PASSWORD,
      tryKeyboard: true
    });
}

conn.on('ready', () => {
    connReady = true;

    waitingActions.forEach(actionCb => {
        actionCb();
    });
});

conn.on('end', () => {
    connReady = false;
});

const launchCommand = (command) => {
    _checkConnectionOkOrWait(() => {
        conn.exec(command, (err, stream) => {
            if (err) throw err;

            stream.on('close', (code, signal) => {
                console.log('Stream :: close :: code: ' + code + ', signal: ' + signal);
            }).on('data', (data) => {
                console.info(data.toString());
                console.log('STDOUT: ' + data);
            }).stderr.on('data', (data) => {
                console.log('STDERR: ' + data);
            });
        });
    });
};

const squeue = async () => new Promise((resolve, reject) => {
    _checkConnectionOkOrWait(() => {
        const command = `squeue`;
        let result = null;

        conn.exec(command, (err, stream) => {
            if (err) throw err;

            stream.on('close', (code, signal) => {
                console.log('Stream :: close :: code: ' + code + ', signal: ' + signal);
                resolve(result);
            }).on('data', (data) => {
                const output = data.toString();
                result = _parseSqueue(output);

                console.log('STDOUT: ' + data);
            }).stderr.on('data', (data) => {
                console.log('STDERR: ' + data);
            });
        });
    });
});

const initScenario = async (experimentFile, experimentId) => new Promise((resolve, reject) => {
    _checkConnectionOkOrWait(() => {
        const command = `sbatch $HOME/auto/launch.sh ${experimentFile} ${experimentId}`;
        let jobId = '';

        conn.exec(command, (err, stream) => {
            if (err) throw err;

            stream.on('close', (code, signal) => {
                console.log('Stream :: close :: code: ' + code + ', signal: ' + signal);
                resolve(jobId);
            }).on('data', (data) => {
                const output = data.toString();
                jobId = output.match('job (.*)\n')[1];

                console.log('STDOUT: ' + data);
            }).stderr.on('data', (data) => {
                console.log('STDERR: ' + data);
            });
        });
    });
});

const _parseSqueue = string => {
    const array = [];

    const lines = string.split('\n');
    lines.forEach((line, index) => {
        if (index === 0 || line === '') return;
        const values = line.match('            (.*)   (.*) (.*) (.*)  (.*)       (.*)      (.*) (.*)');
        if (values === null)
            return;
        array.push({
            jobId: values[1],
            partition: values[2],
            name: values[3],
            user: values[4],
            status: values[5],
            time: values[6],
            nodes: values[7],
            nodelist: values[8]
        });
    });

    return array;
};

const upload = async filename => new Promise((resolve, reject) => {
    const config = {
        host: process.env.SSH_HOST,
        port: process.env.SSH_PORT,
        username: process.env.SSH_USERNAME,
        password: process.env.SSH_PASSWORD,
        path: `${process.env.SCRATCH_PATH}${process.env.INPUT_SCRATCH_PATH}`
    };
    const filePath = `${__dirname}/../input/${filename}`;

    console.info(`[SSH] Local input path: ${filePath}`);

    scpClient.scp(filePath, config, (err) => {
        if (err) {
            console.error(err);
            reject();
            return;
        }

        resolve();
    });
});

const download = async filename => new Promise((resolve, reject) => {
    const config = {
        host: process.env.SSH_HOST,
        port: process.env.SSH_PORT,
        username: process.env.SSH_USERNAME,
        password: process.env.SSH_PASSWORD,
        path: `${process.env.SCRATCH_PATH}${process.env.OUTPUT_SCRATCH_PATH}/${filename}`
    };
    const filePath = `${__dirname}/../output/`;

    console.info(`[SSH] Local ouput path: ${filePath}`);

    scpClient.scp(config, filePath, (err) => {
        if (err) {
            console.error(err);
            reject();
            return;
        }

        resolve();
    });
});

module.exports = {
    upload,
    download,
    initScenario,
    squeue,
    launchCommand
}