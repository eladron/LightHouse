import {Request, Response} from 'express';
import { spawn } from 'child_process';
import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';

export const calcPlacements = async (req: Request, res: Response) => {
  try {
    // run algorithm and send back the placements
    const file = req.file;
    console.log(file);
    const hours = req.body.hours;
    console.log(hours);
    const tableValues = JSON.parse(req.body.tableValues);
    console.log(tableValues);
    const gain3 = req.body.gain3;
    console.log(gain3);
    const gain4 = req.body.gain4;
    console.log(gain4);
    const IN_FILE_PATH = join(__dirname,"/../", "input.xlsx");
    writeFileSync(IN_FILE_PATH, file.buffer, {
      flag: 'w',
    });
    const proc = spawn('python3', ['/home/migdalor/LightHouse/Assignment/Maximize/maximize_productivity.py',IN_FILE_PATH, tableValues[0][2], tableValues[0][3], tableValues[0][1], tableValues[0][0], tableValues[1][2], tableValues[1][3], tableValues[1][1], tableValues[1][0], hours, gain3, gain4]);
    /**proc.stdout.on('data', (data) => {
      console.log(`stdout: ${data}`);
    });
      **/
    proc.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
    });


    proc.on('exit', function() {
      try
      {
        const OUT_FILE_PATH = join(__dirname,"/../", "output.json");
        const jsonString = readFileSync(OUT_FILE_PATH, 'utf-8');
        const placements = JSON.parse(jsonString);

        if(proc.exitCode != 0)
        {
          throw new Error('algo failed unexpectedly!');
        }

        console.log(placements);

        res.status(200);
        res.setHeader('Content-Type', 'application/json');
        res.write(JSON.stringify(placements));
        res.end();
      }
      catch (error) {
        console.log(error);
        res.status(400).end('Bad Request')
      }
    })
  } catch (error) {
    console.log(error);
    res.status(400).end('Bad Request')
  }
};