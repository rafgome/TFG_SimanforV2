if (!process.env.PRODUCTION) require('dotenv').config();

const express = require('express');
const bodyParser = require('body-parser')
const fileUpload = require('express-fileupload');
const swaggerUi = require('swagger-ui-express');
const cors = require('cors');
const YAML = require('yamljs');
const swaggerDocument = YAML.load('./docs/openapi.yaml');
const app = express();
const router = express.Router();

app.options('*', cors());
app.use(cors());

app.use(bodyParser.json());

app.use('/api-docs', swaggerUi.serve);
app.get('/api-docs', swaggerUi.setup(swaggerDocument));

app.use(fileUpload());

require('./tools/auth.js')(app);

app.get('/', (req, res) => {
  res.send('Hello World');
});

require('./tools/monitorize.js');
require('./api/actions.js')(app);
require('./api/inventory.js')(app);
require('./api/model.js')(app);
require('./api/scenario.js')(app);

const PORT = process.env.PORT || 3000;

app.listen(PORT);
