This repository holds the data for the Yanorra maps and the code to generate them. 

## Steps to Importing Data from Azkaar's Map Generator into QGIS

### 1. Export the map from **Azkaar's Map Generator**

### 2. Smooth the cell data using `add_random_points.php`

The raw cell data from Azkaar's Map Generator has very jagged borders. To smooth them out, we can add random points along the borders of the cells. 

```bash
php add_random_points.php cells.csv > cells_smoothed.csv
```


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
