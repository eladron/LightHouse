import {Request, Response} from 'express';

export const placements = {
  '1': {'worker': 8, 'station': 'water'},
  '2': {'worker': 18, 'station': 'water'},
  '3': {'worker': 6, 'station': 'screw'},
  '4': {'worker': 1, 'station': 'piston'},
  '5': {'worker': 16, 'station': 'water'},
  '6': {'worker': 19, 'station': 'piston'},
  '7': {'worker': 10, 'station': 'screw'},
  '8': {'worker': 20, 'station': 'screw'},
  '9': {'worker': 17, 'station': 'piston'},
  '10': {'worker': 7, 'station': 'screw'},
  '11': {'worker': 2, 'station': 'handle'},
  '12': {'worker': 9, 'station': 'screw'},
  '13': {'worker': 12, 'station': 'piston'},
  '14': {'worker': 15, 'station': 'screw'},
  '15': {'worker': 3, 'station': 'handle'},
  '16': {'worker': 14, 'station': 'screw'},
  '17': {'worker': 13, 'station': 'screw'},
  '18': {'worker': 11, 'station': 'screw'},
  '19': {'worker': 4, 'station': 'handle'},
  '20': {'worker': 5, 'station': 'screw'}
};

export const calcPlacements = async (req: Request, res: Response) => {
  try {
    // run algorithm and send back the placements
    const file = req.file;
    console.log(file);
    const hours = req.body.hours;
    console.log(hours);
    const tableValues = JSON.parse(req.body.tableValues);
    console.log(tableValues);
    res.status(200);
    res.setHeader('Content-Type', 'application/json');
    res.write(JSON.stringify(placements));
    res.end();
  } catch (error) {
    console.log(error);
    res.status(400).end('Bad Request')
  }
};