import axios from 'axios';
import cors from 'cors';
import * as dotenv from 'dotenv';
import express, {Express, Request, Response} from 'express';
import {calcPlacements} from './routes.js';
import multer, { Multer } from 'multer';

const app: Express = express();
const upload: Multer = multer();

app.use(express.json());

const port = process.env.PORT || 3000;

app.use(cors({credentials: true, origin: true}));

app.post('/api/calculate',  upload.single('file'), (req: Request, res: Response) => {
    calcPlacements(req, res);
});

app.use((req: Request, res: Response) => {
  res.status(404).send('404 Not Found').end();
});

app.listen(port, () => {console.log(`Service listening on port ${port}`)});