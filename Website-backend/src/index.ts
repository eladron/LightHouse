import axios from 'axios';
import cors from 'cors';
import * as dotenv from 'dotenv';
import express, {Express, Request, Response} from 'express';
import {calcPlacements} from './routes.js';
import multer, { Multer } from 'multer';
import fs from 'fs';
import https from 'https';

var privateKey  = fs.readFileSync('/home/migdalor/LightHouse/keystore/private.key', 'utf8');
var certificate = fs.readFileSync('/home/migdalor/LightHouse/keystore/certificate.crt', 'utf8');

var credentials = {key: privateKey, cert: certificate};

const app: Express = express();
const upload: Multer = multer();

app.use(express.json());

const port = process.env.PORT || 443;

app.use(cors({credentials: true, origin: true}));

app.post('/api/calculate',  upload.single('file'), (req: Request, res: Response) => {
    calcPlacements(req, res);
});

//if we ever need to create a certificate again, use zerossl site and this snippet
/**app.get('/.well-known/pki-validation/C449B9537CA7AF8182332C838DD9C55F.txt', function(req, res){
  const file = `${__dirname}/../../C449B9537CA7AF8182332C838DD9C55F.txt`;
  res.download(file); // Set disposition and send it.
});**/

app.use((req: Request, res: Response) => {
  res.status(404).send('404 Not Found').end();
});

var httpsServer = https.createServer(credentials, app);

console.log(`Service listening on port ${port}`);

//use sudo nohup npm run start & 
//to run the server indefinitley
httpsServer.listen(port);