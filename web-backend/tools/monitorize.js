const CHECK_FRECUENCY = 30 * 1000; // 30 seconds.
const mongo = require('./mongo.js');
const ssh = require('./ssh.js');

const { ObjectID } = require('mongodb');

setInterval(async () => {
    const notFinishedScenarios = await mongo.find('scenario', {
        status: { $nin: [ 'FINISHED', 'NOT_STARTED' ] }
    });

    if (notFinishedScenarios.length === 0) return;

    const jobsStatus = await ssh.squeue();

    console.info(notFinishedScenarios, jobsStatus);

    for (scenario of notFinishedScenarios) {
        const currentStatus = jobsStatus.filter((job) => (job.jobId === scenario.jobId))[0];
        
        if (currentStatus) {
            // Update item on mongo
            switch (currentStatus.status) {
                case 'R':
                    await mongo.update('scenario', { _id: new ObjectID(scenario._id) }, { status: 'RUNNING' });
                    break;
                default:
                    break;
            }
        } else {
            // Download results.
            console.info(`[Monitorize] Job finished - Updating scenario: ${scenario._id}`);
            await mongo.update('scenario', { _id: new ObjectID(scenario._id) }, { status: 'FINISHED', outputFile: `${scenario._id}.zip` });
            console.info(`[Monitorize] Job finished - Downloading results: ${scenario._id}`);
            await ssh.download(`${scenario._id}.zip`)
        }
    }
}, CHECK_FRECUENCY);
