import {Request, Response} from 'express';


export const calcPlacements = async (req: Request, res: Response) => {
  try {
    // run algorithm and send back the placements
    const file = req.file;
    console.log(file);
    const hours = req.body.hours;
    console.log(hours);
    const tableValues = JSON.parse(req.body.tableValues);
    console.log(tableValues);
    res.status(200)
        .setHeader('Content-Type', 'application/json')
        .write(JSON.stringify({id: 0}))
        .end();
  } catch (error) {
    res.status(400).end('Bad Request')
  }
};