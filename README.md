This repository holds the data for the Yanorra maps and the code to generate them. 

## Tools

This project makes extensive use of:
- [Azkaar's Map Generator](https://github.com/azgaar/Fantasy-Map-Generator/)
- [QGIS](https://www.qgis.org/en/site/)

## Scripts

### `add_random_points.php`

This script is used after importing `cells` from [Azkaar's Map Generator](https://github.com/azgaar/Fantasy-Map-Generator/) into QGIS in order to smooth out the borders of the cells. 

Useage:
```bash
php add_random_points.php <filename> > <newfilename>
```
