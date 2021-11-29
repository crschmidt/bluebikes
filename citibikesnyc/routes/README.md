# Generating Routes

In order to generate routing pairs between stations:

- First, we fetch the list of used stations from the trip data. (n^2 with an n of 1500 is large.) Use the export.sql script in the parent directory to do this.
- Then, we loop through and call to a local OSRM backend. https://hub.docker.com/r/osrm/osrm-backend/
- Then, you can call extract_polylines.py to generate the polylines-nyc.csv file.
