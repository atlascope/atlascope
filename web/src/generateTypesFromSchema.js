/* eslint-disable @typescript-eslint/no-var-requires */
const { generateApi } = require('swagger-typescript-api');
const axios = require('axios');
const path = require('path');

async function generateTypes(schemaUrl) {
  let schema;
  try {
    const res = await axios.get(schemaUrl);
    schema = res.data;
  } catch (e) {
    console.error(`Unable to obtain Swagger schema from the given URL: ${e}.`);
    process.exit(1);
  }

  // validate the provided schema is for Atlascope
  if (!schema.info || schema.info.title !== 'Atlascope') {
    console.error('OpenAPI schema at the given URL is not for Atlascope.');
    process.exit(1);
  }

  generateApi({
    name: 'AtlascopeTypes.ts',
    output: path.join(__dirname, 'generatedTypes'),
    url: schemaUrl,
    extractRequestParams: true,
    extractRequestBody: true,
    generateResponses: true,
    generateRouteTypes: true,
    generateClient: false,
  });
}

if (process.argv.length !== 3) {
  console.error('USAGE: generateTypes [schema url]');
  process.exit(1);
}

generateTypes(process.argv[2]);
